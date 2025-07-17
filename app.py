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
page = st.sidebar.radio("導航", ["首頁", "部落格", "免費資源", "關於我", "聯絡我"])

# ===== 首頁 =====
if page == "首頁":
    # Banner
    st.image("assets/banner.jpg", use_container_width=True)

    # 主要介紹
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

elif page == "部落格":
    st.title("日常探索部落格")

    # 側邊欄：SEO 範本 + 文章選擇
    tpl = st.sidebar.selectbox("載入 SEO 範本", ["— 無 —"] + list(TEMPLATES.keys()))
    choice = st.sidebar.selectbox(
        "文章列表",
        ["── 新增文章 ──"] + sorted(os.listdir(CONTENT_DIR), reverse=True),
    )

    # ── 新增文章 ──
    if choice == "── 新增文章 ──":
        with st.sidebar.form("new_post_form"):
            title       = st.text_input("標題")
            keywords    = st.text_input("關鍵字（逗號分隔）")
            description = st.text_area("摘要 / 描述", height=60)
            outline     = st.text_area("章節大綱（每行一項）", height=100)
            content     = st.text_area("內文")
            images      = st.file_uploader(
                "上傳圖片 (可多選)", type=["png", "jpg", "jpeg"], accept_multiple_files=True
            )
            submit      = st.form_submit_button("發布文章")

        # 套用範本
        if tpl != "— 無 —" and submit:
            tmp = TEMPLATES[tpl]
            if not keywords:    keywords    = tmp["keywords"]
            if not description: description = tmp["description"]
            if not outline:     outline     = "\n".join(tmp["outline"])

        # 處理發布
        if submit:
            if not title or not content:
                st.sidebar.error("請填寫標題與內文")
            else:
                # 儲存圖片
                saved_imgs = []
                for idx, img in enumerate(images or [], start=1):
                    ext = os.path.splitext(img.name)[1]
                    fname = f"{slugify(title)}-{idx}{ext}"
                    fpath = os.path.join(IMAGE_DIR, fname)
                    with open(fpath, "wb") as f:
                        f.write(img.getbuffer())
                    saved_imgs.append(fname)

                # 建立 Markdown
                date_str = datetime.now().strftime("%Y-%m-%d")
                slug = slugify(title)
                md_filename = f"{date_str}-{slug}.md"
                md_path = os.path.join(CONTENT_DIR, md_filename)
                with open(md_path, "w", encoding="utf-8") as md:
                    md.write("---\n")
                    md.write(f"title: {title}\n")
                    md.write(f"date: {date_str}\n")
                    md.write(f"keywords: {keywords}\n")
                    md.write(f"description: {description}\n")
                    md.write("outline:\n")
                    for line in outline.split("\n"):
                        md.write(f"  - {line.strip()}\n")
                    md.write(f"images: {saved_imgs}\n")
                    md.write("---\n\n")
                    md.write(content)

                st.sidebar.success(f"🎉 文章已保存：{md_filename}")
                st.experimental_rerun()

    # ── 顯示／刪除文章 ──
    else:
        # 讀取文章內容
        path = os.path.join(CONTENT_DIR, choice)
        data = load_md(path)
        meta, body = data["meta"], data["body"]

        # 標題
        st.header(meta.get("title", ""))

         # Carousel 圖片顯示（點擊可放大）
        images = meta.get("images", [])
        if images:
            import base64
            html = "<div style='display:flex; gap:8px; overflow-x:auto; padding:8px 0;'>"
            for img in images:
                img_path = os.path.join(IMAGE_DIR, img)
                # 讀檔並轉 base64
                with open(img_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                data_uri = f"data:image/png;base64,{b64}"
                # 把 <img> 包在 <a> 裡，點擊就會在新分頁開啟原圖
                html += (
                    f"<a href='{data_uri}' target='_blank' style='flex-shrink:0;'>"
                    f"<img src='{data_uri}' "
                    "style='height:200px; width:auto; border-radius:8px; margin-right:8px;'/>"
                    "</a>"
                )
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

        # 文章內容套用 prose 樣式
        html_body = markdown.markdown(body)
        styled = f"""
        <div class="prose prose-lg mx-auto my-6">
          {html_body}
        </div>
        """
        st.markdown(styled, unsafe_allow_html=True)

        # 刪除按鈕
        if st.button("🗑️ 刪除文章"):
            os.remove(path)
            for img in images:
                ip = os.path.join(IMAGE_DIR, img)
                if os.path.exists(ip):
                    os.remove(ip)
            st.success("文章已刪除！請重新整理。")
            st.experimental_rerun()



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
