## app.py
```python
import streamlit as st
from utils.loader import load_markdown
from utils.mailchimp import subscribe_email
from PIL import Image
import os

st.set_page_config(
    page_title="Tilandky的覺察日常",
    layout="wide",
)

# 注入 Tailwind CSS
st.markdown(
    "<link href='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css' rel='stylesheet'>",
    unsafe_allow_html=True
)

# 側邊欄導覽：只保留部落格、免費資源、關於我、聯絡我
st.sidebar.title("Tilandky的覺察日常")
page = st.sidebar.radio("導航", ["部落格", "免費資源", "關於我", "聯絡我"])

# 路由選擇
if page == "部落格":
    from views.blog import show as show_blog
    show_blog()
elif page == "免費資源":
    from views.resources import show as show_resources
    show_resources()
elif page == "關於我":
    # 優化版關於我頁
    st.markdown("<div class='text-center mb-4'>", unsafe_allow_html=True)
    # 縮小 Logo
    st.image("assets/logo.png", width=180)
    st.markdown("</div>", unsafe_allow_html=True)
    cols = st.columns([1, 3])
    with cols[0]:
        # 調整諮詢師照片尺寸
        st.image("assets/about_photo.png", width=240)
    with cols[1]:
        st.markdown(
            """
            <div class='prose prose-lg'>
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
            </div>
            """,
            unsafe_allow_html=True
        )
    # 底部社群連結
    st.markdown("---")
    st.markdown(
        "<div class='text-center mt-4'>"
        "<p><strong>Tilandky的覺察日常</strong></p>"
        "<p><a href='https://www.facebook.com/soulclean1413' target='_blank'>facebook.com/soulclean1413</a></p>"
        "</div>",
        unsafe_allow_html=True
    )elif page == "聯絡我":
    from views.contact import show as show_contact
    show_contact()
