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

# ── 讀取環境變數 ──
load_dotenv()
MC = Client()
MC.set_config({
    "api_key": os.getenv("MAILCHIMP_API_KEY"),
    "server": os.getenv("MAILCHIMP_SERVER_PREFIX")
})
MC_LIST_ID = os.getenv("MAILCHIMP_LIST_ID")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT   = int(os.getenv("SMTP_PORT", 587))
SMTP_USER   = os.getenv("SMTP_USER")
SMTP_PASS   = os.getenv("SMTP_PASSWORD")

# ── 資料夾設定 ──
CONTENT_DIR = "content/blog_posts"
IMAGE_DIR   = "assets/blog_images"
FREEBIE     = "content/freebies/guide.pdf"
os.makedirs(CONTENT_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)

# ── 函式定義 ──
def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    return re.sub(r"[\s-]+", "-", s).strip("-")

def load_md(path: str) -> dict:
    lines = open(path, encoding="utf-8").read().splitlines()
    meta, body = {}, []
    in_meta = False
    for l in lines:
        if l.strip()=="---":
            in_meta = not in_meta
            continue
        if in_meta and ":" in l:
            k,v = l.split(":",1)
            meta[k.strip()] = v.strip()
        elif not in_meta:
            body.append(l)
    # 處理 images 與 outline
    meta["images"]   = eval(meta.get("images","[]"))
    meta["outline"]  = eval(meta.get("outline","[]"))
    return {"meta":meta, "body":"\n".join(body)}

def subscribe_email(email: str) -> bool:
    try:
        MC.lists.add_list_member(MC_LIST_ID, {"email_address": email, "status":"subscribed"})
        return True
    except ApiClientError:
        return False

def send_email(to_addr: str, subject: str, body: str) -> bool:
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["From"]    = SMTP_USER
        msg["To"]      = to_addr
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.sendmail(SMTP_USER, [to_addr], msg.as_string())
        return True
    except:
        return False

# ── SEO 範本 ──
TEMPLATES = {
    "星際馬雅曆解析": {
        "keywords":"星際馬雅曆,銀河印記,馬雅圖騰,13月亮曆法,KIN解析,靈魂藍圖",
        "description":"探究星際馬雅曆起源、結構與圖騰意義，教你查詢KIN與銀河音頻機制。",
        "outline":[
            "馬雅曆由來與結構",
            "如何查詢 KIN",
            "圖騰與顏色意義",
            "銀河音頻運作",
            "馬雅曆引導案例"
        ],
    },
    "希塔療癒完整指南": {
        "keywords":"希塔療癒,ThetaHealing,潛意識轉化,靈性療法,希塔腦波,能量療癒",
        "description":"深入說明ThetaHealing原理、步驟與應用，並提供療癒師養成路徑。",
        "outline":[
            "什麼是希塔療癒",
            "腦波與潛意識關係",
            "實作流程",
            "常見應用案例",
            "成為療癒師方法"
        ],
    },
    "十大身心靈整合服務": {
        "keywords":"身心靈整合,靈性療癒,冥想,能量療癒,整合療法,療癒工作坊",
        "description":"介紹十大身心靈療癒服務，教你挑選與辨別優質療癒師。",
        "outline":[
            "身心靈整合定義",
            "十大療癒服務介紹",
            "挑選療法技巧",
            "辨別優質療癒師",
            "個案分享"
        ],
    },
}

# ── 產生 Sitemap & Robots ──
def gen_sitemap():
    base = os.getenv("BASE_URL","https://your-domain.com")
    urls = []
    for fn in os.listdir(CONTENT_DIR):
        if fn.endswith(".md"):
            slug = fn.replace(".md","")
            urls.append(f"{base}/blog/{slug}")
    with open("sitemap.xml","w",encoding="utf-8") as f:
        f.write('<?xml version="1.0"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f"  <url><loc>{u}</loc></url>\n")
        f.write("</urlset>")
    with open("robots.txt","w",encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: /sitemap.xml\n")

gen_sitemap()

# ── Streamlit 設定 ──
st.set_page_config(page_title="Tilandky的覺察日常", layout="wide")
st.markdown("<link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css' rel='stylesheet'>", unsafe_allow_html=True)
st.markdown("<style>[data-testid='stSidebarNav'] > div:nth-child(2){display:none!important;}</style>", unsafe_allow_html=True)

# 側邊欄導航
st.sidebar.title("Tilandky的覺察日常")
page = st.sidebar.radio("導航", ["首頁","部落格","免費資源","關於我","聯絡我"])

# ===== 首頁 =====
if page=="首頁":
    st.image("assets/banner.jpg", use_container_width=True)
    st.markdown("""
    <div class="prose lg:prose-xl mx-auto my-8">
      <h1>歡迎來到 Tilandky的覺察日常</h1>
      <p>陪你探索內在、轉化能量，活出真實自我。</p>
    </div>
    """, unsafe_allow_html=True)

# ===== 部落格 =====
elif page=="部落格":
    st.title("日常探索部落格")
    # 範本選擇
    tpl = st.sidebar.selectbox("載入 SEO 範本", ["— 無 —"]+list(TEMPLATES.keys()))
    # 文章表單
    choice = st.sidebar.selectbox("文章列表", ["── 新增文章 ──"]+sorted(os.listdir(CONTENT_DIR), reverse=True))
    if choice=="── 新增文章 ──":
        with st.sidebar.form("new"):
            title       = st.text_input("標題")
            keywords    = st.text_input("關鍵字")
            description = st.text_area("摘要",height=60)
            outline     = st.text_area("大綱(每行一項)",height=100)
            content     = st.text_area("內文")
            imgs        = st.file_uploader("圖片(多選)", accept_multiple_files=True)
            submit      = st.form_submit_button("發布")
        if tpl!="— 無 —":
            tmp = TEMPLATES[tpl]
            if not keywords:    keywords    = tmp["keywords"]
            if not description: description = tmp["description"]
            if not outline:     outline     = "\n".join(tmp["outline"])
        if submit and title:
            dstr = datetime.now().strftime("%Y-%m-%d")
            slug = slugify(title)
            saved=[]
            for i,im in enumerate(imgs,1):
                ext = os.path.splitext(im.name)[1]
                fn  = f"{slug}-{i}{ext}"
                with open(os.path.join(IMAGE_DIR,fn),"wb") as f: f.write(im.getbuffer())
                saved.append(fn)
            mdn = f"{dstr}-{slug}.md"
            with open(os.path.join(CONTENT_DIR,mdn),"w",encoding="utf-8") as f:
                f.write("---\n")
                f.write(f"title: {title}\n")
                f.write(f"date: {dstr}\n")
                f.write(f"keywords: {keywords}\n")
                f.write(f"description: {description}\n")
                f.write(f"outline: {saved}\n")  # 保存大綱
                f.write(f"images: {saved}\n")
                f.write("---\n\n"+content)
            st.sidebar.success("已發布")
    else:
        data = load_md(os.path.join(CONTENT_DIR,choice))
        meta, body = data["meta"],data["body"]
        st.header(meta["title"])
        for img in meta["images"]:
            ip = os.path.join(IMAGE_DIR,img)
            if os.path.exists(ip): st.image(ip,use_container_width=True)
        st.markdown(markdown.markdown(body),unsafe_allow_html=True)

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
