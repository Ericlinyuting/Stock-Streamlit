import streamlit as st
from FinMind.data import DataLoader
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime

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
def query_dividend_data(stock_code,start_date, end_date):
    try:
        df = FinMindapi.taiwan_stock_dividend(stock_id=stock_code, start_date=start_date, end_date=end_date)
        if not df.empty:
            # 返回 API 查詢的整個 DataFrame
            df=df[["stock_id","date","CashEarningsDistribution"]]
            df=df.rename(columns={"stock_id":"股票代號","date":"除息日期","CashEarningsDistribution":"現金股利"})
            return df
        else:
            st.warning(f"不到股票代號 {stock_code} 的相關資料")
            return df
    except Exception as e:
        # st.error(f"查詢股票代號 {stock_code} 時發生錯誤：{e}")
        return pd.DataFrame(columns=["股票代號","除息日期","現金股利","股數","總額"])
def plot_dividends_bar_chart(dividends_df):
    # 將日期轉換為月份
    dividends_df['除息日期'] = pd.to_datetime(dividends_df['除息日期'])
    dividends_df['月份'] = dividends_df['除息日期'].dt.month
    # 創建包含所有月份的 DataFrame
    all_months_df = pd.DataFrame({'月份': range(1, 13)})
    # 合併兩個 DataFrame，使用左連接確保所有月份都包含在內
    grouped_df = all_months_df.merge(dividends_df, on='月份', how='left')
    # 以月份和股利金額進行分組加總
    grouped_df = grouped_df.groupby(['月份'])['總額'].sum().reset_index()
    # 創建 Figure
    fig = go.Figure()
    # 加入長條圖
    fig.add_trace(go.Bar(
        x=grouped_df['月份'],
        y=grouped_df["總額"].fillna(0),
        name='',#去掉名稱
        hovertemplate='%{x}月: %{y}元',
        marker_color='skyblue'
    ))
    # 設定標題和圖例
    fig.update_layout(xaxis_title='月份',yaxis_title='總額 (元)',title_text="每月股利現金流統計表", title_x=0.45, xaxis=dict(tickmode='linear'))
    # 顯示圖表
    st.plotly_chart(fig, use_container_width=True)


# 主要的Streamlit應用程序
def main():
    st.set_page_config(page_title='存股計算機', 
                    layout='wide')
    # 應用程式標題
    st.title("存股計算機")

    #region 左側的sidebar
    with st.sidebar:
        st.title('投資組合')
        if "fields_size" not in st.session_state:
            st.session_state.fields_size = 0
            st.session_state.fields = []
            st.session_state.deletes = []
        # c_up contains the stock input
        # c_down contains the add and remove buttons
        c_up = st.container()
        c_down = st.container()
        with c_up:
            c1 = st.container() # c1 contains input choices
            c2 = st.container() # c2 contains submit button
        with c_down:
            col_l,_,col_r = st.columns((6,10,6))
            with col_l:
                st.button("➕增加一筆", on_click=add_field)
            with col_r:
                if st.session_state.fields_size>0:
                    st.button("❌刪除一筆", on_click=delete_field)
                
        for i in range(st.session_state.fields_size):
            with c1:
                col_stock_code, col_shares, col_date= st.columns((8,6,4))
                with col_stock_code:
                    # 輸入股票代號
                    st.session_state.fields.append(st.text_input(f"股票代號_ {i+1}", key=f"Stock_Code_{i+1}"))
                with col_shares:
                    # 輸入股票股數
                    st.session_state.fields.append(st.number_input(f"股數_ {i+1}", key=f"Shares_{i+1}", min_value=0, value=0))
                with col_date:
                    today = datetime.datetime.now()
                    last_year = today - datetime.timedelta(days=1*365)
                    st.session_state.fields.append(st.date_input(f"持有時間_ {i+1}", key=f"Duration_{i+1}", value=(last_year,today)))
    #endregion
    #region 右側的主要內容
    # 創建一個空的DataFrame來存儲股票資訊
    stocks_df = pd.DataFrame(columns=["股票代號","除息日期","現金股利","股數","總額"])
    # st.subheader(f"{selected_year} 年度現金股利統計")
    for i in range(st.session_state.fields_size):
        stock_code_key = f"Stock_Code_{i+1}"
        shares_key = f"Shares_{i+1}"
        duration_key = f"Duration_{i+1}"
        APIdata=query_dividend_data(st.session_state[stock_code_key],start_date=st.session_state[duration_key][0],end_date=st.session_state[duration_key][1])
        if not APIdata.empty:
            APIdata["股數"]=st.session_state[shares_key]
            APIdata["總額"]=np.round(APIdata["股數"]*APIdata["現金股利"])
            stocks_df = pd.concat([stocks_df, APIdata], ignore_index=True)
        else :
            continue
    st.dataframe(stocks_df, hide_index=True, use_container_width=True)
    # 以長條圖顯示現金股利金額
    st.subheader("現金股利金額長條圖")
    plot_dividends_bar_chart(stocks_df)
    #endregion
# 啟動應用程式
if __name__ == "__main__":
    main()