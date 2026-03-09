import streamlit as st
import yfinance as yf
import pandas as pd
import json
import os
import time

st.title("🦾 自動更新價格+永久歷史AI投資")

# 永久數據文件
DATA_FILE = "trades.json"

# 讀取永久歷史
if os.path.exists(DATA_FILE):
    try:
        with open(DATA_FILE, "r") as f:
            trades_data = json.load(f)
    except:
        trades_data = []
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
@st.cache_data(ttl=30)
def get_price():
    try:
        ticker = yf.Ticker('NEE')
        price = ticker.history(period="1d")['Close'][-1]
        return round(price, 2)
    except:
        return 80.0

NEE_price = get_price()

# 總資產（真實價格）
總資產 = st.session_state.cash + st.session_state.nEE * NEE_price

col1, col2, col3 = st.columns(3)
col1.metric("💰 總資產", f"${總資產:,.0f}")
col2.metric("💵 現金", f"${st.session_state.cash:,.0f}")
col3.metric("📈 NEE", f"${NEE_price}")

# AI買入
if st.button("🤖 AI買NEE", type="primary"):
    if st.session_state.cash >= NEE_price:
        st.session_state.nEE += 1
        st.session_state.cash -= NEE_price
        
        trades_data.append({
            "時間": str(pd.Timestamp.now()),
            "動作": f"買NEE@{NEE_price}",
            "現金": float(st.session_state.cash),
            "NEE數量": int(st.session_state.nEE),
            "NEE價格": float(NEE_price),
            "總資產": float(總資產)
        })
        
        # 永久保存
        with open(DATA_FILE, "w") as f:
            json.dump(trades_data, f, indent=2)
        
        st.success(f"✅ 買入1股NEE，價${NEE_price}")
        st.rerun()
    else:
        st.error("💸 現金不足！")

# 刷新按鈕
if st.button("🔄 刷新價格"):
    st.cache_data.clear()
    st.rerun()

# 歷史
st.subheader("📈 永久交易歷史")
if trades_
    df = pd.DataFrame(trades_data[-20:])
    st.dataframe(df, use_container_width=True)
else:
    st.info("👆 按AI買入開始！")

st.caption("⏰ 價格每30秒自動更新")
