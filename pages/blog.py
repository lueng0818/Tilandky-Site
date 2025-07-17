import streamlit as st
import os
from utils.loader import load_markdown

CONTENT_DIR = os.path.join("content", "blog_posts")

def show():
    st.title("日常探索部落格")
    posts = sorted([f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')], reverse=True)
    choice = st.selectbox("選擇文章", posts)
    if choice:
        md = load_markdown(os.path.join(CONTENT_DIR, choice))
        st.markdown(md, unsafe_allow_html=True)
