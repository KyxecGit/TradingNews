import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = "twilio номер"
VERIFIED_NUMBER = "телефон"

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "API КЛЮЧ ИЗ ALPHAVANTAGE"
NEWS_API_KEY = "API КЛЮЧ ИЗ NEWSAPI"
TWILIO_SID = "TWILIO АККАУНТ"
TWILIO_AUTH_TOKEN = "TWILIO ТОКЕН"

#Получаем вчерашнюю цену закрытия
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

#Позавчерашняя цена закрытия
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

#Ищем разницу
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#Получаем разницу в процентах
diff_percent = round((difference / float(yesterday_closing_price)) * 100)

#Если разница превышает 5% отправляем новости на телефон.
if abs(diff_percent) > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    #Используем срез чтобы получить три статьи
    three_articles = articles[:3]


    #Создаем список из первых трех статей с помощью генератора 
    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nЗаголовок: {article['title']}. \nОписание: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    #Отправляем выбранные статьи с помощью Twilio
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER)
