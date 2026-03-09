import streamlit as st
import pandas as pd
import json
import os
import numpy as np

st.set_page_config(layout="wide")
st.title("🦾 多股票永久AI投資 $10k")

# 永久儲存
DATA_FILE = "trades.json"
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        trades = json.load(f)
else:
    trades = []

# 初始化
if 'cash' not in st.session_state:
    st.session_state.cash = 10000
    st.session_state.holdings = {'NEE': 0, 'GEV': 0, 'VST': 0}

col1, col2, col3 = st.columns(3)
total_value = st.session_state.cash
for symbol, shares in st.session_state.holdings.items():
    price = 80 if symbol=='NEE' else 450 if symbol=='GEV' else 120
    total_value += shares * price

with col1:
    st.metric("💰 總資產", f"${total_value:,.0f}")
with col2:
    st.metric("💵 現金", f"${st.session_state.cash:,.0f}")
with col3:
    st.metric("📊 總股數", sum(st.session_state.holdings.values()))

# AI智能買入（隨機選3隻）
if st.button("🤖 AI智能買入", type="primary"):
    symbols = ['NEE', 'GEV', 'VST']
    symbol = np.random.choice(symbols)  # AI隨機選股
    prices = {'NEE': 80, 'GEV': 450, 'VST': 120}
    price = prices[symbol]
    
    if st.session_state.cash >= price:
        st.session_state.holdings[symbol] += 1
        st.session_state.cash -= price
        
        trades.append({
            "時間": str(pd.Timestamp.now()),
            "動作": f"AI買入{symbol}",
            "價格": f"${price}",
            "現金": st.session_state.cash,
            "持倉": st.session_state.holdings.copy()
        })
        
        # 永久保存
        with open(DATA_FILE, "w") as f:
            json.dump(trades, f)
        
        st.success(f"✅ AI買入 {symbol} 1股 @ ${price}")
        st.rerun()

# 永久歷史
st.subheader("📈 永久交易歷史")
if trades:
    df = pd.DataFrame(trades[-20:])
    st.dataframe(df[['時間', '動作', '價格', '現金']], use_container_width=True)
else:
    st.info("按AI買入開始記錄歷史！")

# 持倉明細
st.subheader("📊 持倉明細")
holdings_data = []
for symbol, shares in st.session_state.holdings.items():
    if shares > 0:
        price = 80 if symbol=='NEE' else 450 if symbol=='GEV' else 120
        value = shares * price
        holdings_data.append([symbol, shares, f"${price}", f"${value:.0f}"])
if holdings_
    st.dataframe(pd.DataFrame(holdings_data, columns=['股票','股數','現價','市值']))
else:
    st.info("暫無持倉")

if st.button("🔄 重置$10k"):
    st.session_state.cash = 10000
    st.session_state.holdings = {'NEE': 0, 'GEV': 0, 'VST': 0}
    st.rerun()
