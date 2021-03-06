import streamlit as st
import pandas as pd
import datetime
import yfinance as yf
from datetime import date
import plotly.express as px
import ta

def user_input_features():
    today = date.today()
    x = datetime.date.today()
    ticker = st.sidebar.text_input("Ticker", 'AAPL')
    start_date = st.sidebar.text_input("Start Date","2019-01-01")
    end_date = st.sidebar.text_input("End Date",x)
    return ticker, start_date, end_date

def main():
    st.write("""
    # Stocks Analysis Web Application
    Shown below are the **Moving Average Crossovers**, **Bollinger Bands**, **RSI**, **OBV** and **Cumulative Daily Returns** of any stock!
    """)
    st.sidebar.header('User Inputs')

    symbol, start, end = user_input_features()

    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    data = yf.download(symbol,start,end)
    data =data.dropna()

#Indicator Options
    indicators = st.sidebar.selectbox("Indicators", options=('None','Simple Moving Average','Bollinger Bands',"RSI","OBV"))
    #Adjusted Close Price
    st.header("Adjusted Close Price")
    fig=px.area(data,x= data.index, y = 'Adj Close',template = "plotly_dark",width=900,height=500,labels={"Adj Close":"Adjusted Close"})
    st.plotly_chart(fig)

    #Simple Moving Average
    if indicators == 'Simple Moving Average':
        period = st.sidebar.slider('Time Period', 0, 150, 30)
        data['Simple Moving Average'] = data['Adj Close'].rolling(period).mean()
        st.header("Simple Moving Average")
        fig=px.line(data,x= data.index, y = ['Adj Close','Simple Moving Average'],width=900,height=500,template = "plotly_dark",labels={"variable":"","value":"Value","Adj Close":"Adjusted Close"})
        st.plotly_chart(fig)


    # Bollinger Bands
    if indicators == 'Bollinger Bands':
        period = st.sidebar.slider('Time Period', 0, 150, 30)
        data['Upper Band']=(data['Adj Close'].rolling(period).mean() + data['Adj Close'].rolling(period).std()*2)
        data['Lower Band']=(data['Adj Close'].rolling(period).mean() - data['Adj Close'].rolling(period).std()*2)
        data['Simple Moving Average'] = data['Adj Close'].rolling(period).mean()
        st.header("Bollinger Bands")
        fig=px.line(data,x= data.index, y = ['Adj Close','Upper Band','Simple Moving Average','Lower Band'],width=900,height=500,template = "plotly_dark",labels={"variable":"","Adj Close":"Adjusted Close","value":"Value"})
        st.plotly_chart(fig)
    #RSI
    if indicators == 'RSI':
        period = st.sidebar.slider('Time Period', 0, 150, 14)
        data['RSI']= ta.momentum.rsi(data['Adj Close'],n=period)
        st.header("Relative Strength Index")
        fig=px.line(data,x= data.index, y = 'RSI',width=900,height=500,template = "plotly_dark")
        st.plotly_chart(fig)

    #OBV
    if indicators =='OBV':
        data['OBV'] = ta.volume.on_balance_volume(data['Adj Close'],data['Volume'])
        st.header("On Balance Volume")
        fig=px.line(data,x= data.index, y = 'OBV',width=900,height=500,template = "plotly_dark")
        st.plotly_chart(fig)

#Other Graphs Options
    other_graphs = st.sidebar.selectbox("Other graphs", options=('None','Cumulative Returns'))

    #Cumulative Daily Returns
    if other_graphs == 'Cumulative Returns':
        data['Returns']=data['Adj Close'].pct_change(1)
        data['Cumulative Return'] = ( 1 + data['Returns'] ).cumprod()
        st.header("Cumulative Daily Returns")
        fig=px.area(data,x= data.index, y = 'Cumulative Return',width=900,height=500,template = "plotly_dark")
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
