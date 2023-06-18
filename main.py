from binance.spot import Spot as Client
import schedule as schedule

from config import API_KEY, API_SECRET
from utils import read_candles, save_candles_to_csv, CandleInfoCSV

api_key = API_KEY                                                            # Your api key for work with binance api
api_secret = API_SECRET                                                      # Your api secret for work with binance api

client = Client(api_key, api_secret)

SYMBOL = "BNBUSDT"                                                                        # Trading symbol,
SYMBOL_LIST = [
    coin["symbol"] for coin in client.exchange_info()["symbols"]                          # List of trading symbols
]
INTERVAL = "1m"                                                                           # Candle interval in minutes
LIMIT = 100                                                                               # Number of candles to request


def get_candles(symbol, interval, limit):
    candles = client.klines(symbol=symbol, interval=interval, limit=limit)
    data = []
    for candle in candles:
        candle_info_csv = read_candles(candle, symbol, CandleInfoCSV)
        data.append(candle_info_csv)
    # save_candles_to_db(candles, symbol)                            # Save candles to db(sqlite3) (optional)
    return data


def job():
    data = get_candles(SYMBOL, INTERVAL, LIMIT)
    save_candles_to_csv(data, SYMBOL)
    print(data)


def main(symbol: str = SYMBOL, interval: str = INTERVAL, limit: int = LIMIT):
    global SYMBOL, INTERVAL, LIMIT
    LIMIT = limit
    SYMBOL = symbol
    INTERVAL = interval
    if symbol not in SYMBOL_LIST:
        raise ValueError(f"Invalid symbol - '{symbol}'")
    intervals = {
        "1m": 1, "3m": 3, "5m": 5, "15m": 15, "30m": 30, "1h": 60, "2h": 120, "4h": 240,
        "6h": 360, "8h": 480, "12h": 720, "1d": 1440, "3d": 4320, "1w": 10080, "1M": 43200
    }
    if interval not in intervals:
        raise ValueError(f"Invalid interval - '{interval}'")

    schedule_interval = intervals[INTERVAL]
    if schedule_interval < 60:
        schedule.every(schedule_interval).minutes.do(job)
    elif schedule_interval < 1440:
        schedule.every(schedule_interval // 60).hours.do(job)
    elif schedule_interval < 10080:
        schedule.every(schedule_interval // 1440).days.at("12:00").do(job)
    else:
        if INTERVAL == "1w":
            schedule.every().sunday.at("12:00").do(job)
        elif INTERVAL == "1M":
            schedule.every().month.at("12:00").do(job)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main(SYMBOL, INTERVAL, LIMIT)       # Run main() with "Coin", "interval", "num of candles" to start scheduler
    INTERVAL_LIST = [                   # List of available intervals
        "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"
    ]
