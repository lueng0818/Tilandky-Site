## app.py
```python
import streamlit as st
from utils.loader import load_markdown
from utils.mailchimp import subscribe_email
from PIL import Image
import os

st.set_page_config(
    page_title="Tilandky 日常探索",
    layout="wide",
)

# 注入 Tailwind CSS
st.markdown(
    "<link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css' rel='stylesheet'>",
    unsafe_allow_html=True
)

# 側邊欄導覽
st.sidebar.title("Tilandky 日常探索")
page = st.sidebar.radio("導航", ["首頁", "部落格", "免費資源", "關於我", "聯絡我"])

# 路由選擇
if page == "首頁":
    from pages.home import show as show_home
    show_home()
elif page == "部落格":
    from pages.blog import show as show_blog
    show_blog()
elif page == "免費資源":
    from pages.resources import show as show_resources
    show_resources()
elif page == "關於我":
    from pages.about import show as show_about
    show_about()
else:
    from pages.contact import show as show_contact
    show_contact()
