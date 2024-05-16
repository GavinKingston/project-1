# Stock Exploration Tool

**Contributors:** 
* Gavin Kingston
* David Moyes 
* Rob Pavlik 
* Jaime Portillo 

### Summary
This tool will take in a user input with a comma delimited list of ticker symbols of stock market or crypto tickers and it will gather as much data on that symbol as possible of all closing prices based on a user provided frequency. It will then provide predictions on what the next best trade will be in the same frequency

### Questions
* What is the best time to buy, and what is the best time to sell
* what is the overall trend of the stock ticker symbol
* What month, day, time is the best time to buy or sell the stock. 

### Requirements
* Install Python [here](https://www.python.org/downloads/)
* Install Python Libraries (instructions listed below)
* Javascript enabled web browser

### Instructions
* Download the code
* Navigate into the parent directory of the source code using terminal
* Run the following command in terminal to install the required python libraries and run the program
```
pip install -r requirements.txt && streamlit run main.py
```

** Note: If you run into an error saying that the streamlit.cli is an unknown command. A workaround is to run the following to reinstall the streamlit module**
```
pip uninstall streamlit
pip install streamlit
```

