import streamlit as st
import streamlit.components.v1 as components

from libraries import main

with open('app/frontend/info_style.css') as f:
     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# BEGINNING

col1, col2, col3 = st.columns([1, 4, 1])
#IES logo
col1.image('app/frontend/ies.png', width=100)
#Header
#st.markdown("<h1 style='text-align: center;'>WELCOME TO OUR TECHNICAL ANALYSIS PROJECT</h1>", unsafe_allow_html=True)

about_image = main.image_to_base64('app/frontend/info-about.jpg')
indicators_image = main.image_to_base64('app/frontend/info-indicators.png')

html_content_1 = f"""
<table id="about" border="0" width="100%" cellpadding="0" cellspacing="0" bgcolor="#f7ab48">
    <tr>
        <td>
            <table border="0" cellpadding="15" cellspacing="0" width="80%" align="center">
                <tr>
                    <td height="180" align="center" valign="middle" colspan="2">
                        <font face="Verdana" size="7" color="#030804">WELCOME TO OUR TECHNICAL ANALYSIS PROJECT</font>
                        <hr color="#030804" width="90">
                    </td>
                </tr>
                <tr>
                    <td style="width: 40%; vertical-align: top; text-align: left;">
                        <img src="data:image/jpeg;base64,{about_image}" style="max-width: 100%; height: auto; display: block;">
                    </td>
                    <td style="width: 60%; vertical-align: top;">
                        <font face="Verdana" size="4" color="black">
                            The website allows you to input tickers of all financial instruments from Yahoo Finance, displays relevant information about them, and provides interactive price graphs.
                            <hr color="#f7ab48">
                            You can choose from different technical analysis strategies with custom parametrization and compare their historical performance.
                        </font>
                    </td>
                </tr>
            </table>
            <hr color="#f7ab48">
            <hr color="#f7ab48">
            <hr color="#f7ab48">
        </td>
    </tr>
</table>
"""

html_content_2 = """ 
<table id="strategy" border="0" width="100%" cellpadding="0" cellspacing="0" bgcolor="#f7ab48">
    <tr>
        <td>
            <table border="0" cellpadding="15" cellspacing="0" width="80%" align="center">
                <tr>
                    <td height="180" align="center" valign="middle">
                        <font face="Verdana" size="7" color="#030804">CHOOSE YOUR OWN TRADING STRATEGY AND TIME HORIZON<hr color="#030804" width="100"></font>
                    </td>
                </tr>
                <tr>
                    <td>
                        <font face="Verdana" size="4" color="black">
                            <ul>
                                <li>
                                    <b>ENTER THE TICKER OF FINANCIAL INSTRUMENT</b>
                                    <ul>
                                        <li>Input the ticker symbol of any financial instrument from Yahoo Finance (e.g., stocks, ETFs, commodities, cryptocurrencies, etc.).</li>
                                        <li>View relevant financial information for the instrument.</li>
                                    </ul>
                                </li>
                                <li><hr color="#f7ab48"><b>VISUALIZE THE PRICE MOVEMENTS</b>
                                    <ul>
                                        <li>Select time period and time frame to be displayed for historical price data of the specified ticker.</li>
                                        <li>Candlestick chart shows Open, High, Low, and Close prices over time.</li>
                                    </ul>
                                </li>
                                <li><hr color="#f7ab48"><b>APPLY VARIOUS TECHNICAL ANALYSIS TOOLS</b>
                                    <ul>
                                        <li>Choose from 5 different technical analysis indicators with custom parametrization.</li>
                                        <li>See trade statistics and equity curves resulting from the selected strategies.</li>
                                    </ul>
                                </li>
                                <li><hr color="#f7ab48"><b>SEE CURRENT TRADE RECOMMENDATION</b>
                                </li>
                            </ul>
                        </font>
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
"""

html_content_3 = f"""
<table id="indicators" border="0" width="100%" cellpadding="0" cellspacing="0" bgcolor="#c2c0c3">
    <tr>
        <td>
            <table border="0" cellpadding="15" cellspacing="0" width="80%" align="center">
                <tr>
                    <td height="180" align="center" valign="middle" colspan="2">
                        <font face="Verdana" size="7" color="black">TECHNICAL ANALYSIS INDICATORS</font>
                        <hr color="black" width="90">
                    </td>
                </tr>
                <tr>
                    <td height="10" width="55%">
                        <font face="Times New Roman" size="5" color="black">
                            <ul>
                                <li>Moving Average <a href="https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp" target="_blank" style="text-decoration:none">➲</a> smooths out price data by creating a constantly updated average price</li>
                                <li><hr color="#c2c0c3">Relative Strength Index (RSI) <a href="https://www.investopedia.com/terms/r/rsi.asp" target="_blank" style="text-decoration:none">➲</a> measures the speed and magnitude of a security's recent price changes, used in momentum trading</li>
                                <li><hr color="#c2c0c3">Directional Movement Index (DMI) <a href="https://www.investopedia.com/terms/d/dmi.asp" target="_blank" style="text-decoration:none">➲</a> measures both the strength and direction of a price movement and is used to reduce false signals</li>
                                <li><hr color="#c2c0c3">Moving Average Convergence Divergence (MACD) <a href="https://www.investopedia.com/terms/m/macd.asp" target="_blank" style="text-decoration:none">➲</a> a trend-following momentum indicator that shows the relationship between two exponential moving averages of a security's price</li>
                                <li><hr color="#c2c0c3">Trading Range Breakout <a href="https://www.investopedia.com/articles/trading/08/trading-breakouts.asp" target="_blank" style="text-decoration:none">➲</a> a potential trading opportunity that occurs when an asset's price moves above a resistance level or moves below a support level on increasing volume</li>
                            </ul>
                            <hr color="#c2c0c3">
                            <hr color="#c2c0c3">
                            <hr color="#c2c0c3">
                            <hr color="#c2c0c3">
                        </font>
                    </td>
                    <td width="45%" style="text-align: right;">
                        <img src="data:image/jpeg;base64,{indicators_image}" alt="Indicators" class="indicators-img">
                    </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
"""

with open('app/frontend/info_page_style.css') as f:
     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

components.html(html_content_1, height=475)
st.image('app/frontend/info-ta.webp', use_column_width=True)
components.html(html_content_2, height=575)
components.html(html_content_3, height=850)