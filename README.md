# 台股股利試算 Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://stock-app-7bpnvlx8hdshgnkqzpgxsh.streamlit.app)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)

<img width="1280" alt="image" src="https://github.com/Ericlinyuting/Stock-Streamlit/assets/86369645/3c132718-85fa-4378-a194-2034833d4e96">
<img width="1277" alt="image" src="https://github.com/Ericlinyuting/Stock-Streamlit/assets/86369645/b6bda8a7-2435-4d01-bb55-51013dcba81c">

---

## 專案簡介

運用 [Streamlit](https://streamlit.io) 串接免費的 [FinMind API](https://finmindtrade.com/)，打造台股現金股利試算 Dashboard。
輸入持有的股票代號與持股數，即可快速計算指定年度或自訂持有期間內的股利收入，並以互動式圖表呈現現金流分布。

> ⚠️ FinMind 免費方案有 API 請求次數上限，請留意使用頻率。

---

## 功能特色

- **依年度計算**：選擇年份，一覽整年度的股利總額與逐月現金流
- **自訂持有期間**：為每檔股票設定個別的持有起訖日，精確計算實際入帳股利
- **動態持股管理**：在側邊欄自由新增／刪除股票（股票代號 + 持股張數）
- **互動式長條圖**：顯示每月股利現金流入，支援 hover 詳細資訊
- **互動式圓餅圖**：呈現各股票股利佔比，一目了然
- **資料來源**：FinMind 免費 API（台股基本面資料）

---

## 技術棧

| 套件 | 用途 |
|------|------|
| [Streamlit](https://streamlit.io) | 前端 UI 框架 |
| [Plotly](https://plotly.com) | 互動式資料視覺化 |
| [Pandas](https://pandas.pydata.org) | 資料處理 |
| [FinMind](https://finmindtrade.com) | 台股財務資料 API |
| [python-dotenv](https://github.com/theskumar/python-dotenv) | 環境變數管理 |

---

## 本地執行

```bash
# 1. 複製專案
git clone https://github.com/Ericlinyuting/Stock-Streamlit.git
cd Stock-Streamlit

# 2. 安裝相依套件
pip install -r requirements.txt

# 3. 建立 .env 並填入 FinMind API Key
echo "FINMIND_API_KEY=your_token_here" > .env

# 4. 啟動應用
streamlit run 依年度計算.py
```

### Conda 環境（選用）

```bash
conda env create -f environment_try.yml
conda activate streamlit
streamlit run 依年度計算.py
```

---

## 線上 Demo(免費線上資源可能會失效QAQ)

[https://stock-app-7bpnvlx8hdshgnkqzpgxsh.streamlit.app](https://stock-app-7bpnvlx8hdshgnkqzpgxsh.streamlit.app)
