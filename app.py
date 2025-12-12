import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

# --- 1. 設定網頁標題與版面 ---
st.set_page_config(page_title="雲端留言板", page_icon="☁️")
st.title("☁️ 大家共享的雲端留言板")

# --- 2. 連線 Google Sheets 的函數 ---
@st.cache_resource
def init_connection():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
    ]
    
    # 讀取 Secrets 裡的原始字串
    raw_json = st.secrets["google_credentials"]
    
    # [關鍵修改] 這裡加上 strict=False
    # 這會告訴 Python：如果遇到奇怪的控制字元(如換行)，請忽略它，不要報錯！
    creds_dict = json.loads(raw_json, strict=False)
    
    # 建立憑證
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    client = gspread.authorize(creds)
    
    # 開啟試算表
    return client.open_by_url(st.secrets["spreadsheet_url"]).sheet1

# 執行連線
try:
    sheet = init_connection()
except Exception as e:
    st.error(f"連線失敗，請檢查 Secrets 設定。\n錯誤原因: {e}")
    st.stop()

# --- 3. 處理資料輸入的函數 ---
def submit():
    text_to_save = st.session_state.widget_input
    if text_to_save:
        try:
            sheet.insert_row([text_to_save], index=1)
            st.success("✅ 儲存成功！")
            st.session_state.widget_input = ""
        except Exception as e:
            st.error(f"寫入失敗: {e}")

# --- 4. 網頁排版區域 ---

st.subheader("📝 最新留言：")

try:
    messages = sheet.col_values(1)
    if not messages:
        st.info("目前還沒有人留言，搶個頭香吧！")
    else:
        for message in messages:
            st.info(f"📍 {message}")
except Exception as e:
    st.warning("讀取資料時發生錯誤，請稍後再試。")

st.markdown("---")
st.write("### 我要留言：")
st.text_input("輸入內容後按 Enter 送出", key="widget_input", on_change=submit)

if st.button("🔄 重新整理查看最新內容"):
    st.rerun()
