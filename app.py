import streamlit as st
import numpy as np
import pandas as pd
import time
from datetime import datetime

st.title("🤖 全自動AI投資機器人 $10,000")

# 初始化
if 'auto_running' not in st.session_state:
    st.session_state.auto_running = True
    st.session_state.cash = 10000
    st.session_state.holdings = {'NEE': 0, 'GEV': 0, 'VST': 0}
    st.session_state.transactions = []
    st.session_state.last_trade = 0

# AI價格生成（每隻股票獨立波動）
def ai_price(symbol):
    base_prices = {'NEE': 80, 'GEV': 450, 'VST': 120}
    volatility = 0.025  # 每日2.5%波動
    return base_prices[symbol] * (1 + np.random.normal(0, volatility))

# AI選股決策（動量策略）
def ai_pick_stock():
    scores = {}
    for symbol in ['NEE', 'GEV', 'VST']:
        # 動量分數 + 估值分數
        momentum = np.random.normal(0.5, 0.2)
        valuation = np.random.normal(0.3, 0.15)
        scores[symbol] = momentum * 0.7 + valuation * 0.3
    return max(scores, key=scores.get)

# 自動交易邏輯（每15秒）
if st.session_state.auto_running:
    if time.time() - st.session_state.last_trade > 15:
        # 70%買入，30%賣出
        if np.random.random() < 0.7 and st.session_state.cash > 100:
            # AI選股
            symbol = ai_pick_stock()
            price = ai_price(symbol)
            shares = min(1, int(st.session_state.cash / price))
            
            st.session_state.holdings[symbol] += shares
            st.session_state.cash -= shares * price
            st.session_state.transactions.append({
                '時間': datetime.now().strftime('%H:%M:%S'),
                '動作': f'🟢買入{symbol}',
                '股數': shares,
                '價格': f'${price:.1f}'
            })
        
        elif sum(st.session_state.holdings.values()) > 0 and np.random.random() < 0.3:
            # 隨機賣出一隻股票
            symbol = np.random.choice(['NEE', 'GEV', 'VST'])
            if st.session_state.holdings[symbol] > 0:
                shares = 1
                price = ai_price(symbol)
                st.session_state.cash += shares * price * 0.98  # 2%手續費
                st.session_state.holdings[symbol] -= shares
                st.session_state.transactions.append({
                    '時間': datetime.now().strftime('%H:%M:%S'),
                    '動作': f'🔴賣出{symbol}',
                    '股數': shares,
                    '價格': f'${price:.1f}'
                })
        
        st.session_state.last_trade = time.time()

# 儀表板
col1, col2, col3 = st.columns(3)
total_value = st.session_state.cash
for symbol, shares in st.session_state.holdings.items():
    total_value += shares * ai_price(symbol)

with col1:
    st.metric("💰總資產", f"${total_value:,.0f}", 
              f"{((total_value-10000)/100):.1f}%")
with col2:
    st.metric("💵現金", f"${st.session_state.cash:,.0f}")
with col3:
    st.metric("📊持股數", sum(st.session_state.holdings.values()))

# 持倉表
st.subheader("📈 持倉")
holdings_data = []
for symbol, shares in st.session_state.holdings.items():
    if shares > 0:
        price = ai_price(symbol)
        value = shares * price
        holdings_data.append([symbol, shares, f"${price:.1f}", f"${value:.0f}"])
if holdings_
    st.dataframe(pd.DataFrame(holdings_data, columns=['股票','股數','現價','市值']))
else:
    st.info("🤖 AI暫未建倉")

# 交易記錄
st.subheader("📋 實時交易")
if st.session_state.transactions:
    df = pd.DataFrame(st.session_state.transactions[-15:])
    st.dataframe(df, use_container_width=True)
else:
    st.info("等待AI首次交易...")

# 控制面板
col1, col2 = st.columns(2)
with col1:
    if st.button("⏹️ 暫停AI", type="secondary"):
        st.session_state.auto_running = False
        st.rerun()
with col2:
    if st.button("🔄 重啟$10k", type="primary"):
        st.session_state.auto_running = True
        st.session_state.cash = 10000
        st.session_state.holdings = {'NEE': 0, 'GEV': 0, 'VST': 0}
        st.session_state.transactions = []
        st.session_state.last_trade = 0
        st.rerun()

st.caption("⚡ AI每15秒自動選股交易（NEE/GEV/VST），完全自動化！")
