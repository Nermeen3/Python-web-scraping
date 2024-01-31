import time
from seleniumwire import webdriver
from random import randint
import requests
from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import os
import json

def check_if_publish_date_within_timeframe(article_date):
    # TODO: CHANGE PUBLISH TIME RANGE HERE
    today_date = datetime.today().strftime("%m-%d-%Y")
    three_months_ago = (datetime.today() - timedelta(days=90)).strftime("%m-%d-%Y")
    article_date_format = datetime.strptime(article_date, "%B %d, %Y").strftime("%m-%d-%Y")

    print(f"article {article_date} | 3 months {three_months_ago} | today {today_date}")
    # check if article publish date is between today and three_months_ago
    if three_months_ago <= article_date_format <= today_date and article_date_format.split("-")[2] == today_date.split("-")[2]:
        return True
    return False


def scrape_google_search_results():
    all_article_urls = []
    not_ap_site = 0
    while True:
        article_urls = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
        for link in article_urls:
            if not link.get_attribute('href').startswith('https://www.bloomberg.com/'): not_ap_site = 1
            if link.get_attribute('href') not in all_article_urls and link.get_attribute('href').startswith('https://www.bloomberg.com/'):
                all_article_urls.append(link.get_attribute('href'))

        print(f"valid articles are {len(all_article_urls)} {all_article_urls}")
        next_page = driver.find_elements(By.ID, 'pnnext')
        if len(next_page) == 0 or not_ap_site == 1: break

        next_page[0].click()
        time.sleep(3)

    return all_article_urls


def save_json(json_data, filename=' bloomberg_json_data.txt'):
    if os.path.exists(filename):
        # read existing file and append new data
        with open(filename, "r") as file:
            data = json.load(file)
        data.append(json_data[0])
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
    else:
        # create new json
        with open(filename, "w") as file:
            json.dump(json_data, file, indent=4)


def scrape_bloomberg_articles(url_):
    scraped_data_json = []
    driver = webdriver.Chrome()
    driver.get(f"https://proxy.scrapeops.io/v1/?api_key=9b11ca93-93a6-4760-8e92-0a0341506dc7&url={url_}&render_js=true")
    driver.maximize_window()

    # GET REQUIRED FIELDS
    if url_.startswith('https://www.bloomberg.com/news/articles'):
        time.sleep(5)

        article_title = driver.find_element(By.CSS_SELECTOR, '.headline__699ae8fb').text
        published_date = driver.find_element(By.CSS_SELECTOR, '.lede-times__03902805 time').text
        # if len(published_date_el) > 0:
        #     if published_date_el[0].get_attribute('data-key') == 'timestamp':
        #         published_date = published_date_el[0].text
        #     else:
        #         published_date = published_date_el[1].text

        # categories = [category.text for category in driver.find_elements(By.CLASS_NAME, 'related-topic-link')]
        article_content = driver.find_elements(By.CSS_SELECTOR, 'body-content.teaser-content__388dc739 p')
        # article_content = '\n'.join([paragraph.text for paragraph in article_contents])

        scraped_data_json.append({
            'article_title': article_title,
            # 'categories': categories,
            'published_date': published_date,
            'article_content': article_content,
            'article_url': url
        })

        print(f"final json {scraped_data_json}")
        # save_json(scraped_data_json)

    time.sleep(2)
    driver.quit()

# TODO: ADD YOUR CUSTOM USER SEARCH QUERY
# search_query = "tesla" #input("add user search query\n")
# driver = webdriver.Chrome()
# today = datetime.today().strftime("%m/%d/%Y")
# three_months_ago = (datetime.today() - timedelta(days=90)).strftime("%m/%d/%Y")
# driver.get(f"https://www.google.com/search?q=site%3A+bloomberg.com+{search_query}&tbs=cdr:1,cd_min:{three_months_ago},cd_max:{today}&hl=en")
# # driver.get(f"https://proxy.scrapeops.io/v1/?api_key=9b11ca93-93a6-4760-8e92-0a0341506dc7&url=https://www.bloomberg.com/search?query={search_query}&render_js=true&country=uk")
#
# all_articles_urls = scrape_google_search_results()
# driver.quit()

