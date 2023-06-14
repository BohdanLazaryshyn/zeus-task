import os
import secrets

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///market_data.db"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
