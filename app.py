import streamlit as st
st.title("🦾 AI投資模擬器")
if 'cash' not in st.session_state:
    st.session_state.cash = 10000
st.metric("現金", f"${st.session_state.cash:,.0f}")
if st.button("AI買NEE"):
    st.session_state.cash -= 80
    st.rerun()
