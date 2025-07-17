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

# 將專案根目錄加入模組搜尋路徑（保險）
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# 載入環境變數
load_dotenv()

# —— Mailchimp 設定 —— #
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

# —— SMTP 寄信設定 —— #
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT   = int(os.getenv("SMTP_PORT", 587))
SMTP_USER   = os.getenv("SMTP_USER")
SMTP_PASS   = os.getenv("SMTP_PASSWORD")

def send_email(to_address: str, subject: str, body: str) -> bool:
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"] = SMTP_USER
        msg["To"] = to_address
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_USER, [to_address], msg.as_string())
        return True
    except Exception:
        return False

# —— 目錄設定 —— #
CONTENT_DIR = "content/blog_posts"
IMAGE_DIR   = "assets/blog_images"
FREEBIE     = "content/freebies/guide.pdf"
os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# —— SEO 範本 —— #
TEMPLATES = {
    "星際馬雅曆解析": {
        "keywords": "星際馬雅曆,銀河印記,馬雅圖騰,13月亮曆法,KIN 解析,靈魂藍圖",
        "description": "探究星際馬雅曆起源、結構與圖騰意義，並教你查詢 KIN、理解銀河音頻機制。",
        "outline": [
            "星際馬雅曆的由來與基礎結構",
            "如何查詢自己的 KIN",
            "每個圖騰與顏色的意義",
            "銀河音頻的運作方式",
            "馬雅曆引導靈魂方向示例",
        ],
    },
    "希塔療癒完整指南": {
        "keywords": "希塔療癒,ThetaHealing 教學,潛意識轉化,靈性療法,希塔腦波,能量療癒技巧",
        "description": "深入說明 ThetaHealing 原理、步驟與應用，並提供成為療癒師的完整路徑。",
        "outline": [
            "什麼是希塔療癒？與其他療法的不同",
            "腦波與潛意識如何連結",
            "希塔療癒步驟與實作流程",
            "常見應用：金錢、人際、靈魂目的",
            "如何成為希塔療癒師",
        ],
    },
    "十大身心靈整合服務推薦": {
        "keywords": "身心靈整合,靈性療癒服務,冥想與能量療癒,整合療法,療癒工作坊,靈性成長課程",
        "description": "列出十大身心靈療癒服務，教你選擇合適療法與辨別優質療癒師。",
        "outline": [
            "什麼是身心靈整合？",
            "十大療癒服務（EFT、希塔、阿卡西、水晶、脈輪）",
            "選擇適合療癒方式的技巧",
            "如何分辨合格療癒師",
            "個案成功案例分享",
        ],
    },
}

def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    return re.sub(r"[\s-]+", "-", s).strip("-")

def parse_frontmatter(path: str) -> dict:
    meta = {"title":"","date":"","keywords":"","description":"","outline":[], "images":[]}
    lines = open(path, encoding="utf-8").read().splitlines()
    in_meta = False
    for line in lines:
        if line.strip()=="---":
            in_meta = not in_meta
            continue
        if in_meta and ":" in line:
            k,v = line.split(":",1)
            k,v = k.strip(), v.strip()
            if k in ["title","date","keywords","description"]:
                meta[k]=v
            elif k=="images":
                try: meta["images"]=eval(v)
                except: meta["images"]=[]
            elif k=="outline":
                # 後續幾行為 - 列表
                pass
        if in_meta and line.strip().startswith("-"):
            meta["outline"].append(line.strip("- ").strip())
    return meta

