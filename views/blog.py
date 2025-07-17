## views/blog.py
```python
import streamlit as st
import os
from utils.loader import load_markdown
from datetime import datetime
import re

CONTENT_DIR = os.path.join("content", "blog_posts")
IMAGE_DIR = os.path.join("assets", "blog_images")

# 確保目錄存在
os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text).strip('-')
    return text

# 貼文表單
st.sidebar.header("撰寫新文章")
with st.sidebar.form(key='new_post_form'):
    title = st.text_input("標題")
    content = st.text_area("內文")
    image_file = st.file_uploader("上傳封面圖片", type=['png','jpg','jpeg'])
    submit = st.form_submit_button("發布文章")

if submit and title and content:
    image_filename = None
    if image_file:
        ext = os.path.splitext(image_file.name)[1]
        image_filename = slugify(title) + ext
        img_path = os.path.join(IMAGE_DIR, image_filename)
        with open(img_path, 'wb') as f:
            f.write(image_file.getbuffer())
    date_str = datetime.now().strftime('%Y-%m-%d')
    slug = slugify(title)
    md_filename = f"{date_str}-{slug}.md"
    md_path = os.path.join(CONTENT_DIR, md_filename)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"---\ntitle: {title}\ndate: {date_str}\n")
        if image_filename:
            f.write(f"image: ../assets/blog_images/{image_filename}\n")
        f.write("---\n\n")
        f.write(content)
    st.sidebar.success("文章已發布！請重新整理列表。")

# 顯示現有文章
st.title("Tilandky的覺察日常部落格")
posts = sorted([f for f in os.listdir(CONTENT_DIR) if f.endswith('.md')], reverse=True)
choice = st.selectbox("選擇文章", posts)
if choice:
    md = load_markdown(os.path.join(CONTENT_DIR, choice))
    st.markdown(md, unsafe_allow_html=True)
