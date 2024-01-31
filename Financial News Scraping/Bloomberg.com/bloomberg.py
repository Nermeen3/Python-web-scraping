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
import json
import urllib.parse


def check_if_publish_date_within_timeframe(article_date):
    # print(f"data {article_date}")
    article_date = "June 8, 2023"
    # TODO: CHANGE PUBLISH TIME RANGE HERE
    today_date = datetime.today().strftime("%m-%d-%Y")
    three_months_ago = (datetime.today() - timedelta(days=90)).strftime("%m-%d-%Y")
    article_date_format = datetime.strptime(article_date, "%B %d, %Y").strftime("%m-%d-%Y")

    # print(f"article {article_date} | 3 months {three_months_ago} | today {today_date}")
    # check if article publish date is between today and three_months_ago
    if three_months_ago <= article_date_format <= today_date:
        return True
    return False


def scrape_bloomberg_search_results():
    urls = []
    index = 0
    all_article_urls = []

    # print(driver.find_element(By.CSS_SELECTOR, 'div.loadMoreButtonContainer__bbd655a679 button').text)
    # print(len(driver.find_elements(By.CSS_SELECTOR, 'div.loadMoreButtonContainer__bbd655a679 button')))
    while len(driver.find_elements(By.CSS_SELECTOR, 'div.loadMoreButtonContainer__bbd655a679 button')) > 0:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        # print(f"date is {driver.find_elements(By.CSS_SELECTOR, 'div.publishedAt__dc9dff8db4')[-1].text}")
        if not check_if_publish_date_within_timeframe(driver.find_elements(By.CSS_SELECTOR, 'div.publishedAt__dc9dff8db4')[-1].text): break
        # print("true")
        driver.find_element(By.CSS_SELECTOR, 'div.loadMoreButtonContainer__bbd655a679 button').click()
        time.sleep(5)

    published_dates = driver.find_elements(By.CSS_SELECTOR, "div.publishedAt__dc9dff8db4")
    article_urls = driver.find_elements(By.CSS_SELECTOR, ".headline__3a97424275")
    for link in article_urls:
        if link.get_attribute('href') not in urls:
            urls.append(link.get_attribute('href'))

    for date in published_dates:
        date_text = date.text
        if check_if_publish_date_within_timeframe(date_text):
            all_article_urls.append(urls[index])
        index += 1

    print(f"All articles are {len(all_article_urls)} {all_article_urls}")
    return all_article_urls


js_scenario = {
    "instructions": [
        {"wait": 2000},
        {"scroll_y": 1000000},
        {"wait_for_and_click": "button.button__f6b7ccfb8d.secondary__ed561f3e09.block__9a48a7253d"},
        {"wait": 5000},
    ]
}
js_scenario_string = json.dumps(js_scenario)
encoded_js_scenario = urllib.parse.quote(js_scenario_string)
# print(encoded_js_scenario)

# TODO: ADD YOUR CUSTOM USER SEARCH QUERY
search_query = "tesla"  # input("add user search query\n")
driver = webdriver.Chrome()
driver.get(f"https://proxy.scrapeops.io/v1/?api_key=9b11ca93-93a6-4760-8e92-0a0341506dc7&url=https://www.bloomberg.com/search?query={search_query}&js_scenario={encoded_js_scenario}&render_js=true")
# driver.get(f"https://proxy.scrapeops.io/v1/?api_key=9b11ca93-93a6-4760-8e92-0a0341506dc7&url=https://www.bloomberg.com/search?query={search_query}")
# driver.get(f"https://www.bloomberg.com/search?query={search_query}")
time.sleep(5)

all_articles_urls = scrape_bloomberg_search_results()
driver.quit()
