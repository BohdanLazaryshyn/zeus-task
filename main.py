from binance.spot import Spot as Client
import schedule as schedule

from config import API_KEY, API_SECRET
from models import CandleInfoCSV
from utils import read_candles, save_candles_to_csv

api_url = "https://api.binance.com/api/v3"

api_key = API_KEY                              # Your api key
api_secret = API_SECRET                        # Your api secret

client = Client(api_key, api_secret)    # Create client object

SYMBOL = "BNBUSDT"  # Trading symbol,
SYMBOL_LIST = [coin["symbol"] for coin in client.exchange_info()["symbols"]]  # List of trading symbols
INTERVAL = "1m"  # Candle interval in minutes
LIMIT = 100  # Number of candles to request


def get_candles(symbol, interval, limit):       # Get candles from binance api and return list of CandleInfoCSV objects
    candles = client.klines(symbol=symbol, interval=interval, limit=limit)
    data = []
    for candle in candles:
        candle_info_csv = read_candles(candle, symbol, CandleInfoCSV)
        data.append(candle_info_csv)
    # save_candles_to_db(candles, symbol)                            # Save candles to db(sqlite3) (optional)
    return data


def job():                                      # Job for schedule module
    data = get_candles(SYMBOL, INTERVAL, LIMIT)           # Get candles from binance api
    save_candles_to_csv(data, SYMBOL)                     # Save candles to csv
    print(data)


def main(symbol: str = SYMBOL, interval: str = INTERVAL, limit: int = LIMIT):  # Main function to start scheduler
    global SYMBOL, INTERVAL, LIMIT
    LIMIT = limit
    SYMBOL = symbol
    INTERVAL = interval
    if symbol not in SYMBOL_LIST:
        raise ValueError(f"Invalid symbol - '{symbol}'")
    if INTERVAL == "1m":
        schedule.every(1).minutes.do(job)
    if INTERVAL == "3m":
        schedule.every(3).minutes.do(job)
    if INTERVAL == "5m":
        schedule.every(5).minutes.do(job)
    if INTERVAL == "15m":
        schedule.every(15).minutes.do(job)
    if INTERVAL == "30m":
        schedule.every(30).minutes.do(job)
    if INTERVAL == "1h":
        schedule.every().hour.do(job)
    if INTERVAL == "2h":
        schedule.every(2).hours.do(job)
    if INTERVAL == "4h":
        schedule.every(4).hours.do(job)
    if INTERVAL == "6h":
        schedule.every(6).hours.do(job)
    if INTERVAL == "8h":
        schedule.every(8).hours.do(job)
    if INTERVAL == "12h":
        schedule.every(12).hours.do(job)
    if INTERVAL == "1d":
        schedule.every().day.at("12:00").do(job)
    if INTERVAL == "3d":
        schedule.every(3).days.at("12:00").do(job)
    if INTERVAL == "1w":
        schedule.every().sunday.at("12:00").do(job)
    if INTERVAL == "1M":
        schedule.every().month.at("12:00").do(job)

    while True:
        schedule.run_pending()


if __name__ == "__main__":
    main(SYMBOL, INTERVAL, LIMIT)       # Run main() with "Coin", "interval", "num of candles" to start scheduler
    INTERVAL_LIST = [             # List of available intervals
        "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"
    ]
