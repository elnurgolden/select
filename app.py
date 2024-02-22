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

st.set_page_config(layout="wide")


def fetch_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

# Streamlit UI
st.title("Stock Data Dashboard")


# Sidebar for user input
symbol1 = st.sidebar.text_input("Enter Stock Symbol 1:", "SPY")
symbol2 = st.sidebar.text_input("Enter Stock Symbol 2:", "QQQ")
symbol3 = st.sidebar.text_input("Enter Stock Symbol 3:", "GOOGL")

today_date = datetime.now().date()

# Set default values for start and end dates
start_date = st.sidebar.date_input("Select Start Date:", value=pd.to_datetime('2024-01-01'))
end_date = st.sidebar.date_input("Select End Date:", value=today_date)

# Fetch data for all three symbols
stock_data1 = fetch_stock_data(symbol1, start_date, end_date)
stock_data2 = fetch_stock_data(symbol2, start_date, end_date)
stock_data3 = fetch_stock_data(symbol3, start_date, end_date)

# Layout in two columns
col1, col2 = st.columns(2)

# Left column with stock closing prices comparison
with col1:
    st.write("## Stock Data Comparison (Line Plot)")

    # Line plot for all three stocks
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=stock_data1.index, y=stock_data1['Close'], mode='lines', name=symbol1))
    fig.add_trace(go.Scatter(x=stock_data2.index, y=stock_data2['Close'], mode='lines', name=symbol2))
    fig.add_trace(go.Scatter(x=stock_data3.index, y=stock_data3['Close'], mode='lines', name=symbol3))

    fig.update_layout(title='Stock Closing Prices Comparison',
                      xaxis_title='Date',
                      yaxis_title='Closing Price')

    st.plotly_chart(fig)

    # Display fetched data for each stock
    st.write(f"### {symbol1} Stock Data")
    st.write(stock_data1)

    st.write(f"### {symbol2} Stock Data")
    st.write(stock_data2)

    st.write(f"### {symbol3} Stock Data")
    st.write(stock_data3)

# Right column with cumulative return on investment
with col2:
    st.write("## Cumulative Return on Investment")

    # Calculate and plot the cumulative return
    fig_roi = go.Figure()

    roi1 = (stock_data1['Close'] / stock_data1['Close'].iloc[0] - 1) * 100
    roi2 = (stock_data2['Close'] / stock_data2['Close'].iloc[0] - 1) * 100
    roi3 = (stock_data3['Close'] / stock_data3['Close'].iloc[0] - 1) * 100

    fig_roi.add_trace(go.Scatter(x=roi1.index, y=roi1, mode='lines', name=f"{symbol1} ROI"))
    fig_roi.add_trace(go.Scatter(x=roi2.index, y=roi2, mode='lines', name=f"{symbol2} ROI"))
    fig_roi.add_trace(go.Scatter(x=roi3.index, y=roi3, mode='lines', name=f"{symbol3} ROI"))

    fig_roi.update_layout(title='Cumulative Return on Investment',
                          xaxis_title='Date',
                          yaxis_title='ROI (%)')

    st.plotly_chart(fig_roi)