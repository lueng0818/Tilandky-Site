import streamlit as st
from utils.loader import load_markdown
from utils.mailchimp import subscribe_email
from PIL import Image
import os

st.set_page_config(
    page_title="Tilandky的覺察日常",
    layout="wide",
)

# 注入 Tailwind CSS 樣式
st.markdown(
    "<link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css' rel='stylesheet'>",
    unsafe_allow_html=True
)

# 隱藏 Streamlit 自動產生的「Pages」導航（可視需要使用）
hide_css = """
<style>
[data-testid="stSidebarNav"] > div:nth-child(2) {
    display: none !important;
}
</style>
"""
st.markdown(hide_css, unsafe_allow_html=True)

# 側邊欄導航：僅保留部落格、免費資源、關於我、聯絡我
st.sidebar.title("Tilandky的覺察日常")
page = st.sidebar.radio("導航", ["部落格", "免費資源", "關於我", "聯絡我"])

# 根據選擇載入對應頁面
if page == "部落格":
    from views.blog import show as show_blog
    show_blog()
elif page == "免費資源":
    from views.resources import show as show_resources
    show_resources()
elif page == "關於我":
    from views.about import show as show_about
    show_about()
elif page == "聯絡我":
    from views.contact import show as show_contact
    show_contact()
