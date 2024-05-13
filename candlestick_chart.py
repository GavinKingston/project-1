import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
from datetime import datetime
import streamlit as st

ticker_data = yf.Ticker('META')
ticker_history = ticker_data.history(
    period='1d', start='2024-01-01', end='2024-05-10')

fig = go.Figure(data=[go.Candlestick(x=ticker_history.index,
                                     open=ticker_history['Open'],
                                     high=ticker_history['High'],
                                     low=ticker_history['Low'],
                                     close=ticker_history['Close'])])

st.plotly_chart(fig, theme="streamlit")
