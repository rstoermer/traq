import os
import sqlite3
import json

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

def load_config(filename):
    with open(filename) as json_data_file:
        config = json.load(json_data_file)
    return config

def db_connect(db_path=DEFAULT_PATH):  
    con = sqlite3.connect(db_path)
    return con

def save_db(date, account, isin, name, market_value, value_symbol, pieces, total_value, acq_price):
    if os.path.isfile(DEFAULT_PATH) == False:
        statement = """
        CREATE TABLE accountholdings (
            id INTEGER PRIMARY KEY,
            date TEXT,
            account INTEGER,
            isin TEXT,
            name TEXT,
            market_value FLOAT,
            value_symbol TEXT,
            pieces INTEGER,
            total_value FLOAT,
            acq_price FLOAT)
        """
        con = db_connect() # connect to the database
        cur = con.cursor() # instantiate a cursor obj
        cur.execute(statement)

    con = db_connect() # connect to the database
    cur = con.cursor() # instantiate a cursor obj        
    statement = """INSERT INTO accountholdings
    (date, account, isin, name, market_value, value_symbol, pieces, total_value, acq_price)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cur.execute(statement, (date, account, isin, name, market_value, value_symbol, pieces, total_value, acq_price))
    con.commit()
    con.close()