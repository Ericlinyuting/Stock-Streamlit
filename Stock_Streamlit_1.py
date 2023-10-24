import streamlit as st
from FinMind.data import DataLoader
import pandas as pd
import numpy as np
#use token login package
# 初始化 FinMind DataLoader
FinMindapi = DataLoader()
FinMindapi.login_by_token(api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyMy0xMC0yNCAxMTozOToxNCIsInVzZXJfaWQiOiJsaW55dXRpbmcwNTExIiwiaXAiOiI2MC4yNTAuMTIzLjc3In0.9NsDPKa0Chwffr9k-QHXs09AhTDLln1ZFd1RPfwc3Ug')
#region components control
def add_field():
    st.session_state.fields_size += 1

def delete_field():
    st.session_state.fields_size -= 1
#endregion

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
        st.title('投資組合')
        if "fields_size" not in st.session_state:
            st.session_state.fields_size = 0
            st.session_state.fields = []
            st.session_state.deletes = []
        # c_up contains the form
        # c_down contains the add and remove buttons
        c_up = st.container()
        c_down = st.container()
        with c_up:
            c1 = st.container() # c1 contains input choices
            c2 = st.container() # c2 contains submit button
        with c_down:
            col_l,_,col_r = st.columns((6,13,6))
            with col_l:
                st.button("➕增加一筆", on_click=add_field)
            with col_r:
                if st.session_state.fields_size>0:
                    st.button("❌刪除一筆", on_click=delete_field)
                
        for i in range(st.session_state.fields_size):
            with c1:
                col_stock_code, col_shares= st.columns((8,6))
                with col_stock_code:
                    # 輸入股票代號
                    st.session_state.fields.append(st.text_input(f"股票代號_ {i+1}", key=f"Stock_Code_{i+1}"))
                with col_shares:
                    # 輸入股票股數
                    st.session_state.fields.append(st.number_input(f"股數_ {i+1}", key=f"Shares_{i+1}", min_value=0, value=0))

    # 右側的主要內容
    # 創建一個空的DataFrame來存儲股票資訊
    stocks_df = pd.DataFrame(columns=["股票代號","除息日期","現金股利","股數","總額"])
    st.subheader(f"{selected_year} 年度現金股利統計")
    for i in range(st.session_state.fields_size):
        stock_code_key = f"Stock_Code_{i+1}"
        shares_key = f"Shares_{i+1}"
        st.write(f"{stock_code_key}: {st.session_state[stock_code_key]}", f"{shares_key}: {st.session_state[shares_key]}")
        APIdata=query_dividend_data(st.session_state[stock_code_key],selected_year,start_date=start_date,end_date=end_date)
        if not APIdata.empty:
            APIdata["股數"]=st.session_state[shares_key]
            APIdata["總額"]=np.round(APIdata["股數"]*APIdata["現金股利"])
            stocks_df = pd.concat([stocks_df, APIdata], ignore_index=True)
        else :
            continue
    st.dataframe(stocks_df)
# 啟動應用程式
if __name__ == "__main__":
    main()
