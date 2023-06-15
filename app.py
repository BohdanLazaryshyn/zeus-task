import csv

from flask import render_template, request, flash
import plotly.graph_objs as go

from config import app
from main import get_candles, SYMBOL_LIST
from models import CandleInfoSQL
from utils import build_graph


def get_capital_data(symbols: list, interval, limit) -> dict:        # Get capital data for pie chart from binance api
    data = {}
    for symbol in symbols:
        candle_info = get_candles(symbol, interval, limit)
        # save_candles_to_csv_for_pie(candle_info, symbol)         # Save candles to csv (optional)
        # save_candles_to_db(candle_info, symbol)                  # Save candles to db(sqlite3) (optional)
        data[symbol] = []
        for candle in candle_info:
            capital = candle.close_price * candle.volume
            data[symbol].append(capital)
        data[symbol] = sum(data[symbol])
    return data


def symbol_is_not_valid(symbol: str) -> bool:
    if symbol not in SYMBOL_LIST:
        flash(f"Введено невірний символ {symbol}")
        return True


def symbol_repeat(symbol_list: list) -> bool:
    for symbol in symbol_list:
        if symbol_list.count(symbol) > 1:
            flash(f"Symbol {symbol} is repeated")
            return True


def get_data(symbol: str) -> list:
    data = []
    try:
        with open(f"candles_{symbol}.csv", "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                data.append(row)
        return data
    except FileNotFoundError:
        flash(f"Для символу {symbol} немає даних")


@app.route("/", methods=["GET"])
def date_form():
    return render_template("index.html")


@app.route("/data_csv", methods=["GET"])
def get_data_from_csv():

    symbol = request.args.get("symbol_csv")

    if not symbol:
        symbol = "BNBUSDT"
    else:
        if symbol_is_not_valid(symbol):
            return render_template("index.html")
    candles = get_data(symbol)

    if not candles:
        return render_template("index.html")

    time_open = [row[1] for row in candles if symbol in row]
    prices_open = [row[2] for row in candles if symbol in row]
    prices_high = [row[3] for row in candles if symbol in row]
    prices_low = [row[4] for row in candles if symbol in row]
    prices_close = [row[5] for row in candles if symbol in row]

    fig = build_graph(
        time_open, prices_open, prices_high, prices_low, prices_close, symbol
    )
    return fig.to_html(full_html=False)


@app.route("/data_db", methods=["GET"])                     # Get data from db and build graph (optional)
def get_data_from_db():
    symbol = request.args.get("symbol_db")

    if not symbol:
        symbol = "BNBUSDT"
    else:
        if symbol_is_not_valid(symbol):
            return render_template("index.html")

    candles = CandleInfoSQL.query.filter_by(symbol=symbol).all()

    if not candles:
        flash(f"Для символу {symbol} немає даних в базі даних")
        return render_template("index.html")

    time_open = [candle.time_open for candle in candles]
    prices_open = [candle.open_price for candle in candles]
    prices_high = [candle.high_price for candle in candles]
    prices_low = [candle.low_price for candle in candles]
    prices_close = [candle.close_price for candle in candles]

    fig = build_graph(
        time_open, prices_open, prices_high, prices_low, prices_close, symbol
    )
    return fig.to_html(full_html=False)


@app.route("/data_csv_pie", methods=["GET"])
def get_data_from_csv_pie():
    interval = request.args.get("interval")
    limit = request.args.get("limit")
    symbols = [request.args.get(f"symbol_{i}") for i in range(1, 11)]             # Get symbols from form for pie chart

    for symbol in symbols:
        if symbol_is_not_valid(symbol):
            return render_template("index.html")
    if symbol_repeat(symbols):
        return render_template("index.html")

    volumes = get_capital_data(symbols, interval, limit)

    fig = go.Figure(data=[go.Pie(labels=symbols, values=list(volumes.values()))])

    fig.update_layout(
        title="Capital of symbols",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    return fig.to_html(full_html=False)


if __name__ == '__main__':
    app.run()
