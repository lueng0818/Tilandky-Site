import streamlit as st
from utils.mailchimp import subscribe_email

def show():
    st.title("免費資源")
    st.markdown("下載我的免費手冊，開啟日常療癒練習：")
    email = st.text_input("Email")
    if st.button("訂閱並下載 PDF"):
        if subscribe_email(email):
            with open("content/freebies/guide.pdf", "rb") as f:
                st.download_button("點此下載 PDF", f, file_name="guide.pdf")
        else:
            st.error("訂閱失敗，請稍後再試。")

    st.markdown("---")
    st.markdown("### 延伸免費資源")
    st.markdown(
        """
        <ul class='list-disc list-inside'>
          <li><a href='https://maya-self-explore.streamlit.app/' target='_blank'>自我探索</a></li>
          <li><a href='https://maya-wealth.streamlit.app/' target='_blank'>金錢能量頻率</a></li>
          <li><a href='https://maya-emotion.streamlit.app/' target='_blank'>情感關係解讀</a></li>
        </ul>
        """,
        unsafe_allow_html=True
    )
