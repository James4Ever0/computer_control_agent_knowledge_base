from lib import EmbedApp


def check_single_url(app:EmbedApp, url:str):
    added = app.check_url_is_added(url)

    if added:
        print('[+] URL added:', url)
        documents = app.get_all_documents_by_url()[url]
        if len(documents) == 0:
            print('[-] No document retreieved')
        for index, chunk in enumerate(documents):
            print("[*] Document chunk #"+str(index))
            print(chunk)
    else:
        print('[-] URL not added')

def main():
    app = EmbedApp()
    url = "https://ar5iv.org/pdf/2401.16158"
    check_single_url(app, url)

if __name__ == "__main__":
    main()