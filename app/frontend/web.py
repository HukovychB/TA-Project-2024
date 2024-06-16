import streamlit as st

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

st.image("app/frontend/ies.png", width=100)

st.markdown("<h1 style='text-align: center;'>TECHNICAL ANALYSIS TEST AREA</h1>", unsafe_allow_html=True)

st.write("")
st.write("")

ticker_input = st.text_input("Enter the ticker (e.g., AAPL, MSFT):")
#m.ticker_input = ticker_input




