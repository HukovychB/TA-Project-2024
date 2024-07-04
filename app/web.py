import streamlit as st
import os
from datetime import datetime
from streamlit_lottie import st_lottie
import json
from streamlit_option_menu import option_menu
import pandas as pd

from libraries import main


def data_table(header, keys):
    data = []
    for key in keys:
        # Capitalize the first letter of the key, while preserving other capitalization
        formatted_key = key[:1].upper() + key[1:]
        value = stock_info.get(key, '-')
        # Handle Unix epoch timestamps
        if key in date_keys:
            try:
                date_value = datetime.utcfromtimestamp(value).strftime('%Y-%m-%d')
                data.append([formatted_key, date_value])
            except ValueError:
                data.append([formatted_key, value])
        else:
            data.append([formatted_key, value])
    
    table_markdown = "<table>"
    for row in data:
        table_markdown += f"<tr><td><strong>{row[0]}</strong></td><td>{row[1]}</td></tr>"
    table_markdown += "</table>"
    st.markdown(f"### {header}")
    st.markdown(table_markdown, unsafe_allow_html=True)

st.set_page_config(page_title="TA App",
                page_icon=":chart_with_upwards_trend:",
                layout="wide",
                initial_sidebar_state="collapsed" 
)

#Colors
#Background: #3f3b3b
#Text: #f2e1e1
#Other elements: #FF5500
#Font: serif

#STYLES
with open('frontend/main_style.css') as f:
     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


#BEGINNING


col1, col2, col3 = st.columns([1, 4, 1])
#IES logo
col1.image('frontend/ies.png', width=100)

col3.page_link("pages/info_page.py", label = "About the project")

#Header
st.markdown("<h1 style='text-align: center;'>TECHNICAL ANALYSIS TEST AREA</h1>", unsafe_allow_html=True)
st.write("")
st.write("")
#Animation
with open("frontend/Animation.json") as source:
        animation = json.load(source)

col1, col2 = st.columns([2, 1])
with col1:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    #USER FORM
    ticker_input = st.text_input("Enter the ticker (e.g. AAPL, MSFT):", max_chars=10,)
    period = st.selectbox("Choose time interval:", ["","1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"])
    s_btn = st.button("SEARCH")
    if s_btn:
        st.session_state.ticker_input = ticker_input
        st.session_state.period = period
        st.session_state.s_btn = True    
with col2:
    st_lottie(animation, height = 400, width = 400)
