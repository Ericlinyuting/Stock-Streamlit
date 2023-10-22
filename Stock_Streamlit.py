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

# df = api.taiwan_stock_dividend(
#     stock_id="2330",
#     start_date='2019-03-31',
# )

import streamlit as st
import pandas as pd

# 創建一個空的DataFrame來存儲股票信息
stocks_df = pd.DataFrame(columns=["股票代號", "張數"])

# 主要的Streamlit應用程序
def main():
    # 應用程式標題
    st.title("台股現金股利計算器")
    
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

    # 添加按鈕，當按下時執行添加股票信息的代碼
    if st.sidebar.button("新增"):
        add_stock_info(stock_code, shares)

    # 右側的主要內容
    st.subheader("股票信息及現金股利計算")
    st.dataframe(stocks_df)

# 添加股票信息到DataFrame
def add_stock_info(stock_code, shares):
    global stocks_df
    new_row = {"股票代號": stock_code, "張數": shares}
    stocks_df = stocks_df.append(new_row, ignore_index=True)

# 啟動應用程式
if __name__ == "__main__":
    main()
