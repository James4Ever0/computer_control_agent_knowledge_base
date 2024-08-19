# TODO: use ai scientist to review paper
# ref: https://github.com/SakanaAI/AI-Scientist

from lib import EmbedApp
import traceback


def commandline_knowledge_base_chat():
    print("[*] Welcome to computer control agent knowledge base chat")
    app = EmbedApp()
    while True:
        try:
            query = input("user> ").strip()
            if query:
                app.query(query)
        except KeyboardInterrupt:
            print("[*] Keyboard interrupted received")
            print("[*] Exiting")
            exit(0)
        except:
            traceback.print_exc()
            print("[-] Exception happened while processing query")


def main():
    commandline_knowledge_base_chat()


if __name__ == "__main__":
    main()
