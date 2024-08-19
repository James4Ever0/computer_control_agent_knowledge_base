from lib import EmbedApp
from urlextract import URLExtract
import re
from typing import DefaultDict
import requests
from urllib.parse import urlparse, urlunparse
import rich

# you can check dns for eligible links

ARXIV_PREPRINT_REGEX = re.compile(r"arXiv:\d+.[\da-zA-Z]+")
IP_ADDRESS_REGEX = re.compile(r"\d+.\d+.\d+.\d+")
URL_REGEX = re.compile(
    r"((((https?|ftps?|gopher|telnet|nntp)://)|(mailto:|news:))([-%()_.!~*';/?:@&=+$,A-Za-z0-9])+)"
)
URL_PREFIXES = ["https://", "http://"]
WHITESPACE = " "
EXTRACTOR = URLExtract()
REMOVABLE_PUNCTUATIONS = ["(", ")", "'", '"']
HOSTNAME_LOWERCASE_BLACKLIST = [
    "localhost",
    "asp.net",
    "img.shields.io",
    "discord.gg",
    "chatgpt.com",
    "cdn.rawgit.com",
    "patreon.com",
]
NETLOC_SUFFIX_LOWERCASE_BLACKLIST = ["md"]
INDEX_HTML = "index.html"

ARXIV_NETLOC = "arxiv.org"
AR5IV_NETLOC = "ar5iv.org"


def detect_loop_url(url: str):
    ret = False
    url_len = len(url)
    if url_len % 2 == 0:
        # even length
        left, right = url[: url_len / 2], url[url_len / 2 :]
        ret = left == right
    return ret


def check_has_url_prefix(chunk: str):
    for it in URL_PREFIXES:
        if chunk.startswith(it):
            return True
    return False


def extract_urls_by_urlextract(text: str):
    ret = list(EXTRACTOR.gen_urls(text))
    return ret


def extract_urls_by_regex(text: str) -> list[str]:
    # pattern = r'https?://(?:www\.)?[\w\d\-]+\.[\w\d\-\.]+(?:/[\w\d\-\._~:/?#[\]@!$&\'()*+,;=]*)?'
    results = URL_REGEX.findall(text)
    ret = [it[0] for it in results]
    return ret


def fix_invalid_protocols(text: str):
    ret = text.replace("http:/", "http://").replace("https:/", "https://")
    ret = ret.replace(":///", "://")
    return ret


def extract_urls_by_prefix(text: str) -> list[str]:
    chunks = text.split(WHITESPACE)
    ret = []
    for it in chunks:
        it = it.strip()
        if check_has_url_prefix(it):
            ret.append(it)
    return ret


def extract_arxiv_preprint_codes(text: str) -> list[str]:
    ret = ARXIV_PREPRINT_REGEX.findall(text)
    return ret


def convert_arxiv_preprint_code_into_pdf_url(preprint_code: str):
    numeric_code = preprint_code.split(":")[-1]
    ret = f"https://arxiv.org/pdf/{numeric_code}"
    return ret


def convert_arxiv_pdf_url_into_html_url(pdf_url: str):
    ret = pdf_url.replace("arxiv", "ar5iv")
    return ret


def preprocess_text_for_url_extraction(text: str):
    ret = text
    for it in REMOVABLE_PUNCTUATIONS:
        ret = ret.replace(it, WHITESPACE)
    ret = fix_invalid_protocols(ret)
    return ret


def remove_query_and_anchor(url: str):
    parsed_url = urlparse(url)
    clean_url = urlunparse(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", "", "")
    )
    return clean_url


def categorize_collected_urls(urls: list[str]) -> dict:
    ret = DefaultDict(list)
    for it in urls:
        category = "with_prefix"
        if not check_has_url_prefix(it):
            has_loop = detect_loop_url(it)
            if has_loop:
                print("[*] Skipping url because loop has been detected")
                continue
            fixed_url = fix_unprefixed_url(it)
            if fixed_url is None:
                category = "no_prefix"
            else:
                it = fixed_url
        if category == "with_prefix":
            it = remove_query_and_anchor(it)
        ret[category].append(it)
    ret = dict(ret)
    return ret


def save_urls_to_file(urls: list[str], filepath: str):
    print("[*] Collect URLs count:", len(urls))
    print("[*] Exported to:", filepath)
    content = "\n".join(urls)
    with open(filepath, "w+") as f:
        f.write(content)


def fix_unprefixed_url(url: str):
    for prefix in URL_PREFIXES:
        ret = f"{prefix}{url}"
        try:
            requests.get(ret, timeout=3)
            print("[+] Fixed url:", ret)
            return ret
        except:
            print("[-] Timeout accessing fixed url:", ret)
    print("[-] Unable to fix url:", url)


def cleanse_urls(urls: list[str]):
    print("[*] Input URLs:", len(urls))
    url_set = set()
    for it in urls:
        it = it.strip("/")
        if it:
            url_set.add(it)
    ret = list(url_set)
    ret.sort()
    print("[*] Cleansed URLs:", len(ret))
    return ret


def import_urls_from_file(filepath: str):
    with open(filepath, "r") as f:
        ret = f.read().strip().splitlines()
        ret = cleanse_urls(ret)
        return ret


def check_is_ip_address(hostname: str) -> bool:
    ret = False
    if IP_ADDRESS_REGEX.match(hostname) is not None:
        ret = True
    return ret


