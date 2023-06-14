import csv
import datetime
import os

from dataclasses import astuple
import plotly.graph_objs as go

from config import app, db
from models import CANDLE_FIELD, CandleInfoSQL


def read_candles(candle, symbol, class_name):    # candle - list of candle info from binance api
    return class_name(                           # class_name - class of db or CSV model
        symbol=symbol,
        time_open=datetime.datetime.fromtimestamp(candle[0] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
        open_price=round(float(candle[1]), 8),
        high_price=round(float(candle[2]), 8),
        low_price=round(float(candle[3]), 8),
        close_price=round(float(candle[4]), 8),
        volume=round(float(candle[5]), 8),
        time_close=datetime.datetime.fromtimestamp(candle[6] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
    )


def save_candles_to_csv_for_pie(candles_info, symbol):       # save candles to csv for pie chart (optional)
    filename = f"candles_{symbol} - PIE.csv"

    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(CANDLE_FIELD)
        writer.writerows([astuple(item) for item in candles_info])


def save_candles_to_csv(candles_info, symbol):
    filename = f"candles_{symbol}.csv"
    if not os.path.isfile(filename):
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerow(CANDLE_FIELD)

    with open(filename, "a") as f:
        writer = csv.writer(f)
        writer.writerows([astuple(item) for item in candles_info if item is not None])


def save_candles_to_db(candles_info: list, symbol):        # save candles to db(sqlite3) (optional)
    with app.app_context():
        for candle in candles_info:
            candle = read_candles(candle, symbol, CandleInfoSQL)
            db.session.add(candle)
        db.session.commit()


def build_graph(time, open_price, high_price, low_price, close_price, symbol):    # build candlestick chart with plotly
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=time,
                                 open=open_price,
                                 high=high_price,
                                 low=low_price,
                                 close=close_price))
    fig.update_layout(
        title=f"{symbol} Candlestick Chart",
        xaxis_title="Time",
        yaxis_title="Price",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )
    return fig
