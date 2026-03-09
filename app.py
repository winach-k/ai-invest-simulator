import streamlit as st
import yfinance as yf
import json
import os
import pandas as pd

st.title("🤖 AI電力股投資")

stocks = ['NEE','GEV','VST']

# 安全載入
if os.path.exists('portfolio.json'):
    try:
        with open('portfolio.json','r') as f:
            portfolio = json.load(f)
    except:
        portfolio = {'cash':10000,'holdings':{},'history':[]}
else:
    portfolio = {'cash':10000,'holdings':{},'history':[]}

# 初始化持倉
for s in stocks:
    if s not in portfolio['holdings']:
        portfolio['holdings'][s] = 0

@st.cache_data(ttl=30)
def get_prices():
    prices = {}
    for s in stocks:
        try:
            data = yf.download(s,period='1d',progress=False)
            prices[s] = round(data['Close'].iloc[-1],2)
        except:
            prices[s] = 80.0
    return prices

prices = get_prices()

# AI決策（簡化版）
def ai_signal(stock):
    try:
        ticker = yf.Ticker(stock)
        pe = ticker.info.get('forwardPE',25)
        return '買入' if pe < 20 else '賣出' if pe > 30 else '持有'
    except:
        return '持有'

# 價格+建議
st.subheader("📊 實時價格 & AI")
cols = st.columns(3)
for i,s in enumerate(stocks):
    with cols[i]:
        st.metric(s,f"${prices[s]}")
        signal = ai_signal(s)
        st.success(f"AI: {signal}")

# 總資產
total = portfolio['cash']
for s in stocks:
    total += portfolio['holdings'][s] * prices[s]
st.metric("💰 總資產",f"${total:,.0f}")

# 持倉表
hold_df = pd.DataFrame([
    {'股票':s,'股數':portfolio['holdings'][s],'市值':portfolio['holdings'][s]*prices[s]}
    for s in stocks
])
st.subheader("💼 持倉")
st.dataframe(hold_df)

# AI自動交易
if st.button("🚀 AI執行交易",type="primary"):
    for s in stocks:
        signal = ai_signal(s)
        shares = portfolio['holdings'][s]
        p = prices[s]
        
        if signal=='買入' and portfolio['cash']>=p and shares<20:
            portfolio['holdings'][s] +=1
            portfolio['cash'] -=p
            portfolio['history'].append(f"買{s}@{p}")
        elif signal=='賣出' and shares>0:
            portfolio['holdings'][s] -=1
            portfolio['cash'] +=p
            portfolio['history'].append(f"賣{s}@{p}")
    
    with open('portfolio.json','w') as f:
        json.dump(portfolio,f)
    st.rerun()

st.subheader("📈 歷史")
st.write(portfolio['history'][-8:])

st.caption("✅ 30秒更新價 | ✅ AI基於PE自動交易")