def filter_unwanted_hosts_from_urls(urls: list[str]) -> list[str]:
    ret = []

    for it in urls:
        # print("[*] Filtering URL:", it)
        netloc = get_url_netloc(it)
        hostname = netloc.split(":")[0]
        hostname_lower = hostname.lower()
        hostname_lower_suffix = hostname_lower.split(".")[-1]
        if hostname_lower in HOSTNAME_LOWERCASE_BLACKLIST:
            print("[-] Skipping because host in blacklist:", hostname_lower)
            continue
        elif hostname_lower_suffix in NETLOC_SUFFIX_LOWERCASE_BLACKLIST:
            print(
                "[-] SKipping because containing unwanted netloc suffix:",
                hostname_lower_suffix,
            )
            continue
        elif check_is_ip_address(hostname):
            print("[-] Skipping because host is IP address:", hostname)
            continue
        else:
            # check if it is index.html variant
            if it.endswith(INDEX_HTML):
                baseform_variant = it[: len(INDEX_HTML) + 1]
                if baseform_variant in ret:
                    print("[*] Skipping because base form variant detected")
                    continue
            else:
                html_variant_url = "/".join([it.strip("/"), INDEX_HTML])
                if html_variant_url in ret:
                    print("[*] Skipping because index.html variant detected")
                    continue
        ret.append(it)

    return ret


def collect_all_urls_from_database(app: EmbedApp) -> list[str]:
    ret = []

    for it in app.get_all_document_chunks():
        text = it["document"]
        text = preprocess_text_for_url_extraction(text)
        print("[*] Document:")
        print(text)
        urls_urlextract = extract_urls_by_urlextract(text)
        print("[*] Extracted URLs by URLExtract:")
        print(urls_urlextract)
        urls_regex = extract_urls_by_regex(text)
        print("[*] URLs by regex:")
        print(urls_regex)
        urls_prefix = extract_urls_by_prefix(text)
        print("[*] URLs by prefix:")
        print(urls_prefix)
        arxiv_codes = extract_arxiv_preprint_codes(text)
        print("[*] Arxiv preprint codes:")
        print(arxiv_codes)
        arxiv_pdf_urls = [
            convert_arxiv_preprint_code_into_pdf_url(it) for it in arxiv_codes
        ]
        print("[*] Arxiv PDF URLs:")
        print(arxiv_pdf_urls)
        arxiv_html_urls = [
            convert_arxiv_pdf_url_into_html_url(it) for it in arxiv_pdf_urls
        ]
        print("[*] Arxiv HTML URLs:")
        print(arxiv_html_urls)
        collected_urls = (
            urls_urlextract
            + urls_regex
            + urls_prefix
            + arxiv_pdf_urls
            + arxiv_html_urls
        )
        ret.extend(collected_urls)
    return ret


def get_url_netloc(url: str):
    url_parsed = urlparse(url)
    ret = url_parsed.netloc
    return ret


def group_urls_by_netloc(urls: list[str]) -> dict[str, list[str]]:
    ret = DefaultDict(list)
    for it in urls:
        netloc = get_url_netloc(it)
        ret[netloc].append(it)
    ret = dict(ret)
    return ret


def extract_arxiv_codes_from_urls(arxiv_urls: list[str]):
    ret = []
    for it in arxiv_urls:
        results = extract_arxiv_preprint_codes(it)
        if results:
            ret.append(results[0])
    return ret


def convert_arxiv_to_ar5iv(grouped_urls: dict[str, list[str]]):
    arxiv_urls = grouped_urls[ARXIV_NETLOC]
    arxiv_codes = extract_arxiv_codes_from_urls(arxiv_urls)
    new_ar5iv_urls = [
        convert_arxiv_preprint_code_into_pdf_url(it) for it in arxiv_codes
    ]
    grouped_urls[AR5IV_NETLOC] = list(set(grouped_urls[AR5IV_NETLOC] + new_ar5iv_urls))
    del grouped_urls[ARXIV_NETLOC]
    return grouped_urls


def test_collect_all_urls_from_database_and_export_to_file():
    # example_text = "Text with URLs. Let's have URL janlipovsky.cz as an example."
    print("[*] Fetching URLs:")
    export_url_path = "test_fetched_urls.txt"
    app = EmbedApp()
    urls = collect_all_urls_from_database(app)
    save_urls_to_file(urls, export_url_path)


def test_categorize_collected_urls():
    import_filepath = "test_fetched_urls.txt"
    urls = import_urls_from_file(import_filepath)
    categorized_urls = categorize_collected_urls(urls)
    export_filepath = "test_urls_with_schema.txt"
    for category, it in categorized_urls.items():
        print("[*] Category:", category)
        print("[*] URLs:", it)
    urls_with_schema = categorized_urls["with_prefix"]
    save_urls_to_file(urls_with_schema, export_filepath)


def test_filter_unwanted_hosts():
    import_filepath = "test_urls_with_schema.txt"
    urls = import_urls_from_file(import_filepath)
    filtered_urls = filter_unwanted_hosts_from_urls(urls)
    export_filepath = "test_filter_host_urls.txt"
    save_urls_to_file(filtered_urls, export_filepath)


def test_group_filtered_urls_by_netloc():
    import_filepath = "test_filter_host_urls.txt"
    urls = import_urls_from_file(import_filepath)
    grouped_urls = group_urls_by_netloc(urls)
    stats = []
    for netloc, it in grouped_urls.items():
        stats.append((netloc, len(it)))
    # now, convert the grouped_urls.
    grouped_urls = convert_arxiv_to_ar5iv(grouped_urls)
    # stats.sort(key = lambda x: x[1])
    export_urls = [it for netloc_urls in grouped_urls.values() for it in netloc_urls]
    export_filepath = "test_grouped_urls_reprocessed.txt"
    save_urls_to_file(export_urls, export_filepath)
    # rich.print(stats)


if __name__ == "__main__":
    # test_collect_all_urls_from_database_and_export_to_file()
    # test_categorize_collected_urls()
    test_filter_unwanted_hosts()
    test_group_filtered_urls_by_netloc()
