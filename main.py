import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from prophet import Prophet
import streamlit as st
import json

def calculate_percent_return(ticker):
    # Calculate the percentage return for user specified frequency
    first_close = ticker["ticker_history"]["Close"].iloc[-1]
    last_close = ticker["ticker_history"]["Close"].iloc[0]
    total_return = round(((last_close - first_close) / first_close) * 100, 2)
    percent_return = f"{total_return:.2f}%"
    return percent_return

def get_research_tool_tab_data(tickerData):
    for ticker in tickerData:

        # Make header for stock analyst recommendations and call corresponding function
        st.header(f"Stock analyst recommendations for {ticker['ticker_name']}")

        # Use dictionary to rename dataframe with new column names
        new_column_names = {
            "strongBuy": "Strong Buy",
            "buy": "Buy",
            "hold": "Hold",
            "sell": "Sell",
            "strongSell": "Strong Sell"
        }
        recommend_new = ticker["recommendations"].rename(columns=new_column_names)
        recommend_new_t = recommend_new.transpose()
        recommend_new_t = recommend_new_t.drop("period", axis=0)
        recommend_new_total = recommend_new_t.sum(axis=1)
        recommend_new_total = recommend_new_total.reset_index()
        recommend_new_total = recommend_new_total.rename(columns=
                                                            {"index": "labels",
                                                            0 : "values"})

        # Assign the pie chart labels, values, and colors
        colors = ["darkgreen", "green", "gold", "red", "darkred"]
        pie = go.Pie(labels=recommend_new_total["labels"], values=recommend_new_total["values"], marker=dict(colors=colors))

        # Create the figure and add the trace
        fig = go.Figure(pie)

        # Display the pie chart in Streamlit
        st.plotly_chart(fig)

        # Make header for income statement and call corresponding function
        st.header(f"Income statement: {ticker['ticker_name']}")
        
        # Transpose data frame and create visualization
        st.line_chart(ticker['income_stmt'].transpose()[["Total Revenue", "Net Income", "Gross Profit", "EBITDA"]])
        
        # Make header for balance sheet and call corresponding function
        st.header(f"Balance sheet: {ticker['ticker_name']}")
        
        # Transpose data frame and create visualization
        st.line_chart(ticker['balance_sheet'].transpose()[["Total Assets", "Total Liabilities Net Minority Interest", "Stockholders Equity", "Long Term Debt"]])
        
        # Make header for cash flow statement and call corresponding function
        st.header(f"Cash flow statement: {ticker['ticker_name']}")
        
        # Transpose data frame and create visualization
        st.line_chart(ticker['cashflow'].transpose()[["Free Cash Flow", "Operating Cash Flow", "Issuance Of Debt", "Net Income From Continuing Operations"]])
        
        # Make header for stock ticker news and call corresponding function
        st.header(f"Recent news articles mentioning {ticker['ticker_name']}")
        
        # Loop through each news article and display the title and link
        for item in ticker['news']:
            st.link_button(item['title'], item['link'])



# Set page title and subheader
st.title('Stock Market Analysis Tool')
st.subheader('This tool will allow you to analyze stock market data for any ticker symbol you input.')


