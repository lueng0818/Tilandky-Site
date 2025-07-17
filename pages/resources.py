import streamlit as st
from utils.mailchimp import subscribe_email

def show():
    st.title("免費資源")
    st.markdown("下載我的免費手冊，開啟日常療癒練習：")
    email = st.text_input("Email")
    if st.button("訂閱並下載 PDF"):
        if subscribe_email(email):
            with open('content/freebies/guide.pdf', 'rb') as f:
                st.download_button("點此下載 PDF", f, file_name='guide.pdf')
        else:
            st.error("訂閱失敗，請稍後再試。")
