from FinMind.data import DataLoader
import streamlit as st
import pandas as pd

#use token login package
# 初始化 FinMind DataLoader
FinMindapi = DataLoader()
FinMindapi.login_by_token(api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyMy0xMC0yNCAxMTozOToxNCIsInVzZXJfaWQiOiJsaW55dXRpbmcwNTExIiwiaXAiOiI2MC4yNTAuMTIzLjc3In0.9NsDPKa0Chwffr9k-QHXs09AhTDLln1ZFd1RPfwc3Ug')

#FinMind API 查詢股票現金股利
def query_dividend_data(stock_code, selected_year,start_date, end_date):
    try:
        df = FinMindapi.taiwan_stock_dividend(stock_id=stock_code, start_date=start_date, end_date=end_date)
        if not df.empty:
            # 返回 API 查詢的整個 DataFrame
            df=df[["stock_id","date","CashEarningsDistribution"]]
            df=df.rename(columns={"stock_id":"股票代號","date":"除息日期","CashEarningsDistribution":"現金股利"})
            return df
        else:
            st.warning(f"{selected_year}年度找不到股票代號 {stock_code} 的相關資料")
            return df
    except Exception as e:
        # st.error(f"查詢股票代號 {stock_code} 時發生錯誤：{e}")
        return pd.DataFrame(columns=["股票代號","除息日期","現金股利","股數","總額"])