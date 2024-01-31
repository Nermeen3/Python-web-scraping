import time
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import os
import json
from selenium.webdriver.common.action_chains import ActionChains
import re

def check_if_publish_date_within_timeframe(article_date):
    # Process Publish Date
    article_date_split = article_date.split()
    day = re.sub('\D', '', article_date_split[0])
    article_date = f"{day} {article_date_split[1]} {article_date_split[2]}"

    # TODO: CHANGE PUBLISH TIME RANGE HERE
    today_date = datetime.today().strftime("%m-%d-%Y")
    three_months_ago = (datetime.today() - timedelta(days=90)).strftime("%m-%d-%Y")
    article_date_format = datetime.strptime(article_date, '%d %B %Y').strftime("%m-%d-%Y")

    # check if article publish date is between today and three_months_ago
    if three_months_ago <= article_date_format <= today_date and article_date_format.split("-")[2] == today_date.split("-")[2]:
        return True
    return False

def scrape_interactive_investor_search_results(search_query):
    urls = []
    index = 0
    all_article_urls = []
    # Click on first search result
    search_button = driver.find_element(By.CSS_SELECTOR, ".ii-1nx0ar8")
    ActionChains(driver).move_to_element(search_button).click(search_button).perform()
    driver.find_element(by=By.CSS_SELECTOR, value='.chakra-input.ii-8530ov').send_keys(search_query)
    time.sleep(2)
    first_result = driver.find_element(By.CSS_SELECTOR, ".chakra-stack.ii-1dcyh6p div div ul a").get_attribute("href") +"/news-and-analysis"
    driver.get(first_result)
    time.sleep(5)

    while len(driver.find_elements(By.CSS_SELECTOR, '.chakra-button.css-1g6hxdv')) > 0:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        if not scrape_interactive_investor_articles(driver.find_elements(By.CSS_SELECTOR, '.chakra-link.css-15268ks')[-1].get_attribute('href'), True): break
        driver.find_elements(By.CSS_SELECTOR, '.chakra-button.css-1g6hxdv')[0].click()
        time.sleep(2)

    published_dates = driver.find_elements(By.CSS_SELECTOR, "span.chakra-text.css-1fhmwxj")
    article_urls = driver.find_elements(By.CSS_SELECTOR, ".chakra-link.css-15268ks")
    for link in article_urls:
        if link.get_attribute('href') not in urls:
            urls.append(link.get_attribute('href'))

    for date in published_dates:
        date_text = date.text.split()[1]
        if date_text in [datetime.today().strftime("%B"), (datetime.today() - timedelta(days=30)).strftime("%B"), (datetime.today() - timedelta(days=60)).strftime("%B"), (datetime.today() - timedelta(days=90)).strftime("%B")]:
            all_article_urls.append(urls[index])
        index += 1

    print(f"All articles are {len(all_article_urls)} {all_article_urls}")
    return all_article_urls

def save_json(json_data, filename='interactive_investor_json_data.json'):
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

def scrape_interactive_investor_articles(url_, check_year=False):
    scraped_data_json = []
    driver = webdriver.Chrome()
    driver.get(url_)

    try:
        driver.find_element(By.CLASS_NAME, "chakra-button.ii-7kliwd").click()
        driver.maximize_window()
        driver.refresh()
    except:
        pass

    time.sleep(3)
    # Check if publish date is in range
    published_date = driver.find_element(By.CSS_SELECTOR, ".chakra-text.ii-sd2w5x").text
    if check_year:
        publish_year = published_date.split()[2]
        if publish_year != datetime.today().strftime('%Y'):
            return False
        return True

    if check_if_publish_date_within_timeframe(published_date):

        # GET REQUIRED FIELDS
        article_title = driver.find_element(By.CSS_SELECTOR, '.chakra-heading.ii-1dxxayf').text
        categories = ','.join(category.text for category in driver.find_elements(By.CSS_SELECTOR, '.chakra-wrap.ii-bm29qb ul div'))

        if url_.startswith("https://www.ii.co.uk/analysis-commentary"):
            article_contents = driver.find_elements(By.CSS_SELECTOR, 'span.ii-0')
        else:
            article_contents = driver.find_elements(By.CSS_SELECTOR, "div.ii-nx7nia p")
        article_content = '\n'.join([paragraph.text for paragraph in article_contents])

        scraped_data_json.append({
            'article_title': article_title,
            'categories': categories,
            'published_date': published_date,
            'article_content': article_content,
            'article_url': url
        })

        print(f"final json {url_} {scraped_data_json}")
        save_json(scraped_data_json)

    time.sleep(2)
    driver.quit()


