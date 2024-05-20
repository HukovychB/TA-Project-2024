import streamlit as st

#Colors
#Background: #3f3b3b
#Text: #f2e1e1
#Other elements: #FF5500
#Font: Serif

st.set_page_config(layout="wide")

st.image("app/frontend/ies.png", width=100)

st.markdown("<h1 style='text-align: center;'>TECHNICAL ANALYSIS TEST AREA</h1>", unsafe_allow_html=True)

st.write("")
st.write("")

ticker_input = st.text_input("Enter the ticker (e.g., AAPL, MSFT):")




