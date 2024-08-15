from lib import EmbedApp
from urlextract import URLExtract
import re
import copy
# you can check dns for eligible links

ARXIV_PREPRINT_REGEX = re.compile(r"arXiv:\d+.\d+")
URL_PREFIXES = ['http://', 'https://']
WHITESPACE = " "

def check_has_url_prefix(chunk:str):
    for it in URL_PREFIXES:
        if chunk.startswith(it):
            return True
    return False

def extract_urls_by_urlextract(text:str):
    ret = list(EXTRACTOR.gen_urls(text))
    return ret

def extract_urls_by_regex(text:str) -> list[str]:
    # pattern = r'https?://(?:www\.)?[\w\d\-]+\.[\w\d\-\.]+(?:/[\w\d\-\._~:/?#[\]@!$&\'()*+,;=]*)?' 
    pattern = r"((((https?|ftps?|gopher|telnet|nntp)://)|(mailto:|news:))([-%()_.!~*';/?:@&=+$,A-Za-z0-9])+)"
    results = re.findall(pattern, text)
    ret = [it[0] for it in results]
    return ret

def fix_invalid_protocols(text:str):
    ret = text.replace("http:/", 'http://').replace('https:/', 'https://')
    ret = ret.replace(':///', '://')
    return ret

def extract_urls_by_prefix(text:str) -> list[str]:
    chunks = text.split(WHITESPACE)
    ret = []
    for it in chunks:
        it = it.strip()
        if check_has_url_prefix(it):
            ret.append(it)
    return ret

APP = EmbedApp()
EXTRACTOR = URLExtract()

REMOVABLE_PUNCTUATIONS = ["(", ")", "'", '"']

def preprocess_text_for_url_extraction(text: str):
    ret = text
    for it in REMOVABLE_PUNCTUATIONS:
        ret = ret.replace(it, WHITESPACE)
    ret = fix_invalid_protocols(ret)
    return ret

def test_all():
    # example_text = "Text with URLs. Let's have URL janlipovsky.cz as an example."
    print("[*] Fetching URLs:")

    for it in APP.get_all_document_chunks():
        text = it["document"]
        text = preprocess_text_for_url_extraction(text)
        print('[*] Document:')
        print(text)
        urls_urlextract = extract_urls_by_urlextract(copy.copy(text))
        print("[*] Extracted URLs by URLExtract:")
        print(urls_urlextract)
        urls_regex = extract_urls_by_regex(copy.copy(text))
        print('[*] URLs by regex:')
        print(urls_regex)
        urls_prefix = extract_urls_by_prefix(copy.copy(text))
        print('[*] URLs by prefix:')
        print(urls_prefix)

if __name__ == "__main__":
    test_all()