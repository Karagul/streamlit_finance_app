import yfinance as yf
import streamlit as st
import json
import datetime

st.write("""
# Stock Price Application
### - Currently in test phase. See Description at bottom.
Closing price per day is shown. 1 Dataset per day.
""")

#user_input = st.text_input("Stock", "GOOGL")
#startDate = st.date_input("Beginn of Timeframe")
#endDate = st.date_input("End of Timeframe")

#sidebar with input parameters
st.sidebar.header('User Input Parameters')

def user_input_features():
    stringinput = st.sidebar.text_input("Stock", "GOOGL")
    startDate = st.sidebar.date_input("Beginn of Timeframe", datetime.date(2010,5,31))
    endDate2 = st.sidebar.date_input("End of Timeframe", datetime.date(2020,8,2))

    return stringinput

user_input = user_input_features()

#define the ticker symbol
stockname = user_input
#get data on this ticker
tickerData = yf.Ticker(stockname)
#st.write(yf.Ticker(stockname))
#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start= startDate, end='2020-5-31')
#st.write(tickerDf.empty )
# Open	High	Low	Close	Volume	Dividends	Stock Splits

if tickerDf.empty == True :
    st.write("""No Data found for entry. Please enter another stock-identifyer""")
else:
    st.write("Stock Name **", str(tickerData.info["longName"]), "**")
    st.write("Current Ask Price **",  str(tickerData.info["ask"]), "**")
    st.write("""Curreny:""", str(tickerData.info["currency"]))
    st.write("""Closure Values""")
    st.line_chart(tickerDf.Close)
    st.write("""Volume of Stock""")
    st.line_chart(tickerDf.Volume)

st.write("""
##Documentation.
The Code for this application can be found on github @ https://github.com/SirVectrex/heroku_test_deployment.
Repository is public.
""")
