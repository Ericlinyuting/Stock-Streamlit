import streamlit as st

# 主要的Streamlit應用程序
def main():
    # 應用程式標題
    st.title("TEST123")
    
    # 年度的 Slide bar
    selected_year = st.sidebar.slider("選擇年度", 2019, 2023, value=2022)
    
    # 計算 start_date 和 end_date
    start_date = f"{selected_year}-01-01"
    end_date = f"{selected_year}-12-31"

    # 左側的sidebar
    with st.sidebar:
        st.title('Title2')

        # add the key choices_len to the session_state
        if not "choices_len" in st.session_state:
            st.session_state["choices_len"] = 0

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
                if st.button("增加"):
                    st.session_state["choices_len"] += 1
                
        for x in range(st.session_state["choices_len"]): # create many choices
            with c1:
                col_stock_code, col_shares,col_remove  = st.columns((10,5,1))
                with col_stock_code:
                    # 輸入股票代號
                    stock_code = st.text_input("input1", key=f"Stock_Code_{x}")
                with col_shares:
                    # 輸入股票股數
                    shares = st.number_input("input2",key=f"Shares_{x}", min_value=0, value=0)
                with col_remove:
                    if st.button("X",key=f"X_{x}") and st.session_state["choices_len"] >= 1:
                        st.session_state["choices_len"] -= 1
                        st.session_state.pop(f'Stock_Code_{x}')
                        st.session_state.pop(f'Shares_{x}')

    # 右側的主要內容
    st.subheader(f"{selected_year} Subheader1")
    st.write(st.session_state["choices_len"])
# 啟動應用程式
if __name__ == "__main__":
    main()
