import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import threading
import json
import os

def check_if_publish_date_within_timeframe(article_date):
    # TODO: CHANGE PUBLISH TIME RANGE HERE
    today_date = datetime.today().strftime("%m-%d-%Y")
    three_months_ago = (datetime.today() - timedelta(days=90)).strftime("%m-%d-%Y")
    article_date_format = datetime.strptime(article_date, '%d/%m/%Y').strftime("%m-%d-%Y")

    # check if article publish date is between today and three_months_ago
    if three_months_ago <= article_date_format <= today_date:
        return True
    return False


def scrape_advfn_search_results(search_query):
    in_timeframe = True
    all_article_urls = []

    try:
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        driver.find_element(By.ID, "interstitial-close-btn").click()
        time.sleep(1)
    except:
        pass

    # Click on first search result
    search_button = driver.find_element(By.ID, "autosuggest-news")
    search_button.send_keys(search_query)
    time.sleep(2)
    search_button.send_keys(Keys.DOWN)
    search_button.send_keys(Keys.ENTER)
    time.sleep(2)

    while in_timeframe:
        all_article_elements = driver.find_elements(By.CSS_SELECTOR, "table#newsList tbody tr td table tbody tr")[1:]

        for article in all_article_elements:
            article_elements = article.find_elements(By.CSS_SELECTOR, "tr td")
            published_date = article_elements[0].text
            if check_if_publish_date_within_timeframe(published_date):
                article_url = article_elements[3].find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                all_article_urls.append(article_url)
            else:
                in_timeframe = False

        driver.find_element(By.LINK_TEXT, "Next >>").click()
        time.sleep(3)
        print(f"All articles are {len(all_article_urls)} {all_article_urls}")

    return all_article_urls

def get_save_id(current_id=0, filename='advfn_article_id.txt'):
    if os.path.exists(filename):
        # read existing file and save new ID
        with open(filename, "r") as file:
            data = file.readline()
        current_id = int(data) + 1
        with open(filename, "w") as file:
            file.write(str(current_id))
        return current_id
    else:
        # create new txt file
        with open(filename, "w") as file:
            json.dump(current_id, file)
        return current_id

def save_json(json_data, filename='advfn_json_data.json'):
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

def scrape_advfn_articles(url_):
    article_id = get_save_id()
    scraped_data_json = []
    article_sub_title = ""
    driver = webdriver.Chrome()
    driver.get(url_)
    time.sleep(3)

    try:
        # GET REQUIRED FIELDS
        if url_.startswith("https://uk.advfn.com"):
            article_title = driver.find_element(By.CSS_SELECTOR, 'div#printableContent h2').text
            author_time = driver.find_elements(By.CSS_SELECTOR, 'div#printableContent h3')
            if len(author_time) > 0:
                published_date = author_time[0].text
                article_sub_title = author_time[1].text
            article_contents = driver.find_elements(By.CSS_SELECTOR, 'div#printableContent span p')
            article_content = '\n'.join([paragraph.text for paragraph in article_contents if "terms and conditions" not in paragraph.text.lower()])
        else:
            article_title = driver.find_element(By.CSS_SELECTOR, 'div.news-details-right div div h2').text
            published_date = driver.find_element(By.CSS_SELECTOR, 'div.published-at-role span').text
            article_contents = driver.find_elements(By.CSS_SELECTOR, 'div.news-details-inner div p')
            article_content = '\n'.join([paragraph.text for paragraph in article_contents if "terms and conditions" not in paragraph.text.lower()])

        scraped_data_json.append({
            'article_id': article_id,
            'article_title': article_title,
            'article_sub_title': article_sub_title,
            'published_date': published_date,
            'article_content': article_content,
            'article_url': url_
        })

        print(f"final json {scraped_data_json}")
        save_json(scraped_data_json)

    except:
        pass

    time.sleep(2)
    driver.quit()


# TODO: ADD YOUR CUSTOM USER SEARCH QUERY
search_query = input("add user search query\n")
driver = webdriver.Chrome()
driver.get(f"https://uk.advfn.com/p.php?pid=news")

driver.find_element(By.ID, "login-username").send_keys("enter_user_name_here")
driver.find_element(By.ID, "login-password").send_keys("enter_password_here")
driver.find_element(By.ID, "login-password").send_keys(Keys.ENTER)
time.sleep(2)

driver.get(f"https://uk.advfn.com/p.php?pid=news")
all_articles_urls = scrape_advfn_search_results(search_query)
driver.quit()

if len(all_articles_urls) > 0:
    thread_list = list()
    for url in all_articles_urls:
        t = threading.Thread(name='Test {}'.format(url), target=scrape_advfn_articles(url))
        t.start()
        time.sleep(1)
        thread_list.append(t)

    for thread in thread_list:
        thread.join()
