import streamlit as st
import os
import re
from datetime import datetime
from PIL import Image
import markdown

# 目錄設定
CONTENT_DIR = os.path.join("content", "blog_posts")
IMAGE_DIR = os.path.join("assets", "blog_images")
os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

def slugify(text):
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s-]+", "-", s).strip("-")
    return s

# =========================
# 側邊欄：貼文表單
# =========================
st.sidebar.header("撰寫新文章")
with st.sidebar.form("new_post"):
    title = st.text_input("標題")
    content = st.text_area("內文")
    # 接受多張檔案
    images = st.file_uploader("上傳圖片 (可多選)", type=["png","jpg","jpeg"], accept_multiple_files=True)
    submit = st.form_submit_button("發布")

if submit and title and content:
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = slugify(title)
    # 儲存所有上傳圖片
    saved_images = []
    for img in images:
        ext = os.path.splitext(img.name)[1]
        fname = f"{slug}-{len(saved_images)+1}{ext}"
        path = os.path.join(IMAGE_DIR, fname)
        with open(path, "wb") as f:
            f.write(img.getbuffer())
        saved_images.append(fname)
    # 建立 Markdown 檔，不再放 image 欄，而是純文字
    md_name = f"{date_str}-{slug}.md"
    md_path = os.path.join(CONTENT_DIR, md_name)
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"---\ntitle: {title}\ndate: {date_str}\nimages: {saved_images}\n---\n\n")
        f.write(content)
    st.sidebar.success("文章已發布！重新整理列表。")

# =========================
# 主區：顯示文章
# =========================
st.title("日常探索部落格")
# 取出所有 .md
posts = sorted([fn for fn in os.listdir(CONTENT_DIR) if fn.endswith(".md")], reverse=True)
sel = st.selectbox("選擇文章", posts)

if sel:
    md_path = os.path.join(CONTENT_DIR, sel)
    text = open(md_path, encoding="utf-8").read().splitlines()
    # 先解析 frontmatter，找出 images 欄位
    images_line = next((line for line in text if line.startswith("images:")), "")
    img_list = []
    if images_line:
        # 將 Python-list 字串轉回 list
        try:
            img_list = eval(images_line.split("images:")[1].strip())
        except:
            img_list = []
    # 顯示標題與日期
    #   也可在 frontmatter 中解析 title/date
    # 顯示每張圖片
    for img_fname in img_list:
        img_path = os.path.join(IMAGE_DIR, img_fname)
        if os.path.exists(img_path):
            st.image(Image.open(img_path), use_container_width=True)
    # 剩餘的 Markdown 內容，用 markdown 套件轉 HTML
    # 跳過前三行 frontmatter
    body = "\n".join(text[text.index("")+1:]) if "" in text else "\n".join(text)
    st.markdown(markdown.markdown(body), unsafe_allow_html=True)
