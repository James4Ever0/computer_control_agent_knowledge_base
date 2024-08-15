from spider_rs import Website

# set delay, otherwise being blocked.
# need to have chromium installed. nut do not install it with snap.
# use playwright instead. also install chromium dependencies with playwright.
# link the playwright chromium to /usr/bin/ with absolute path
def main():
    website = Website("https://github.com/james4ever0/agi_computer_control") # class attributes: ['build', 'clear', 'crawl', 'crawl_smart', 'drain_links', 'get_configuration_headers', 'get_links', 'get_pages', 'run_cron', 'scrape', 'size', 'status', 'stop', 'subscribe', 'unsubscribe', 'with_blacklist_url', 'with_budget', 'with_caching', 'with_chrome_intercept', 'with_cron', 'with_delay', 'with_depth', 'with_external_domains', 'with_full_resources', 'with_headers', 'with_http2_prior_knowledge', 'with_openai', 'with_proxies', 'with_request_timeout', 'with_respect_robots_txt', 'with_screenshot', 'with_stealth', 'with_subdomains', 'with_tld', 'with_user_agent', 'with_wait_for_idle_network', 'with_whitelist_url']
    # website = Website("https://choosealicense.com")
    website.crawl()
    print(website.get_links())
    # breakpoint()

if __name__ == "__main__":
    main()