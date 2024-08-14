from lib import EmbedApp

def import_all_urls(urls:list[str]):
    app = EmbedApp()
    for index, it in enumerate(urls):
        print("[*] Loading url:", f"{index+1}/{len(urls)}")
        app.add(it, data_type="web_page")

def main():
    urls = open("test_urls.txt", "r").read().strip().splitlines()
    import_all_urls(urls)

if __name__ == "__main__":
    main()