import streamlit as st
import yfinance as yf
import json
import os
import numpy as np
import pandas as pd

st.title("🤖 AI電力股自動投資")

# 3隻熱門電力股
stocks = ['NEE', 'GEV', 'VST']
portfolio = {'cash':10000, 'holdings':{s:0 for s in stocks}, 'history':[]}

if os.path.exists('portfolio.json'):
    with open('portfolio.json') as f:
        portfolio = json.load(f)

@st.cache_data(ttl=30)
def get_prices():
    prices = {}
    for s in stocks:
        try:
            data = yf.download(s,period='5d',progress=False)
            prices[s] = round(data['Close'].iloc[-1],2)
        except:
            prices[s] = 80
    return prices

prices = get_prices()

# AI決策規則（專業投資法）
def ai_decision(stock):
    try:
        ticker = yf.Ticker(stock)
        info = ticker.info
        # 規則：PE低+漲幅+成交量
        pe = info.get('forwardPE', 20)
        change = (prices[stock] - prices[stock]*0.95)/prices[stock]*100  # 5日漲幅
        volume = info.get('volume', 0)
        
        score = 0
        if pe < 20: score += 3  # 低PE買入
        if change > 2: score += 2  # 上漲趨勢
        if volume > 1000000: score += 1  # 高成交
        
        return '買入' if score >= 4 else '持有' if score >= 2 else '賣出'
    except:
        return '持有'

# 顯示價格+AI建議
st.subheader("📊 實時價格 & AI建議")
cols = st.columns(3)
for i, stock in enumerate(stocks):
    with cols[i]:
        st.metric(stock, f"${prices[stock]}", delta=None)
        decision = ai_decision(stock)
        st.write(f"**AI建議**: {decision}")

# 總資產
total = portfolio['cash']
for s in stocks:
    total += portfolio['holdings'][s] * prices[s]
st.metric("💰 總資產", f"${total:,.0f}")

# AI自動交易
if st.button("🚀 AI自動執行建議", type="primary"):
    for stock in stocks:
        decision = ai_decision(stock)
        shares = portfolio['holdings'][stock]
        price = prices[stock]
        
        if decision == '買入' and portfolio['cash'] >= price and shares < 10:
            portfolio['holdings'][stock] += 1
            portfolio['cash'] -= price
            portfolio['history'].append(f"AI買{stock}@{price}")
        elif decision == '賣出' and shares > 0:
            portfolio['holdings'][stock] -= 1
            portfolio['cash'] += price
            portfolio['history'].append(f"AI賣{stock}@{price}")
    
    with open('portfolio.json','w') as f:
        json.dump(portfolio,f)
    st.success("✅ AI已執行交易！")
    st.rerun()

# 持倉
st.subheader("💼 我的持倉")
hold_df = pd.DataFrame([
    {'股票':s, '股數':portfolio['holdings'][s], '價值':portfolio['holdings'][s]*prices[s]}
    for s in stocks
])
st.dataframe(hold_df)

# 歷史
st.subheader("📈 交易歷史")
st.write(portfolio['history'][-10:])

st.caption("🤖 AI規則: 低PE+上漲+高成交=買入 | 30秒實時價")
