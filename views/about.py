## views/about.py
```python
import streamlit as st
from PIL import Image

def show():
    st.title("關於我")
    # 顯示上方 Logo
    logo = Image.open("assets/logo.png")
    st.image(logo, use_container_width=True)

    # 顯示個人照片與介紹
    cols = st.columns([1, 2])
    with cols[0]:
        photo = Image.open("assets/about_photo.png")  # 諮詢師個人照片檔名請對應
        st.image(photo, use_container_width=True)
    with cols[1]:
        st.markdown(
            """
            <div class='prose prose-lg'>
              <h3>諮詢師介紹：<strong>Tilandky</strong> (KIN 2 月亮白風•紅龍波)</h3>
              <ol>
                <li>星際馬雅13月亮曆 & 彩虹數字學 | 整合型諮詢師</li>
                <li>希塔療癒師暨原型卡・靈魂藍圖引導者</li>
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

    # 底部社群資訊
    st.markdown("---")
    st.markdown(
        "<div class='text-center'>"
        "<p>Tilandky的覺察日常</p>"
        "<p><a href='https://www.facebook.com/soulclean1413' target='_blank'>https://www.facebook.com/soulclean1413</a></p>"
        "</div>",
        unsafe_allow_html=True
    )
```python
import streamlit as st


def show():
    st.title("關於我")
    st.markdown(
        """
        **Tilandky**，資深療癒師，結合瑪雅曆法與 Theta Healing，
        陪伴你探索內在，轉化能量，活出真實自我。

        - 服務內容：個人諮詢、線上課程、工作坊
        - 專業認證：XXX、YYY
        """,
        unsafe_allow_html=True
    )
