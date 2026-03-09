import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

st.set_page_config(page_title="電力股遊戲", layout="wide")
st.title("⚡ 電力股交易大賽 ⚡")

# 遊戲初始化
if 'round' not in st.session_state:
    st.session_state.round = 1
    st.session_state.cash = 10000
    st.session_state.holdings = {'NEE':0, 'GEV':0, 'VST':0}
    st.session_state.ai_cash = 10000
    st.session_state.ai_holdings = {'NEE':0, 'GEV':0, 'VST':0}
    st.session_state.prices = {'NEE':91, 'GEV':785, 'VST':159}
    st.session_state.history = []

stocks = ['NEE','GEV','VST']
stock_names = {'NEE':'NextEra','GEV':'GE Vernova','VST':'Vistra'}

# 每輪隨機波動
def update_prices():
    for s in stocks:
        change = np.random.uniform(-5, +8) / 100
        st.session_state.prices[s] = round(st.session_state.prices[s] * (1 + change), 1)

# AI對手（簡單策略）
def ai_trade():
    for s in stocks:
        p = st.session_state.prices[s]
        # AI隨機買低賣高
        if np.random.random() > 0.7 and st.session_state.ai_cash >= p:
            st.session_state.ai_holdings[s] += 1
            st.session_state.ai_cash -= p
        elif st.session_state.ai_holdings[s] > 0 and np.random.random() > 0.8:
            st.session_state.ai_holdings[s] -= 1
            st.session_state.ai_cash += p

# 遊戲主畫面
col_round, col_time = st.columns(2)
col_round.metric("🏆 當前輪數", st.session_state.round)
col_time.metric("⏰ 遊戲時間", f"{datetime.now().strftime('%H:%M:%S')}")

# 價格表
st.subheader("📈 實時股價")
price_df = pd.DataFrame([
    {'股票':s, '價格':f"${st.session_state.prices[s]}", 
     '漲跌':f"{np.random.uniform(-5,5):+.1f}%"}
    for s in stocks
])
st.dataframe(price_df.style.highlight_max(axis=0), use_container_width=True)

# 玩家vs AI對戰
st.subheader("⚔️ 你 vs AI對手")
col_player, col_ai = st.columns(2)

with col_player:
    st.markdown("### 🟢 你")
    player_total = st.session_state.cash
    for s in stocks:
        player_total += st.session_state.holdings[s] * st.session_state.prices[s]
    st.metric("總資產", f"${player_total:,.0f}")
    st.write("持倉:", {k:v for k,v in st.session_state.holdings.items() if v>0})

with col_ai:
    st.markdown("### 🔴 AI對手")
    ai_total = st.session_state.ai_cash
    for s in stocks:
        ai_total += st.session_state.ai_holdings[s] * st.session_state.prices[s]
    st.metric("總資產", f"${ai_total:,.0f}")
    st.write("持倉:", {k:v for k,v in st.session_state.ai_holdings.items() if v>0})

# 交易區
st.subheader("💼 你的操作")
col1, col2, col3, col4 = st.columns(4)
if col1.button("➕ 買NEE", type="secondary"):
    if st.session_state.cash >= st.session_state.prices['NEE']:
        st.session_state.holdings['NEE'] += 1
        st.session_state.cash -= st.session_state.prices['NEE']
        st.session_state.history.append(f"買NEE ${st.session_state.prices['NEE']}")
        st.rerun()

if col2.button("➕ 買GEV", type="secondary"):
    if st.session_state.cash >= st.session_state.prices['GEV']:
        st.session_state.holdings['GEV'] += 1
        st.session_state.cash -= st.session_state.prices['GEV']
        st.session_state.history.append(f"買GEV ${st.session_state.prices['GEV']}")
        st.rerun()

if col3.button("➕ 買VST", type="secondary"):
    if st.session_state.cash >= st.session_state.prices['VST']:
        st.session_state.holdings['VST'] += 1
        st.session_state.cash -= st.session_state.prices['VST']
        st.session_state.history.append(f"買VST ${st.session_state.prices['VST']}")
        st.rerun()

if col4.button("💰 全賣", type="primary"):
    for s in stocks:
        st.session_state.cash += st.session_state.holdings[s] * st.session_state.prices[s]
        st.session_state.holdings[s] = 0
    st.session_state.history.append("全賣清倉")
    st.rerun()


