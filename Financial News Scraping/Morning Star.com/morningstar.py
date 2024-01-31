import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import json
import os

def is_time_format(date):
    try:
        time.strptime(date, '%H:%M')
        return True
    except ValueError:
        return False

def check_if_publish_date_within_timeframe(article_date, article_url):
    # TODO: CHANGE PUBLISH TIME RANGE HERE
    today_date = datetime.today()
    three_months_ago = (datetime.today() - timedelta(days=90))
    article_date_format = datetime.strptime(datetime.strptime(article_date, '%b %d, %Y').strftime("%m-%d-%Y"), "%m-%d-%Y")

    # print(f"article date {article_date_format} | timeframe from {three_months_ago} | to {today_date}")
    # check if article publish date is between today and three_months_ago
    if three_months_ago <= article_date_format <= today_date:
        return True
    return False

def scrape_morningstar_search_results():
    all_article_urls = []
    i = 0

    while True:
        index = 0
        urls = []
        published_dates = driver.find_elements(By.TAG_NAME, "time")
        article_urls = driver.find_elements(By.CSS_SELECTOR, "h2.mdc-heading.mdc-lineup-module__headline.mdc-heading--level-4.mdc-heading--bold a")

        for link in article_urls:
            if link.get_attribute('href') not in urls:
                urls.append(link.get_attribute('href'))

        for date in published_dates:
            date_text = date.text
            if check_if_publish_date_within_timeframe(date_text, urls[index]):
                all_article_urls.append(urls[index])
            index += 1

        print(f"valid articles are {all_article_urls}")
        next_page = driver.find_element(By.LINK_TEXT, 'Next')
        if int(next_page.get_attribute("tabindex")) == -1: break

        wait = WebDriverWait(driver, 30)
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Next')))
        next_page.click()
        time.sleep(3)

    return all_article_urls



def save_json(json_data, filename='morningstar_json_data.txt'):
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

def scrape_morningstar_articles(url_):
    scraped_data_json = []
    driver = webdriver.Chrome()
    driver.get(url_)
    time.sleep(10)

    # GET REQUIRED FIELDS
    article_title = driver.find_element(By.CSS_SELECTOR, 'header.story__header h1').text
    article_sub_title = driver.find_element(By.CSS_SELECTOR, 'header.story__header p').text
    published_date = driver.find_element(By.TAG_NAME, "time").text
    article_contents = driver.find_elements(By.CSS_SELECTOR, "div.story__body.mdc-story-body__mdc p")
    article_content = '\n'.join([paragraph.text for paragraph in article_contents])

    scraped_data_json.append({
        'article_title': article_title,
        'article_sub_title': article_sub_title,
        'published_date': published_date,
        'article_content': article_content,
        'article_url': url
    })

    print(f"final json {scraped_data_json}")
    save_json(scraped_data_json)

    time.sleep(2)
    driver.quit()


# TODO: ADD YOUR CUSTOM USER SEARCH QUERY
search_query = input("add user search query\n")
driver = webdriver.Chrome()
driver.get(f"https://www.morningstar.com/search/articles?query={search_query}")
all_articles_urls = scrape_morningstar_search_results()
driver.quit()

if len(all_articles_urls) > 0:
    thread_list = list()
    for url in all_articles_urls:
        t = threading.Thread(name='Test {}'.format(url), target=scrape_morningstar_articles(url))
        t.start()
        time.sleep(1)
        thread_list.append(t)

    for thread in thread_list:
        thread.join()


