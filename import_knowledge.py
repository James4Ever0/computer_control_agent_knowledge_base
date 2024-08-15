from lib import EmbedApp

def import_all_urls(urls:list[str]):
    app = EmbedApp()
    for index, it in enumerate(urls):
        print("[*] Progress:", f"{index+1}/{len(urls)}")
        it = it.strip()
        if it:
            print('[*] Processing URL:', it)
            found_in_index = app.check_url_is_added(it)
            if found_in_index:
                print('[*] Skipping added URL')
                continue
            app.add(it, data_type="web_page")
        else:
            print("[*] Skipping empty URL")
            continue

def main():
    urls = open("test_urls.txt", "r").read().strip().splitlines()
    import_all_urls(urls)

if __name__ == "__main__":
    main()