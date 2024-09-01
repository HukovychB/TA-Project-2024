import streamlit as st
from streamlit_lottie import st_lottie
import json
from streamlit_option_menu import option_menu

from libraries import main, constants as c, indicators as ind

st.set_page_config(
    page_title="TA App",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------------
# Colors
# Background: #3f3b3b
# Text: #f2e1e1
# Other elements: #FF5500
# Font: serif
# ------------------------------------------------------------------

# ------------------------------------------------------------------
# STYLES
# ------------------------------------------------------------------
with open("app/frontend/styles/main_style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------------------------------------------------------------------------------------------
# PAGE BEGINNING
# --------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 4, 1])
# IES logo
col1.image("app/frontend/ies.png", width=100)
# Link to info page
col3.page_link("pages/info_page.py", label="About the project")

st.markdown(
    "<h1 style='text-align: center;'>TECHNICAL ANALYSIS TEST AREA</h1>",
    unsafe_allow_html=True,
)
st.write("")
st.write("")

# ------------------------------------------------------------------
# USER FORM
# ------------------------------------------------------------------
# Animation
with open("app/frontend/Animation.json") as source:
    animation_front = json.load(source)

col1, col2 = st.columns([2, 1])
with col1:
    st.session_state.setdefault("search_btn", False)
    # USER FORM
    ticker_input = st.text_input(
        "Enter the ticker (e.g. AAPL, MSFT):",
        max_chars=10,
    )
    period_input = st.selectbox(
        "Choose time period:",
        ["", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
    )
    interval_input = st.selectbox("Choose time frame:", ["", "5m", "1h", "1d", "1wk"])
    search_btn = st.button("SEARCH")
    # Proper functioning of the SEARCH button
    if search_btn and not st.session_state.search_btn:
        st.session_state.ticker_input = ticker_input
        st.session_state.period_input = period_input
        st.session_state.interval_input = interval_input
        st.session_state.search_btn = True
with col2:
    # Animation display
    st_lottie(animation_front, height=400, width=400)

# FETCHING DATA AND GRAPH
if (
    st.session_state.get("search_btn", False)
    and st.session_state.get("ticker_input")
    and st.session_state.get("period_input")
    and st.session_state.get("interval_input")
):
    with st.spinner("SEARCHING"):
        ticker_data = main.fetch_data(ticker_input, period_input, interval_input)
        if search_btn:
            st.session_state.graph = main.create_graph(
                ticker_data, period_input, interval_input
            )
        # Placeholders for the graphs
        graph_place = st.empty()
        MACD_place = st.empty()
        DMI_place = st.empty()
        RSI_place = st.empty()
        Remove_btn_place = st.empty()
        # Main graph
        graph_place.plotly_chart(st.session_state.graph, config=dict(scrollZoom=True))
        if "macd_graph" in st.session_state:
            MACD_place.plotly_chart(
                st.session_state.macd_graph, config=dict(scrollZoom=True)
            )
        if "dmi_graph" in st.session_state:
            DMI_place.plotly_chart(
                st.session_state.dmi_graph, config=dict(scrollZoom=True)
            )
        if "rsi_graph" in st.session_state:
            RSI_place.plotly_chart(
                st.session_state.rsi_graph, config=dict(scrollZoom=True)
            )
    # 2 suporting sections
    selected_page = option_menu(
        menu_title=None,
        options=["INFO", "TECHNICAL ANALYSIS"],
        orientation="horizontal",
        icons=["info-circle", "bar-chart-steps"],
        styles=c.styles_option_menu,
    )

    # ------------------------------------------------------------------
    # INFO SECTION
    # ------------------------------------------------------------------
    if selected_page == "INFO":
        col1, col2, col3 = st.columns(3)

        # STOCK INFO
        country = ticker_data.info.get("country", "N/A")
        sector = ticker_data.info.get("sector", "N/A")
        industry = ticker_data.info.get("industry", "N/A")
        market_cap = ticker_data.info.get("marketCap", "N/A")
        ent_value = ticker_data.info.get("enterpriseValue", "N/A")
        employees = ticker_data.info.get("fullTimeEmployees", "N/A")

        stock_info = [
            ("Stock Info", f"{ticker_input}"),
            ("Country", country),
            ("Sector", sector),
            ("Industry", industry),
            ("Market Cap", main.format_value(market_cap)),
            ("Enterprise Value", main.format_value(ent_value)),
            ("Employees", employees),
        ]

        with col1:
            st.markdown(main.html_table(stock_info), unsafe_allow_html=True)

        # PRICE INFO
        current_price = ticker_data.info.get("currentPrice", "N/A")
        prev_close = ticker_data.info.get("previousClose", "N/A")
        day_high = ticker_data.info.get("dayHigh", "N/A")
        day_low = ticker_data.info.get("dayLow", "N/A")
        ft_week_high = ticker_data.info.get("fiftyTwoWeekHigh", "N/A")
        ft_week_low = ticker_data.info.get("fiftyTwoWeekLow", "N/A")

        price_info = [
            ("Price Info", f"{ticker_input}"),
            ("Current Price", f"${current_price:.2f}"),
            ("Previous Close", f"${prev_close:.2f}"),
            ("Day High", f"${day_high:.2f}"),
            ("Day Low", f"${day_low:.2f}"),
            ("52 Week High", f"${ft_week_high:.2f}"),
            ("52 Week Low", f"${ft_week_low:.2f}"),
        ]

        with col2:
            st.markdown(main.html_table(price_info), unsafe_allow_html=True)

        # BUSINESS METRICS
        forward_eps = ticker_data.info.get("forwardEps", "N/A")
        forward_pe = ticker_data.info.get("forwardPE", "N/A")
        peg_ratio = ticker_data.info.get("pegRatio", "N/A")
        dividend_rate = ticker_data.info.get("dividendRate", "N/A")
        dividend_yield = ticker_data.info.get("dividendYield", "N/A")
        recommendation = ticker_data.info.get("recommendationKey", "N/A")

        biz_metrics = [
            ("Business Metrics", f"{ticker_input}"),
            ("EPS (FWD)", f"{forward_eps:.2f}"),
            ("P/E (FWD)", f"{forward_pe:.2f}"),
            ("PEG Ratio", f"{peg_ratio:.2f}"),
            ("Div Rate (FWD)", f"${dividend_rate:.2f}"),
            ("Div Yield (FWD)", f"{dividend_yield * 100:.2f}%"),
            ("Recommendation", recommendation.capitalize()),
        ]

        with col3:
            st.markdown(main.html_table(biz_metrics), unsafe_allow_html=True)

    # ------------------------------------------------------------------
    # SECTION TA
    # ------------------------------------------------------------------
    if selected_page == "TECHNICAL ANALYSIS":
        selected_indicators = st.multiselect(
            "**Select technical indicators:**",
            [
                "Moving Average",
                "Relative Strength Index (RSI)",
                "Directional Movement Index (DMI)",
                "Moving Average Converge Divergence (MACD)",
                "Trading Range Breakout",
            ],
        )

        # Parameter section layout
        if selected_indicators != []:
            st.write("")
            st.markdown(
                "<h4 style='text-align: center; font-size: 25px; font-family: serif;'>SELECT PARAMETERS FOR THE INDICATORS</h4>",
                unsafe_allow_html=True,
            )
            st.write("")

        # Dynamic adjustments to the # of cols depending on the # of indicators
        num_indicator_columns = min(len(selected_indicators), 3)
        indicator_columns = st.columns(num_indicator_columns)
        indicator_columns_counter = 0

        if "Moving Average" in selected_indicators:
            with indicator_columns[indicator_columns_counter]:
                st.write("**MOVING AVERAGE**")
                ma_short = st.number_input(
                    "Length of short moving average:",
                    min_value=1,
                    max_value=len(
                        ticker_data.history(
                            period=period_input, interval=interval_input
                        )
                    )
                    - 1,
                    value=20,
                )
                ma_long = st.number_input(
                    "Length of long moving average:",
                    min_value=2,
                    max_value=len(
                        ticker_data.history(
                            period=period_input, interval=interval_input
                        )
                    ),
                    value=50,
                )
                ema_checkbox = st.checkbox("Use exponential moving average.")
            indicator_columns_counter = (
                indicator_columns_counter + 1
            ) % num_indicator_columns
        else:
            ma_short = None
            ma_long = None
            ema_checkbox = None
        if "Relative Strength Index (RSI)" in selected_indicators:
            with indicator_columns[indicator_columns_counter]:
                st.write("**RSI**")
                rsi_length = st.number_input(
                    "Length of indicator:",
                    min_value=1,
                    max_value=len(
                        ticker_data.history(
                            period=period_input, interval=interval_input
                        )
                    ),
                    value=14,
                )
                rsi_thresholds = st.selectbox(
                    "Thresholds values:",
                    ["30/70", "40/60", "25/75", "20/80", "15/85", "10/90"],
                )
                rsi_checkbox = st.checkbox("Add simple moving average.")
            indicator_columns_counter = (
                indicator_columns_counter + 1
            ) % num_indicator_columns
        else:
            rsi_length = None
            rsi_thresholds = None
            rsi_checkbox = None
        if "Directional Movement Index (DMI)" in selected_indicators:
            with indicator_columns[indicator_columns_counter]:
                st.write("**DMI**")
                dmi_length = st.number_input(
                    "Length of indicator:",
                    min_value=1,
                    max_value=len(
                        ticker_data.history(
                            period=period_input, interval=interval_input
                        )
                    )
                    - 1,
                    value=14,
                )
                adx_smoothing = st.number_input(
                    "ADX smoothing:",
                    min_value=1,
                    max_value=len(
                        ticker_data.history(
                            period=period_input, interval=interval_input
                        )
                    )
                    - dmi_length,
                    value=14,
                )
            indicator_columns_counter = (
                indicator_columns_counter + 1
            ) % num_indicator_columns
        else:
            dmi_length = None
            adx_smoothing = None
        if "Moving Average Converge Divergence (MACD)" in selected_indicators:
            with indicator_columns[indicator_columns_counter]:
                st.write("**MACD**")
                macd_fast = st.number_input(
                    "Length of fast moving average:",
                    min_value=1,
                    max_value=len(
                        ticker_data.history(
                            period=period_input, interval=interval_input
                        )
                    )
                    - 1,
                    value=12,
                )
                macd_slow = st.number_input(
                    "Length of slow moving average:",
                    min_value=2,
                    max_value=len(
                        ticker_data.history(
                            period=period_input, interval=interval_input
                        )
                    ),
                    value=26,
                )
                macd_signal = st.number_input(
                    "Length of signal moving average:",
                    min_value=1,
                    max_value=len(
                        ticker_data.history(
                            period=period_input, interval=interval_input
                        )
                    )
                    - macd_slow
                    + 1,
                    value=9,
                )
            indicator_columns_counter = (
                indicator_columns_counter + 1
            ) % num_indicator_columns
        else:
            macd_fast = None
            macd_slow = None
            macd_signal = None
        if "Trading Range Breakout" in selected_indicators:
            with indicator_columns[indicator_columns_counter]:
                st.write("**TRADING RANGE BREAKOUT**")
                trb_length = st.number_input(
                    "Length of indicator:",
                    min_value=1,
                    max_value=len(
                        ticker_data.history(
                            period=period_input, interval=interval_input
                        )
                    ),
                    value=20,
                )
                trb_width = st.number_input(
                    "Width of channel:", min_value=0.000001, max_value=10.0, value=0.1
                )
                trb_num_periods_to_hold = st.number_input(
                    "Number of periods to hold a position:",
                    min_value=1,
                    max_value=10000,
                    value=20,
                )
            indicator_columns_counter = (
                indicator_columns_counter + 1
            ) % num_indicator_columns
        else:
            trb_length = None
            trb_width = None
            trb_num_periods_to_hold = None

        if selected_indicators != []:
            st.session_state.setdefault("parameter_btn", False)
            parameter_btn = st.button("ANALYZE")
            if parameter_btn:
                st.session_state.parameter_btn = True

        # Plot indicators
        if st.session_state.parameter_btn:
            main.execute_ta(
                selected_indicators,
                ticker_data,
                period_input,
                interval_input,
                st.session_state.graph,
                graph_place,
                RSI_place,
                MACD_place,
                DMI_place,
                ma_short,
                ma_long,
                ema_checkbox,
                rsi_length,
                rsi_thresholds,
                rsi_checkbox,
                macd_fast,
                macd_slow,
                macd_signal,
                dmi_length,
                adx_smoothing,
                trb_length,
                trb_width,
            )

            # Remove indicators
            remove_indicators_btn = Remove_btn_place.button("REMOVE INDICATORS")
            if remove_indicators_btn:
                st.session_state.graph = main.create_graph(
                    ticker_data, period_input, interval_input
                )
                graph_place.plotly_chart(
                    st.session_state.graph, config=dict(scrollZoom=True)
                )
                st.session_state.pop("macd_graph", None)
                st.session_state.pop("dmi_graph", None)
                st.session_state.pop("rsi_graph", None)
                MACD_place.empty()
                DMI_place.empty()
                RSI_place.empty()
                selected_indicators = []

            # ------------------------------------------------------------------
            # ANALYSIS
            # ------------------------------------------------------------------
            price_df = main.add_ta_to_df(
                ticker_data,
                period_input,
                interval_input,
                selected_indicators,
                ma_short,
                ma_long,
                ema_checkbox,
                rsi_length,
                rsi_thresholds,
                macd_fast,
                macd_slow,
                macd_signal,
                dmi_length,
                adx_smoothing,
                trb_length,
                trb_width,
                trb_num_periods_to_hold,
            )

            ta_statistics = main.do_ta_analysis(price_df)
            ta_statistics_styled = main.apply_styles_df(ta_statistics)

            st.markdown(
                "<h4 style='text-align: center; font-size: 25px; font-family: serif;'>TRADE STATISTICS</h4>",
                unsafe_allow_html=True,
            )
            st.dataframe(ta_statistics_styled)

            st.write("")
            st.write("")
            st.write("")
            st.write("")
            equity_df = main.extract_equity_curves(price_df)
            main.plot_equity_curves(equity_df)

            main.current_recommendation(ta_statistics)

elif search_btn:
    st.error("Please enter the ticker and choose time interval.", icon="❗")
