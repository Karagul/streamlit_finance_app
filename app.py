import datetime
import streamlit as st
import yfinance as yf


# --- Definition of Functions ---

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

st.write("""
# Stock Price Application
### - Currently in test phase. See Description at bottom. -
Closing price per day is shown. 1 Dataset per day.
""")
# sidebar with input parameters
st.sidebar.header('User Input Parameters')

favoredstocks = read_saved_stocks()
user_input = user_input_features()

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
