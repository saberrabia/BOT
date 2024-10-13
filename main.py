import ccxt
import pandas as pd
import numpy as np
import time
import asyncio
from telegram import Bot

# إعداد البورصة
exchange = ccxt.okx()  # استبدال Binance بـ Coinbase
symbols = [
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT',
]
timeframe = '15m'

# إعداد بوت تلجرام
TELEGRAM_API_TOKEN = '7391308695:AAGZ2pF2NwuNOTAdC9034YBeJhHrkpLPBvM'
CHAT_ID = '7039034340'
bot = Bot(token=TELEGRAM_API_TOKEN)

# دالة للحصول على بيانات الشمعة
def fetch_data(symbol):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# دالة لحساب EMA
def calculate_ema(data, period):
    return data['close'].ewm(span=period, adjust=False).mean()

# دالة لتوليد التنبيهات
def check_signals(df):
    df['ema_5'] = calculate_ema(df, 5)
    df['ema_100'] = calculate_ema(df, 100)
    df['rolling_mean'] = df['close'].rolling(window=20).mean()
    df['rolling_std'] = df['close'].rolling(window=20).std()
    df['upper'] = df['rolling_mean'] + (df['rolling_std'] * 2)
    df['lower'] = df['rolling_mean'] - (df['rolling_std'] * 2)

    last_row = df.iloc[-1]
    previous_row = df.iloc[-2]

    # شروط الشراء
    buy_signal = (last_row['close'] > last_row['upper']) and (last_row['high'] == df['high'].max()) and (last_row['ema_5'] > last_row['ema_100'])

    # شروط البيع
    sell_signal = (last_row['close'] < last_row['lower']) and (last_row['low'] == df['low'].min()) and (last_row['ema_5'] < last_row['ema_100'])

    return buy_signal, sell_signal

# دالة لإرسال الرسالة عبر تلجرام
async def send_message(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

# حلقة التحقق المستمرة
async def main():
    previous_signals = {symbol: {'buy': False, 'sell': False} for symbol in symbols}

    while True:
        for symbol in symbols:
            df = fetch_data(symbol)
            buy_signal, sell_signal = check_signals(df)

            # طباعة التنبيهات وإرسالها عبر تلجرام
            if buy_signal and not previous_signals[symbol]['buy']:
                message = f"تنبيه: إشارة شراء لـ {symbol} في {df['timestamp'].iloc[-1]}"
                print(message)
                await send_message(message)
                previous_signals[symbol]['buy'] = True
                previous_signals[symbol]['sell'] = False

            if sell_signal and not previous_signals[symbol]['sell']:
                message = f"تنبيه: إشارة بيع لـ {symbol} في {df['timestamp'].iloc[-1]}"
                print(message)
                await send_message(message)
                previous_signals[symbol]['sell'] = True
                previous_signals[symbol]['buy'] = False

        await asyncio.sleep(900)  # الانتظار لمدة 15 دقيقة قبل التحقق مرة أخرى

if __name__ == "__main__":
    asyncio.run(main())

