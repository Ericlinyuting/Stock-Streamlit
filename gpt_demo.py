#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 15:50:16 2023

@author: linyuting
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# 創建一個空的DataFrame來存儲股票信息
stocks_df = pd.DataFrame(columns=["股票代號", "張數"])

# 主要的Streamlit應用程序
def main():
    # 添加應用程式標題
    st.title("股票現金股利計算器")

    # 左側的sidebar
    st.sidebar.header("添加股票信息")
    stock_code = st.sidebar.text_input("股票代號")
    shares = st.sidebar.number_input("張數", min_value=0, value=0)

    # 添加按鈕，當按下時執行添加股票信息的代碼
    if st.sidebar.button("添加"):
        add_stock_info(stock_code, shares)

    # 右側的主要內容
    st.subheader("股票信息及現金股利計算")
    st.dataframe(stocks_df)

    # 計算並顯示現金股利金額及月份
    dividends_df = calculate_dividends(stocks_df)
    st.subheader("現金股利金額及月份")
    st.dataframe(dividends_df)

    # 以長條圖顯示現金股利金額
    st.subheader("現金股利金額長條圖")
    plot_dividends_bar_chart(dividends_df)

    # 以圓餅圖呈現總額與佔比
    st.subheader("總額與佔比圓餅圖")
    plot_pie_chart(dividends_df)

# 添加股票信息到DataFrame
def add_stock_info(stock_code, shares):
    global stocks_df
    new_row = {"股票代號": stock_code, "張數": shares}
    stocks_df = stocks_df.append(new_row, ignore_index=True)

# 計算並返回現金股利金額及月份
def calculate_dividends(stocks_df):
    # 在這裡添加你的股利計算邏輯
    # 這裡只是一個示例，請根據實際需求修改
    dividends_data = {
        "股票代號": stocks_df["股票代號"],
        "現金股利金額": stocks_df["張數"] * 10,  # 假設每張股票的現金股利為10元
        "月份": pd.to_datetime("2023-01-01"),  # 假設所有股票的股利都在2023年1月支付
    }
    dividends_df = pd.DataFrame(dividends_data)
    return dividends_df

# 以長條圖顯示現金股利金額
def plot_dividends_bar_chart(dividends_df):
    fig = px.bar(dividends_df, x="股票代號", y="現金股利金額", color="月份", title="現金股利金額長條圖")
    st.plotly_chart(fig)

# 以圓餅圖呈現總額與佔比
def plot_pie_chart(dividends_df):
    total_dividends = dividends_df["現金股利金額"].sum()
    labels = dividends_df["股票代號"]
    values = dividends_df["現金股利金額"]

    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct=lambda p: '{:.1f}% ({:.0f}元)'.format(p, p * total_dividends / 100))
    ax.set_title("總額與佔比")
    st.pyplot(fig)

# 啟動應用程式
if __name__ == "__main__":
    main()
