import streamlit as st
from PIL import Image

def show():
    st.title("歡迎來到 Tilandky的覺察日常")

    # Logo 與服務簡介
    cols = st.columns([1, 2])
    with cols[0]:
        logo = Image.open("assets/logo.png")
        st.image(logo, caption="Tilandky 馬雅之鏡", use_container_width=True)
    with cols[1]:
        services = Image.open("assets/services.png")
        st.image(services, use_container_width=True)

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
            <svg class='w-6 h-6' fill='currentColor' viewBox='0 0 24 24'>
              <path d='M22 12a10 10 0 10-11.5 9.87v-6.99h-2.1v-2.88h2.1V9.77c0-2.08 1.24-3.23 3.14-3.23.91 0 1.86.16 1.86.16v2.05h-1.05c-1.04 0-1.36.65-1.36 1.32v1.58h2.31l-.37 2.88h-1.94V21.9A10 10 0 0022 12z' />
            </svg>
            <span>Facebook</span>
          </a>
          <a href='https://www.instagram.com/tilandky/' target='_blank' class='flex items-center space-x-2 hover:text-pink-500'>
            <svg class='w-6 h-6' fill='currentColor' viewBox='0 0 24 24'>
              <path d='M7.75 2h8.5A5.75 5.75 0 0122 7.75v8.5A5.75 5.75 0 0116.25 22h-8.5A5.75 5.75 0 012 16.25v-8.5A5.75 5.75 0 017.75 2zm0 1.5A4.25 4.25 0 003.5 7.75v8.5A4.25 4.25 0 007.75 20.5h8.5a4.25 4.25 0 004.25-4.25v-8.5A4.25 4.25 0 0016.25 3.5h-8.5z'/>
              <circle cx='12' cy='12' r='3.5'/>
              <path d='M17.5 6.5a.5.5 0 11-1 0 .5.5 0 011 0z'/>
            </svg>
            <span>Instagram</span>
          </a>
        </div>
        """,
        unsafe_allow_html=True
    )