if st.session_state.get('s_btn', False) and st.session_state.get('ticker_input') and st.session_state.get('period'):
    with st.spinner("SEARCHING"):
        ticker_data = main.fetch_data(ticker_input)
        main.create_graph(ticker_data, period)
    selected = option_menu(
            menu_title=None,
            options = ["INFO", "TECHNICAL ANALYSIS"],
            orientation="horizontal",
            icons = ['info-circle','bar-chart-steps'],
            styles={
                "container": {
                    "padding": "0!important",  
                    "background-color": "#3f3b3b",  
                },
                "nav-link": {
                    "font-size": "24px",  
                    "text-align": "center", 
                    "margin": "0px",  
                    "color": "#f2e1e1",  
                    "font-family": "serif", 
                    "padding": "10px 20px", 
                    "--hover-color": "#FF5500",
                },
                "nav-link-selected": {
                    "background-color": "#FF5500",  
                    "color": "white",  
                },
                "icon": {
                    "color": "#f2e1e1", 
                    "font-size": "20px"
                },
            }   
    )
    if selected == "INFO":
        st.markdown("""
        <style>
            .custom-table {
                border-spacing: 0;
                border-collapse: collapse;
                width: 100%;
            }
            .custom-table th, .custom-table td {
                border: 1px solid #ddd;
                padding: 8px;
                color: #333;
            }
            .custom-table th {
                padding-top: 12px;
                padding-bottom: 12px;
                text-align: left;
                background-color: #4CAF50;
                color: white;
            }
            .custom-table tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .custom-table tr:hover {
                background-color: #ddd;
            }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        #STOCK INFO
        country = ticker_data.info.get('country', 'N/A')
        sector = ticker_data.info.get('sector', 'N/A')
        industry = ticker_data.info.get('industry', 'N/A')
        market_cap = ticker_data.info.get('marketCap', 'N/A')
        ent_value = ticker_data.info.get('enterpriseValue', 'N/A')
        employees = ticker_data.info.get('fullTimeEmployees', 'N/A')

        stock_info = [
            ("Stock Info", "Value"),
            ("Country", country),
            ("Sector", sector),
            ("Industry", industry),
            ("Market Cap", main.format_value(market_cap)),
            ("Enterprise Value", main.format_value(ent_value)),
            ("Employees", employees)
        ]
                
        with col1:
            st.markdown(main.html_table(stock_info), unsafe_allow_html=True)
                
        #PRICE INFO
        current_price = ticker_data.info.get('currentPrice', 'N/A')
        prev_close = ticker_data.info.get('previousClose', 'N/A')
        day_high = ticker_data.info.get('dayHigh', 'N/A')
        day_low = ticker_data.info.get('dayLow', 'N/A')
        ft_week_high = ticker_data.info.get('fiftyTwoWeekHigh', 'N/A')
        ft_week_low = ticker_data.info.get('fiftyTwoWeekLow', 'N/A')
                
        price_info = [
            ("Price Info", "Value"),
            ("Current Price", f"${current_price:.2f}"),
            ("Previous Close", f"${prev_close:.2f}"),
            ("Day High", f"${day_high:.2f}"),
            ("Day Low", f"${day_low:.2f}"),
            ("52 Week High", f"${ft_week_high:.2f}"),
            ("52 Week Low", f"${ft_week_low:.2f}")
        ]
                
        with col2:
            st.markdown(main.html_table(price_info), unsafe_allow_html=True)

        #BUSINESS METRICS
        forward_eps = ticker_data.info.get('forwardEps', 'N/A')
        forward_pe = ticker_data.info.get('forwardPE', 'N/A')
        peg_ratio = ticker_data.info.get('pegRatio', 'N/A')
        dividend_rate = ticker_data.info.get('dividendRate', 'N/A')
        dividend_yield = ticker_data.info.get('dividendYield', 'N/A')
        recommendation = ticker_data.info.get('recommendationKey', 'N/A')
                
        biz_metrics = [
            ("Business Metrics", "Value"),
            ("EPS (FWD)", f"{forward_eps:.2f}"),
            ("P/E (FWD)", f"{forward_pe:.2f}"),
            ("PEG Ratio", f"{peg_ratio:.2f}"),
            ("Div Rate (FWD)", f"${dividend_rate:.2f}"),
            ("Div Yield (FWD)", f"{dividend_yield * 100:.2f}%"),
            ("Recommendation", recommendation.capitalize())
        ]
                
        with col3:
            st.markdown(main.html_table(biz_metrics), unsafe_allow_html=True)
    if selected == "TECHNICAL ANALYSIS":
        st.write("ANALYSIS")

elif s_btn:
    st.error("Please enter the ticker and choose time interval.", icon="❗")



# #INFO
# # Keys to disregard for companyOfficers
# keys_to_disregard = ['maxAge', 'exercisedValue', 'unexercisedValue']

# if ticker_input:
#     try:
#         # Fetch financial data
#         ticker = yf.Ticker(ticker_input)
#         # Get stock info
#         stock_info = ticker.info
#         # Get historical market data
#         hist = ticker.history(period="1y")
#         # Modify the 'Date' index to display only the date and not the time
#         hist.index = hist.index.date
#         # Reverse the order of rows so the newest date are at the top
#         hist = hist.iloc[::-1]

#         # List of keys to exclude from display
#         keys_to_exclude = ['industryKey', 'industryDisp', 'sectorKey', 'sectorDisp', 
#                            'compensationAsOfEpochDate', 'underlyingSymbol', 
#                            'uuid', 'regularMarketPreviousClose', 'regularMarketOpen', 
#                            'regularMarketDayLow', 'regularMarketDayHigh', 'regularMarketVolume']
        
#         # List of keys representing dates
#         date_keys = ['governanceEpochDate', 'exDividendDate', 'lastDividendDate', 'sharesShortPreviousMonthDate', 'dateShortInterest', 
#                      'lastFiscalYearEnd', 'nextFiscalYearEnd', 'mostRecentQuarter', 'lastSplitDate', 'firstTradeDateEpochUtc']
        
#         keys_1 = ['symbol', 'longName', 'shortName', 'exchange', 'currency', 'quoteType']
#         keys_2 = ['currentPrice', 'open', 'dayLow', 'dayHigh', 'previousClose']
#         keys_3 = ['fiftyDayAverage', 'twoHundredDayAverage', 'fiftyTwoWeekLow', 'fiftyTwoWeekHigh']
#         keys_4 = ['volume', 'averageVolume', 'averageVolume10days', 'averageDailyVolume10Day']
#         keys_5 = ['timeZoneFullName', 'timeZoneShortName', 'gmtOffSetMilliseconds']
#         keys_6 = ['priceHint', 'bid', 'bidSize', 'ask', 'askSize', 'longBusinessSummary', 'maxAge', 'trailingPE', 'messageBoardId', 
#                   'currency', 'firstTradeDateEpochUtc', 'trailingPegRatio']

#         # Display stock information
#         st.subheader(f"Stock Information for {ticker_input}")

#         # Add space
#         st.write("")

#         stock_info_items = list(stock_info.items())

#         for key, value in stock_info_items[:14]:
#             # Capitalize the first letter of the key, while preserving other capitalization
#             formatted_key = key[:1].upper() + key[1:]

#             # Check if the key is not in keys_to_exclude
#             if key not in keys_to_exclude:
#                 # Handle Unix epoch timestamps
#                 if key in date_keys:
#                     try:
#                         date_value = datetime.utcfromtimestamp(value).strftime('%Y-%m-%d')
#                         st.write(f"**{formatted_key}:** {date_value}")
#                     except ValueError:
#                         st.write(f"**{formatted_key}:** {value}")
#                 else:
#                     st.write(f"**{formatted_key}:** {value}")
        

#         # Add space
#         st.write("")

    
#         # Display first 3 tables in one row
#         col1, col2, col3 = st.columns(3)
#         with col1:
#             data_table("General Information", keys_1)
#         with col2:
#             data_table("Pricing Data", keys_2)
#         with col3:
#             data_table("Pricing Stats", keys_3)
        
#         # Add space between rows
#         st.write("")

#         # Display next 2 tables in another row
#         col4, col5 = st.columns(2)
#         with col4:
#             data_table("Time Data", keys_5)
#         with col5:
#             data_table("Volume", keys_4)
        
#         # Add space between rows
#         st.write("")
        
#         # Display last table separately
#         data_table("Other Information", keys_6)


#         # Add space between rows
#         st.write("")
#         st.markdown("<style>.stMarkdown {margin-bottom: 15px;}</style>", unsafe_allow_html=True)
#         st.write("")


#         for key, value in stock_info_items:
#             # Capitalize the first letter of the key, while preserving other capitalization
#             formatted_key = key[:1].upper() + key[1:]
#             # Handle special case for companyOfficers
#             if key == 'companyOfficers' and isinstance(value, list):
#                 st.write(f"**{formatted_key}:**")
#                 for officer in value:
#                     # Filter out keys to disregard
#                     filtered_officer = {k: v for k, v in officer.items() if k not in keys_to_disregard}
#                     # Display dataframe
#                     st.dataframe(filtered_officer, width=800)
        

#         # Add space
#         st.write("")
#         st.markdown("<style>.stMarkdown {margin-bottom: 15px;}</style>", unsafe_allow_html=True)
#         st.write("")
        

#         # Display historical data
#         st.subheader(f"Historical Market Data for {ticker_input}")
#         st.dataframe(hist)



#         # Add space
#         st.write("")
#         st.markdown("<style>.stMarkdown {margin-bottom: 15px;}</style>", unsafe_allow_html=True)
#         st.write("")



#         for key, value in stock_info_items[16:]:
#             # Capitalize the first letter of the key, while preserving other capitalization
#             formatted_key = key[:1].upper() + key[1:]

#             # Check if the key is not in keys_to_exclude
#             if key not in keys_to_exclude:
#                 # Handle Unix epoch timestamps
#                 if key in date_keys:
#                     try:
#                         date_value = datetime.utcfromtimestamp(value).strftime('%Y-%m-%d')
#                         st.write(f"**{formatted_key}:** {date_value}")
#                     except ValueError:
#                         st.write(f"**{formatted_key}:** {value}")
#                 else:
#                     st.write(f"**{formatted_key}:** {value}")

        

#     except Exception as e:
#         st.error(f"Error fetching data for ticker {ticker_input}: {e}")




