import streamlit as st
# import os
# from datetime import datetime
from streamlit_lottie import st_lottie
import json
from streamlit_option_menu import option_menu
import pandas as pd

from libraries import main, constants as c


# def data_table(header, keys):
#     data = []
#     for key in keys:
#         # Capitalize the first letter of the key, while preserving other capitalization
#         formatted_key = key[:1].upper() + key[1:]
#         value = stock_info.get(key, '-')
#         # Handle Unix epoch timestamps
#         if key in date_keys:
#             try:
#                 date_value = datetime.utcfromtimestamp(value).strftime('%Y-%m-%d')
#                 data.append([formatted_key, date_value])
#             except ValueError:
#                 data.append([formatted_key, value])
#         else:
#             data.append([formatted_key, value])
    
#     table_markdown = "<table>"
#     for row in data:
#         table_markdown += f"<tr><td><strong>{row[0]}</strong></td><td>{row[1]}</td></tr>"
#     table_markdown += "</table>"
#     st.markdown(f"### {header}")
#     st.markdown(table_markdown, unsafe_allow_html=True)

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
with open('app/frontend/main_style.css') as f:
     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


#BEGINNING


col1, col2, col3 = st.columns([1, 4, 1])
#IES logo
col1.image('app/frontend/ies.png', width=100)
#Link to info page
col3.page_link("pages/info_page.py", label = "About the project")

#Header
st.markdown("<h1 style='text-align: center;'>TECHNICAL ANALYSIS TEST AREA</h1>", unsafe_allow_html=True)
st.write("")
st.write("")
#Animation
with open("app/frontend/Animation.json") as source:
        animation_front = json.load(source)

col1, col2 = st.columns([2, 1])
with col1:
    st.session_state.setdefault('search_btn', False)
    #USER FORM
    ticker_input = st.text_input("Enter the ticker (e.g. AAPL, MSFT):", max_chars=10,)
    period_input = st.selectbox("Choose time period:", ["","1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"])
    interval_input = st.selectbox("Choose time frame:", ["", "5m", "1h", "1d", "1wk"])
    search_btn = st.button("SEARCH")
    #Proper functioning of the SEARCH button
    if search_btn and not st.session_state.search_btn:
        st.session_state.ticker_input = ticker_input
        st.session_state.period_input = period_input
        st.session_state.interval_input = interval_input
        st.session_state.search_btn = True    
with col2:
    #Animation display
    st_lottie(animation_front, height = 400, width = 400)

