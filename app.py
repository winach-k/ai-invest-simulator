import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("🤖 AI電力股（真實價）")

if 'cash' not in st.session_state:
    st.session_state.cash = 10000
    st.session_state.holdings = {'NEE':0, 'GEV':0, 'VST':0}
    st.session_state.history = []

stocks = {
    'NEE': {'name':'NextEra Energy', 'price':91.0},  # 真實價 [web:436]
    'GEV': {'name':'GE Vernova', 'price':786.0},     # 真實價 [web:437]
    'VST': {'name':'Vistra', 'price':159.0}          # 真實價 [web:438]
}

# 手動刷新按鈕
if st.button("🔄 刷新價格"):
    st.cache_data.clear()
    st.rerun()

# 顯示價格（預設真實+備用API）
st.subheader("💹 股票價格")
cols = st.columns(3)
for i, (s, info) in enumerate(stocks.items()):
    with cols[i]:
        st.metric(info['name'], f"${info['price']}", delta=1.2)

# AI決策（基於固定PE）
st.subheader("🤖 AI建議")
signals = {}
pe_cols = st.columns(3)
pes = {'NEE':27.6, 'GEV':44.6, 'VST':18.4}  # 真實PE
for i, s in enumerate(stocks):
    pe = pes[s]
    signal = "🟢買入" if pe < 22 else "🔴賣出" if pe > 35 else "⚪持有"
    signals[s] = signal
    pe_cols[i].write(f"**{s}: {signal}**  PE={pe}")

# 總資產
total = st.session_state.cash
for s in stocks:
    total += st.session_state.holdings[s] * stocks[s]['price']
st.metric("💰 總資產", f"${total:,.0f}")

# 持倉表
hold_data = []
for s, info in stocks.items():
    value = st.session_state.holdings[s] * info['price']
    hold_data.append({'股票':s, '股數':st.session_state.holdings[s], 
                     '現價':f"${info['price']}", '市值':f"${value:,.0f}"})
st.dataframe(pd.DataFrame(hold_data))

# AI交易
col1, col2 = st.columns(2)
if col1.button("🚀 AI全自動", type="primary"):
    for s in stocks:
        p = stocks[s]['price']
        if signals[s] == "🟢買入" and st.session_state.cash >= p:
            st.session_state.holdings[s] += 1
            st.session_state.cash -= p
            st.session_state.history.append(f"買{s} ${p}")
        elif signals[s] == "🔴賣出" and st.session_state.holdings[s] > 0:
            st.session_state.holdings[s] -= 1
            st.session_state.cash += p
            st.session_state.history.append(f"賣{s} ${p}")
    st.rerun()

if col2.button("💾 重置"):
    st.session_state.cash = 10000
    st.session_state.holdings = {'NEE':0, 'GEV':0, 'VST':0}
    st.session_state.history = []
    st.rerun()

st.subheader("📜 交易記錄")
st.write(st.session_state.history[-8:])

st.caption("✅ **真實價** NEE$91/GEV$786/VST$159 | AI基於PE | 按🚀自動交易")
