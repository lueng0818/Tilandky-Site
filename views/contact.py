## views/contact.py
```python
import streamlit as st
from email_sender import send_email


def show():
    st.title("聯絡我")
    st.markdown("如有任何需求，可透過 Line@ 或下方表單聯繫我：")
    st.markdown("[加入我的 Line@](https://line.me/R/ti/p/%40690ZLAGN)")

    name = st.text_input("姓名")
    email = st.text_input("Email")
    message = st.text_area("訊息內容")
    if st.button("送出"):
        # 寄信通知
        subject = f"新訊息：{name} 的聯絡表單"
        body = f"姓名: {name}
Email: {email}

訊息內容:
{message}"
        success = send_email(
            to_address="lueng1314@gmail.com",
            subject=subject,
            body=body
        )
        if success:
            st.success("已收到你的訊息，並已寄送通知信！")
        else:
            st.error("訊息發送失敗，請稍後再試或直接寫信至 lueng1314@gmail.com。")
```python
import streamlit as st


def show():
    st.title("聯絡我")
    name = st.text_input("姓名")
    email = st.text_input("Email")
    message = st.text_area("訊息內容")
    if st.button("送出"):
        # TODO: 整合 Email API 或 Google Forms
        st.success("已收到你的訊息，會儘快回覆！")
