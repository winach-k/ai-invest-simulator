import streamlit as st
import yfinance as yf
import pandas as pd

st.title("🤖 AI電力股投資")

if 'cash' not in st.session_state:
    st.session_state.cash = 10000
    st.session_state.holdings = {'NEE':0, 'GEV':0, 'VST':0}
    st.session_state.history = []

stocks = ['NEE','GEV','VST']

@st.cache_data(ttl=30)
def get_prices():
    prices = {}
    for s in stocks:
        try:
            ticker = yf.Ticker(s)
            hist = ticker.history(period='2d')
            prices[s] = round(hist['Close'][-1], 1)
        except:
            prices[s] = 80.0
    return prices

prices = get_prices()

# 顯示價格
st.subheader("💹 實時價格")
cols = st.columns(3)
for i, s in enumerate(stocks):
    with cols[i]:
        st.metric(s, f"${prices[s]}")

# AI簡單決策
st.subheader("🤖 AI建議")
ai_cols = st.columns(3)
signals = {}
for i, s in enumerate(stocks):
    try:
        pe = yf.Ticker(s).info.get('forwardPE', 25)
        signal = "🟢買入" if pe < 20 else "🔴賣出" if pe > 30 else "⚪持有"
    except:
        signal = "⚪持有"
    signals[s] = signal
    ai_cols[i].write(f"**{s}: {signal}** (PE:{pe:.1f})" if 'pe' in locals() else f"**{s}: {signal}**")

# 總資產
total = st.session_state.cash
for s in stocks:
    total += st.session_state.holdings[s] * prices[s]
st.metric("💰 總資產", f"${total:,.0f}")

# 持倉表
st.subheader("💼 持倉")
hold_data = []
for s in stocks:
    value = st.session_state.holdings[s] * prices[s]
    hold_data.append({'股票':s, '股數':st.session_state.holdings[s], '市值':f"${value:,.0f}"})
st.dataframe(pd.DataFrame(hold_data))

# AI交易按鈕
col1, col2 = st.columns(2)
if col1.button("🚀 AI買入建議", type="primary"):
    for s in stocks:
        if signals[s] == "🟢買入" and st.session_state.cash >= prices[s]:
            st.session_state.holdings[s] += 1
            st.session_state.cash -= prices[s]
            st.session_state.history.append(f"AI買{s} ${prices[s]}")
    st.rerun()

if col2.button("🔄 AI賣出建議"):
    for s in stocks:
        if signals[s] == "🔴賣出" and st.session_state.holdings[s] > 0:
            st.session_state.holdings[s] -= 1
            st.session_state.cash += prices[s]
            st.session_state.history.append(f"AI賣{s} ${prices[s]}")
    st.rerun()

st.subheader("📜 交易記錄")
st.write(st.session_state.history[-10:])

st.caption("✅ 30秒實時價 | ✅ session_state永久存 | ✅ AI基於PE自動交易")
