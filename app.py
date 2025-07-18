import os, sys, re, shutil
from datetime import datetime
from PIL import Image
import streamlit as st
import markdown
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# Mailchimp
MC = Client()
MC.set_config({
    "api_key": os.getenv("MAILCHIMP_API_KEY"),
    "server": os.getenv("MAILCHIMP_SERVER_PREFIX")
})
MC_LIST_ID = os.getenv("MAILCHIMP_LIST_ID")

def subscribe_email(email: str) -> bool:
    try:
        MC.lists.add_list_member(MC_LIST_ID, {"email_address": email, "status": "subscribed"})
        return True
    except ApiClientError:
        return False

# SMTP
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT   = int(os.getenv("SMTP_PORT", 587))
SMTP_USER   = os.getenv("SMTP_USER")
SMTP_PASS   = os.getenv("SMTP_PASSWORD")

def send_email(to_addr: str, subject: str, body: str) -> bool:
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = SMTP_USER
        msg["To"] = to_addr
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.sendmail(SMTP_USER, [to_addr], msg.as_string())
        return True
    except:
        return False

# 資料夾
CONTENT_DIR = "content/blog_posts"
IMAGE_DIR   = "assets/blog_images"
FREEBIE     = "content/freebies/guide.pdf"
os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# Utility: slug
def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    return re.sub(r"[\s-]+", "-", s).strip("-")

# 解析 frontmatter and body
def load_md(path: str) -> dict:
    lines = open(path, encoding="utf-8").read().splitlines()
    meta, body = {}, []
    in_meta = False
    for l in lines:
        if l.strip() == "---":
            in_meta = not in_meta
            continue
        if in_meta and ":" in l:
            k, v = l.split(":", 1)
            meta[k.strip()] = v.strip()
        elif not in_meta:
            body.append(l)
    meta["images"] = eval(meta.get("images", "[]"))
    return {"meta": meta, "body": "\n".join(body)}

# SEO templates
TEMPLATES = {
    "星際馬雅曆解析": {...},
    "希塔療癒完整指南": {...},
    "十大身心靈整合服務": {...},
}

# Sitemap & robots
# [省略，保持原樣]

