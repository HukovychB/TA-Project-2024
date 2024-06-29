import streamlit as st
import os
from datetime import datetime
from streamlit_lottie import st_lottie
import json
import plotly.graph_objs as go

import main


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
                layout="wide"
)

#Colors
#Background: #3f3b3b
#Text: #f2e1e1
#Other elements: #FF5500
#Font: Serif

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


#BEGINNING

col1, col2, col3 = st.columns([1, 4, 1])
#IES logo
col1.image('app/ies.png', width=100)
#Header
col2.markdown("<h1 style='text-align: center;'>TECHNICAL ANALYSIS TEST AREA</h1>", unsafe_allow_html=True)
st.write("")
#Animation
with open("app/Animation.json") as source:
        animation = json.load(source)

col1, col2 = st.columns([2, 1])
with col1:
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    #USER FORM
    ticker_input = st.text_input("Enter the ticker (e.g. AAPL, MSFT):", max_chars=10,)
    period = st.selectbox("Choose the time interval:", ["","1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"])
    s_btn = st.button("SEARCH")
with col2:
    st_lottie(animation, height = 400, width = 400)
if s_btn:
        ticker_data = main.fetch_data(ticker_input)
        main.create_graph(ticker_data, period)


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




