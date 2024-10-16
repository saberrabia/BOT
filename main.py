import ccxt
import pandas as pd
import asyncio
from telegram import Bot

# إعداد مفاتيح API
API_KEY = 'vb8XtTkcJLgNPV4YksosK2OxlLxSR29CYC7Lk9SdfRVI7bJMEMoIlom9zrpZxD27'
API_SECRET = 'xVAsBuzajfnWnxm5BYfTuMWdhyVgsGs0EOR9DBsbxfvsOd4ZfdipQO4aZ9uVakDe'
TELEGRAM_TOKEN = '7391308695:AAGZ2pF2NwuNOTAdC9034YBeJhHrkpLPBvM'
CHAT_ID = '7039034340'

# إعداد البورصة
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

# إعداد بوت تلغرام
bot = Bot(token=TELEGRAM_TOKEN)

# قائمة الرموز الزمنية
symbols = [
    'BTC/USDT', 'ETH/USDT', 'NEIRO/USDT', 'SOL/USDT', '1000PEPE/USDT',
     'WIF/USDT', '1MBABYDOGE/USDT', 'ENA/USDT', 'WLD/USDT',
    'POPCAT/USDT', 'EIGEN/USDT', 'DOGE/USDT', 'DOGS/USDT', 'SAGA/USDT',
    'TAO/USDT', 'TIA/USDT', 'SEI/USDT', 'SXP/USDT', 'REEF/USDT',
    'TURBO/USDT', 'BNB/USDT', '1000SHIB/USDT', 'ORDI/USDT', 'FTM/USDT',
    'AVAX/USDT', 'XRP/USDT', 'PEOPLE/USDT', 'MEW/USDT', 'APT/USDT',
    'UNI/USDT', 'AXL/USDT', 'BANANA/USDT', 'CATI/USDT', 'ARKM/USDT',
    'FET/USDT', 'NOT/USDT', 'NEAR/USDT', '1000SATS/USDT', 'BOME/USDT',
    'CELO/USDT', 'DIA/USDT', '1000BONK/USDT', 'MYRO/USDT', '1000FLOKI/USDT',
    'ARK/USDT', 'HMSTR/USDT', 'LINK/USDT', 'OP/USDT', 'AAVE/USDT',
    'FIL/USDT', 'ADA/USDT', 'IO/USDT', 'ARB/USDT', 'BIGTIME/USDT',
    'INJ/USDT', 'BCH/USDT', 'TRX/USDT', 'TON/USDT', 'CFX/USDT',
    '1000RATS/USDT', 'GALA/USDT', 'OM/USDT', 'DOT/USDT', 'ZRO/USDT',
    'STX/USDT', 'ZEC/USDT', 'ALT/USDT', 'CHZ/USDT', 'ETHFI/USDT',
    'PHB/USDT', 'REZ/USDT', 'HIFI/USDT', 'RUNE/USDT', 'UXLINK/USDT',
    'ETC/USDT', 'LTC/USDT', 'GAS/USDT', 'DYDX/USDT', 'W/USDT',
    'ONDO/USDT', 'PENDLE/USDT', 'RENDER/USDT', 'SUN/USDT', 'DYM/USDT',
    'BNX/USDT', 'XAI/USDT', 'CRV/USDT', 'MEME/USDT', 'AR/USDT',
    'SUPER/USDT', 'TRB/USDT', 'FIDA/USDT', 'STRK/USDT', 'JUP/USDT',
    'LISTA/USDT', 'CKB/USDT', 'JTO/USDT', 'MKR/USDT', 'LDO/USDT',
    'ATOM/USDT', 'JASMY/USDT', 'ZK/USDT', 'ENS/USDT', 'ORBS/USDT',
    'APE/USDT', 'POL/USDT', 'BLUR/USDT', 'VIDT/USDT', 'ICP/USDT',
    'ZETA/USDT', 'GRT/USDT', 'AI/USDT', 'BB/USDT', 'ETHW/USDT',
    'SUSHI/USDT', 'STORJ/USDT', 'EOS/USDT', 'VANRY/USDT', 'KAVA/USDT',
    'RARE/USDT', 'OMNI/USDT', 'SYN/USDT', 'NEO/USDT', 'KAS/USDT',
    'IMX/USDT', 'AXS/USDT', 'GMT/USDT', 'THETA/USDT', 'SAND/USDT',
    '1000LUNC/USDT', 'PIXEL/USDT', 'ROSE/USDT', 'DAR/USDT', 'UMA/USDT',
    'AEVO/USDT', 'MANTA/USDT', 'XLM/USDT', 'YGG/USDT', 'MINA/USDT',
    'UNFI/USDT', 'LPT/USDT', 'BEAMX/USDT', 'NFP/USDT', 'USTC/USDT',
    'BAKE/USDT', 'BRETT/USDT', 'HBAR/USDT', 'PORTAL/USDT', 'LQTY/USDT',
    'POWR/USDT', 'PYTH/USDT', 'KDA/USDT', 'COTI/USDT', 'BSW/USDT',
    'MASK/USDT', 'CYBER/USDT', 'WOO/USDT', 'TNSR/USDT', 'POLYX/USDT',
    'XMR/USDT', 'ACH/USDT', 'GLM/USDT', 'ONG/USDT', 'SSV/USDT',
    'ALPACA/USDT', 'FIO/USDT', 'MAVIA/USDT', 'RDNT/USDT', 'TRU/USDT',
    'KEY/USDT', 'HOOK/USDT', 'EGLD/USDT', 'TWT/USDT', 'MANA/USDT',
    'TOKEN/USDT', 'VET/USDT', 'ALGO/USDT', 'LUNA2/USDT', 'DUSK/USDT',
    'ACE/USDT', '1000XEC/USDT', 'AGLD/USDT', 'WAXP/USDT', 'RSR/USDT',
    'SNX/USDT', '1INCH/USDT', 'FLOW/USDT', 'HIGH/USDT', 'EDU/USDT',
    'ONE/USDT', 'JOE/USDT', 'CAKE/USDT', 'LOOM/USDT', 'IOTX/USDT',
    'GTC/USDT', 'METIS/USDT', 'ONT/USDT', 'COMP/USDT', 'ZIL/USDT',
    'ZEN/USDT', 'CHR/USDT', 'MBOX/USDT', 'API3/USDT', 'G/USDT',
    'AMB/USDT', 'ASTR/USDT', 'VOXEL/USDT', 'AUCTION/USDT', 'ALICE/USDT',
    'ID/USDT', 'BOND/USDT', 'RONIN/USDT', 'XTZ/USDT', 'MAV/USDT',
    'QNT/USDT', 'RVN/USDT', 'ILV/USDT', 'NMR/USDT', 'SYS/USDT',
    'IOTA/USDT', 'QTUM/USDT', 'GMX/USDT', 'REN/USDT', 'STMX/USDT',
    'MTL/USDT', 'FXS/USDT', 'BICO/USDT', 'LRC/USDT', 'BEL/USDT',
    'COS/USDT', 'LINA/USDT', 'AERGO/USDT', 'BAND/USDT', 'ENJ/USDT',
    'BLZ/USDT', 'DODO/USDT', 'CELR/USDT', 'LEVER/USDT', 'SKL/USDT',
    'OMG/USDT', 'REI/USDT', 'NULS/USDT', 'MAGIC/USDT', 'YFI/USDT',
    'HOT/USDT', 'MOVR/USDT', 'QUICK/USDT', 'T/USDT', 'ZRX/USDT',
    'FLM/USDT', 'RIF/USDT', 'KSM/USDT', 'DASH/USDT', 'TLM/USDT',
    'LOKA/USDT', 'XVG/USDT', 'C98/USDT', 'NTRN/USDT', 'IOST/USDT',
    'BSV/USDT', 'ATA/USDT', 'ALPHA/USDT', 'RPL/USDT', 'GHST/USDT',
    'SPELL/USDT', 'FLUX/USDT', 'KLAY/USDT', 'ANKR/USDT', 'RLC/USDT',
    'BAL/USDT', 'BAT/USDT', 'CTSI/USDT', 'OGN/USDT', 'STG/USDT',
    'KNC/USDT', 'STEEM/USDT', 'PERP/USDT', 'CHESS/USDT', 'LIT/USDT',
    'BADGER/USDT', 'ICX/USDT', 'SFP/USDT', 'XVS/USDT', 'NKN/USDT',
    'ARPA/USDT', 'DENT/USDT', 'XEM/USDT', 'BTCDOM/USDT', 'COMBO/USDT',
    'OXT/USDT', 'HFT/USDT', 'BNT/USDT', 'LSK/USDT', 'DEFI/USDT',
]


