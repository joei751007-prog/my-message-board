import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

# --- 1. 設定網頁標題與版面 ---
st.set_page_config(page_title="雲端留言板", page_icon="☁️")
st.title("☁️ 大家共享的雲端留言板")

# --- 2. 連線 Google Sheets 的函數 ---
# 使用 @st.cache_resource 讓連線只需執行一次，加快網頁速度
@st.cache_resource
def init_connection():
    # 定義我們需要的權限範圍
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    
    # 從 Streamlit Secrets 讀取我們存好的 JSON 密碼
    # 注意：這裡對應您在 Secrets 裡設定的變數名稱
    creds_dict = json.loads(st.secrets["google_credentials"])
    
    # 建立憑證
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    
    # 授權 gspread
    client = gspread.authorize(creds)
    
    # 開啟試算表 (使用 Secrets 裡的網址)
    return client.open_by_url(st.secrets["spreadsheet_url"]).sheet1

# 執行連線
try:
    sheet = init_connection()
except Exception as e:
    st.error(f"連線失敗，請檢查 Secrets 設定是否正確。\n錯誤訊息: {e}")
    st.stop()

# --- 3. 處理資料輸入的函數 ---
def submit():
    text_to_save = st.session_state.widget_input
    if text_to_save:
        try:
            # 將資料插入到試算表的第 1 列 (index=1)
            # 這樣最新的資料永遠會在最上面
            sheet.insert_row([text_to_save], index=1)
            st.success("✅ 儲存成功！")
            # 清空輸入框
            st.session_state.widget_input = ""
        except Exception as e:
            st.error(f"寫入失敗: {e}")

# --- 4. 網頁排版區域 ---

# A. 顯示資料區 (從試算表讀取)
st.subheader("📝 最新留言：")

# 讀取試算表所有資料 (col 1 代表第一欄)
try:
    # 這裡只讀取第一欄的資料
    messages = sheet.col_values(1)
    
    if not messages:
        st.info("目前還沒有人留言，搶個頭香吧！")
    else:
        # 顯示每一筆留言
        for message in messages:
            st.info(f"📍 {message}")
            
except Exception as e:
    st.warning("讀取資料時發生錯誤，請稍後再試。")

st.markdown("---")

# B. 輸入區
st.write("### 我要留言：")
st.text_input("輸入內容後按 Enter 送出", key="widget_input", on_change=submit)

# 加入一個手動重新整理按鈕 (以防有人剛留言，你沒看到)
if st.button("🔄 重新整理查看最新內容"):
    st.rerun()