# Streamlit init
st.set_page_config(page_title="Tilandky的覺察日常", layout="wide")
st.markdown("<link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css' rel='stylesheet'>", unsafe_allow_html=True)
st.markdown("<style>[data-testid='stSidebarNav'] > div:nth-child(2){display:none!important;}</style>", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Tilandky的覺察日常")
page = st.sidebar.radio("導航", [
    "首頁",
    "星際馬雅曆法",
    "ThetaHealing 希塔療癒",
    "身心靈整合服務",
    "部落格",
    "免費資源",
    "關於我",
    "聯絡我",
])

# ===== 首頁 =====
if page == "首頁":
    # Banner 圖片
    st.image("assets/banner.jpg", use_container_width=True)

    # 主要介紹文字
    st.markdown(
        """
        <div class='prose lg:prose-xl mx-auto my-4'>
          <p>這裡是 <strong>Tilandky 的覺察日常</strong>。<br>
          陪你一起練習在關係裡，不再把自己藏起來；<br>
          在創業路上不再懷疑自己的價值。<br>
          我相信每個人都有自己的節奏與方式，<br>
          你不是不夠好，也不是走太慢，<br>
          只是需要被自己好好看見。</p>
          <p>你不需要一次改變所有事情，<br>
          只要願意從現在的你開始。</p>
          <p class='mt-2'><em>#Tilandky的覺察日常  #關係裡的自己也重要  #慢慢靠近自己  #相信才會看見</em></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 三大服務概覽
    st.markdown(
        """
        <div class='grid grid-cols-1 md:grid-cols-3 gap-4 my-4'>
          <div class='p-4 border rounded-lg hover:shadow-lg'>
            <h2 class='text-lg font-semibold'>星際馬雅曆解析</h2>
            <p>探索靈魂天命與銀河印記，解析你的 KIN。</p>
          </div>
          <div class='p-4 border rounded-lg hover:shadow-lg'>
            <h2 class='text-lg font-semibold'>ThetaHealing 希塔療癒</h2>
            <p>轉化潛意識，重啟靈魂程式的神聖技術。</p>
          </div>
          <div class='p-4 border rounded-lg hover:shadow-lg'>
            <h2 class='text-lg font-semibold'>身心靈整合服務</h2>
            <p>全方位療癒方案，從冥想到能量轉化。</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
elif page == "身心靈整合服務":
    st.title("身心靈整合服務貼文")

    # 指定這個主題的存檔資料夾
    TOPIC_DIR = os.path.join("content", "integrative_posts")
    os.makedirs(TOPIC_DIR, exist_ok=True)

    # 讀取現有文章
    posts = sorted([f for f in os.listdir(TOPIC_DIR) if f.endswith(".md")], reverse=True)

    # 側欄：新增 or 選擇文章
    choice = st.sidebar.selectbox(
        "文章列表",
        ["── 新增文章 ──"] + posts,
        key="integrative_choice"
    )

    # ---- 新增文章 ----
    if choice == "── 新增文章 ──":
        with st.sidebar.form("integrative_form"):
            title   = st.text_input("標題")
            html    = st.text_area("HTML 內文（可直接貼入）", height=200)
            imgs    = st.file_uploader("上傳圖片 (可多選)", accept_multiple_files=True)
            submit  = st.form_submit_button("發布文章", key="integrative_submit")

        if submit:
            # 存圖片
            img_names = []
            for idx, img in enumerate(imgs or [], start=1):
                ext = os.path.splitext(img.name)[1]
                fn  = f"{slugify(title)}-{idx}{ext}"
                path = os.path.join("assets", fn)
                with open(path, "wb") as f: f.write(img.getbuffer())
                img_names.append(fn)

            # 寫 Markdown：frontmatter 裡留 html 與 images 欄位
            date_str = datetime.now().strftime("%Y-%m-%d")
            slug = slugify(title)
            md_fn = f"{date_str}-{slug}.md"
            with open(os.path.join(TOPIC_DIR, md_fn), "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"title: {title}\n")
                f.write(f"date: {date_str}\n")
                f.write(f"images: {img_names}\n")
                f.write("---\n\n")
                f.write(html)
            st.sidebar.success("文章已發布！")
            st.experimental_rerun()

    # ---- 顯示／編輯／刪除文章 ----
    else:
        # 解析選中檔案
        path = os.path.join(TOPIC_DIR, choice)
        text = open(path, encoding="utf-8").read().splitlines()
        # 取出 frontmatter 與 body
        fm = {}
        body_lines = []
        in_meta = False
        for l in text:
            if l.strip()=="---":
                in_meta = not in_meta
                continue
            if in_meta and ":" in l:
                k, v = l.split(":",1)
                fm[k.strip()] = eval(v.strip()) if k.strip()=="images" else v.strip()
            elif not in_meta:
                body_lines.append(l)
        # 標題
        st.header(fm.get("title",""))
        # 圖片
        for img in fm.get("images", []):
            st.image(os.path.join("assets", img), use_container_width=True)
        # HTML 內文
        st.markdown("\n".join(body_lines), unsafe_allow_html=True)

        # 編輯／刪除按鈕
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ 編輯", key="integrative_edit"):
                st.session_state.edit_mode = True
        with col2:
            if st.button("🗑️ 刪除", key="integrative_delete"):
                os.remove(path)
                for img in fm.get("images", []):
                    pimg = os.path.join("assets", img)
                    if os.path.exists(pimg): os.remove(pimg)
                st.success("文章已刪除！")
                st.experimental_rerun()

        # 編輯模式
        if st.session_state.get("edit_mode", False):
            with st.form("integrative_edit_form"):
                new_html = st.text_area("HTML 內文", value="\n".join(body_lines), height=200)
                new_imgs = st.file_uploader("新增圖片 (可多選)", accept_multiple_files=True)
                save = st.form_submit_button("儲存修改", key="integrative_save")
            if save:
                # 同樣流程：存新圖、寫回檔案
                imgs = fm.get("images", [])
                for idx, img in enumerate(new_imgs or [], start=len(imgs)+1):
                    ext = os.path.splitext(img.name)[1]
                    fn  = f"{slugify(fm['title'])}-{idx}{ext}"
                    pathimg = os.path.join("assets", fn)
                    with open(pathimg, "wb") as f: f.write(img.getbuffer())
                    imgs.append(fn)
                # 重寫 md
                with open(path, "w", encoding="utf-8") as f:
                    f.write("---\n")
                    f.write(f"title: {fm['title']}\n")
                    f.write(f"date: {fm['date']}\n")
                    f.write(f"images: {imgs}\n")
                    f.write("---\n\n")
                    f.write(new_html)
                st.success("文章已更新！")
                st.session_state.edit_mode = False
                st.experimental_rerun()

elif page == "星際馬雅曆法":
    st.title("星際馬雅曆法解析貼文")

    # 指定這個主題的存檔資料夾
    TOPIC_DIR = os.path.join("content", "maya_posts")
    os.makedirs(TOPIC_DIR, exist_ok=True)

    # 讀取現有文章
    posts = sorted([f for f in os.listdir(TOPIC_DIR) if f.endswith(".md")], reverse=True)

    # 側欄：新增 or 選擇文章
    choice = st.sidebar.selectbox(
        "文章列表",
        ["── 新增文章 ──"] + posts,
        key="maya_choice"
    )

    # ---- 新增文章 ----
    if choice == "── 新增文章 ──":
        with st.sidebar.form("maya_form"):
            title   = st.text_input("標題")
            html    = st.text_area("HTML 內文（可直接貼入）", height=200)
            imgs    = st.file_uploader("上傳圖片 (可多選)", accept_multiple_files=True)
            submit  = st.form_submit_button("發布文章", key="maya_submit")

        if submit:
            # 存圖片
            img_names = []
            for idx, img in enumerate(imgs or [], start=1):
                ext = os.path.splitext(img.name)[1]
                fn  = f"{slugify(title)}-{idx}{ext}"
                path = os.path.join("assets", fn)
                with open(path, "wb") as f: f.write(img.getbuffer())
                img_names.append(fn)

            # 寫 Markdown：frontmatter 裡留 html 與 images 欄位
            date_str = datetime.now().strftime("%Y-%m-%d")
            slug = slugify(title)
            md_fn = f"{date_str}-{slug}.md"
            with open(os.path.join(TOPIC_DIR, md_fn), "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"title: {title}\n")
                f.write(f"date: {date_str}\n")
                f.write(f"images: {img_names}\n")
                f.write("---\n\n")
                f.write(html)
            st.sidebar.success("文章已發布！")
            st.experimental_rerun()

    # ---- 顯示／編輯／刪除文章 ----
    else:
        # 解析選中檔案
        path = os.path.join(TOPIC_DIR, choice)
        text = open(path, encoding="utf-8").read().splitlines()
        # 取出 frontmatter 與 body
        fm = {}
        body_lines = []
        in_meta = False
        for l in text:
            if l.strip()=="---":
                in_meta = not in_meta
                continue
            if in_meta and ":" in l:
                k, v = l.split(":",1)
                fm[k.strip()] = eval(v.strip()) if k.strip()=="images" else v.strip()
            elif not in_meta:
                body_lines.append(l)
        # 標題
        st.header(fm.get("title",""))
        # 圖片
        for img in fm.get("images", []):
            st.image(os.path.join("assets", img), use_container_width=True)
        # HTML 內文
        st.markdown("\n".join(body_lines), unsafe_allow_html=True)

        # 編輯／刪除按鈕
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ 編輯", key="maya_edit"):
                st.session_state.edit_mode = True
        with col2:
            if st.button("🗑️ 刪除", key="maya_delete"):
                os.remove(path)
                for img in fm.get("images", []):
                    pimg = os.path.join("assets", img)
                    if os.path.exists(pimg): os.remove(pimg)
                st.success("文章已刪除！")
                st.experimental_rerun()

        # 編輯模式
        if st.session_state.get("edit_mode", False):
            with st.form("maya_edit_form"):
                new_html = st.text_area("HTML 內文", value="\n".join(body_lines), height=200)
                new_imgs = st.file_uploader("新增圖片 (可多選)", accept_multiple_files=True)
                save = st.form_submit_button("儲存修改", key="maya_save")
            if save:
                # 同樣流程：存新圖、寫回檔案
                imgs = fm.get("images", [])
                for idx, img in enumerate(new_imgs or [], start=len(imgs)+1):
                    ext = os.path.splitext(img.name)[1]
                    fn  = f"{slugify(fm['title'])}-{idx}{ext}"
                    pathimg = os.path.join("assets", fn)
                    with open(pathimg, "wb") as f: f.write(img.getbuffer())
                    imgs.append(fn)
                # 重寫 md
                with open(path, "w", encoding="utf-8") as f:
                    f.write("---\n")
                    f.write(f"title: {fm['title']}\n")
                    f.write(f"date: {fm['date']}\n")
                    f.write(f"images: {imgs}\n")
                    f.write("---\n\n")
                    f.write(new_html)
                st.success("文章已更新！")
                st.session_state.edit_mode = False
                st.experimental_rerun()
             
elif page == "ThetaHealing 希塔療癒":
    st.title("ThetaHealing 希塔療癒貼文")

    # 指定這個主題的存檔資料夾
    TOPIC_DIR = os.path.join("content", "theta_posts")
    os.makedirs(TOPIC_DIR, exist_ok=True)

    # 讀取現有文章
    posts = sorted([f for f in os.listdir(TOPIC_DIR) if f.endswith(".md")], reverse=True)

    # 側欄：新增 or 選擇文章
    choice = st.sidebar.selectbox(
        "文章列表",
        ["── 新增文章 ──"] + posts,
        key="theta_choice"
    )

    # ---- 新增文章 ----
    if choice == "── 新增文章 ──":
        with st.sidebar.form("theta_form"):
            title   = st.text_input("標題")
            html    = st.text_area("HTML 內文（可直接貼入）", height=200)
            imgs    = st.file_uploader("上傳圖片 (可多選)", accept_multiple_files=True)
            submit  = st.form_submit_button("發布文章", key="theta_submit")

        if submit:
            # 存圖片
            img_names = []
            for idx, img in enumerate(imgs or [], start=1):
                ext = os.path.splitext(img.name)[1]
                fn  = f"{slugify(title)}-{idx}{ext}"
                path = os.path.join("assets", fn)
                with open(path, "wb") as f: f.write(img.getbuffer())
                img_names.append(fn)

            # 寫 Markdown：frontmatter 裡留 html 與 images 欄位
            date_str = datetime.now().strftime("%Y-%m-%d")
            slug = slugify(title)
            md_fn = f"{date_str}-{slug}.md"
            with open(os.path.join(TOPIC_DIR, md_fn), "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"title: {title}\n")
                f.write(f"date: {date_str}\n")
                f.write(f"images: {img_names}\n")
                f.write("---\n\n")
                f.write(html)
            st.sidebar.success("文章已發布！")
            st.experimental_rerun()

    # ---- 顯示／編輯／刪除文章 ----
    else:
        # 解析選中檔案
        path = os.path.join(TOPIC_DIR, choice)
        text = open(path, encoding="utf-8").read().splitlines()
        # 取出 frontmatter 與 body
        fm = {}
        body_lines = []
        in_meta = False
        for l in text:
            if l.strip()=="---":
                in_meta = not in_meta
                continue
            if in_meta and ":" in l:
                k, v = l.split(":",1)
                fm[k.strip()] = eval(v.strip()) if k.strip()=="images" else v.strip()
            elif not in_meta:
                body_lines.append(l)
        # 標題
        st.header(fm.get("title",""))
        # 圖片
        for img in fm.get("images", []):
            st.image(os.path.join("assets", img), use_container_width=True)
        # HTML 內文
        st.markdown("\n".join(body_lines), unsafe_allow_html=True)

        # 編輯／刪除按鈕
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✏️ 編輯", key="theta_edit"):
                st.session_state.edit_mode = True
        with col2:
            if st.button("🗑️ 刪除", key="theta_delete"):
                os.remove(path)
                for img in fm.get("images", []):
                    pimg = os.path.join("assets", img)
                    if os.path.exists(pimg): os.remove(pimg)
                st.success("文章已刪除！")
                st.experimental_rerun()

        # 編輯模式
        if st.session_state.get("edit_mode", False):
            with st.form("theta_edit_form"):
                new_html = st.text_area("HTML 內文", value="\n".join(body_lines), height=200)
                new_imgs = st.file_uploader("新增圖片 (可多選)", accept_multiple_files=True)
                save = st.form_submit_button("儲存修改", key="theta_save")
            if save:
                # 同樣流程：存新圖、寫回檔案
                imgs = fm.get("images", [])
                for idx, img in enumerate(new_imgs or [], start=len(imgs)+1):
                    ext = os.path.splitext(img.name)[1]
                    fn  = f"{slugify(fm['title'])}-{idx}{ext}"
                    pathimg = os.path.join("assets", fn)
                    with open(pathimg, "wb") as f: f.write(img.getbuffer())
                    imgs.append(fn)
                # 重寫 md
                with open(path, "w", encoding="utf-8") as f:
                    f.write("---\n")
                    f.write(f"title: {fm['title']}\n")
                    f.write(f"date: {fm['date']}\n")
                    f.write(f"images: {imgs}\n")
                    f.write("---\n\n")
                    f.write(new_html)
                st.success("文章已更新！")
                st.session_state.edit_mode = False
                st.experimental_rerun()

elif page == "部落格":
    st.title("日常探索部落格")

    # 為每個 selectbox 加上不同的 key
    tpl = st.sidebar.selectbox(
        "載入 SEO 範本",
        ["— 無 —"] + list(TEMPLATES.keys()),
        key="tpl_selectbox"
    )
    choice = st.sidebar.selectbox(
        "文章列表",
        ["── 新增文章 ──"] + sorted(os.listdir(CONTENT_DIR), reverse=True),
        key="choice_selectbox"
    )

    # 新增文章
    if choice == "── 新增文章 ──":
        with st.sidebar.form("new"):
            title = st.text_input("標題")
            keywords = st.text_input("關鍵字")
            description = st.text_area("摘要", height=60)
            outline = st.text_area("大綱(每行一項)", height=100)
            content = st.text_area("內文")
            imgs = st.file_uploader("圖片(多選)", accept_multiple_files=True)
            submit = st.form_submit_button("發布")
        # apply template...
        if submit and title:
            # ... save logic ...
            st.sidebar.success("已發布文章！")
    # 顯示／編輯／刪除文章
    else:
        path = os.path.join(CONTENT_DIR, choice)
        data = load_md(path)
        meta, body = data["meta"], data["body"]
        st.header(meta["title"])
        # 顯示 images
        for img in meta["images"]:
            p = os.path.join(IMAGE_DIR, img)
            if os.path.exists(p): st.image(p, use_container_width=True)
        st.markdown(markdown.markdown(body), unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("編輯文章"):
                st.warning("編輯暫不支援！")
        with col2:
            if st.button("刪除文章"):
                os.remove(path)
                for img in meta["images"]:
                    ip = os.path.join(IMAGE_DIR, img)
                    if os.path.exists(ip): os.remove(ip)
                st.success("文章已刪除，請重新整理！")


# ===== 免費資源 =====
elif page=="免費資源":
    st.title("免費資源")
    e = st.text_input("Email")
    if st.button("訂閱&下載"):
        if subscribe_email(e):
            with open(FREEBIE,"rb") as f: st.download_button("下載",f,"guide.pdf")
        else: st.error("失敗")
    st.markdown("""
    <ul class="list-disc list-inside">
      <li><a href="https://maya-self-explore.streamlit.app/" target="_blank">自我探索</a></li>
      <li><a href="https://maya-wealth.streamlit.app/" target="_blank">金錢能量頻率</a></li>
      <li><a href="https://maya-emotion.streamlit.app/" target="_blank">情感關係解讀</a></li>
    </ul>
    """, unsafe_allow_html=True)

# ===== 關於我 =====
elif page=="關於我":
    st.markdown("<div class='text-center mb-4'>",unsafe_allow_html=True)
    st.image("assets/logo.png", width=180)
    st.markdown("</div>",unsafe_allow_html=True)
    c1,c2 = st.columns([1,3])
    with c1:
        st.image("assets/about_photo.png", width=240)
    with c2:
        st.markdown("""
        <h3>諮詢師介紹：<strong>Tilandky</strong> (KIN 2 月亮白風·紅龍波)</h3>
        <ol>
          <li>星際馬雅13月亮曆 & 彩虹數字學</li>
          <li>希塔療癒師暨原型卡引導者</li>
          <li>伴侶合盤解讀與信念轉化</li>
          <li>前軍職資訊教官，ISO 27001/27701 背景</li>
          <li>服務 300+ 個案、推廣四梯課程</li>
          <li>溫柔覺察 × 結構清晰 × 信仰友善</li>
        </ol>
        """,unsafe_allow_html=True)

# ===== 聯絡我 =====
elif page=="聯絡我":
    st.title("聯絡我")
    st.markdown("Line@：[加入點我](https://line.me/R/ti/p/%40690ZLAGN)")
    n = st.text_input("姓名")
    m = st.text_input("Email")
    t = st.text_area("訊息")
    if st.button("送出"):
        sub = f"新訊息：{n}"
        bd  = f"姓名:{n}\nEmail:{m}\n\n{t}"
        if send_email("lueng1314@gmail.com", sub, bd): st.success("已寄信")
        else: st.error("失敗")
