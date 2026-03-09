import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(layout="wide")
st.title("🏢 動態上市公司分析")

# 多模式輸入
tab1, tab2, tab3 = st.tabs(["股票代碼", "上傳Excel", "華潤新能源"])

with tab1:
    ticker = st.text_input("股票代碼", "0700.HK")
    if st.button("🚀 即時分析"):
        stock = yf.Ticker(ticker)
        info = stock.info
        
        col1, col2, col3 = st.columns(3)
        col1.metric("市值", f"${info.get('marketCap','N/A')/1e9:.1f}B")
        col2.metric("PE", info.get('forwardPE','N/A'))
        col3.metric("股價", f"${stock.history(period='1d')['Close'][-1]:.1f}")
        
        hist = stock.history(period="2y")
        fig = px.line(hist, y='Close', title=f"{ticker} 股價趨勢")
        st.plotly_chart(fig)

with tab2:
    uploaded = st.file_uploader("📁 上傳財報Excel")
    if uploaded:
        df = pd.read_excel(uploaded)
        st.dataframe(df)
        # 自動計算比率
        if '收入' in df.columns and '淨利' in df.columns:
            df['淨利率'] = df['淨利']/df['收入']
            fig = px.bar(df, x=df.columns[0], y='淨利率', title="淨利率分析")
            st.plotly_chart(fig)

with tab3:
    # 華潤新能源專區
    st.subheader("☀️ 華潤新能源動態")
    cr_data = {
        '期間': ['2022','2023','2024','2025H1'],
        '收入億': [181.98,205.12,228.74,130.14],
        '淨利億': [62.96,82.80,79.53,47.02]
    }
    df_cr = pd.DataFrame(cr_data)
    fig_cr = px.line(df_cr, x='期間', y=['收入億','淨利億'])
    st.plotly_chart(fig_cr)
    
    # 即時新聞（模擬）
    st.info("最新：IPO進展順利，募資245億擴風光")

# 通用分析工具
st.sidebar.header("🔧 分析工具")
if st.sidebar.button("計算ROE"):
    roe = st.sidebar.number_input("淨利/億") / st.sidebar.number_input("權益/億")
    st.sidebar.metric("ROE", f"{roe:.1%}")

st.success("✅ **動態分析就緒**！輸入代碼/文件即分析")
