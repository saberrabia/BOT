import ccxt
import pandas as pd
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
from time import sleep
from flask import Flask, request
# إعدادات بوت تلجرام
TELEGRAM_TOKEN = '7391308695:AAGZ2pF2NwuNOTAdC9034YBeJhHrkpLPBvM'
CHAT_ID = '7039034340'
bot = Bot(token=TELEGRAM_TOKEN)

# إعدادات KuCoin
kucoin = ccxt.kucoin({
    'apiKey': '6607359fb8fd3800012ae3ba',
    'secret': '@Se123456789',
    'password': '9499b29e-4f5f-4453-8468-1346f9a1308d'
})

def fetch_symbols():
    markets = kucoin.load_markets()
    return [symbol for symbol in markets if markets[symbol]['quote'] == 'USDT']

def fetch_ohlcv(symbol, timeframe):
    return kucoin.fetch_ohlcv(symbol, timeframe)

def calculate_ema(prices, period):
    return pd.Series(prices).ewm(span=period).mean().iloc[-1]

def fetch_bollinger_bands(prices, period):
    series = pd.Series(prices)
    sma = series.rolling(window=period).mean().iloc[-1]
    std = series.rolling(window=period).std().iloc[-1]
    upper_band = sma + (std * 2)
    lower_band = sma - (std * 2)
    return upper_band, lower_band

def check_conditions(symbol):
    try:
        ohlcv_1m = fetch_ohlcv(symbol, '1m')
        ohlcv_1w = fetch_ohlcv(symbol, '1w')

        # الحصول على الأسعار
        high_prices_1m = [x[2] for x in ohlcv_1m]
        high_price_1m = high_prices_1m[-1]
        high_price_1w = max([x[2] for x in ohlcv_1w])

        # حساب EMA5 و EMA100
        close_prices_1m = [x[4] for x in ohlcv_1m]
        ema5 = calculate_ema(close_prices_1m, 5)
        ema100 = calculate_ema(close_prices_1m, 100)

        # حساب بولنجر باند
        upper_band, _ = fetch_bollinger_bands(close_prices_1m, 20)

        if ema5 > ema100 and high_price_1m > upper_band and high_price_1m == high_price_1w:
            return high_price_1m
    except Exception as e:
        print(f"Error with {symbol}: {e}")
    return None

def send_alert(symbol, price):
    message = f"سعر إغلاق العملة: {price}\nاسم العملة: {symbol}"
    bot.send_message(chat_id=CHAT_ID, text=message)

def monitor_symbols():
    symbols = fetch_symbols()
    print(f"Monitoring {len(symbols)} symbols...")
    for symbol in symbols:
        price = check_conditions(symbol)
        if price:
            send_alert(symbol, price)
        sleep(1)  # لتجنب تجاوز الحدود المسموح بها من قبل API
@app.route('/')
def home(): 

	return 'Your telegram bot is Working !'
    
def main():
    while True:
        monitor_symbols()
        sleep(60)  # الانتظار لمدة 60 ثانية قبل المراقبة مرة أخرى

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000)
