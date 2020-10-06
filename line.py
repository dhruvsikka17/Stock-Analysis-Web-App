import streamlit as st
import pandas as pd
import datetime
import yfinance as yf
from datetime import date

def user_input_features():
    today = date.today()
    x = today.strftime("%Y-%m-%d")
    ticker = st.sidebar.text_input("Ticker", 'AAPL')
    start_date = st.sidebar.text_input("Start Date", '2020-01-01')
    end_date = st.sidebar.text_input("End Date",x)
    return ticker, start_date, end_date

def main():
    st.write("""
    # Stocks Analysis Web Application
    Shown below are the **Moving Average Crossovers**, **Bollinger Bands** and **Cumulative Daily Returns** of any stock!
    """)
    st.sidebar.header('User Inputs')

    symbol, start, end = user_input_features()

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    data = yf.download(symbol,start,end)
    data =data.dropna()
    #Adjusted Close Price
    st.header("Adjusted Close Price")
    st.area_chart(data['Adj Close'])

    #Simple Moving Average
    data['Simple Moving Average'] = data['Adj Close'].rolling(30).mean()
    st.header("Simple Moving Average")
    st.line_chart(data[['Adj Close','Simple Moving Average']])

    # Bollinger Bands
    data['Upper Band']=(data['Adj Close'].rolling(30).mean() + data['Adj Close'].rolling(30).std()*2)
    data['Lower Band'] =(data['Adj Close'].rolling(30).mean() - data['Adj Close'].rolling(30).std()*2)
    st.header("Bollinger Bands")
    st.line_chart(data[['Adj Close','Upper Band','Simple Moving Average','Lower Band']])

    #Cumulative Daily Returns
    data['Returns']=data['Adj Close'].pct_change(1)
    data['Cumulative Return'] = ( 1 + data['Returns'] ).cumprod()
    st.header("Cumulative Daily Returns")
    st.area_chart(data['Cumulative Return'])

if __name__ == "__main__":
    main()
