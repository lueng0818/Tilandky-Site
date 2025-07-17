import streamlit as st

def show():
    st.title("聯絡我")
    name = st.text_input("姓名")
    email = st.text_input("Email")
    message = st.text_area("訊息內容")
    if st.button("送出"):
        # TODO: 整合 Email API 或 Google Forms
        st.success("已收到你的訊息，會儘快回覆！")
