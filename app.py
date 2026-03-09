import streamlit as st
import yfinance as yf
import json
import os

st.title("🦾 AI投資 - 永久版")

# 數據文件
DATA_FILE = "portfolio.json"

# 讀取持倉
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    cash = data.get('cash', 10000)
    nee_shares = data.get('nee_shares', 0)
else:
    cash = 10000
    nee_shares = 0

# 獲取NEE價格
@st.cache_data(ttl=60)
def get_nee_price():
    try:
        price = yf.download('NEE', period='1d', progress=False)['Close'][-1]
        return round(price, 2)
    except:
        return 80.0

price = get_nee_price()
total_value = cash + nee_shares * price

# 顯示
col1, col2, col3 = st.columns(3)
col1.metric("總資產", f"${total_value:,.0f}")
col2.metric("現金", f"${cash:,.0f}")
col3.metric("NEE價格", f"${price}")

# 買入按鈕
if st.button("🤖 AI買NEE", type="primary") and cash >= price:
    cash -= price
    nee_shares += 1
    
    # 保存
    portfolio = {'cash': cash, 'nee_shares': nee_shares}
    with open(DATA_FILE, 'w') as f:
        json.dump(portfolio, f)
    
    st.success(f"買入! 剩餘現金: ${cash:,.0f}")
    st.rerun()
elif st.button("🤖 AI買NEE"):
    st.error("現金不足!")

# 歷史按鈕
if st.button("📊 交易歷史"):
    st.info("歷史記錄保存在 portfolio.json")

st.caption("💡 每60秒自動更新價格，刷新不丟數據")
