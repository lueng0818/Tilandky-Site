## views/about.py
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
