import streamlit as st
import time
import numpy as np
import pandas as pd

st.set_page_config(page_title="惡師傅瞓覺遊戲", layout="wide")
st.title("😴 惡師傅瞓覺大逃亡 😴")

# 遊戲狀態
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.teacher_face = "back"  # back/front
    st.session_state.students_sleep = 0
    st.session_state.max_score = 0

students = 6  # 6個小朋友

# 大教室畫面
st.markdown("## 🏫 教室情況")

# 老師狀態
col_teacher, col_score = st.columns([1,1])
with col_teacher:
    if st.session_state.teacher_face == "back":
        st.markdown("""
        ### 👨‍🏫 惡師傅（轉身寫黑板）
        ```
          O
         /|\\
         / \\
        黑板←
        ```
        """)
    else:
        st.markdown("""
        ### 😠 惡師傅（轉身檢查！）
        ```
          O←
         /|\\
         / \\
        檢查！
        ```
        """)

with col_score:
    st.metric("分數", st.session_state.score)
    st.metric("最高分", st.session_state.max_score)
    if st.session_state.game_over:
        st.error("💥 畀捉！遊戲完！")

# 小朋友座位（點擊控制）
st.subheader("👦👧 小朋友（點擊瞓/醒）")
student_cols = st.columns(students)
for i in range(students):
    with student_cols[i]:
        status = "😴瞓緊" if np.random.random() > 0.6 else "👀醒緊"
        if st.button(status, key=f"kid_{i}"):
            st.session_state.students_sleep += 1 if "瞓" in status else -1
            st.rerun()

st.info(f"現有 **{st.session_state.students_sleep}** 個小朋友瞓緊")

# 遊戲控制
st.subheader("🎮 控制")
col1, col2, col3 = st.columns(3)

if col1.button("🔄 師傅轉身檢查！", type="primary"):
    if st.session_state.teacher_face == "back":
        st.session_state.teacher_face = "front"
        if st.session_state.students_sleep > 0:
            st.session_state.score -= st.session_state.students_sleep * 10
            st.session_state.game_over = True
        st.rerun()
    else:
        st.session_state.teacher_face = "back"
        st.session_state.game_over = False
        st.rerun()

if col2.button("😴 全班瞓覺"):
    st.session_state.students_sleep = students
    st.rerun()

if col3.button("👀 全班醒覺"):
    st.session_state.students_sleep = 0
    st.rerun()

# 下一輪（自動加分）
if st.button("⏭️ 下一輪（師傅寫黑板）"):
    if st.session_state.teacher_face == "back" and not st.session_state.game_over:
        st.session_state.score += st.session_state.students_sleep * 5
        if st.session_state.score > st.session_state.max_score:
            st.session_state.max_score = st.session_state.score
    st.session_state.teacher_face = "back"
    st.session_state.game_over = False
    st.rerun()

# 排行榜
st.subheader("🏆 歷史分數")
scores = [st.session_state.max_score, 150, 220, 180, 300]
pd.DataFrame({'名次':['你',2,3,4,1], '分數':scores}).style.background_gradient()

st.caption("""
🎮 **玩法**：
1. 按「⏭️下一輪」→師傅轉身寫黑板
2. 點擊小朋友「😴瞓緊」→偷瞓加分
3. 唔好畀太多人瞓→按「🔄師傅檢查」會扣分！
4. 最高分贏！
""")