all_articles_urls = ['https://www.bloomberg.com/news/articles/2023-05-13/four-reasons-tesla-prices-keep-changing', 'https://www.bloomberg.com/news/articles/2023-05-31/tesla-plans-to-showcase-updated-model-3-with-musk-in-shanghai', 'https://www.bloomberg.com/news/articles/2023-05-16/tesla-revamped-model-3-nears-final-trial-production-in-shanghai', 'https://www.bloomberg.com/news/articles/2023-06-01/tesla-is-still-auto-stock-despite-ai-hype-says-morgan-stanley', 'https://www.bloomberg.com/news/articles/2023-04-25/tesla-drops-model-y-starting-price-below-the-average-us-vehicle', 'https://www.bloomberg.com/news/articles/2023-06-06/byd-evs-are-biting-into-tesla-s-market-share-except-in-the-usa', 'https://www.bloomberg.com/news/articles/2023-06-02/tesla-s-ev-price-war-padded-by-windfall-from-biden-s-ira', 'https://www.bloomberg.com/news/articles/2023-05-03/tesla-resumes-orders-for-popular-model-3-long-range-at-47-240', 'https://www.bloomberg.com/news/articles/2023-04-14/tesla-goes-after-america-s-top-selling-suvs', 'https://www.bloomberg.com/news/articles/2023-05-03/tesla-price-cuts-tsla-aren-t-over-as-inventory-keeps-rising', 'https://www.bloomberg.com/news/articles/2023-05-30/elon-musk-expected-to-visit-china-in-first-trip-in-three-years', 'https://www.bloomberg.com/news/articles/2023-05-12/tesla-tweaks-prices-in-us-again-increasing-as-much-as-1-000', 'https://www.bloomberg.com/news/articles/2023-05-15/tesla-contributes-almost-25-of-shanghai-s-total-auto-production', 'https://www.bloomberg.com/news/articles/2023-05-16/tesla-executives-to-visit-india-this-week-in-pivot-beyond-china', 'https://www.bloomberg.com/news/articles/2023-04-21/tesla-s-struggle-to-lure-buyers-paints-a-grim-economic-picture', 'https://www.bloomberg.com/news/articles/2023-05-16/musk-says-tesla-will-try-advertising-in-shift-for-ev-maker', 'https://www.bloomberg.com/news/articles/2023-03-28/do-you-own-a-tesla-we-want-to-hear-from-you', 'https://www.bloomberg.com/news/articles/2023-04-25/tesla-model-y-price-cuts-mean-elon-musk-s-either-disruptive-or-desperate', 'https://www.bloomberg.com/news/articles/2023-04-26/tesla-s-plunge-drags-valuation-below-500-billion-on-margin-fear', 'https://www.bloomberg.com/news/articles/2023-05-31/musk-starts-second-day-of-china-visit-after-emphasizing-ties', 'https://www.bloomberg.com/news/articles/2023-04-21/tesla-increases-price-of-model-s-x-in-us-after-shares-slump', 'https://www.bloomberg.com/news/articles/2023-05-19/tesla-stops-short-of-committing-to-india-plant-in-renewed-talks', 'https://www.bloomberg.com/quote/TL0:GR', 'https://www.bloomberg.com/news/articles/2023-05-16/tesla-shareholders-have-some-major-governance-calls-to-make', 'https://www.bloomberg.com/news/articles/2023-04-02/tesla-tsla-deliveries-rise-to-record-after-slashing-ev-prices', 'https://www.bloomberg.com/news/articles/2023-04-20/tesla-s-tsla-thinning-margins-have-another-analyst-saying-sell-now', 'https://www.bloomberg.com/news/features/2023-04-04/how-tesla-tsla-elon-musk-are-helping-australia-quit-coal-power']

if len(all_articles_urls) > 0:
    thread_list = list()
    for url in all_articles_urls:
        t = threading.Thread(name='Test {}'.format(url), target=scrape_bloomberg_articles(url))
        t.start()
        time.sleep(1)
        thread_list.append(t)

    for thread in thread_list:
        thread.join()

