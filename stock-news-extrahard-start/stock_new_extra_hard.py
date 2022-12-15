import requests
from twilio.rest import Client
import datetime
import math
# from newsapi import NewsApiClient
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
alpha_api_key = "0FC5B5FORD836Y5H"
url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={alpha_api_key}"
response = requests.get(url)
data = response.json()["Time Series (Daily)"]

big_increases = []
stock_emoji = None
data_list = [value for (key, value) in data.items()]
for i in range(len(data_list)-2):
    current_stock = data_list[i]["4. close"]
    yesterday_stock = data_list[i+1]["4. close"]
    difference = float(yesterday_stock) - float(current_stock)
    percentage = round((difference / float(yesterday_stock)) * 100, 1)
    if percentage > 5:
        big_increases += [[percentage]]
    if difference > 0:
        stock_emoji = "🔺"
    else:
        stock_emoji = "🔻"

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
news_api_key = "40fff642e04d4b2189b5c693bf7432e3"
if big_increases:
    url = (f'https://newsapi.org/v2/everything?'
           f'q={COMPANY_NAME}&'
           'from={big_increases[0][0]}&'
           'sortBy=popularity&'
           f'apiKey={news_api_key}&'
           'searchIn=title,description&'
           'pageSize=3'
           )
    sources = requests.get(url).json()["articles"][0]
    big_increases[0].append([sources["title"], sources["description"]])
print(big_increases)

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
account_sid = "AC8d94d30af05d44101787ca272e41de56"
auth_token = "416c08a8fd0b9991f2749587b890a9e0"
client = Client(account_sid, auth_token)
message = client.messages.create(
             body=f"TSLA: 🔺{big_increases[0][0]}%\nHeadline: {big_increases[0][1][0]}\nBrief: {big_increases[0][1][1]}",
             from_='+19283707954',
             to='+995558871331'  # 995593319561
         )
print(message.sid)

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