# User input for ticker symbols
ticker_input = st.text_input("Enter ticker symbols to analyze (separated by commas):")
ticker_frequency = st.selectbox("Select the data frequency:",
    ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'], index=4)

# Analyze ticker symbols when user inputs data and clicks the button
if st.button('Analyze Tickers'):
    if ticker_input:

        # Split Ticker Symbols by comma and Loop through each one to grab the data from Yahoo Finance
        tickerList = ticker_input.split(',')

        # Remove blank values from tickerList
        tickerList = [ticker for ticker in tickerList if ticker.strip()]

        # Create an empty list to store the ticker data
        tickerData = []

        # Loop through each ticker symbol and retrieve the data
        for ticker_symbol in tickerList:
            
            # Strip Whitespace Off Ticker Symbol
            ticker_symbol = ticker_symbol.strip()

            # Query Yahoo Finance API for ticker data
            try:
                ticker = yf.Ticker(ticker_symbol)
                ticker_info = ticker.info
                ticker_name = ticker_info["longName"]
                ticker_history = ticker.history(period=ticker_frequency)
                ticker_history.sort_index(inplace=True, ascending=False)

                # Append the data to the tickerData list
                tickerData.append({"ticker_symbol": ticker_symbol, 
                                   "recommendations": ticker.recommendations, 
                                   "ticker_info": ticker_info, 
                                   "ticker_name": ticker_name, 
                                   "ticker_history": ticker_history,
                                   "income_stmt": ticker.income_stmt,
                                   "balance_sheet": ticker.balance_sheet,
                                   "cashflow": ticker.cashflow,
                                   "news": ticker.news})
            
            # Handle exceptions from the Yahoo Finance API
            except Exception as e:
                st.error(f"Could not retrieve data for ticker symbol: {ticker_symbol}.")

        # Create tabs
        tab_titles = ["Stock History", "Stock Prediction", "Research Tool", "Market Trends" ]
        tabs = st.tabs(tab_titles)

        # Stock History Tab
        with tabs[0]:
            for ticker in tickerData:
                # Show forst 5 rows of data & displays ticker symbol
                st.header(f"Ticker symbol: {ticker['ticker_symbol']}")
                st.subheader(f"Last 5 days of price data for {ticker['ticker_name']}")
                st.table(ticker['ticker_history'].head())

                st.subheader(f"Closing Price for {ticker['ticker_name']} over the past {ticker_frequency}")
                # Plot the close data on a line chart
                line_chart_data = ticker['ticker_history']['Close'].copy().reset_index()
                line_chart_data.columns = ['Date', 'Close Price']
                st.line_chart(line_chart_data, x="Date", y="Close Price")
                # Calculate the percentage return for each ticker and display it
                percent_return = calculate_percent_return(ticker)
                st.write(f"<h5>{ticker['ticker_name']} saw a {percent_return} return on investment over the past {ticker_frequency}.</h5>", unsafe_allow_html=True)

        with tabs[1]:
            for ticker in tickerData:
                # Formatting data to work with Prophet Forcasting Model
                prophet_df = ticker["ticker_history"][['Close']]
                prophet_df.reset_index(inplace=True)
                prophet_df.dropna(inplace=True)
                prophet_df.columns = ['ds', 'y']

                # Convert ds column to datetime
                prophet_df['ds'] = pd.to_datetime(prophet_df['ds'])

                # Remove timezone from prophet_df ds column
                prophet_df['ds'] = prophet_df['ds'].dt.tz_localize(None)

                # Building Prophet Model and fitting the data
                prophet = Prophet()
                prophet.fit(prophet_df)

                # Building Forecast DataFrame
                #config_period = st.slider("Forecast Period", 1, 90, 30)
                config_period = 90
                config_freq = "D"
                forecast_df = prophet.make_future_dataframe(periods=config_period, 
                                                            freq=config_freq, 
                                                            include_history=True)
                prophet_forecast = prophet.predict(forecast_df)

                # Display the forecast data
                fig1 = prophet.plot(prophet_forecast, xlabel='Date', ylabel='Close Price')
                fig1.suptitle(f"{ticker['ticker_name']} Forecast", fontsize=20)
                fig1.tight_layout()
                st.write(fig1)
                
                # Use the plot_components function to visualize the forecast components
                fig = prophet.plot_components(prophet_forecast)
                fig.tight_layout()
                fig.subplots_adjust(top=0.9)
                fig.suptitle(f"{ticker['ticker_name']} Forecast Components", fontsize=20)
                fig.get_children()[1].set_xlabel('Date')
                st.write(fig)
                                 
        # Add content to the Research tab
        with tabs[2]:
            # Create explanation for the Research page
            st.header("Detailed Ticker Analysis")
            st.write("In addition to predictions of a stock's closing price, there a lot of factors that need to be considered before investing in any stock. This page allows you to review stock analyst recommendations, numerous financial statements, and relevant news articles.")

            # Call function to get data for the Research Tool tab
            get_research_tool_tab_data(tickerData)

        # Benchmark Data Tab
        with tabs[3]:

            # Create explaination for the Market Trends page
            st.header("General Market Trends")
            st.write("Buying individual stocks comes with a higher level of risk compared to investing in an index fund, as the performance of the individual company can be more volatile and subject to market fluctuations, company-specific risks, and unforeseen events. While individual stocks offer the potential for higher returns, they also come with the possibility of significant losses, making thorough research an important part of mitigating risk in your investment portfolio.")

            # Create a list of the user specified tickers including the Dow Jones Industrial Average, Nasdaq Composite, and S&P 500 
            benchmark_ticker = ["^DJI", "^IXIC", "^GSPC"]
            benchmark_ticker_data = []
            # Loop through each benchmark ticker and retrieve the data
            for benchmark_symbol in benchmark_ticker:
                try:
                    # Query Yahoo Finance API for benchmark data of Dow Jones Industrial Average, Nasdaq Composite, and S&P 500
                    benchmark = yf.Ticker(benchmark_symbol)
                    benchmark_name = benchmark.info["longName"]
                    benchmark_history = benchmark.history(period=ticker_frequency)
                    benchmark_history.sort_index(inplace=True, ascending=False)
                    benchmark_ticker_data.append({"ticker_symbol": benchmark_symbol, "ticker_info": benchmark.info, "ticker_name": benchmark_name, "ticker_history": benchmark_history})
                    
                except Exception as e:
                    st.error(f"Could not retrieve data for ticker symbol: {benchmark_symbol}. Error: {e}")
            # Loop through tickerData and display the total return percentage for each ticker including the Dow Jones Industrial Average, Nasdaq Composite, and S&P 500
            for ticker in benchmark_ticker_data:

                # Display the close prices for each ticker
                st.header(f"Close prices for {ticker['ticker_name']}")
                #st.area_chart(ticker["ticker_history"]["Close"])
                ticker["ticker_history"].dropna(inplace=True)
                fig = go.Figure(data=[go.Candlestick(x=ticker["ticker_history"].index,
                                     open=ticker["ticker_history"]['Open'],
                                     high=ticker["ticker_history"]['High'],
                                     low=ticker["ticker_history"]['Low'],
                                     close=ticker["ticker_history"]['Close'])])
                st.plotly_chart(fig, theme="streamlit")

                # Calculate the percentage return for each ticker and display it
                percent_return = calculate_percent_return(ticker)
                st.write(f"<h5>{ticker['ticker_name']} saw a {percent_return} return on investment over the past {ticker_frequency}.</h5>", unsafe_allow_html=True)
    
    # Calculate the MACD indicator
    # macd = ta.macd(benchmark_history["Close"])
    # macd
    # # Create a Plotly figure
    # fig = go.Figure()

    # # Add the MACD lines
    # fig.add_trace(go.Scatter(x=benchmark_history.index, y=macd["MACD_12_26_9"], name="MACD"))
    # fig.add_trace(go.Scatter(x=benchmark_history.index, y=macd["MACD_Signal_9"], name="Signal"))

    # # Add the MACD histogram
    # fig.add_trace(go.Bar(x=benchmark_history.index, y=macd["MACDhist"], name="Histogram"))

    # # Update the layout
    # fig.update_layout(xaxis_rangeslider_visible=False)

    # # Display the chart
    # st.plotly_chart(fig)


