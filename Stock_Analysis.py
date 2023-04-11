import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import plotly.express as px
import matplotlib.pyplot as plt
from yahooquery import Ticker

with st.sidebar:
    st.title("Stock Analysis")
    ticker_list = []

    num_of_symbols = st.number_input("Number of Symbols", 1, 5)
    for i in range(num_of_symbols):
        symbol = st.text_input("Enter Stock Symbol e.g.`TSLA, MSFT`", value='TSLA',
                               key=f"symbol{i}").upper()
        ticker_list.append(symbol)
    period = st.selectbox(
        "Stock History Period", ['5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max'])
    interval = st.selectbox(
        "Interval of records.", ['1d', '5d', '1wk', '1mo', '3mo'])

if st.sidebar.button("Analyze Stock Data"):
    for i in (ticker_list):
        # Create a list of tabs
        tab_names = [ticker_list[i] for i in range(num_of_symbols)]

    # Create the tabs
    tag_tabs = st.tabs(tab_names)
    for i in range(num_of_symbols):
        tab_content = tag_tabs[i]
        tab_content.subheader(f"Stock Price Movement `{ticker_list[i]}`: ")
        yf_ticker = yf.Ticker(ticker_list[i])
        yf_ticker_data = yf_ticker.history(
            period=period,
            interval=interval)
        yf_ticker_data = yf_ticker_data.sort_values(by='Date', ascending=True)

        # -------------------------------------------------------------------------
        # Plotting historic data
        fig = px.line(yf_ticker_data, x=None, y='Close')
        fig.update_yaxes(rangemode="tozero")
        tab_content.plotly_chart(fig)

        # Share Information
        ticker = Ticker(ticker_list[i])
        # data = pd.DataFrame.from_dict(ticker.asset_profile).transpose()
        # tab_content.subheader("Overview")
        # tab_content.dataframe(
        #    data[['country', 'fullTimeEmployees', 'industry', 'sector']].transpose())

        # -------------------------------------------------------------------------
        # Balance Sheet
        tab_content.subheader("Balance Sheet (Past 4 Years)")
        balance_sheet_df = ticker.balance_sheet()
        tab_content.dataframe(balance_sheet_df)
        fig = px.bar(balance_sheet_df, x='asOfDate',
                     y=['AccountsPayable', 'AccountsReceivable', 'CurrentAssets', 'CurrentDebt'], text_auto=True, height=500)
        tab_content.plotly_chart(fig)
        # -------------------------------------------------------------------------

        # Income Statement

        tab_content.header("Income Statement")
        income_statement_df = ticker.income_statement().dropna(axis=1).drop_duplicates(
            subset='asOfDate', keep='first')
        tab_content.subheader(
            "Total Revenue, Total Expense & Gross Profit (USD)")
        fig = px.line(income_statement_df, x='asOfDate',
                      y=['TotalRevenue', 'TotalExpenses', 'GrossProfit'])
        fig.update_yaxes(rangemode='tozero')
        tab_content.plotly_chart(fig)

        # -------------------------------------------------------------------------
        # News
        tab_content.subheader("Latest News")
        for index, news in enumerate(yf_ticker.news):
            tab_content.write(f"{index+1}.  {news['title']}")
            tab_content.write(news['link'])
