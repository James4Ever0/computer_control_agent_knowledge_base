from bs4 import BeautifulSoup
import re

def cleanup_text(text:str):
    ret = ""
    for line in text.splitlines():
        line = line.strip()
        if line:
            ret+= line+'\n'
    return ret

filepath = "test_spider_rs_scrape_result.html"
html = open(filepath, 'r').read()
soup = BeautifulSoup(html, features='lxml')

# tag = "turbo-frame"
tag = "article"
target_elem = soup.find(tag)
readme_html = str(target_elem)
readme_text = target_elem.text
readme_text = cleanup_text(readme_text)
print("[*] HTML:")
print(readme_html)
print("[*] Text:")
print(readme_text)