import streamlit as st
from FinMind.data import DataLoader
import pandas as pd
#use token login package
# 初始化 FinMind DataLoader
FinMindapi = DataLoader()
FinMindapi.login_by_token(api_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRlIjoiMjAyMy0xMC0yMiAxMjo0ODowNiIsInVzZXJfaWQiOiJsaW55dXRpbmcwNTExIiwiaXAiOiIxMTEuMTI1LjEzMi4xNzMifQ.gMdpVVw1brneniLZu79UShcipwLemDhlNGVnBd_8Ruc')
# 創建一個空的DataFrame來存儲股票資訊
stocks_df = pd.DataFrame(columns=["股票代號", "張數", "除息日期", "現金股利"])

def add_field():
    st.session_state.fields_size += 1

def delete_field(index):
    st.session_state.fields_size -= 1
    del st.session_state.fields[index]
    del st.session_state.deletes[index]

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
            col_l,col_r = st.columns((15,4))
            with col_r:
                st.button("➕", on_click=add_field)
                
        for i in range(st.session_state.fields_size):
            with c1:
                col_stock_code, col_shares,col_remove,col_  = st.columns((8,5,1,1))
                with col_stock_code:
                    # 輸入股票代號
                    st.session_state.fields.append(st.text_input(f"股票代號_ {i+1}", key=f"Stock_Code_{i+1}"))
                with col_shares:
                    # 輸入股票股數
                    st.session_state.fields.append(st.number_input(f"股數_ {i+1}", key=f"Shares_{i+1}", min_value=0, value=0))
                with col_remove:
                    st.session_state.deletes.append(st.button("❌", key=f"delete{i+1}", on_click=delete_field, args=(i+1,)))

    # 右側的主要內容
    st.subheader(f"{selected_year} 年度現金股利統計")
    for i in range(st.session_state.fields_size):
        stock_code_key = f"Stock_Code_{i+1}"
        shares_key = f"Shares_{i+1}"
        st.write(f"{stock_code_key}: {st.session_state[stock_code_key]}", f"{shares_key}: {st.session_state[shares_key]}")
        
# 啟動應用程式
if __name__ == "__main__":
    main()
