import streamlit as st
import yfinance as yf
import json
import os

st.title("🦾 AI投資")

portfolio = {'cash':10000, 'nee':0, 'history':[]}

if os.path.exists('data.json'):
    with open('data.json') as f:
        portfolio = json.load(f)

@st.cache_data(ttl=30)
def get_price():
    try:
        return round(yf.download('NEE',period='1d',progress=False)['Close'].iloc[-1],2)
    except:
        return 80

price = get_price()
total = portfolio['cash'] + portfolio['nee'] * price

col1,col2,col3 = st.columns(3)
col1.metric("總資產",f"${total:,.0f}")
col2.metric("現金",f"${portfolio['cash']:,.0f}")
col3.metric("NEE",f"{portfolio['nee']} @ ${price}")

if st.button("🟢 買NEE") and portfolio['cash']>=price:
    portfolio['nee'] += 1
    portfolio['cash'] -= price
    portfolio['history'].append(f"買@{price}")
    with open('data.json','w') as f:
        json.dump(portfolio,f)
    st.rerun()

if st.button("🔴 賣NEE") and portfolio['nee']>0:
    portfolio['nee'] -= 1
    portfolio['cash'] += price
    portfolio['history'].append(f"賣@{price}")
    with open('data.json','w') as f:
        json.dump(portfolio,f)
    st.rerun()

st.write("歷史:",portfolio['history'][-5:])
st.caption("30秒自動價 | 永久保存")
