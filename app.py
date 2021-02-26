import datetime
import streamlit as st
import yfinance as yf
import sqlite3
from sqlite3 import Error
import os.path


database = r".\DB\portfolio.db"


# --- Definition of Functions ---
# --- Definitions of DB access ---
def check_conn():
    if os.path.isfile('.DB\portfolio.db'):
        print("File exist")
    else:
        print("File not exist")

def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)

    return conn

def create_portfolio_entry(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = """ CREATE TABLE IF NOT EXISTS portfolio (
                                        portfolio_ID integer NOT NULL,
                                        stock text NOT NULL,
                                        buyin double NOT NULL,
                                        buyindate date
                                    ); """
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def select_all_playbacks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM portfolio")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def get_amount_of_playbacks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    return cur.execute("SELECT SUM * FROM portfolio")


# --- Read and make SQL Available to edit ---
listelement = [('BMW.DE', '50.25', '', )]

# will return the list of saved stocks from file "mystocks.txt"
def read_saved_stocks():
    file = open("mystocks.txt", "r")
    filecontent_array = file.read().split(",")
    return filecontent_array


def get_USD_to_EUR():
    USDTicker = yf.Ticker("USDEUR=X")
    value = USDTicker.info["bid"]
    return value


# will create the user input features
def user_input_features():
    stocksymbol = st.sidebar.text_input("Please enter a stock")
    stockoption = st.sidebar.selectbox('Or select a stock from the list below.', favoredstocks)
    startDate = st.sidebar.date_input("Beginn of Timeframe", datetime.date(2010, 5, 30))
    endDate = st.sidebar.date_input("End of Timeframe", datetime.date.today())
    if stocksymbol == "":
        user_input_array = [stockoption, startDate, endDate]
    else:
        user_input_array = [stocksymbol, startDate, endDate]
    return user_input_array


# --- Website Structure and Design ---

# --- Prep Data ---
# Array built: 2d
# [ [ Stockname ,  Stockvalue_now, Stockvalue_old, Stockvalue_diff, Buyindate, Totalmoney  ]
#   next stock, next stock

st.write("""
# Stock Price Application
### - Currently in test phase. See Description at bottom. -
Closing price per day is shown. 1 Dataset per day.
""")
# sidebar with input parameters
st.sidebar.header('User Input Parameters')

favoredstocks = read_saved_stocks()
user_input = user_input_features()


# Check if show own stocks or not
if st.checkbox('Show own Stocks'):
    st.write('Personal Portfolio. To be added')

else:

    # define the ticker symbol
    stockname = user_input[0]
    # get data on this ticker
    tickerData = yf.Ticker(stockname)
    # st.write(yf.Ticker(stockname))
    # get the historical prices for this ticker
    user_startdate = user_input[1]
    user_enddate = user_input[2]
    # Open	High	Low	Close	Volume	Dividends	Stock Splits
    tickerDf = tickerData.history(period='1d', start=user_startdate, end=user_enddate)
    # st.write(tickerDf.empty )

    if tickerDf.empty:
        st.write("""No Data found for entry. Please enter another stock-identifyer""")
    else:
        st.write("Stock Name **", str(tickerData.info["longName"]), "**")
        st.write("Current Ask Price **", str(tickerData.info["ask"]), str(tickerData.info["currency"]), "**")
        #refactor Dollar into Euro, when stock is traded in Euros
        if str(tickerData.info["currency"]) == "USD":
            st.write("That equals **", str(tickerData.info["ask"] * get_USD_to_EUR()), "€ **")
        st.write("""Closure Values""")
        st.line_chart(tickerDf.Close)
        st.write("""Volume of Stock""")
        st.line_chart(tickerDf.Volume)

st.write("""
## Additional Information.
The Code for this application can be found on github @ https://github.com/SirVectrex/heroku_test_deployment.
Repository is public. Code is currently in an experimental state.

Author: Florian Schulenberg
""")
