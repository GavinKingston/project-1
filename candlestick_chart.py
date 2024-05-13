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

# Bollinger Bands
# Calculate the 14-period Simple Moving Average (SMA)
ticker_history['SMA'] = ticker_history['Close'].rolling(window=14).mean()

# Calculate the 14-period Standard Deviation (SD)
ticker_history['SD'] = ticker_history['Close'].rolling(window=14).std()

# Calculate the Upper Bollinger Band (UB) and Lower Bollinger Band (LB)
ticker_history['UB'] = ticker_history['SMA'] + 2 * ticker_history['SD']
ticker_history['LB'] = ticker_history['SMA'] - 2 * ticker_history['SD']

# Create a Plotly figure
fig1 = go.Figure()

# Add the price chart
fig1.add_trace(go.Scatter(x=ticker_history.index,
               y=ticker_history['Close'], mode='lines', name='Price'))

# Add the Upper Bollinger Band (UB) and shade the area
fig1.add_trace(go.Scatter(x=ticker_history.index,
               y=ticker_history['UB'], mode='lines', name='Upper Bollinger Band', line=dict(color='red')))
fig1.add_trace(go.Scatter(x=ticker_history.index,
               y=ticker_history['LB'], fill='tonexty', mode='lines', name='Lower Bollinger Band', line=dict(color='green')))

# Add the Middle Bollinger Band (MA)
fig1.add_trace(go.Scatter(x=ticker_history.index,
               y=ticker_history['SMA'], mode='lines', name='Middle Bollinger Band', line=dict(color='blue')))

# Customize the chart layout
fig1.update_layout(title='Stock Price with Bollinger Bands',
                   xaxis_title='Date',
                   yaxis_title='Price',
                   showlegend=True)

# Show the chart
# fig.show()
st.plotly_chart(fig1, theme="streamlit")
