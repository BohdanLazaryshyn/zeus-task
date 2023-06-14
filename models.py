from dataclasses import dataclass, fields

from config import db


class CandleInfoSQL(db.Model):                             # model for work with SQLite database (SQLAlchemy) (optional)
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    time_open = db.Column(db.String(20), nullable=False)
    open_price = db.Column(db.Float, nullable=False)
    high_price = db.Column(db.Float, nullable=False)
    low_price = db.Column(db.Float, nullable=False)
    close_price = db.Column(db.Float, nullable=False)
    volume = db.Column(db.Float, nullable=False)
    time_close = db.Column(db.String(20), nullable=False)


@dataclass
class CandleInfoCSV:                                        # model for work with CSV file
    symbol: str
    time_open: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    time_close: str


CANDLE_FIELD = [field.name for field in fields(CandleInfoCSV)]   # list of fields for CSV file
