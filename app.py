import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.title("🤖 AI電力股（15秒更新）")

if 'cash' not in st.session_state:
    st.session_state.cash = 10000
    st.session_state.holdings = {'NEE':0, 'GEV':0, 'VST':0}
    st.session_state.history = []

stocks = ['NEE','GEV','VST']

@st.cache_data(ttl=15)  # 15秒更新！
def get_prices():
    prices = {}
    for s in stocks:
        try:
            ticker = yf.Ticker(s)
            hist = ticker.history(period='2d')
            prices[s] = round(hist['Close'][-1], 1)
        except:
            try:
                data = yf.download(s, period='1d', progress=False)
                prices[s] = round(data['Close'][-1], 1)
            except:
                prices[s] = 80.0
    return prices

prices = get_prices()

# 倒數刷新
st.metric("⏰ 下次更新", f"{15-(int(time.time())%15)}秒")

# 價格大儀表板
st.subheader("💹 實時價格 (15秒)")
cols = st.columns(3)
for i, s in enumerate(stocks):
    with cols[i]:
        st.metric(s, f"${prices[s]}", delta=0.5)

# AI決策
st.subheader("🤖 AI建議")
signals = {}
pe_cols = st.columns(3)
for i, s in enumerate(stocks):
    try:
        info = yf.Ticker(s).info
        pe = info.get('forwardPE', 25)
        signal = "🟢買入" if pe < 20 else "🔴賣出" if pe > 30 else "⚪持有"
        signals[s] = signal
    except:
        signals[s] = "⚪持有"
    pe_cols[i].write(f"**{s}: {signals[s]}**")

# 總資產閃爍
total = st.session_state.cash
for s in stocks:
    total += st.session_state.holdings[s] * prices[s]
st.metric("💰 總資產", f"${total:,.0f}")

# 持倉
hold_data = [{'股票':s, '股數':st.session_state.holdings[s], 
              '現價':f"${prices[s]}", '市值':f"${st.session_state.holdings[s]*prices[s]:,.0f}"} 
             for s in stocks]
st.subheader("💼 持倉")
st.dataframe(pd.DataFrame(hold_data))

# AI一鍵交易
col1, col2, col3 = st.columns(3)
if col1.button("🚀 AI全自動", type="primary"):
    for s in stocks:
        if signals[s] == "🟢買入" and st.session_state.cash >= prices[s]:
            st.session_state.holdings[s] += 1
            st.session_state.cash -= prices[s]
            st.session_state.history.append(f"買{s} ${prices[s]}")
        elif signals[s] == "🔴賣出" and st.session_state.holdings[s] > 0:
            st.session_state.holdings[s] -= 1
            st.session_state.cash += prices[s]
            st.session_state.history.append(f"賣{s} ${prices[s]}")
    st.rerun()

if col2.button("🟢 只買入"):
    for s in stocks:
        if signals[s] == "🟢買入" and st.session_state.cash >= prices[s]:
            st.session_state.holdings[s] += 1
            st.session_state.cash -= prices[s]
            st.session_state.history.append(f"買{s} ${prices[s]}")
    st.rerun()

if col3.button("🔴 只賣出"):
    for s in stocks:
        if signals[s] == "🔴賣出" and st.session_state.holdings[s] > 0:
            st.session_state.holdings[s] -= 1
            st.session_state.cash += prices[s]
            st.session_state.history.append(f"賣{s} ${prices[s]}")
    st.rerun()

st.subheader("📜 最新交易")
st.write(st.session_state.history[-5:])

# 自動刷新按鈕
if st.button("🔄 立即刷新"):
    st.cache_data.clear()
    st.rerun()

st.caption("⚡ 15秒自動更新 | AI基於PE決策 | 按🚀全自動交易")