# TODO: ADD YOUR CUSTOM USER SEARCH QUERY
# search_query = input("add user search query\n")
# driver = webdriver.Chrome()
# driver.get("https://www.ii.co.uk")
# driver.maximize_window()
#
# try:
#     driver.find_element(By.CLASS_NAME, "chakra-button.ii-7kliwd").click()
# except:
#     pass
# time.sleep(2)
#
# all_articles_urls = scrape_interactive_investor_search_results(search_query)
# driver.quit()
all_articles_urls = ['https://www.ii.co.uk/analysis-commentary/most-bought-investments-april-2023-ii527769', 'https://www.ii.co.uk/news/new-york-market-close-wall-street-rallies-as-debt-ceiling-jitters-ebb-al1684354909705175300', 'https://www.ii.co.uk/analysis-commentary/scottish-mortgage-periods-poor-performance-are-inevitable-ii527916', 'https://www.ii.co.uk/news/scottish-mortgage-has-confidence-in-long-term-despite-underperformance-al1684312778103565800', 'https://www.ii.co.uk/news/update-teslas-musk-considering-significant-investments-in-france-al1684170130689854200', 'https://www.ii.co.uk/news/french-president-macron-talks-with-teslas-musk-on-investing-in-france-al1684157262119279300', 'https://www.ii.co.uk/news/elon-musk-confirms-former-nbcuniversal-executive-as-new-twitter-boss-al1683973930287165100', 'https://www.ii.co.uk/news/new-york-market-close-us-stocks-ease-on-fresh-economic-concerns-al1683922437617010500', 'https://www.ii.co.uk/news/tesla-ceo-elon-musk-says-new-twitter-chief-has-been-hired-al1683885583005640900', 'https://www.ii.co.uk/analysis-commentary/ii-view-ford-starts-year-well-guidance-unchanged-ii527776', 'https://www.ii.co.uk/analysis-commentary/most-bought-investments-april-2023-ii527769', 'https://www.ii.co.uk/analysis-commentary/ian-cowie-four-golden-oldies-have-stood-test-time-ii527715', 'https://www.ii.co.uk/analysis-commentary/ask-ii-what-best-way-invest-passively-us-stock-market-ii527711', 'https://www.ii.co.uk/news/global-broker-ratings-jefferies-cuts-tesla-deutsche-likes-novartis-al1682506582934432000', 'https://www.ii.co.uk/analysis-commentary/ii-view-google-owner-alphabet-beats-estimates-ii527701', 'https://www.ii.co.uk/news/new-york-market-close-us-stocks-end-losing-week-in-lacklustre-fashion-al1682108253532432400', 'https://www.ii.co.uk/news/tesla-shares-rebound-as-tweaks-prices-on-luxury-models-al1682095100922047600', 'https://www.ii.co.uk/news/global-broker-ratings-db-says-buy-veolia-but-hold-severn-trent-al1682074570231306900', 'https://www.ii.co.uk/analysis-commentary/market-snapshot-keeping-lid-sentiment-ahead-new-acid-test-ii527651', 'https://www.ii.co.uk/news/new-york-market-close-weak-earnings-knock-us-stocks-tesla-slides-10-al1682021572570199700', 'https://www.ii.co.uk/news/london-market-close-ftse-directionless-but-european-carmakers-slump-al1682006640139633400', 'https://www.ii.co.uk/news/london-market-midday-rate-fears-hit-indices-tesla-results-hurt-peers-al1681989385218944800', 'https://www.ii.co.uk/news/global-broker-ratings-warburg-cuts-adidas-to-hold-al1681989258488936300', 'https://www.ii.co.uk/analysis-commentary/ii-view-tesla-shares-reverse-inflationary-costs-dent-margins-ii527646', 'https://www.ii.co.uk/analysis-commentary/must-read-tesla-deliveroo-foxtons-haleon-ii527638', 'https://www.ii.co.uk/analysis-commentary/scottish-mortgage-should-you-hold-fold-or-be-bold-ii527629', 'https://www.ii.co.uk/news/london-market-early-call-stocks-set-for-muted-start-tesla-down-6-al1681970228727711100', 'https://www.ii.co.uk/news/tesla-profit-falls-as-rising-costs-and-falling-prices-dent-margins-al1681937229177461900', 'https://www.ii.co.uk/news/new-york-market-close-us-stocks-mixed-as-banking-worries-knock-mood-al1681935645547425100', 'https://www.ii.co.uk/news/global-broker-ratings-lbbw-raises-vinci-to-buy-ubs-likes-netflix-al1681902598926227800', 'https://www.ii.co.uk/analysis-commentary/must-read-ftse-100-snaps-winning-streak-netflix-heineken-national-express-ii527619', 'https://www.ii.co.uk/news/new-york-market-close-us-stocks-muted-after-sluggish-goldman-results-al1681849286244908700', 'https://www.ii.co.uk/analysis-commentary/will-tesla-and-netflix-shares-join-results-season-rally-ii527609', 'https://www.ii.co.uk/analysis-commentary/decarbonisation-shares-funds-and-trusts-race-net-zero-ii527601', 'https://www.ii.co.uk/news/us-scraps-tax-credits-for-e-cars-from-vw-bmw-nissan-and-others-al1681793793142458100', 'https://www.ii.co.uk/news/new-york-market-close-us-stocks-marked-higher-ahead-of-earnings-al1681762417562284000', 'https://www.ii.co.uk/analysis-commentary/market-snapshot-important-week-company-results-flood-ii527590', 'https://www.ii.co.uk/news/elon-musk-forms-xai-artificial-intelligence-company-al1681562870585849000', 'https://www.ii.co.uk/news/new-york-market-close-strong-bank-results-fail-to-halt-fall-in-stocks-al1681503606765695000', 'https://www.ii.co.uk/news/tesla-slashes-prices-of-vehicles-to-improve-sales-in-europe-al1681502670465680200', 'https://www.ii.co.uk/news/new-york-market-close-tech-leads-us-stocks-higher-as-inflation-cools-al1681416910773621700', 'https://www.ii.co.uk/analysis-commentary/ian-cowie-my-tech-bets-bouncing-back-and-beating-scottish-mortgage-ii527557', 'https://www.ii.co.uk/news/global-company-events-calendar-next-7-days-al1681310531500353000', 'https://www.ii.co.uk/analysis-commentary/ii-private-investor-performance-index-q1-2023-ii527544', 'https://www.ii.co.uk/analysis-commentary/artificial-intelligence-hype-real-and-how-invest-winners-ii527528', 'https://www.ii.co.uk/news/tesla-sued-over-workers-alleged-access-to-car-video-imagery-al1681189336886811400', 'https://www.ii.co.uk/news/tesla-to-build-second-battery-plant-in-shanghai-state-media-reports-al1681048559566093700', 'https://www.ii.co.uk/analysis-commentary/most-bought-investments-march-2023-ii527481', 'https://www.ii.co.uk/news/california-jury-orders-tesla-to-pay-former-worker-in-racism-case-al1680584876117243700', 'https://www.ii.co.uk/news/new-york-market-close-soaring-oil-price-lifts-dow-holds-back-tech-al1680553004986953700', 'https://www.ii.co.uk/analysis-commentary/ii-view-tesla-deliveries-hit-new-record-ii527469', 'https://www.ii.co.uk/analysis-commentary/must-read-oil-prices-china-natwest-tesla-ii527466', 'https://www.ii.co.uk/news/tesla-reports-36-increase-in-deliveries-in-first-quarter-al1680497519874169800', 'https://www.ii.co.uk/analysis-commentary/how-two-investment-trust-analysts-are-investing-tax-year-ii527450', 'https://www.ii.co.uk/analysis-commentary/nine-last-minute-investment-trust-bargains-your-isa-ii527419', 'https://www.ii.co.uk/news/tesla-producing-5000-cars-per-week-in-brandenburg-half-of-target-al1679827413847136700', 'https://www.ii.co.uk/news/new-york-market-close-stocks-march-higher-ahead-of-fed-rate-call-al1679429660619143200', 'https://www.ii.co.uk/news/tesla-files-application-to-expand-gigafactory-plant-near-berlin-al1678986859030573000', 'https://www.ii.co.uk/analysis-commentary/ii-view-how-volkswagen-will-spend-eu180bn-next-five-years-ii527251', 'https://www.ii.co.uk/news/volkswagen-joins-e-car-price-war-as-global-rivalry-with-tesla-heats-up-al1678609070150035200', 'https://www.ii.co.uk/analysis-commentary/isa-ideas-investors-hunting-income-ii527209', 'https://www.ii.co.uk/news/new-york-market-close-stocks-end-mixed-as-focus-switches-to-jobs-data-al1678310022944378500', 'https://www.ii.co.uk/news/us-investigates-tesla-for-steering-wheels-that-can-fall-off-al1678280229563317200', 'https://www.ii.co.uk/news/global-broker-ratings-berenberg-cuts-tesla-ubs-raises-rolls-royce-al1678275446303115600', 'https://www.ii.co.uk/news/new-york-market-close-stocks-down-following-hawkish-comments-from-fed-al1678224959361713100', 'https://www.ii.co.uk/news/global-broker-ratings-hsbc-likes-diasorin-goldman-says-buy-apple-al1678189399790480600', 'https://www.ii.co.uk/analysis-commentary/high-risk-i-dont-see-it-way-investment-secrets-isa-millionaire-ii527175', 'https://www.ii.co.uk/news/prices-cut-at-tesla-again-as-it-looks-to-boost-sales-al1678169560579489900', 'https://www.ii.co.uk/news/new-york-close-us-stocks-pause-for-breath-ahead-of-powell-testimony-al1678137288729222600', 'https://www.ii.co.uk/news/new-york-close-us-stocks-end-higher-salesforce-leads-blue-chip-gains-al1677791538473578000', 'https://www.ii.co.uk/analysis-commentary/must-read-ftse-100-pearson-arm-rightmove-ii527143', 'https://www.ii.co.uk/news/tesla-shares-slip-on-lack-of-clarity-on-next-generation-vehicles-al1677775099222903400', 'https://www.ii.co.uk/analysis-commentary/most-bought-investments-february-2023-ii527132', 'https://www.ii.co.uk/news/musk-eyes-torrid-growth-at-tesla-but-offers-no-big-new-reveals-al1677738279860849300', 'https://www.ii.co.uk/analysis-commentary/10-uk-shares-warren-buffett-might-put-his-isa-2023-ii527109', 'https://www.ii.co.uk/news/tesla-to-open-plant-in-northern-mexico-government-says-al1677597324226624600', 'https://www.ii.co.uk/news/new-york-close-us-stocks-end-higher-rising-after-worst-week-of-2023-al1677533147714746700', 'https://www.ii.co.uk/news/teslas-10000-workers-producing-4000-e-cars-at-factory-near-berlin-al1677508198803934000', 'https://www.ii.co.uk/news/global-broker-ratings-jyske-cuts-bmw-socgen-cuts-burberry-al1677240162260788100', 'https://www.ii.co.uk/analysis-commentary/ftse-100-price-shocks-after-year-war-ukraine-ii527050', 'https://www.ii.co.uk/news/tesla-refutes-allegations-of-firing-employees-for-union-activity-al1676620407712933300', 'https://www.ii.co.uk/news/new-york-market-close-stocks-close-lower-after-hot-inflation-data-al1676582891322350600', 'https://www.ii.co.uk/news/tesla-recalls-362758-vehicles-in-the-us-over-self-driving-crash-risk-al1676579564782300300', 'https://www.ii.co.uk/news/bp-invests-usd1-billion-in-us-electric-vehicle-charging-points-by-2030-al1676548841161213900', 'https://www.ii.co.uk/news/someone-else-could-be-running-twitter-this-year-says-musk-al1676483748699530300', 'https://www.ii.co.uk/analysis-commentary/10-shares-diversify-your-isa-portfolio-ii526953', 'https://www.ii.co.uk/news/global-broker-ratings-hbsc-cuts-michelin-bryan-garnier-likes-danone-al1676461758268517400', 'https://www.ii.co.uk/news/buffalo-workers-launch-drive-to-become-first-tesla-union-al1676407829757200300', 'https://www.ii.co.uk/analysis-commentary/why-were-ignoring-tech-and-sticking-these-unloved-markets-ii526933', 'https://www.ii.co.uk/analysis-commentary/are-we-heading-lost-decade-investment-returns-ii526923', 'https://www.ii.co.uk/news/new-york-market-close-tech-shares-struggle-but-dow-and-sp-rise-al1676063991492078100', 'https://www.ii.co.uk/news/access-intelligence-wins-contracts-around-the-world-al1676029600371010100', 'https://www.ii.co.uk/news/global-broker-ratings-berenberg-cuts-airbus-kepler-cheuvreux-ups-abb-al1675771220803878000', 'https://www.ii.co.uk/news/new-york-market-close-equity-markets-rattled-by-interest-rate-worries-al1675718597792609400', 'https://www.ii.co.uk/analysis-commentary/ii-view-ford-suffers-tough-final-quarter-ii526839', 'https://www.ii.co.uk/news/us-jury-finds-elon-musk-not-liable-in-tesla-take-private-tweet-trial-al1675506788310064800', 'https://www.ii.co.uk/analysis-commentary/stocks-could-be-headed-new-bull-market-ii526829', 'https://www.ii.co.uk/analysis-commentary/stockwatch-rally-these-consumer-shares-justified-ii526819', 'https://www.ii.co.uk/analysis-commentary/how-long-can-growth-stock-rally-last-ii526809', 'https://www.ii.co.uk/analysis-commentary/most-bought-investments-january-2023-ii526802']

if len(all_articles_urls) > 0:
    thread_list = list()
    for url in all_articles_urls:
        t = threading.Thread(name='Test {}'.format(url), target=scrape_interactive_investor_articles(url))
        t.start()
        time.sleep(1)
        thread_list.append(t)

    for thread in thread_list:
        thread.join()

