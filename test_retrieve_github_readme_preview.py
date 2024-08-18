from import_knowledge import extract_github_readme_from_html

def test():
    filepath = "test_spider_rs_scrape_result.html"
    html = open(filepath, 'r').read()
    extract_github_readme_from_html(html)

if __name__ == "__main__":
    test()
