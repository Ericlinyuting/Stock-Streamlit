# STREAMLIT套件
import streamlit as st
# 可以互動的PLOT套件
import plotly.graph_objects as go
# 設置日期格式的套件
import datetime
from datetime import datetime as dt
from datetime import timedelta
#import tejapi
# 登入TEJ API
#tejapi.ApiConfig.api_key = "your_key"
#把時間取消保留日期 (無視)
#tejapi.ApiConfig.ignoretz = True

with st.sidebar:
    st.title('TEJAPI股票學習')
    col1, col2 = st.columns(2)
    with col1:
        # 將股票起使日期設置為變數d1
        d1 = st.date_input(
        "股票起始日期",
        # 並將預設資料設定為2022年的1/1
        datetime.date(2022, 1, 1))
    with col2:
        # 將股票起使日期設置為變數d2
        d2= st.date_input(
        "股票結束日期",
        datetime.date(2023, 2, 3))
    #輸入股價
    # 使用date套件的date獲取今天日期資料
    current_date = dt.now().date()
    # 使用date套件的timedelta獲取昨天的日期資料
    previous_date = current_date - timedelta(days=1)
    '''
    data = tejapi.get('TWN/APIPRCD',
    mdate=previous_date,
    opts={'columns':['coid']},
    paginate=True)
    
    coids = data['coid'].tolist()
    stock_code = st.selectbox('選擇股票代碼', data)
    st.write('你選擇股票是: ', stock_code)
    stock_id = {stock_code}
    gte, lte = {d1}, {d2}
    tejdata= tejapi.get('TWN/APIPRCD',
    paginate = True,
    coid = stock_id,
    mdate = {'gte':gte, 'lte':lte},
    chinese_column_name=True
    )
    df = tejdata
    df.reset_index(drop=True, inplace=True)
    
    # 預設選取 checkbox，並將結果儲存到變數 is_checked 中
    EMA1_checked = st.checkbox("發散指標(EMA1)(短線)", value=True,key="EMA1")
    # Add a slider to the sidebar:
    slider1 = st.sidebar.slider(
    '設置EMA1參數',
    1, 31, 7
    )
    EMA2_checked = st.checkbox("發散指標(EMA2)(長線)", value=True,key='EMA2')
    # Add a slider to the sidebar:
    slider2 = st.sidebar.slider(
    '設置EMA2參數',
    1, 31, 21
    )
    '''


#右側欄位
st.title('🌐STREAMLIT股票資料EMA應用')
st.write("")
fig = go.Figure()
# 根據 slider 的值來計算 EMA，並加入到圖表中
#df['EMA1'] = df['收盤價'].ewm(span=slider1, adjust=False).mean()
#df['EMA2'] = df['收盤價'].ewm(span=slider2, adjust=False).mean()


# 如果 checkbox 被選取，則畫出 EMA1 的線
'''
if EMA1_checked:
    fig.add_trace(go.Scatter(x=df['資料日'], y=df['EMA1'],
                             mode='lines',
                             name=f'EMA{slider1}'))

if EMA2_checked:
    fig.add_trace(go.Scatter(x=df['資料日'], y=df['EMA2'],
                             mode='lines',
                             name=f'EMA{slider2}'))   

fig.add_trace(go.Scatter(x=df['資料日'], y=df['收盤價'],
                    mode='lines',
                    name='收盤價'))


fig.update_layout(
    title=f"{stock_code} 股票價格走勢圖",
    xaxis_title="股票時間",
    yaxis_title="股票價格",
    legend_title="指標",
    autosize=True
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("🌐點此查看股票資料"):
        
        st.dataframe(df, height=500)
        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode("utf-8")
        csv = convert_df(df)

        st.download_button(
            label="點此下載資料範例",
            data=csv,
            file_name="股價資料.csv",
            mime="text/csv",
        )
'''