import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
import time

st.title("🦾 自動更新價格+永久歷史AI投資")

# 永久數據文件
DATA_FILE = "trades.json"
prices_cache = {}

# 讀取永久歷史
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        trades_data = json.load(f)
else:
    trades_data = []

# 初始化持倉（刷新都記得）
if trades_
    last = trades_data[-1]
    st.session_state.cash = last.get('現金', 10000)
    st.session_state.nEE = last.get('NEE數量', 0)
else:
    st.session_state.cash = 10000
    st.session_state.nEE = 0

# 自動更新真實價格（每30秒）
symbols = ['NEE']
@st.cache_data(ttl=30)  # 30秒緩存
def get_prices():
    prices = {}
    for sym in symbols:
        try:
            ticker = yf.Ticker(sym)
            price = ticker.history(period="1d")['Close'][-1]
            prices[sym] = round(price, 2)
        except:
            prices[sym] = 80.0  # 默認價
    return prices

prices = get_prices()

# 總資產（真實價格）
NEE_price = prices['NEE']
總資產 = st.session_state.cash + st.session_state.nEE * NEE_price

col1, col2, col3 = st.columns(3)
col1.metric("💰 總資產", f"${總資產:,.0f}", delta=None)
col2.metric("💵 現金", f"${st.session_state.cash:,.0f}")
col3.metric("📈 NEE價格", f"${NEE_price}", delta=None)

# AI買入（自動用最新價）
if st.button("🤖 AI買NEE", type="primary"):
    if st.session_state.cash >= NEE_price:
        st.session_state.nEE += 1
        st.session_state.cash -= NEE_price
        
        trades_data.append({
            "時間": str(pd.Timestamp.now()),
            "動作": f"買NEE@{NEE_price}",
            "現金": st.session_state.cash,
            "NEE數量": st.session_state.nEE,
            "NEE價格": NEE_price,
            "總資產": 總資產
        })
        
        # 永久保存
        with open(DATA_FILE, "w") as f:
            json.dump(trades_data, f)
        
        st.success(f"✅ 買入1股NEE，價${NEE_price}")
        st.rerun()

# 自動刷新按鈕
if st.button("🔄 強制刷新價格"):
    st.cache_data.clear()
    st.rerun()

st.subheader("📈 永久交易歷史")
if trades_
    df = pd.DataFrame(trades_data[-20:])
    st.dataframe(df, use_container_width=True)
else:
    st.info("👆 按AI買入開始記錄！")

# 狀態顯示
st.info(f"⏰ 下次自動更新：{time.time() + 30:.0f}秒")
