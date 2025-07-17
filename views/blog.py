import streamlit as st
import os
import re
from datetime import datetime
from PIL import Image
import markdown
import shutil

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

def parse_frontmatter(path):
    """讀取 markdown 前置欄，回傳 dict 包含 title, date, images(list)"""
    meta = {"title": "", "date": "", "images": []}
    lines = open(path, encoding="utf-8").read().splitlines()
    in_meta = False
    for line in lines:
        if line.strip() == "---":
            if not in_meta:
                in_meta = True
            else:
                break
        elif in_meta and ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if key in ["title", "date"]:
                meta[key] = val
            elif key == "images":
                try:
                    meta["images"] = eval(val)
                except:
                    meta["images"] = []
    return meta

# 列出所有文章，並用「日期 + 標題」做成選單
posts = sorted([fn for fn in os.listdir(CONTENT_DIR) if fn.endswith(".md")], reverse=True)
labels = []
map_label_to_file = {}
for fn in posts:
    meta = parse_frontmatter(os.path.join(CONTENT_DIR, fn))
    label = f"{meta['date']} － {meta['title']}"
    labels.append(label)
    map_label_to_file[label] = fn

st.title("日常探索部落格")
choice = st.selectbox("選擇文章", ["── 新增文章 ──"] + labels)

# ***** 新增文章 *****
if choice == "── 新增文章 ──":
    st.header("新增文章")
    with st.form("new_post"):
        title = st.text_input("標題")
        content = st.text_area("內文")
        images = st.file_uploader("上傳圖片 (可多選)", type=["png","jpg","jpeg"], accept_multiple_files=True)
        if st.form_submit_button("發布"):
            date_str = datetime.now().strftime("%Y-%m-%d")
            fn_slug = slugify(title)
            # 儲存圖片
            saved = []
            for i, img in enumerate(images, start=1):
                ext = os.path.splitext(img.name)[1]
                fname = f"{fn_slug}-{i}{ext}"
                with open(os.path.join(IMAGE_DIR, fname), "wb") as f:
                    f.write(img.getbuffer())
                saved.append(fname)
            # 寫 markdown
            md_name = f"{date_str}-{fn_slug}.md"
            md_path = os.path.join(CONTENT_DIR, md_name)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(f"---\n")
                f.write(f"title: {title}\n")
                f.write(f"date: {date_str}\n")
                f.write(f"images: {saved}\n")
                f.write(f"---\n\n")
                f.write(content)
            st.success("文章已新增！請重新整理以查看。")

# ***** 選擇文章後：顯示、編輯、刪除 *****
else:
    fn = map_label_to_file[choice]
    path = os.path.join(CONTENT_DIR, fn)
    meta = parse_frontmatter(path)
    body = "\n".join(open(path, encoding="utf-8").read().split("---")[2:]).strip()
    
    # 顯示
    st.header(meta["title"])

# 圖片橫向滑動顯示（類似 IG Carousel）
images = meta.get("images", [])
if images:
    # 建構一個可左右滑動的容器
    html = "<div style='display:flex; gap:8px; overflow-x:auto; padding:8px 0;'>"
    for img in images:
        img_path = os.path.join(IMAGE_DIR, img)
        # Streamlit 允許用相對路徑直接做 <img> 標籤
        html += f"<img src='{img_path}' style='height:300px; flex-shrink:0; border-radius:8px;'/>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)
    
    # 編輯與刪除按鈕
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✏️ 編輯文章"):
            st.session_state.edit_mode = True
    with col2:
        if st.button("🗑️ 刪除文章"):
            # 刪除 markdown
            os.remove(path)
            # 刪除對應圖片
            for img in meta["images"]:
                p = os.path.join(IMAGE_DIR, img)
                if os.path.exists(p):
                    os.remove(p)
            st.success("文章已刪除！請重新整理。")
            st.experimental_rerun()
    
    # 編輯模式
    if st.session_state.get("edit_mode", False):
        st.subheader("編輯文章")
        with st.form("edit_post"):
            new_title = st.text_input("標題", meta["title"])
            new_body = st.text_area("內文", body)
            new_images = st.file_uploader("新增圖片 (可多選)", type=["png","jpg","jpeg"], accept_multiple_files=True)
            if st.form_submit_button("儲存修改"):
                # 新增圖片至列表
                saved = meta["images"][:]
                for i, img in enumerate(new_images, start=len(saved)+1):
                    ext = os.path.splitext(img.name)[1]
                    fname = f"{slugify(meta['title'])}-{i}{ext}"
                    with open(os.path.join(IMAGE_DIR, fname), "wb") as f:
                        f.write(img.getbuffer())
                    saved.append(fname)
                # 重寫 markdown (保留舊圖片，也可自行改成整組替換)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(f"---\n")
                    f.write(f"title: {new_title}\n")
                    f.write(f"date: {meta['date']}\n")
                    f.write(f"images: {saved}\n")
                    f.write(f"---\n\n")
                    f.write(new_body)
                st.success("文章已更新！")
                # 離開編輯模式並重新整理
                st.session_state.edit_mode = False
                st.experimental_rerun()
