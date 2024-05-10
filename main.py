import yfinance as yf
import pandas as pd
from prophet import Prophet
import streamlit as st

# Set page title and subheader
st.title('Stock Market Analysis Tool')
st.subheader('This tool will allow you to analyze stock market data for any ticker symbol you input.')

# User input for ticker symbols
ticker_input = st.text_input("Enter ticker symbols to analyze (separated by commas):")
ticker_frequency = st.selectbox("Select the data frequency:",
    ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'])

# Analyze ticker symbols when user inputs data and clicks the button
if st.button('Analyze Tickers'):
    if ticker_input:

        # Split Ticker Symbols by comma and Loop through each one to grab the data from Yahoo Finance
        tickerList = ticker_input.split(',')
        for ticker_symbol in tickerList:

            # Strip Whitespace Off Ticker Symbol
            ticker_symbol = ticker_symbol.strip()
            try:
                ticker = yf.Ticker(ticker_symbol)
                ticker_info = ticker.info
                ticker_history = ticker.history(period=ticker_frequency)

                # Formatting data to work with Prophet Forcasting Model
                prophet_df = ticker_history[['Close']]
                prophet_df.reset_index()
                prophet_df.columns = ['ds', 'y']
                
                # Building Prophet Model and fitting the data
                prophet = Prophet()
                prophet.fit(prophet_df)

                # Building Forecast DataFrame
                config_period = 10
                config_freq = "D"
                forecast_df = prophet.make_future_dataframe(periods=config_period, 
                                                            freq=config_freq, 
                                                            include_history=True)
                
                # Rob - Finish the Prophet Forecasting Model and display the forecast
                # Rob - Add forecast components to the streamlit app
                
                # Show forst 5 rows of data & displays ticker symbol
                st.write(f"Ticker symbol: {ticker_symbol}")
                st.table(ticker_history.head())

                # Plot the close data on a line chart
                st.line_chart(ticker_history['Close'])

                # Jamie - Add Candlestick Chart using plotly and streamlit
                # Jamie - Add Bollinger Bands using plotly and streamlit

                # David - Add MACD Indicator using plotly and streamlit
                # David - Add additional tabs into streamlit to show more information

                # Gavin - Add RSI Indicator using plotly and streamlit
                # Gavin - Add Correlation Matrix using plotly and streamlit

            # Handle exceptions from the Yahoo Finance API
            except Exception as e:
                st.error(f"Could not retrieve data for ticker symbol: {ticker_symbol}. Error: {e}")