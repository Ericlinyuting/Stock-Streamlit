import pandas as pd
import plotly.graph_objects as go
import streamlit as st
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

def plot_dividends_pie_chart(dividends_df):
    fig_pie = go.Figure(data=[go.Pie(
        labels=dividends_df["股票代號"],
        values=dividends_df["總額"],
        hovertemplate="股票代號: %{label} <br>股利: %{value}元 <br>佔比: %{percent}%"
    )])
    st.plotly_chart(fig_pie, use_container_width=True)