# —— 產生 sitemap/robots —— #
def generate_sitemap():
    base = os.getenv("BASE_URL","https://your-domain.com")
    urls = []
    for fn in os.listdir(CONTENT_DIR):
        if fn.endswith(".md"):
            slug = fn.replace(".md","")
            urls.append(f"{base}/blog/{slug}")
    with open("sitemap.xml","w",encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"  <url><loc>{u}</loc></url>\n")
        f.write("</urlset>")
    with open("robots.txt","w",encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n")
generate_sitemap()

# —— Streamlit 設定 —— #
st.set_page_config(page_title="Tilandky的覺察日常", layout="wide")

# 注入 Tailwind CSS
st.markdown("<link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css' rel='stylesheet'>", unsafe_allow_html=True)

# 隱藏自動 Pages
st.markdown("""
<style>
[data-testid="stSidebarNav"] > div:nth-child(2){display:none!important;}
</style>
""", unsafe_allow_html=True)

# 側邊欄 & 選單
st.sidebar.title("Tilandky的覺察日常")
page = st.sidebar.radio("導航", ["首頁","部落格","免費資源","關於我","聯絡我"])

# ===== 首頁 =====
if page == "首頁":
    st.image("assets/banner.jpg", use_container_width=True)
    st.markdown("""
    <div class="prose lg:prose-xl mx-auto my-8">
      <h1>歡迎來到 Tilandky的覺察日常</h1>
      <p>陪你探索內在、轉化能量，活出真實自我。</p>
      <ul>
        <li>星際馬雅曆解析</li>
        <li>ThetaHealing 希塔療癒</li>
        <li>身心靈整合服務</li>
      </ul>
    </div>
    """, unsafe_allow_html=True)

# ===== 部落格 =====
elif page == "部落格":
    st.title("日常探索部落格")
    # 範本選擇
    st.sidebar.header("載入 SEO 範本")
    tpl_name = st.sidebar.selectbox("範本", ["— 無 —"]+list(TEMPLATES.keys()))
    # 撰寫表單
    st.sidebar.header("撰寫/編輯文章")
    choice = st.sidebar.selectbox("選擇文章", ["── 新增文章 ──"] + sorted(os.listdir(CONTENT_DIR), reverse=True))
    if choice == "── 新增文章 ──":
        with st.sidebar.form("form_new"):
            title = st.text_input("標題")
            keywords = st.text_input("關鍵字（逗號分隔）")
            description = st.text_area("摘要 / 描述", height=60)
            outline = st.text_area("章節大綱（每行一項）", height=100)
            content = st.text_area("內文")
            images = st.file_uploader("上傳圖片 (多選)", accept_multiple_files=True)
            submit = st.form_submit_button("發布文章")
        # 套用範本
        if tpl_name!="— 無 —":
            tpl = TEMPLATES[tpl_name]
            if not keywords:    keywords    = tpl["keywords"]
            if not description: description = tpl["description"]
            if not outline:     outline     = "\n".join(tpl["outline"])
        # 處理發布
        if submit and title and content:
            date_str = datetime.now().strftime("%Y-%m-%d")
            slug = slugify(title)
            imgs=[]
            for i, img in enumerate(images,1):
                ext = os.path.splitext(img.name)[1]
                fn  = f"{slug}-{i}{ext}"
                with open(os.path.join(IMAGE_DIR,fn),"wb") as f: f.write(img.getbuffer())
                imgs.append(fn)
            mdn = f"{date_str}-{slug}.md"
            with open(os.path.join(CONTENT_DIR,mdn),"w",encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"title: {title}\n")
                f.write(f"date: {date_str}\n")
                f.write(f"keywords: {keywords}\n")
                f.write(f"description: {description}\n")
                f.write("outline:\n")
                for ln in outline.split("\n"): f.write(f"  - {ln.strip()}\n")
                f.write(f"images: {imgs}\n")
                f.write("---\n\n")
                f.write(content)
            st.sidebar.success("文章已發布！")

    else:
        # 讀取 frontmatter
        path = os.path.join(CONTENT_DIR, choice)
        meta = parse_frontmatter(path)
        body = "\n".join(open(path,encoding="utf-8").read().split("---")[2:]).strip()
        # 顯示
        st.header(meta["title"])
        for img in meta["images"]:
            ip = os.path.join(IMAGE_DIR,img)
            if os.path.exists(ip): st.image(ip, use_container_width=True)
        st.markdown(markdown.markdown(body), unsafe_allow_html=True)

    # SEO 分析
    st.sidebar.markdown("---")
    st.sidebar.subheader("SEO 分析")
    st.sidebar.write(f"標題長度：{len(title) if 'title' in locals() else 0} 字")
    kwc = len([k for k in (keywords if 'keywords' in locals() else "").split(",") if k.strip()])
    st.sidebar.write(f"關鍵字數：{kwc} 個")
    st.sidebar.write(f"摘要長度：{len(description) if 'description' in locals() else 0} 字")

# ===== 免費資源 =====
elif page == "免費資源":
    st.title("免費資源")
    email = st.text_input("Email 用於下載")
    if st.button("訂閱並下載 PDF"):
        if subscribe_email(email):
            with open(FREEBIE,"rb") as f:
                st.download_button("點此下載 PDF",f,file_name="guide.pdf")
        else:
            st.error("訂閱失敗")
    st.markdown("---")
    st.markdown("""
    <ul class="list-disc list-inside">
      <li><a href="https://maya-self-explore.streamlit.app/" target="_blank">自我探索</a></li>
      <li><a href="https://maya-wealth.streamlit.app/" target="_blank">金錢能量頻率</a></li>
      <li><a href="https://maya-emotion.streamlit.app/" target="_blank">情感關係解讀</a></li>
    </ul>
    """, unsafe_allow_html=True)

# ===== 關於我 =====
elif page == "關於我":
    st.image("assets/logo.png", use_container_width=True)
    cols = st.columns([1,2])
    with cols[0]:
        st.image("assets/about_photo.png", use_container_width=True)
    with cols[1]:
        st.markdown("""
        <h3>諮詢師介紹：<strong>Tilandky</strong> (KIN 2 月亮白風·紅龍波)</h3>
        <ol>
          <li>星際馬雅13月亮曆 & 彩虹數字學 | 整合型諮詢師</li>
          <li>希塔療癒師暨原型卡‧靈魂藍圖引導者</li>
          <li>擅長伴侶合盤解讀與信念轉化對話</li>
          <li>曾任軍職資訊教官，具 ISO 27001/27701 顧問背景</li>
          <li>已服務超過 300 位個案、推廣四梯馬雅課程</li>
          <li>結合邏輯與感知，陪你理解愛，走向信任與共識</li>
        </ol>
        <p>🌿 <em>Tilandky 的陪伴風格：溫柔覺察 × 結構清晰 × 信仰友善</em></p>
        <hr>
        <p class="text-center">Tilandky的覺察日常<br><a href="https://www.facebook.com/soulclean1413" target="_blank">facebook.com/soulclean1413</a></p>
        """, unsafe_allow_html=True)

# ===== 聯絡我 =====
elif page == "聯絡我":
    st.title("聯絡我")
    st.markdown("Line@：[加入點我](https://line.me/R/ti/p/%40690ZLAGN)")
    name = st.text_input("姓名")
    email = st.text_input("Email")
    msg   = st.text_area("訊息")
    if st.button("送出"):
        subject = f"新訊息：{name}"
        body    = f"姓名：{name}\nEmail：{email}\n\n{msg}"
        if send_email("lueng1314@gmail.com", subject, body):
            st.success("已寄送通知信！")
        else:
            st.error("寄信失敗，請直接寫信至 lueng1314@gmail.com")
