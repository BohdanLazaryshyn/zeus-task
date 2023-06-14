# To prepare for working with these scripts, complete the following steps.
***
```
- Write in Git Bash
git clone https://github.com/BohdanLazaryshyn/zeus-task
- Open the project in your interpreter
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```

## Environment variables
create .env file in root directory with following variables
```
API_KEY='your API key'
API_SECRET='your API secret'
```

 ### If you want to work with DB you need to do the following:
* default db is sqlite
```
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```
***
# How to run the script
* This script retrieves data from the Binance API and saves it to a CSV file with a filename in the format "candles_{symbol}-{date}.csv".
* You can change the symbol and interval in the "main.py" file(see the comments in the file).
```
python main.py
```
***
# In this time you can run the script for working with data from CSV (and DB, it`s optional) form Flask API
* You can get information in the form of a candlestick chart for the symbol you are interested in
* You can get information in the form of a pie chart for the default 10 symbols or those you choose.
```
python app.py
```
***
