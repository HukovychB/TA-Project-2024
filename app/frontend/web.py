import streamlit as st
from streamlit_lottie import st_lottie
import json

st.set_page_config(page_title="TA App",
                page_icon=":chart_with_upwards_trend:",
                layout="wide"
)

#import sys
#sys.path.append("C:/Files/study/semestr6/TA project")
#from app.backend import main as m

#Colors
#Background: #3f3b3b
#Text: #f2e1e1
#Other elements: #FF5500
#Font: Serif

#BEGINNING

#Hide 'Deploy' and 'Span' buttons
# st.markdown("""
# <style>
# .st-emotion-cache-w9v1j9.ef3psqc5
# {
#     visibility: hidden;            
# }
# .st-emotion-cache-czk5ss.e16jpq800
# {
#     visibility: hidden;            
# }
# </style>
# """, unsafe_allow_html=True)

st.image("app/frontend/ies.png", width=100)

st.markdown("<h1 style='text-align: center;'>TECHNICAL ANALYSIS TEST AREA</h1>", unsafe_allow_html=True)

st.markdown("---")

with open("app/frontend/Animation.json") as source:
    animation = json.load(source)

col1, col2 = st.columns([2, 1])
with col1:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    ticker_input = st.text_input("Enter the ticker (e.g. AAPL, MSFT):", max_chars=10,)
with col2:
    st_lottie(animation, height = 400, width = 400)

if ticker_input:
    print(ticker_input)




