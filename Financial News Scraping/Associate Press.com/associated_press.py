import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import os
import json


def scrape_google_search_results():
    all_article_urls = []
    not_ap_site = 0
    while True:
        article_urls = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
        for link in article_urls:
            if not link.get_attribute('href').startswith('https://apnews.com'): not_ap_site = 1
            if link.get_attribute('href') not in all_article_urls and link.get_attribute('href').startswith('https://apnews.com'):
                all_article_urls.append(link.get_attribute('href'))
        
        print(f"valid articles are {len(all_article_urls)} {all_article_urls}")
        next_page = driver.find_elements(By.ID, 'pnnext')
        if len(next_page) == 0 or not_ap_site == 1: break

        next_page[0].click()
        time.sleep(3)
    
    return all_article_urls

def save_json(json_data, filename=' associated_press_json_data.txt'):
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

def scrape_ap_news_articles(url_):
    scraped_data_json = []
    driver = webdriver.Chrome()
    driver.get(url_)
    driver.maximize_window()

    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    except:
        pass

    # GET REQUIRED FIELDS
    if not url_.startswith('https://apnews.com/hub'):
        driver.refresh()
        time.sleep(5)

        article_title = driver.find_element(By.CLASS_NAME, 'Page-headline').text
        published_date = driver.find_element(By.CSS_SELECTOR, '.Page-datePublished bsp-timestamp span').text
        # categories = [category.text for category in driver.find_elements(By.CLASS_NAME, 'related-topic-link')]
        article_contents = driver.find_elements(By.CSS_SELECTOR, '.RichTextStoryBody.RichTextBody p')
        article_content = '\n'.join([paragraph.text for paragraph in article_contents])

        scraped_data_json.append({
            'article_title': article_title,
            # 'categories': categories,
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
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
today = datetime.today().strftime("%m/%d/%Y")
three_months_ago = (datetime.today() - timedelta(days=90)).strftime("%m/%d/%Y")
driver.get(f"https://www.google.com/search?q=site%3A+apnews.com+{search_query}&tbs=cdr:1,cd_min:{three_months_ago},cd_max:{today}&hl=en")
try:
    driver.find_element(By.ID, "L2AGLb").click()
except:
    pass
all_articles_urls = scrape_google_search_results()
driver.quit()

if len(all_articles_urls) > 0:
    thread_list = list()
    for url in all_articles_urls:
        t = threading.Thread(name='Test {}'.format(url), target=scrape_ap_news_articles(url))
        t.start()
        time.sleep(1)
        thread_list.append(t)

    for thread in thread_list:
        thread.join()