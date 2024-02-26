#Step 00: git clone https://github.com/elnurgolden/production_forecast.git (not always necessary)
#Step 0: set up enviroment (not always necessary)
#python -m venv ./venv2 
#Step 1: set the enviroment
#.\venv2\Scripts\activate
#Step 2: install requirements (not always necessary)
#pip install -r requirements.txt
#Step 3: Run script:
# streamlit run  .\app.py    

#git checkout -b test
# git status
# git add ./app.py
# git commit -m "testing"   
# git push origin head 

#to remove all the recent local changes use instead of stash: git reset --hard HEAD
import streamlit as st
from datetime import datetime
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import numpy as np
st.set_page_config(layout="wide")



def add_portfolio_QQQ(ticker, stock_prices, start_date, end_date):

    stock_prices_QQQ = fetch_stock_data(ticker, start_date, end_date)
    stock_prices_QQQ.rename(columns={'Close': 'Close_QQQ'}, inplace=True)
    stock_prices_QQQ = stock_prices_QQQ.reset_index()

    stock_prices = pd.merge(stock_prices, stock_prices_QQQ, how='left', on='Date')


    
    stock_prices['NumberStocks_QQQ'] = stock_prices['contribution']/stock_prices['Close_QQQ']
    stock_prices['CumulativeStocks_QQQ'] = stock_prices['NumberStocks_QQQ'].cumsum()
    stock_prices['Portfolio_QQQ'] = stock_prices['CumulativeStocks_QQQ']*stock_prices['Close_QQQ'] 
    return stock_prices



def add_portfolio(ticker, stock_prices, start_date, end_date, contribution_Month):
    new_Close = 'Close_'+ticker
    new_NumberStocks = 'NumberStocks_'+ticker
    new_CumulativeStocks = 'CumulativeStocks_'+ticker
    new_Portfolio = 'Portfolio_'+ticker

    stock_prices_QQQ = fetch_stock_data(ticker, start_date, end_date)
    stock_prices_QQQ.rename(columns={'Close': new_Close}, inplace=True)
    stock_prices_QQQ = stock_prices_QQQ.reset_index()

    stock_prices = pd.merge(stock_prices, stock_prices_QQQ, how='left', on='Date')


    
    stock_prices[new_NumberStocks] = stock_prices[contribution_Month]/stock_prices[new_Close]
    stock_prices[new_CumulativeStocks] = stock_prices[new_NumberStocks].cumsum()
    stock_prices[new_Portfolio] = stock_prices[new_CumulativeStocks]*stock_prices[new_Close] 
    return stock_prices



def fetch_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data[['Close']]

def invest_portfolio(portfolio, amount, date):
    portfolio[date] += amount
    return portfolio

st.title('SPY Stock Investment Portfolio')
symbol1 = st.sidebar.text_input("Enter Stock Symbol 1:", "SPY")
symbol2 = st.sidebar.text_input("Enter Stock Symbol 2:", "QQQ")
symbol3 = st.sidebar.text_input("Enter January Stocks:", "APO,CRBG,TRV,MELI,SAP,NVS,ORLY")
symbol4 = st.sidebar.text_input("Enter February Stocks:", "AMAT,CAT,MAR,KB,LLY,NFLX,JBL,DECK")
symbol5 = st.sidebar.text_input("Enter March Stocks:", "APO,CRBG,TRV,MELI,SAP,NVS,ORLY")
symbol6 = st.sidebar.text_input("Enter April Stocks:", "AMAT,CAT,MAR,KB,LLY,NFLX,JBL,DECK")
symbol7 = st.sidebar.text_input("Enter May Stocks:", "APO,CRBG,TRV,MELI,SAP,NVS,ORLY")
symbol8 = st.sidebar.text_input("Enter June Stocks:", "AMAT,CAT,MAR,KB,LLY,NFLX,JBL,DECK")
symbol9 = st.sidebar.text_input("Enter July Stocks:", "APO,CRBG,TRV,MELI,SAP,NVS,ORLY")
symbol10 = st.sidebar.text_input("Enter August Stocks:", "AMAT,CAT,MAR,KB,LLY,NFLX,JBL,DECK")
symbol11 = st.sidebar.text_input("Enter September Stocks:", "APO,CRBG,TRV,MELI,SAP,NVS,ORLY")
symbol12 = st.sidebar.text_input("Enter October Stocks:", "AMAT,CAT,MAR,KB,LLY,NFLX,JBL,DECK")
symbol13 = st.sidebar.text_input("Enter November Stocks:", "APO,CRBG,TRV,MELI,SAP,NVS,ORLY")
symbol14 = st.sidebar.text_input("Enter December Stocks:", "AMAT,CAT,MAR,KB,LLY,NFLX,JBL,DECK")

