import streamlit as st
from FinMind.data import DataLoader
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import Chart
import Query_FinMind_Data as FinMind
#region components control
def add_field():
    st.session_state.fields_size_1 += 1
def delete_field():
    st.session_state.fields_size_1 -= 1
#endregion

# 主要的Streamlit應用程序
def main():
    st.set_page_config(page_title='存股計算機', 
                    layout='wide')
    # 應用程式標題
    st.title("存股計算機")
    # 年度的 Slide bar
    selected_year = st.sidebar.slider("選擇年度", 2019, 2023, value=2022)
    #region 左側的sidebar
    with st.sidebar:
        st.title('投資組合')
        if "fields_size_1" not in st.session_state:
            st.session_state.fields_size_1 = 0
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
                if st.session_state.fields_size_1>0:
                    st.button("❌刪除一筆", on_click=delete_field)
                
        for i in range(st.session_state.fields_size_1):
            with c1:
                col_stock_code, col_shares, col_date= st.columns((3,2,4))
                with col_stock_code:
                    # 輸入股票代號
                    st.session_state.fields.append(st.text_input(f"股票代號_ {i+1}", key=f"Stock_Code_{i+1}"))
                with col_shares:
                    # 輸入股票股數
                    st.session_state.fields.append(st.number_input(f"股數_ {i+1}", key=f"Shares_{i+1}", min_value=0, value=0))
                with col_date:
                    # today = datetime.datetime.now()
                    # last_year = today - datetime.timedelta(days=1*365)
                    # 計算 start_date 和 end_date
                    start_date = datetime.date(selected_year, 1, 1)
                    end_date = datetime.date(selected_year, 12, 31)
                    st.session_state.fields.append(st.date_input(f"持有時間_ {i+1}", key=f"Duration_{i+1}", value=(start_date,end_date)))
    #endregion
    #region 右側的主要內容
    # 創建一個空的DataFrame來存儲股票資訊
    stocks_df = pd.DataFrame(columns=["股票代號","除息日期","現金股利","股數","總額"])
    st.subheader(f"{selected_year} 年度現金股利統計")
    for i in range(st.session_state.fields_size_1):
        stock_code_key = f"Stock_Code_{i+1}"
        shares_key = f"Shares_{i+1}"
        duration_key = f"Duration_{i+1}"
        if len(st.session_state[duration_key]) >1:
            APIdata=FinMind.query_dividend_data(st.session_state[stock_code_key],selected_year,start_date=st.session_state[duration_key][0],end_date=st.session_state[duration_key][1])
        else:
            APIdata=FinMind.query_dividend_data(st.session_state[stock_code_key],selected_year,start_date=st.session_state[duration_key][0],end_date=f"{selected_year}-12-31")
        if not APIdata.empty:
            APIdata["股數"]=st.session_state[shares_key]
            APIdata["總額"]=np.round(APIdata["股數"]*APIdata["現金股利"])
            stocks_df = pd.concat([stocks_df, APIdata], ignore_index=True)
        else :
            continue
    st.dataframe(stocks_df, hide_index=True, use_container_width=True)
    if st.session_state.fields_size_1!=0:
        # 以長條圖顯示現金股利金額
        st.subheader("現金股利金額長條圖")
        Chart.plot_dividends_bar_chart(stocks_df)
        # 圓餅圖顯示各股票的現金股利總額分布
        st.subheader("各股票現金股利佔比分布圖")
        st.write(f"{selected_year} 年度共拿到"+str(round(stocks_df["總額"].sum()))+"元")
        Chart.plot_dividends_pie_chart(stocks_df)
    #endregion
# 啟動應用程式
if __name__ == "__main__":
    main()