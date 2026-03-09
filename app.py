import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf

st.set_page_config(page_title="AI投資模擬器", layout="wide")
st.title("🦾 AI投資模擬器 $10,000")

if 'cash' not in st.session_state:
    st.session_state.cash = 10000
    st.session_state.holdings = {'NEE':0, 'GEV':0}
    st.session_state.transactions = []

col1, col2 = st.columns(2)

with col1:
    total_value = st.session_state.cash
    for symbol, shares in st.session_state.holdings.items():
        if shares > 0:
            price = 80 if symbol=='NEE' else 450
            total_value += shares * price
    st.metric("總資產", f"${total_value:,.0f}", f"{(total_value-10000)/100:.1f}%")

with col2:
    if st.button("🚀 AI買NEE"):
        if st.session_state.cash >= 80:
            st.session_state.holdings['NEE'] += 1
            st.session_state.cash -= 80
            st.session_state.transactions.append({
                '時間': '現在',
                '動作': '買入',
                '股票': 'NEE',
                '股數': 1,
                '價格': '$80'
            })
            st.rerun()

st.dataframe(pd.DataFrame(st.session_state.transactions))
if st.button("🔄 重置"):
    st.session_state.cash = 10000
    st.session_state.holdings = {'NEE':0, 'GEV':0}
    st.session_state.transactions = []
    st.rerun()
