import streamlit as st
import pandas as pd
import numpy as np

st.title("⚡ 電力股交易遊戲 ⚡")

# 初始化
if 'round' not in st.session_state:
    st.session_state.round = 1
    st.session_state.player_cash = 10000
    st.session_state.player_holdings = {'NEE':0, 'GEV':0, 'VST':0}
    st.session_state.ai_cash = 10000
    st.session_state.ai_holdings = {'NEE':0, 'GEV':0, 'VST':0}
    st.session_state.prices = {'NEE':91.0, 'GEV':785.0, 'VST':159.0}

stocks = ['NEE', 'GEV', 'VST']

# 下一輪（股價變動）
if st.button("⏭️ 下一輪", type="primary"):
    # 股價隨機變
    for s in stocks:
        change = np.random.uniform(-0.08, 0.12)
        st.session_state.prices[s] = round(st.session_state.prices[s] * (1 + change), 1)
    st.session_state.round += 1
    st.rerun()

# AI行動
if st.button("🤖 AI行動"):
    for s in stocks:
        p = st.session_state.prices[s]
        if np.random.random() > 0.8 and st.session_state.ai_cash >= p:
            st.session_state.ai_holdings[s] += 1
            st.session_state.ai_cash -= p
    st.rerun()

# 股價顯示
st.subheader("📈 當前股價")
price_df = pd.DataFrame([
    {'股票': s, '價格': f"${st.session_state.prices[s]}", '漲跌': f"{np.random.uniform(-12,15):+.1f}%"}
    for s in stocks
])
st.dataframe(price_df, use_container_width=True)

# 總資產計算（修正！）
def calc_total(cash, holdings):
    total = cash
    for s in stocks:
        total += holdings[s] * st.session_state.prices[s]
    return round(total, 0)

player_total = calc_total(st.session_state.player_cash, st.session_state.player_holdings)
ai_total = calc_total(st.session_state.ai_cash, st.session_state.ai_holdings)

# 你 vs AI（加現金顯示）
st.subheader("💰 對戰狀態")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🟢 你")
    st.metric("總資產", f"${player_total:,}")
    st.metric("💵 現金", f"${st.session_state.player_cash:,}")
    st.json(st.session_state.player_holdings)

with col2:
    st.markdown("### 🔴 AI")
    st.metric("總資產", f"${ai_total:,}")
    st.metric("💵 現金", f"${st.session_state.ai_cash:,}")
    st.json(st.session_state.ai_holdings)

if player_total > ai_total:
    st.balloons()
    st.success(f"🎉 你領先 ${player_total - ai_total:,}!")

# 買賣區
st.subheader("💼 買賣（點擊股票）")
buy_cols = st.columns(3)
for i, s in enumerate(stocks):
    with buy_cols[i]:
        p = st.session_state.prices[s]
        col_b, col_s = st.columns(2)
        if col_b.button(f"🟢買{s}", key=f"buy_{i}"):
            if st.session_state.player_cash >= p:
                st.session_state.player_holdings[s] += 1
                st.session_state.player_cash -= p
                st.rerun()
            else:
                st.error("💸 錢不夠！")
        
        if col_s.button(f"🔴賣{s}", key=f"sell_{i}"):
            if st.session_state.player_holdings[s] > 0:
                st.session_state.player_holdings[s] -= 1
                st.session_state.player_cash += p
                st.rerun()
            else:
                st.warning("📭 無貨！")
        st.caption(f"${p}")

# 重置
if st.button("🔄 新遊戲"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.caption("🎮 **玩法**：買低賣高！按⏭️下一輪看誰贏！")
