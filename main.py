import csv
import datetime
import os
from dataclasses import astuple

from binance.spot import Spot as Client

from config import db, app
from models import CANDLE_FIELD, CandleInfoCSV, CandleInfoSQL

api_url = "https://api.binance.com/api/v3"

api_key = "8006684a12dd734255d10da576cb1a06ce5dc7efdf8023d2b14f562466a72cc1"
api_secret = "3aa95ccd1504d03ddc2ed46dad27643416d81d4456fac129d11abba41cafa805"

client = Client(api_key, api_secret)

SYMBOL = "BNBUSDT"  # Trading symbol,
SYMBOL_LIST = [coin["symbol"] for coin in client.exchange_info()["symbols"]]  # List of trading symbols
INTERVAL = "30m"  # Candle interval in minutes
INTERVAL_LIST = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]  # List of candle intervals
LIMIT = 1000  # Number of candles to request


def read_candles(candle, symbol, class_name):
    return class_name(
        symbol=symbol,
        time_open=datetime.datetime.fromtimestamp(candle[0] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
        open_price=round(float(candle[1]), 8),
        high_price=round(float(candle[2]), 8),
        low_price=round(float(candle[3]), 8),
        close_price=round(float(candle[4]), 8),
        volume=round(float(candle[5]), 8),
        time_close=datetime.datetime.fromtimestamp(candle[6] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
        base_asset_volume=round(float(candle[7]), 8),
        number_of_trades=candle[8],
        taker_buy_base_asset_volume=candle[9],
    )


def get_candles(symbol, interval, limit):
    candles = client.klines(symbol=symbol, interval=interval, limit=limit)
    data = []
    with app.app_context():
        for candle in candles:
            candle_info_csv = read_candles(candle, symbol, CandleInfoCSV)
            candle_info_db = read_candles(candle, symbol, CandleInfoSQL)
            data.append(candle_info_csv)
            db.session.add(candle_info_db)
            db.session.commit()
    return data


def save_candles_to_csv(candles_info):
    filename = "candles_1.csv"

    if not os.path.isfile(filename):
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerow(CANDLE_FIELD)

    with open(filename, "a") as f:
        writer = csv.writer(f)
        writer.writerows([astuple(item) for item in candles_info])


if __name__ == "__main__":
    data = get_candles("BNBUSDT", INTERVAL, LIMIT)
    save_candles_to_csv(data)
    print(data)
