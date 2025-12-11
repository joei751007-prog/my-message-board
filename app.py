import streamlit as st

# 1. 設定網頁標題
st.title("📝 我的 Colab 即時看板")

# 2. 初始化 Session State (用來暫存資料)
# 如果這是第一次打開網頁，就建立一個空的清單來放資料
if 'history' not in st.session_state:
    st.session_state.history = []

# 3. 定義處理輸入的函數
def submit():
    # 取得輸入框的內容
    new_text = st.session_state.widget_input
    if new_text: # 如果有內容
        # 將新內容插入到清單的第一個位置 (索引 0)，達成「顯示在最上端」的效果
        st.session_state.history.insert(0, new_text)
        # 清空輸入框
        st.session_state.widget_input = ""

# 4. 網頁排版區域

# --- 顯示區 (在上方) ---
st.subheader("最新輸入內容顯示區：")
# 建立一個容器來裝資料
result_container = st.container()

with result_container:
    if not st.session_state.history:
        st.info("目前沒有資料，請在下方輸入。")
    else:
        # 把清單中的每一筆資料印出來
        for item in st.session_state.history:
            st.success(f"📍 {item}")

st.markdown("---") # 分隔線

# --- 輸入區 (在下方) ---
st.write("### 請輸入資料：")
# 這裡綁定 submit 函數，按下 Enter 或離開輸入框時會觸發
st.text_input("輸入後按 Enter", key="widget_input", on_change=submit)
