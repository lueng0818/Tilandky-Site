import streamlit as st
from PIL import Image

def show():
    st.title("歡迎來到 Tilandky 日常探索")

    # Banner
    banner = Image.open("assets/banner.jpg")
    st.image(banner, use_column_width=True)

    # Logo 與服務簡介
    cols = st.columns([1, 2])
    with cols[0]:
        logo = Image.open("assets/logo.png")
        st.image(logo, caption="Tilandky 馬雅之鏡", use_column_width=True)
    with cols[1]:
        services = Image.open("assets/services.png")
        st.image(services, use_column_width=True)

    # 文字介紹
    st.markdown(
        """
        <div class='prose prose-lg mx-auto my-8'>
          <p>這裡是 <strong>Tilandky 的覺察日常</strong>。<br>
          陪你一起練習在關係裡，不再把自己藏起來；<br>
          在創業路上不再懷疑自己的價值。<br>
          我相信每個人都有自己的節奏與方式，<br>
          你不是不夠好，也不是走太慢，<br>
          只是需要被自己好好看見。<br><br>
          你不需要一次改變所有事情，<br>
          只要願意從現在的你開始。</p>
          <p>#Tilandky的覺察日常  #關係裡的自己也重要  #慢慢靠近自己  #相信才會看見</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 社群連結
    st.markdown(
        """
        <div class='flex justify-center space-x-6 mt-8'>
          <a href='https://www.facebook.com/soulclean1413/' target='_blank' class='flex items-center space-x-2 hover:text-blue-600'>
            <!-- Facebook SVG Icon -->
            <svg class='w-6 h-6' fill='currentColor' viewBox='0 0 24 24'><path d='M22 12...'/></svg>
            <span>Facebook</span>
          </a>
          <a href='https://www.instagram.com/tilandky/' target='_blank' class='flex items-center space-x-2 hover:text-pink-500'>
            <!-- Instagram SVG Icon -->
            <svg class='w-6 h-6' fill='currentColor' viewBox='0 0 24 24'><path d='M7.75 2...'/></svg>
            <span>Instagram</span>
          </a>
        </div>
        """,
        unsafe_allow_html=True
    )
