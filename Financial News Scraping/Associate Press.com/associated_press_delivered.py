import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading

def scrape_google_search_results():
    all_article_urls = []

    while True:
        article_urls = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf a")
        for link in article_urls:
            if link.get_attribute('href') not in all_article_urls and link.get_attribute('href').startswith('https://apnews.com'):
                all_article_urls.append(link.get_attribute('href'))

        next_page = driver.find_elements(By.ID, 'pnnext')
        if len(next_page) == 0: break

        next_page[0].click()
        time.sleep(3)
        print(f"valid articles are {all_article_urls}")

    return all_article_urls

def scrape_ap_news_articles(url_):
    scraped_data_json = []
    driver = webdriver.Chrome()
    driver.get(url_)
    driver.maximize_window()
    time.sleep(10)

    try:
        # GET REQUIRED FIELDS
        if url_.startswith('https://apnews.com/article'):
            article_title = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div[3]/div/div[3]/div[1]/h1').text
        elif url_.startswith('https://apnews.com/hub'):
            article_title = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div[3]/div[2]/div[1]/div/h1').text
        else:
            article_title = driver.find_element(By.XPATH, '//*[@id="root"]/div/main/div[3]/div/div[4]/div/h2').text

        published_date_el = driver.find_elements(By.CSS_SELECTOR, '.Body div div span span')
        if len(published_date_el) > 0:
            if published_date_el[0].get_attribute('data-key') == 'timestamp':
                published_date = published_date_el[0].text
            else:
                published_date = published_date_el[1].text

        categories = [category.text for category in driver.find_elements(By.CLASS_NAME, 'related-topic-link')]
        article_contents = driver.find_elements(By.CSS_SELECTOR, 'div.Article p')
        article_content = '\n'.join([paragraph.text for paragraph in article_contents])

        scraped_data_json.append({
            'article_title': article_title,
            'categories': categories,
            'published_date': published_date,
            'article_content': article_content,
            'article_url': url
        })

        print(f"final json {scraped_data_json}")

    except:
        pass

    time.sleep(2)
    driver.quit()


# TODO: ADD YOUR CUSTOM USER SEARCH QUERY
search_query = input("add user search query\n")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
today = datetime.today().strftime("%m/%d/%Y")
three_months_ago = (datetime.today() - timedelta(days=90)).strftime("%m/%d/%Y")
driver.get(f"https://www.google.com/search?q=site%3A+apnews.com+{search_query}&tbs=cdr:1,cd_min:{three_months_ago},cd_max:{today}")
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