# Split the comma-separated symbols into a list
symbol3_list = [symbol.strip() for symbol in symbol3.split(',')]
symbol4_list = [symbol.strip() for symbol in symbol4.split(',')]

# Parameters
ticker = symbol1
start_date = '2024-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')  # Use today's date
investment_amount = 1000
#investment_days_str = ['2024-01-16','2024-02-15']
#investment_days = pd.to_datetime(investment_days_str)
# Fetch SPY stock data
stock_prices = fetch_stock_data(ticker, start_date, end_date)
stock_prices.rename(columns={'Close': 'Close_SPY'}, inplace=True)
stock_prices = stock_prices.reset_index()

stock_prices['contribution'] = 0
stock_prices.iloc[9, stock_prices.columns.get_loc('contribution')] = investment_amount
stock_prices.iloc[31, stock_prices.columns.get_loc('contribution')] = investment_amount

stock_prices['NumberStocks_SPY'] = stock_prices['contribution']/stock_prices['Close_SPY']
stock_prices['CumulativeStocks_SPY'] = stock_prices['NumberStocks_SPY'].cumsum()
stock_prices['Portfolio_SPY'] = stock_prices['CumulativeStocks_SPY']*stock_prices['Close_SPY'] 


ticker = symbol2
stock_prices = add_portfolio_QQQ(ticker, stock_prices,  start_date, end_date)

contribution_Month = 'contribution_Jan'
stock_prices[contribution_Month] = 0
stock_prices.iloc[9, stock_prices.columns.get_loc('contribution_Jan')] = investment_amount/len(symbol3_list)

for ticker in symbol3_list:
    stock_prices = add_portfolio(ticker, stock_prices, start_date, end_date, contribution_Month)

stock_prices['Portfolio_Jan'] = 0
for ticker in symbol3_list:
    CumulativeStocks_Jan = 'Portfolio_' + ticker
    stock_prices['Portfolio_Jan'] = stock_prices['Portfolio_Jan'] + stock_prices[CumulativeStocks_Jan]

stock_prices = stock_prices[['Date','Portfolio_SPY', 'Portfolio_QQQ','Portfolio_Jan']]

contribution_Month = 'contribution_Feb'
stock_prices[contribution_Month] = 0
stock_prices.iloc[31, stock_prices.columns.get_loc('contribution_Feb')] = investment_amount/len(symbol4_list)

for ticker in symbol4_list:
    stock_prices = add_portfolio(ticker, stock_prices, start_date, end_date, contribution_Month)

stock_prices['Portfolio_Feb'] = 0
for ticker in symbol4_list:
    CumulativeStocks_Feb = 'Portfolio_' + ticker
    stock_prices['Portfolio_Feb'] = stock_prices['Portfolio_Feb'] + stock_prices[CumulativeStocks_Feb]

stock_prices = stock_prices[['Date','Portfolio_SPY', 'Portfolio_QQQ','Portfolio_Jan', 'Portfolio_Feb']]

stock_prices['Portfolio_BlackSea'] = stock_prices['Portfolio_Jan'] + stock_prices['Portfolio_Feb']
#    st.write(stock_prices)
# Calculate portfolio value
st.write(stock_prices)

# Create a DataFrame for plotting

    # Plot the portfolio as a time series
fig = go.Figure()

# Add SPY portfolio line
fig.add_trace(go.Scatter(x=stock_prices['Date'], y=stock_prices['Portfolio_SPY'],
                        mode='lines', name='SPY Portfolio', line=dict(color='blue')))

# Add QQQ portfolio line
fig.add_trace(go.Scatter(x=stock_prices['Date'], y=stock_prices['Portfolio_QQQ'],
                        mode='lines', name='QQQ Portfolio', line=dict(color='red')))

fig.add_trace(go.Scatter(x=stock_prices['Date'], y=stock_prices['Portfolio_BlackSea'],
                        mode='lines', name='Black Sea Portfolio', line=dict(color='green')))

# Set layout options
fig.update_layout(title='Black Sea Portfolio vs SPY and QQQ', xaxis_title='Date', yaxis_title='Portfolio Value',
                  width=1000)  # Adjust the width as needed

st.plotly_chart(fig)

