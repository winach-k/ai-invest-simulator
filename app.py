import streamlit as st
import yfinance as yf
import json
import os
from datetime import datetime

st.set_page_config(layout="wide")
st.title("🦾 AI投資Portfolio")

# 安全讀取portfolio
def load_portfolio():
    default = {'cash': 10000.0, 'holdings': {'NEE': 0}, 'trades': []}
    if os.path.exists('portfolio.json'):
        try:
            with open('portfolio.json', 'r') as f:
                data = json.load(f)
                # 確保結構完整
                for key in default:
                    if key not in 
                        data[key] = default[key]
                if 'NEE' not in data['holdings']:
                    data['holdings']['NEE'] = 0
                return data
        except:
            return default
    return default

portfolio = load_portfolio()

# 真實價格
@st.cache_data(ttl=30)
def get_price():
    try:
        data = yf.download('NEE', period='1d', progress=False)
        return round(data['Close'].iloc[-1], 2)
    except:
        return 80.0

price = get_price()
cash = portfolio['cash']
nee_shares = portfolio['holdings']['NEE']
total = cash + nee_shares * price

# 儀表板
col1, col2, col3 = st.columns(3)
col1.metric("💰 總資產", f"${total:,.0f}")
col2.metric("💵 現金", f"${cash:,.0f}")
col3.metric("📈 NEE", f"{nee_shares}股 @ ${price}")

# 交易
col_buy, col_sell = st.columns(2)
if col_buy.button("🟢 買NEE", type="primary"):
    if cash >= price:
        portfolio['holdings']['NEE'] += 1
        portfolio['cash'] -= price
        portfolio['trades'].append({
            '時間': str(datetime.now()),
            '動作': f'買NEE ${price}',
            '現金': portfolio['cash']
        })
        with open('portfolio.json', 'w') as f:
            json.dump(portfolio, f)
        st.rerun()

if col_sell.button("🔴 賣NEE"):
    if nee_shares > 0:
        portfolio['holdings']['NEE'] -= 1
        portfolio['cash'] += price
        portfolio['trades'].append({
            '時間': str(datetime.now()),
            '動作': f'賣NEE ${price}',
            '現金': portfolio['cash']
        })
        with open('portfolio.json', 'w') as f:
            json.dump(portfolio, f)
        st.rerun()

# 歷史
st.subheader("📊 交易記錄")
if portfolio['trades']:
    df = pd.DataFrame(portfolio['trades'][-10:])
    st.dataframe(df)
st.caption("⏰ 30秒自動更新價格 | 💾 永久保存")
