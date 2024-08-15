from spider_rs import Website

# set delay, otherwise being blocked.
def main():
    website = Website("https://github.com/james4ever0/agi_computer_control")
    # website = Website("https://choosealicense.com")
    website.crawl()
    print(website.get_links())
    breakpoint()

if __name__ == "__main__":
    main()