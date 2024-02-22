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
symbol3 = st.sidebar.text_input("Enter January Portfolio Stocks (comma-separated):", "APO,CRBG,TRV,MELI,SAP,NVS,ORLY")
symbol4 = st.sidebar.text_input("Enter February Portfolio Stocks (comma-separated):", "AMAT,CAT,MAR,KB,LLY,NFLX,JBL,DECK")

# Split the comma-separated symbols into a list
symbol3_list = [symbol.strip() for symbol in symbol3.split(',')]
symbol4_list = [symbol.strip() for symbol in symbol4.split(',')]

today_date = datetime.now().date()

# Set default values for start and end dates
#start_date = st.sidebar.date_input("Select Start Date:", value=pd.to_datetime('2024-15-01'))
start_date = pd.to_datetime('2024-01-15')
end_date = st.sidebar.date_input("Select End Date:", value=today_date)

# Fetch data for all three symbols
stock_data1 = fetch_stock_data(symbol1, start_date, end_date)
stock_data2 = fetch_stock_data(symbol2, start_date, end_date)
stock_data3_list = [fetch_stock_data(symbol, start_date, end_date) for symbol in symbol3_list]
start_date = pd.to_datetime('2024-02-15')
stock_data4_list = [fetch_stock_data(symbol, start_date, end_date) for symbol in symbol4_list]

avg_stock3 = pd.concat([stock_data['Close'] for stock_data in stock_data3_list], axis=1).mean(axis=1)
avg_stock4 = pd.concat([stock_data['Close'] for stock_data in stock_data4_list], axis=1).mean(axis=1)

common_index3 = stock_data3_list[0].index
common_index4 = stock_data4_list[0].index
avg_stock3_df = pd.DataFrame({'Close': avg_stock3})
avg_stock4_df = pd.DataFrame({'Close': avg_stock4})

# Layout in two columns

col1, col2 = st.columns(2)

# Left column with stock closing prices comparison
with col1:
    st.write("## Stock Data Comparison")

    # Line plot for all three stocks
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=stock_data1.index, y=stock_data1['Close'], mode='lines', name=symbol1, line=dict(color='blue', width=4)))
    fig.add_trace(go.Scatter(x=stock_data2.index, y=stock_data2['Close'], mode='lines', name=symbol2, line=dict(color='darkblue', width=4)))

    for i, stock_data in enumerate(stock_data3_list):
        symbol = symbol3_list[i]
        # Use RGBA format for color with transparency
        color = f'rgba(0, 128, 0, {0.5 + i * 0.1})'  # Adjust the transparency based on 'i'        
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name=symbol, line=dict(color=color,dash='dash')))


    for i, stock_data in enumerate(stock_data4_list):
        symbol = symbol4_list[i]
        # Use RGBA format for color with transparency
        color = f'rgba(255, 0, 0, {0.5 + i * 0.1})'  # Adjust the transparency based on 'i'        
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], mode='lines', name=symbol, line=dict(color=color,dash='dash')))

    fig.add_trace(go.Scatter(x=common_index3, y=avg_stock3, mode='lines', name='Avg January Stocks', line=dict(color='green', width=4)))
    fig.add_trace(go.Scatter(x=common_index4, y=avg_stock4, mode='lines', name='Avg February Stocks', line=dict(color='red', width=4)))

    fig.update_layout(title='Stock Closing Prices Comparison',
                      xaxis_title='Date',
                      yaxis_title='Closing Price')

    st.plotly_chart(fig)

# Right column with cumulative return on investment
with col2:
    st.write("## Cumulative Return on Investment")
    
    # Calculate and plot the cumulative return
    fig_roi = go.Figure()

    roi1 = (stock_data1['Close'] / stock_data1['Close'].iloc[0] - 1) * 100
    roi2 = (stock_data2['Close'] / stock_data2['Close'].iloc[0] - 1) * 100
    roi3 = (avg_stock3_df['Close'] / avg_stock3_df['Close'].iloc[0] - 1) * 100
    roi4 = (avg_stock4_df['Close'] / avg_stock4_df['Close'].iloc[0] - 1) * 100
    

    fig_roi.add_trace(go.Scatter(x=roi1.index, y=roi1, mode='lines', name=f"{symbol1} ROI",line=dict(color='blue', width=4)))
    fig_roi.add_trace(go.Scatter(x=roi2.index, y=roi2, mode='lines', name=f"{symbol2} ROI",line=dict(color='darkblue', width=4)))
    fig_roi.add_trace(go.Scatter(x=roi3.index, y=roi3, mode='lines', name="Jan ROI",line=dict(color='green', width=4)))
    fig_roi.add_trace(go.Scatter(x=roi4.index, y=roi4, mode='lines', name="Feb ROI",line=dict(color='red', width=4)))

    fig_roi.update_layout(title='Cumulative Return on Investment',
                          xaxis_title='Date',
                          yaxis_title='ROI (%)')

    st.plotly_chart(fig_roi)