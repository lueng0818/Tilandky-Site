import streamlit as st
import os
import re
from datetime import datetime
from PIL import Image
import markdown
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from dotenv import load_dotenv

# 讀取 .env
load_dotenv()

# Mailchimp 設定
MC_API_KEY = os.getenv("MAILCHIMP_API_KEY")
MC_SERVER = os.getenv("MAILCHIMP_SERVER_PREFIX")
MC_LIST_ID = os.getenv("MAILCHIMP_LIST_ID")
mc_client = Client()
mc_client.set_config({"api_key": MC_API_KEY, "server": MC_SERVER})

# SMTP 設定
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# 資料夾
CONTENT_DIR = "content/blog_posts"
FREEBIE_PATH = "content/freebies/guide.pdf"
IMAGE_DIR = "assets/blog_images"
os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# 載入 Markdown
def load_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return markdown.markdown(text)

# 訂閱 Mailchimp
def subscribe_email(email):
    try:
        mc_client.lists.add_list_member(MC_LIST_ID, {"email_address": email, "status": "subscribed"})
        return True
    except ApiClientError:
        return False

# 寄送通知信
def send_email(to_address, subject, body):
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = SMTP_USER
        msg["To"] = to_address
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [to_address], msg.as_string())
        return True
    except Exception:
        return False

# 文字 slug 化
def slugify(text):
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s-]+", "-", s).strip("-")
    return s

# Streamlit 設定
st.set_page_config(page_title="Tilandky的覺察日常", layout="wide")

# 注入 Tailwind
st.markdown(
    "<link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css' rel='stylesheet'>",
    unsafe_allow_html=True
)

# 隱藏自動 Pages
hide_css = """
<style>
[data-testid="stSidebarNav"] > div:nth-child(2) { display: none !important; }
</style>
"""
st.markdown(hide_css, unsafe_allow_html=True)

# 側邊欄導航
st.sidebar.title("Tilandky的覺察日常")
page = st.sidebar.radio("導航", ["部落格", "免費資源", "關於我", "聯絡我"])

# ===== 部落格頁 =====
if page == "部落格":
    st.sidebar.header("撰寫新文章")
    with st.sidebar.form("new_post"):
        title = st.text_input("標題")
        content = st.text_area("內文")
        img = st.file_uploader("封面圖片", type=["png", "jpg", "jpeg"])
        if st.form_submit_button("發布"):
            fn = slugify(title)
            date = datetime.now().strftime("%Y-%m-%d")
            # 存圖
            img_name = None
            if img:
                ext = os.path.splitext(img.name)[1]
                img_name = f"{fn}{ext}"
                with open(os.path.join(IMAGE_DIR, img_name), "wb") as f:
                    f.write(img.getbuffer())
            # 寫 md
            md_file = f"{date}-{fn}.md"
            with open(os.path.join(CONTENT_DIR, md_file), "w", encoding="utf-8") as f:
                f.write(f"---\ntitle: {title}\ndate: {date}\n")
                if img_name: f.write(f"image: ../assets/blog_images/{img_name}\n")
                f.write("---\n\n" + content)
            st.sidebar.success("文章已發布！重新整理列表。")
    st.title("日常探索部落格")
    posts = sorted([f for f in os.listdir(CONTENT_DIR) if f.endswith(".md")], reverse=True)
    sel = st.selectbox("選文章", posts)
    if sel:
        st.markdown(load_markdown(os.path.join(CONTENT_DIR, sel)), unsafe_allow_html=True)

# ===== 免費資源頁 =====
elif page == "免費資源":
    st.title("免費資源")
    st.markdown("下載我的免費手冊：")
    email = st.text_input("Email 用於下載")
    if st.button("訂閱＆下載"):
        if subscribe_email(email):
            with open(FREEBIE_PATH, "rb") as f:
                st.download_button("下載 PDF", f, file_name="guide.pdf")
        else:
            st.error("訂閱失敗")
    st.markdown("---")
    st.markdown("### 延伸資源")
    st.markdown(
        "<ul class='list-disc list-inside'>"
        "<li><a href='https://maya-self-explore.streamlit.app/' target='_blank'>自我探索</a></li>"
        "<li><a href='https://maya-wealth.streamlit.app/' target='_blank'>金錢能量頻率</a></li>"
        "<li><a href='https://maya-emotion.streamlit.app/' target='_blank'>情感關係解讀</a></li>"
        "</ul>",
        unsafe_allow_html=True,
    )

# ===== 關於我頁 =====
elif page == "關於我":
    st.title("關於我")
    st.markdown(
        "**Tilandky**，資深療癒師，結合瑪雅曆法與 Theta Healing，陪伴你探索內在，活出真我。"
    )

# ===== 聯絡我頁 =====
elif page == "聯絡我":
    st.title("聯絡我")
    st.markdown("Line@：[加入點我](https://line.me/R/ti/p/%40690ZLAGN)")
    name = st.text_input("姓名")
    email = st.text_input("Email")
    msg = st.text_area("訊息")
    if st.button("送出"):
        subject = f"新訊息 - {name}"
        body = f"姓名：{name}\nEmail：{email}\n\n{msg}"
        if send_email("lueng1314@gmail.com", subject, body):
            st.success("已寄送通知信！")
        else:
            st.error("寄信失敗，請直接寫信至 lueng1314@gmail.com")