#FETCHING DATA AND GRAPH
if st.session_state.get('search_btn', False) and st.session_state.get('ticker_input') and st.session_state.get('period_input') and st.session_state.get('interval_input'):
    with st.spinner("SEARCHING"):
        ticker_data = main.fetch_data(ticker_input, period_input,interval_input)
        # if 'graph' not in st.session_state or st.session_state.ticker_input != ticker_input or st.session_state.period_input != period_input:
        if search_btn:
            st.session_state.graph = main.create_graph(ticker_data, period_input, interval_input)
        #Placeholders for the graphs
        graph_place = st.empty()
        MACD_place = st.empty()
        DMI_place = st.empty()
        RSI_place = st.empty()
        Remove_btn_place = st.empty()
        #Main graph
        graph_place.plotly_chart(st.session_state.graph, config=dict(scrollZoom=True))
        if 'macd_graph' in st.session_state:
            MACD_place.plotly_chart(st.session_state.macd_graph, config=dict(scrollZoom=True))
        if 'dmi_graph' in st.session_state:
            DMI_place.plotly_chart(st.session_state.dmi_graph, config=dict(scrollZoom=True))
        if 'rsi_graph' in st.session_state:
            RSI_place.plotly_chart(st.session_state.rsi_graph, config=dict(scrollZoom=True))
    #2 suporting sections
    selected_page = option_menu(
            menu_title=None,
            options = ["INFO", "TECHNICAL ANALYSIS"],
            orientation="horizontal",
            icons = ['info-circle','bar-chart-steps'],
            styles = c.styles_option_menu
    )

    #EVERYTHING RELATED TO THE INSTRUMENT
    if selected_page == "INFO":
        st.markdown("""
        <style>
            .custom-table {
                margin: 0;
                padding: 4px;
                width: calc(129px + 50%);
                font: 11px Arial, Helvetica, sans-serif;
                color: #747474;
                background-color: #0c2a62;
                box-sizing: border-box;
                border: 1px solid #ced9ec;
                border-radius: 4px;
            }

            .table-top {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 46px;
                border-top: 2px solid #FFF;
                background: #eff4ff url(frontend/top-light-blue.png) repeat-x left top;
                border-bottom: 1px solid #ced9ec;
                display: flex;
                align-items: center; 
            }

            .table-top-cell {
                flex: 1; 
                padding: 15px 0;
                text-align: center;
                height: 31px;
                border-right: 1px solid #ced9ec;
                color: #1f3d71;
                font: 13px Arial, Helvetica, sans-serif;
                display: flex;
                align-items: center; 
                justify-content: center; 
            }

            .table-top-cell:first-child {
                border-left: 1px solid #ced9ec;
            }

            .table-middle {
                margin: 0;
                padding: 0;
                width: 100%;
                background: #f6f6f6 url(frontend/center-bcg.png) repeat-y right top;
                overflow: hidden;
                border: 1px solid #ced9ec;
                border-top: none;
                border-left: none;
                border-right: none;
            }

            .table-row {
                clear: both;
                width: 100%;
                display: flex;
                flex-direction: row;
                box-sizing: border-box;
            }

            .table-left {
                flex: 0 0 129px;
                margin: 0;
                padding: 10px 0;
                text-align: center;
                height: 25px;
                border-right: 1px solid #ced9ec;
                border-bottom: 1px solid #b3c1db;
                color: #1f3d71;
                font: 13px Arial, Helvetica, sans-serif;
                display: flex;
                align-items: center; 
                justify-content: center; 
            }

            .table-right {
                flex: 1;
                margin: 0;
                padding: 11px 0;
                text-align: center;
                height: 24px;
                border-right: 1px solid #ced9ec;
                border-bottom: 1px solid #b3c1db;
                display: flex;
                align-items: center; 
                justify-content: center; 
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
            ("Stock Info", f"{ticker_input}"),
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
            ("Price Info", f"{ticker_input}"),
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
            ("Business Metrics", f"{ticker_input}"),
            ("EPS (FWD)", f"{forward_eps:.2f}"),
            ("P/E (FWD)", f"{forward_pe:.2f}"),
            ("PEG Ratio", f"{peg_ratio:.2f}"),
            ("Div Rate (FWD)", f"${dividend_rate:.2f}"),
            ("Div Yield (FWD)", f"{dividend_yield * 100:.2f}%"),
            ("Recommendation", recommendation.capitalize())
        ]

        with col3:
            st.markdown(main.html_table(biz_metrics), unsafe_allow_html=True)

    #EVERYTHING RELATED TO TA
    if selected_page == "TECHNICAL ANALYSIS":
        selected_indicators = st.multiselect("**Select technical indicators:**", [
                    'Moving Average','Relative Strength Index (RSI)', 
                    'Directional Movement Index (DMI)', 'Moving Average Converge Divergence (MACD)',
                    'Trading Range Breakout'])
        
        #Parameter section layout
        if selected_indicators != []:
            st.write("")
            st.markdown("<h4 style='text-align: center; font-size: 25px; font-family: serif;'>SELECT PARAMETERS FOR THE INDICATORS</h4>", unsafe_allow_html=True)
            st.write("")       

        #Dynamic adjustments to the # of cols depending on the # of indicators
        num_indicator_columns = min(len(selected_indicators),3)
        indicator_columns = st.columns(num_indicator_columns)
        indicator_columns_counter = 0
        
        if "Moving Average" in selected_indicators:
            with indicator_columns[indicator_columns_counter]:
                st.write("**MOVING AVERAGE**")
                ma_short = st.number_input("Length of short moving average:", min_value=1, max_value=len(ticker_data.history(period = period_input, interval = interval_input))-1, value = 20)
                ma_long = st.number_input("Length of long moving average:", min_value=2, max_value=len(ticker_data.history(period = period_input, interval = interval_input)), value = 50)
                ema_checkbox = st.checkbox("Use exponential moving average.")
            indicator_columns_counter = (indicator_columns_counter+1) % num_indicator_columns
        else:
            ma_short = None
            ma_long = None
            ema_checkbox = None
        if "Relative Strength Index (RSI)" in selected_indicators:
            with indicator_columns[indicator_columns_counter]:
                st.write("**RSI**")
                rsi_length = st.number_input("Length of indicator:", min_value=1, max_value=len(ticker_data.history(period = period_input, interval = interval_input)), value = 14)
                rsi_thresholds = st.selectbox("Thresholds values:", ['30/70','40/60','25/75','20/80','15/85','10/90'])
                rsi_checkbox = st.checkbox("Add simple moving average.")
            indicator_columns_counter = (indicator_columns_counter+1) % num_indicator_columns

            st.session_state.rsi_graph = main.create_rsi(ticker_data, period_input, interval_input, rsi_length, rsi_thresholds, rsi_checkbox)
        else:
            rsi_length = None
            rsi_thresholds = None
            rsi_checkbox = None
        if "Directional Movement Index (DMI)" in selected_indicators:
            with indicator_columns[indicator_columns_counter]:
                st.write("**DMI**")
                dmi_length = st.number_input("Length of indicator:", min_value=1, max_value=len(ticker_data.history(period = period_input, interval = interval_input))-1, value = 14)
                adx_smoothing = st.number_input("ADX smoothing:", min_value=1, max_value=len(ticker_data.history(period = period_input, interval = interval_input))-dmi_length, value = 14)
            indicator_columns_counter = (indicator_columns_counter+1) % num_indicator_columns

            st.session_state.dmi_graph = main.create_dmi(ticker_data, period_input, interval_input, dmi_length, adx_smoothing)
        else:
            dmi_length = None
            adx_smoothing = None
        if "Moving Average Converge Divergence (MACD)" in selected_indicators:
            with indicator_columns[indicator_columns_counter]:
                st.write("**MACD**")
                macd_fast = st.number_input("Length of fast moving average:", min_value=1, max_value=len(ticker_data.history(period = period_input, interval = interval_input))-1, value = 12)
                macd_slow = st.number_input("Length of slow moving average:", min_value=2, max_value=len(ticker_data.history(period = period_input, interval = interval_input)), value = 26)
                macd_signal = st.number_input("Length of signal moving average:", min_value=1, max_value=len(ticker_data.history(period = period_input, interval = interval_input))-macd_slow+1, value = 9)
            indicator_columns_counter = (indicator_columns_counter+1) % num_indicator_columns

            st.session_state.macd_graph = main.create_macd(ticker_data, period_input, interval_input, macd_fast, macd_slow, macd_signal)
        else:
            macd_fast = None
            macd_slow = None
            macd_signal = None
        if "Trading Range Breakout" in selected_indicators:
            with indicator_columns[indicator_columns_counter]:
                st.write("**TRADING RANGE BREAKOUT**")
                trb_length = st.number_input("Length of indicator:", min_value=1, max_value=len(ticker_data.history(period = period_input, interval = interval_input)), value = 20)
                trb_width = st.number_input("Width of channel:", min_value=0.000001, max_value=10.0, value = 0.1)
                trb_num_periods_to_hold = st.number_input("Number of periods to hold a position:", min_value=1, max_value=10000, value = 20)     
            indicator_columns_counter = (indicator_columns_counter+1) % num_indicator_columns
        else:
            trb_length = None
            trb_width = None
            trb_num_periods_to_hold = None

        if selected_indicators != []:
            st.session_state.setdefault('parameter_btn', False)
            parameter_btn = st.button("ANALYZE")
            if parameter_btn:
                st.session_state.parameter_btn=True

        #Plot indicators
        if st.session_state.parameter_btn:
            main.execute_ta(selected_indicators, ticker_data, period_input, interval_input, st.session_state.graph,
                graph_place, RSI_place, MACD_place, DMI_place,
                ma_short, ma_long, ema_checkbox, rsi_length, rsi_thresholds, rsi_checkbox, 
                macd_fast, macd_slow, macd_signal, dmi_length, adx_smoothing, trb_length, trb_width)
            
            #Remove indicators
            remove_indicators_btn = Remove_btn_place.button("REMOVE INDICATORS")
            if remove_indicators_btn:
                st.session_state.graph = main.create_graph(ticker_data, period_input, interval_input)
                graph_place.plotly_chart(st.session_state.graph, config=dict(scrollZoom=True))
                st.session_state.pop('macd_graph', None)
                st.session_state.pop('dmi_graph', None)
                st.session_state.pop('rsi_graph', None)
                MACD_place.empty()
                DMI_place.empty()
                RSI_place.empty()

        #ANALYSIS
            price_df = main.add_ta_to_df(ticker_data, period_input, interval_input, selected_indicators,
                ma_short, ma_long, ema_checkbox, rsi_length, rsi_thresholds,
                macd_fast, macd_slow, macd_signal, dmi_length, adx_smoothing, trb_length, trb_width, trb_num_periods_to_hold)
            
            ta_statistics = main.do_ta_analysis(price_df)
            ta_statistics_styled = main.apply_styles_df(ta_statistics)

            st.markdown("<h4 style='text-align: center; font-size: 25px; font-family: serif;'>TRADE STATISTICS</h4>", unsafe_allow_html=True)
            st.dataframe(ta_statistics_styled)
            main.current_recommendation(ta_statistics)

elif search_btn:
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




