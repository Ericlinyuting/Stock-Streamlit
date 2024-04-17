# Stock-Streamlit
運用Streamlit連接免費Find Mind API(有request 次數上限)製作dashboard

## APP 連結 https://stock-app-7bpnvlx8hdshgnkqzpgxsh.streamlit.app

### streamlit share 連結：https://share.streamlit.io
<img width="1280" alt="image" src="https://github.com/Ericlinyuting/Stock-Streamlit/assets/86369645/3c132718-85fa-4378-a194-2034833d4e96">
<img width="1277" alt="image" src="https://github.com/Ericlinyuting/Stock-Streamlit/assets/86369645/b6bda8a7-2435-4d01-bb55-51013dcba81c">


# dependency package
pip freeze > requirements.txt
pip install -r requirements.txt

# Conda Environment
conda env export > environment.yml
conda env create -f environment.yml
source activate streamlit

# run project
streamlit run 依年度計算.py