import yfinance as yf
import pandas as pd
from prophet import Prophet
import streamlit as st
import plotly.graph_objects as go
import pandas_ta as ta

# Set page title and subheader
st.title('Stock Market Analysis Tool')
st.subheader('This tool will allow you to analyze stock market data for any ticker symbol you input.')

# Create tabs
tab_titles = ["Stock Prediction", "Research Tool", "Market Trends"]
tabs = st.tabs(tab_titles)

# Add content to the User Input Tool tab
with tabs[0]:
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

                    # # Formatting data to work with Prophet Forcasting Model
                    # prophet_df = ticker_history[['Close']]
                    # prophet_df.reset_index()
                    # prophet_df.columns = ['ds', 'y']
                    
                    # # Building Prophet Model and fitting the data
                    # prophet = Prophet()
                    # prophet.fit(prophet_df)

                    # # Building Forecast DataFrame
                    # config_period = 10
                    # config_freq = "D"
                    # forecast_df = prophet.make_future_dataframe(periods=config_period, 
                    #                                             freq=config_freq, 
                    #                                             include_history=True)
                    
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

# Add content to the Research tab
with tabs[1]:
    # Create explaination for the Research page
    st.header("Detailed Ticker Analysis")
    st.write("In addition to predictions of a stock's closing price, there a lot of factors that need to be considered before investing in any stock. This page allows you to review stock analyst recommendations, numerous financial statements, and relevant news articles.")
    
    # User input for ticker symbols
    research_ticker = st.text_input("Enter ticker symbols to analyze (separated by commas):", key="research")
    
    # Analyze ticker symbols when user inputs data and clicks the button
    if st.button("Research Tickers"):
        if research_ticker:

            # Split Ticker Symbols by comma and Loop through each one to grab the data from Yahoo Finance
            ticker_list = research_ticker.split(',')
            for research_symbol in ticker_list:

                # Strip Whitespace Off Ticker Symbol
                research_symbol = research_symbol.strip()
                try:
                    ticker_value = yf.Ticker(research_symbol)
                    ticker_name = ticker_value.info["longName"]

                    # Make header for stock analyst recommendations and call corresponding function
                    st.header(f"Stock analyst recommendations: {ticker_name}(past 3 months)")
                    recommend = ticker_value.recommendations
                    # Use dictionary to rename dataframe with new column names
                    new_column_names = {
                        "strongBuy": "Strong Buy",
                        "buy": "Buy",
                        "hold": "Hold",
                        "sell": "Sell",
                        "strongSell": "Strong Sell"
                    }
                    recommend_new = recommend.rename(columns=new_column_names)
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
                    st.header(f"Income statement: {ticker_name}")
                    income_stmt = ticker_value.income_stmt
                    # Transpose data frame and create visualization
                    income_stmt_t = income_stmt.transpose()
                    st.line_chart(income_stmt_t[["Total Revenue", "Net Income", "Gross Profit", "EBITDA"]])
                    
                    # Make header for balance sheet and call corresponding function
                    st.header(f"Balance sheet: {ticker_name}")
                    balance_sheet = ticker_value.balance_sheet
                    # Transpose data frame and create visualization
                    balance_sheet_t = balance_sheet.transpose()
                    st.line_chart(balance_sheet_t[["Total Assets", "Total Liabilities Net Minority Interest", "Stockholders Equity", "Long Term Debt"]])
                    
                    # Make header for cash flow statement and call corresponding function
                    st.header(f"Cash flow statement: {ticker_name}")
                    cashflow = ticker_value.cashflow
                    # Transpose data frame and create visualization
                    cashflow_t = cashflow.transpose()
                    st.line_chart(cashflow_t[["Free Cash Flow", "Operating Cash Flow", "Issuance Of Debt", "Net Income From Continuing Operations"]])
                    
                    # Make header for stock ticker news and call corresponding function
                    st.header(f"Recent news articles mentioning {ticker_name}")
                    article_list = ticker_value.news
                    links_and_titles = [(item["link"], item["title"]) for item in article_list]

                    # Display the extracted links and titles
                    for link, title in links_and_titles:
                        st.link_button(title, link)

                # Handle exceptions from the Yahoo Finance API
                except Exception as e:
                    st.error(f"Could not retrieve data for ticker symbol: {research_symbol}. Error: {e}")

# Add content to the Benchmark Data tab
with tabs[2]:
    # Create explaination for the Market Trends page
    st.header("General Market Trends")
    st.write("Buying individual stocks comes with a higher level of risk compared to investing in an index fund, as the performance of the individual company can be more volatile and subject to market fluctuations, company-specific risks, and unforeseen events. While individual stocks offer the potential for higher returns, they also come with the possibility of significant losses, making thorough research an important part of mitigating risk in your investment portfolio.")
    
    benchmark_frequency = st.selectbox("Select the data frequency:",
        ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'], key="benchmark_f")
    benchmark_ticker = ["^DJI", "^IXIC", "^GSPC"]
    if st.button("Review Benchmarks", key="benchmark_b"):
        if benchmark_ticker:
            for benchmark_symbol in benchmark_ticker:
                try:
                    #benchmark = yf.download("^DJI ^IXIC ^GSPC", period=benchmark_frequency)
                    benchmark = yf.Ticker(benchmark_symbol)
                    benchmark_name = benchmark.info["longName"]
                    benchmark_history = benchmark.history(period=benchmark_frequency)
                    st.header(f"Close prices for {benchmark_name}")
                    st.area_chart(benchmark_history["Close"])
                    first_close = benchmark_history["Close"].iloc[0]
                    last_close = benchmark_history["Close"].iloc[-1]
                    total_return = round(((last_close - first_close) / first_close) * 100, 2)
                    percent_return = f"{total_return:.2f}%"
                    st.write(f"<h5>{benchmark_name} saw a {percent_return} return on investment over the past {benchmark_frequency}.</h5>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Could not retrieve data for ticker symbol: {benchmark_symbol}. Error: {e}")
    
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