timeframe = '1m'

# دالة لجلب بيانات الشمعة
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

    # شروط الشراء
    buy_signal = (last_row['close'] > last_row['upper']) and (last_row['high'] == df['high'].max()) and (last_row['ema_5'] > last_row['ema_100'])

    # شروط البيع
    sell_signal = (last_row['close'] < last_row['lower']) and (last_row['low'] == df['low'].min()) and (last_row['ema_5'] < last_row['ema_100'])

    return buy_signal, sell_signal

# دالة لحساب تغير السعر
def fetch_price_change(symbol):
    ohlcv = exchange.fetch_ohlcv(symbol, '1h', limit=24)  # 24 ساعة
    prices = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    prices['timestamp'] = pd.to_datetime(prices['timestamp'], unit='ms')

    change = (prices['close'].iloc[-1] - prices['close'].iloc[0]) / prices['close'].iloc[0] * 100
    return change

# دالة لإرسال التنبيهات عبر تلغرام
async def send_telegram_alert(message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

# حلقة التحقق المستمرة
async def main():
    previous_signals = {symbol: {'buy': False, 'sell': False} for symbol in symbols}

    while True:
        price_changes = {}

        # جلب تغييرات الأسعار
        for symbol in symbols:
            price_changes[symbol] = fetch_price_change(symbol)

        # الحصول على أعلى وأدنى 10 عملات
        top_10 = sorted(price_changes.items(), key=lambda x: x[1], reverse=True)[:10]
        bottom_10 = sorted(price_changes.items(), key=lambda x: x[1])[:10]

        # إعداد قائمة للعملات التي سنقوم بالتنبيه عنها
        alerts = top_10 + bottom_10

        for symbol, change in alerts:
            df = fetch_data(symbol)
            buy_signal, sell_signal = check_signals(df)

            # إرسال التنبيهات عبر تلغرام
            if buy_signal and not previous_signals[symbol]['buy']:
                message = f"تنبيه: إشارة شراء لـ {symbol} (تغير: {change:.2f}%) في {df['timestamp'].iloc[-1]}"
                print(message)
                previous_signals[symbol]['buy'] = True
                previous_signals[symbol]['sell'] = False

                await send_telegram_alert(message)

            if sell_signal and not previous_signals[symbol]['sell']:
                message = f"تنبيه: إشارة بيع لـ {symbol} (تغير: {change:.2f}%) في {df['timestamp'].iloc[-1]}"
                print(message)
                previous_signals[symbol]['sell'] = True
                previous_signals[symbol]['buy'] = False

                await send_telegram_alert(message)

        await asyncio.sleep(60)  # الانتظار لمدة 1 دقيقة


if __name__ == "__main__":
    asyncio.run(main())

