import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import os
import json


def is_time_format(date):
    try:
        time.strptime(date, '%H:%M')
        return True
    except ValueError:
        return False


def check_if_publish_date_within_timeframe(article_date, article_url):
    if is_time_format(article_date.split()[0]) or "ago" in article_date:return True

    # TODO: CHANGE PUBLISH TIME RANGE HERE
    today_date = datetime.today().strftime("%m-%d-%Y")
    three_months_ago = (datetime.today() - timedelta(days=90)).strftime("%m-%d-%Y")
    article_date_format = datetime.strptime(article_date, '%B %d, %Y').strftime("%m-%d-%Y")

    # check if article publish date is between today and three_months_ago
    if three_months_ago <= article_date_format <= today_date and article_date_format.split("-")[2] == today_date.split("-")[2]:
        return True
    return False


def scrape_reuters_search_results():
    all_article_urls = []
    try:
        while True:
            index = 0
            urls = []
            published_dates = driver.find_elements(By.TAG_NAME, "time")
            article_urls = driver.find_elements(By.CSS_SELECTOR, "li.search-results__item__2oqiX a")
            for link in article_urls:
                if link.get_attribute('href') not in urls:
                    urls.append(link.get_attribute('href'))

            for date in published_dates:
                date_text = date.text
                if check_if_publish_date_within_timeframe(date_text, urls[index]):
                    all_article_urls.append(urls[index])
                index += 1

            next_page = driver.find_element(By.XPATH, '//*[@id="fusion-app"]/div[2]/div[2]/div/div[2]/div[3]/button[2]')
            if not next_page.is_enabled(): break

            wait = WebDriverWait(driver, 5)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="fusion-app"]/div[2]/div[2]/div/div[2]/div[3]/button[2]')))
            next_page.click()
            time.sleep(10)
            print(f"valid articles are {all_article_urls}")

        return all_article_urls

    except:
        return all_article_urls


def save_json(json_data, filename='reuters_json_data.txt'):
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


def scrape_reuters_articles(url_):
    scraped_data_json = []
    driver = webdriver.Chrome()
    driver.get(url_)
    time.sleep(10)

    # GET REQUIRED FIELDS
    article_title = driver.find_element(By.CSS_SELECTOR, 'main#main-content article div div header div div h1').text
    categories = driver.find_elements(By.CSS_SELECTOR, '.tags__tag-list__2EKvP li a span span')
    categories_texts = [category.text for category in categories]
    published_date = driver.find_element(By.CSS_SELECTOR, 'main#main-content article div div header div div div div time span').text
    article_contents = driver.find_elements(By.CSS_SELECTOR, "main#main-content article div div div div div p")
    article_content = '\n'.join([paragraph.text for paragraph in article_contents])

    scraped_data_json.append({
        'article_title': article_title,
        'categories': categories_texts,
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
driver.get(f"https://www.reuters.com/site-search/?query={search_query}")
try:
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
except:
    pass
all_articles_urls = scrape_reuters_search_results()
driver.quit()

if len(all_articles_urls) > 0:
    thread_list = list()
    for url in all_articles_urls:
        t = threading.Thread(name='Test {}'.format(url), target=scrape_reuters_articles(url))
        t.start()
        time.sleep(1)
        thread_list.append(t)

    for thread in thread_list:
        thread.join()


