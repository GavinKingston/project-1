import yfinance as yf
import pandas as pd
from prophet import Prophet
import numpy as np
import streamlit as st

# Function to fit Prophet model
def fit_prophet_model(data):

    # Resetting Date index back to a column and renaming to meet Prophet format
    prophet_df = data.reset_index().rename(columns={'Date': 'ds', 'Close': 'y'})
    prophet_df['ds'] = pd.to_datetime(prophet_df['ds']).dt.tz_localize(None)

    # cleaning up the data to remove NAN
    clean_prophet_df = prophet_df.dropna()

    # Calling Prophet and fitting the data
    prophet = Prophet()
    prophet.fit(clean_prophet_df)

    return prophet

# Function to generate Prophet forecast
def generate_prophet_forecast(ticker_symbol, 
                              ticker_frequency, 
                              config_period, 
                              config_freq):
    try:
        # Fit Prophet model
        prophet = fit_prophet_model(ticker_history)

        # Building the Forecast DataFrame
        forecast_df = prophet.make_future_dataframe(periods=config_period,
                                                     freq=config_freq,
                                                     include_history=True)

        # Make the predictions
        prophet_predictions = prophet.predict(forecast_df)

        # Return both the model instance and predictions
        return prophet, prophet_predictions

    except Exception as e:
        return None, str(e)

# Set page title and subheader
st.title('Stock Market Analysis Tool')
st.subheader('This tool allows you to analyze stock market data for any ticker symbol you input.')

# User input for ticker symbols and frequency
ticker_input = st.text_input("Enter ticker symbols to analyze (separated by commas):")
ticker_frequency = st.selectbox("Select the data frequency:",
                                ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'], 
                                index=4)

# Analyze ticker symbols when user inputs data and clicks the button
if st.button('Analyze Ticker(s)'):
    if ticker_input:

        # Split Ticker Symbols by comma and loop through each one to 
        # grab the data from Yahoo Finance
        tickerList = ticker_input.split(',')
        for ticker_symbol in tickerList:

            # Strip whitespace off Ticker Symbol
            ticker_symbol = ticker_symbol.strip()

            try:
                # Fetch data from Yahoo Finance
                ticker = yf.Ticker(ticker_symbol)
                ticker_history = ticker.history(period=ticker_frequency)

                # Display Ticker Symbol and data
                st.write(f"### Ticker symbol: {ticker_symbol}")
                st.write(ticker_history.head())

                # Plot the close data on a line chart
                st.line_chart(ticker_history['Close'])

            except Exception as e:
                st.error(f"Could not retrieve data for ticker symbol: \
                         {ticker_symbol}. Error: {e}")

# This function is not working correctly

            # User input for period and frequency
            st.subheader(f"Prophet Forecast Configuration: {ticker_symbol}")
            default_period = 10  # Set a default value for the period
            config_period = st.slider('Select Period', 
                                      min_value=1, 
                                      max_value=30, 
                                      value=default_period, 
                                      key=f'{ticker_symbol}_period')
            config_freq = st.selectbox('Select Frequency', 
                                       options=['D', 'W', 'M'], 
                                       key=f"{ticker_symbol}_freq")

            # Generate Prophet forecast
            prophet_model, prophet_predictions = generate_prophet_forecast(ticker_symbol, 
                                                                           ticker_frequency, 
                                                                           config_period, 
                                                                           config_freq)

            if prophet_predictions is not None:
                
                # Plot the Prophet predictions
                st.subheader(f"## Prophet Forecast: {ticker_symbol}")
                fig = prophet_model.plot(prophet_predictions, 
                                         xlabel='Date', 
                                         ylabel='Close')

                # Show the plot
                st.pyplot(fig)
            
            else:
                st.error(f"Could not retrieve data for ticker symbol: \
                         {ticker_symbol}. Error: {prophet_model}")