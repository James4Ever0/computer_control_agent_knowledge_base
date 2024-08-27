from lib import EmbedApp
from func_timeout import func_timeout, FunctionTimedOut
import traceback
import subprocess
from bs4 import BeautifulSoup
# import re


def cleanup_text(text: str):
    ret = ""
    for line in text.splitlines():
        line = line.strip()
        if line:
            ret += line + "\n"
    return ret


# one cannot fully retrieve all data using embedchain only from github repo homepage
# TODO: use github api to inspect repo and get major branch name, and readme file path

WEBPAGE_TIMEOUT = 15
ENCODING = "utf-8"
REPLACE_MIRROR_PAIRS = [
        ("huggingface.co", "hf-mirror.com"),
]
def replace_with_mirror_site(url:str):
    for source, target in REPLACE_MIRROR_PAIRS:
        url = url.replace(source, target)
    return url

def add_webpage_url(app: EmbedApp, url: str, timeout=WEBPAGE_TIMEOUT):
    try:  # need timeout
        args = (url,)
        kwargs = dict(data_type="web_page")
        func_timeout(timeout, app.add, args=args, kwargs=kwargs)
        print(f"[+] Adding webpage '{url}' success")
    except FunctionTimedOut:
        print(f"[-] Webpage '{url}' failed to add after {timeout} seconds (timeout)")
    except:
        traceback.print_exc()
        print(f"[-] Failed to add webpage '{url}'")


def retrieve_html_from_url(url: str, timeout=WEBPAGE_TIMEOUT):
    cmdlist = [
        "spider",
        "--url",
        url,
        "scrape",
        "--depth",
        "1",
        "--output-html",
        "--block-images",
    ]
    ret = subprocess.check_output(cmdlist, timeout=timeout, encoding=ENCODING)
    return ret


def extract_github_readme_from_html(html: str):
    soup = BeautifulSoup(html, features="lxml")

    tag = "article"
    target_elem = soup.find(tag)
    readme_html = str(target_elem)
    readme_text = target_elem.text
    readme_text = cleanup_text(readme_text)
    print("[*] HTML:")
    print(readme_html)
    print("[*] Text:")
    print(readme_text)
    return readme_text


def get_github_readme_from_url(url: str):
    html = retrieve_html_from_url(url)
    ret = extract_github_readme_from_html(html)
    return ret


def add_readme_from_github_url(app: EmbedApp, url: str):
    print("[*] Getting README from Github URL:", url)
    try:
        readme_text = get_github_readme_from_url(url)
        app.add(readme_text, data_type="text", metadata=dict(url=url))
        print("[+] README added")
    except subprocess.TimeoutExpired:
        print("[-] Failed to get HTML within timeout")
    except:
        traceback.print_exc()
        print("[-] Failed to add README")


def import_all_urls(urls: list[str]):
    app = EmbedApp()
    for index, it in enumerate(urls):
        print("[*] Progress:", f"{index+1}/{len(urls)}")
        it = it.strip()
        if it:
            print("[*] Processing URL:", it)
            found_in_index = app.check_url_is_added(it)
            if found_in_index:
                print("[*] Skipping added URL")
                continue
            add_webpage_url(app, it)
            # crawl from raw page, then import as text
            # TODO: add url metadata to imported text content, for duplication removal
            # app.add(page_content, data_type="text")
        else:
            print("[*] Skipping empty URL")
            continue

def filter_urls(urls:list[str]):
    ret = []
    added_urls_lowercase_set = set()
    for it in urls:
        it = it.strip(".")
        it = replace_with_mirror_site(it)
        url_lower = it.lower()
        if url_lower not in added_urls_lowercase_set:
            added_urls_lowercase_set.add(url_lower)
            ret.append(it)
    return ret

def import_urls_from_file(filepath: str):
    print("[*] Loading URLs from file:", filepath)
    urls = open(filepath, "r").read().strip().splitlines()
    urls = filter_urls(urls)
    import_all_urls(urls)


def main():
    # input_filepath = "devon_agents_urls.txt"
    input_filepath = "test_run_all.txt"
    # input_filepath = "test_grouped_urls_reprocessed.txt"
    # input_filepath = "test_urls.txt"
    import_urls_from_file(input_filepath)


if __name__ == "__main__":
    main()
