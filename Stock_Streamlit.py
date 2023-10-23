#兩個免費資料庫 
#Finlab https://ai.finlab.tw/stock/?stock_id=1101

#FinMind https://finmindtrade.com/analysis/#/data/api
# import requests
# url = "https://api.web.finmindtrade.com/v2/user_info"
# payload = {
#     "token":'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyMy0xMC0yMiAxMjo0ODowNiIsInVzZXJfaWQiOiJsaW55dXRpbmcwNTExIiwiaXAiOiIxMTEuMTI1LjEzMi4xNzMifQ.gMdpVVw1brneniLZu79UShcipwLemDhlNGVnBd_8Ruc',
# }
# resp = requests.get(url, params=payload)
# resp.json()["user_count"]  # 使用次數
# resp.json()["api_request_limit"]  # api 使用上限

from FinMind.data import DataLoader
#use token login package
api = DataLoader()
api.login_by_token(api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyMy0xMC0yMiAxMjo0ODowNiIsInVzZXJfaWQiOiJsaW55dXRpbmcwNTExIiwiaXAiOiIxMTEuMTI1LjEzMi4xNzMifQ.gMdpVVw1brneniLZu79UShcipwLemDhlNGVnBd_8Ruc')

df = api.taiwan_stock_dividend(
    stock_id="2330",
    start_date='2019-03-31',
    end_date="2010-12-31"
)

import streamlit as st
import pandas as pd
from FinMind.data import DataLoader

# 創建一個空的DataFrame來存儲股票資訊
stocks_df = pd.DataFrame(columns=["股票代號", "張數", "除息日期", "現金股利"])

# 初始化 FinMind DataLoader
api = DataLoader()

# 主要的Streamlit應用程序
def main():
    # 應用程式標題
    st.title("存股計算機")
    
    # 年度的 Slide bar
    selected_year = st.sidebar.slider("選擇年度", 2019, 2023, value=2022)
    
    # 計算 start_date 和 end_date
    start_date = f"{selected_year}-01-01"
    end_date = f"{selected_year}-12-31"

    # 左側的sidebar
    with st.sidebar:
        st.title('增加股票代號')
        col1, col2 = st.columns(2)
        with col1:
            # 輸入股票代號
            stock_code = st.text_input("股票代號")
        with col2:
            # 輸入股票股數
            shares = st.number_input("張數", min_value=0, value=0)

    # # 新增按鈕，當按下時執行新增股票資訊的代碼
    # if st.sidebar.button("新增"):
    add_stock_info(stock_code, shares,start_date,end_date)

    # 右側的主要內容
    st.subheader(f"{selected_year} 年度現金股利統計")
    st.dataframe(stocks_df)

# 增加股票資訊到DataFrame
def add_stock_info(stock_code, shares, start_date, end_date):
    # 使用 FinMind API 查詢股票現金股利
    dividend_data = query_dividend_data(stock_code, start_date, end_date)
    global stocks_df
    # 將查詢結果增加到 DataFrame 中
    if not dividend_data.empty:
        for _, row in dividend_data.iterrows():
            new_row = {
                "股票代號": stock_code,
                "張數": shares,
                "除息日期": row["date"],
                "現金股利": row["CashEarningsDistribution"],
            }
            stocks_df = pd.concat([stocks_df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        st.warning(f"找不到股票代號 {stock_code} 的相關資料")


# 使用 FinMind API 查詢股票現金股利
def query_dividend_data(stock_code, start_date, end_date):
    try:
        df = api.taiwan_stock_dividend(stock_id=stock_code, start_date=start_date, end_date=end_date)
        if not df.empty:
            # 返回 API 查詢的整個 DataFrame
            # df=df["stock_id","date","CashEarningsDistribution"]
            return df
        else:
            st.warning(f"找不到股票代號 {stock_code} 的相關資料")
            return pd.DataFrame(columns=["股票代號", "張數", "除息日期", "現金股利"])
    except Exception as e:
        # st.error(f"查詢股票代號 {stock_code} 時發生錯誤：{e}")
        return pd.DataFrame(columns=["股票代號", "張數", "除息日期", "現金股利"])

# 啟動應用程式
if __name__ == "__main__":
    main()
