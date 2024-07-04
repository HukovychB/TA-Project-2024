import streamlit as st

with open('frontend/info_style.css') as f:
     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# BEGINNING

col1, col2, col3 = st.columns([1, 4, 1])
#IES logo
col1.image('frontend/ies.png', width=100)
#Header
st.markdown("<h1 style='text-align: center;'>WELCOME TO OUR TECHNICAL ANALYSIS PROJECT</h1>", unsafe_allow_html=True)