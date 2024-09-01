## Project Overview

Welcome to the Technical Analysis Web project! This project aims to create a simple and interactive website using the Streamlit package, where users can analyze financial instruments through various technical analysis tools. The website allows users to input tickers of financial instruments from Yahoo Finance (https://finance.yahoo.com/), view relevant information, interact with price graphs, and apply different technical analysis strategies to visualize signals and statistics.

## Features and Usage

- **User Input**: Enter the ticker symbol of any financial instrument from Yahoo Finance (e.g., stocks, ETFs, commodities, cryptocurrencies, etc.). Tickers should be exactly the same as per Yahoo Finance.
- **Data Retrieval**: Fetch and display relevant financial data for the entered ticker.
- **Interactive Graphs**: Visualize the price movements of the financial instrument with an interactive graph using daily prices.
- **Technical Analysis Tools**: Apply various technical analysis tools (MAs, TRB, RSI, MACD, DMI) with custom parametrization and visualize them on the graph(s).
- **Strategy Statistics**: Display statistics of returns and equity curves for different strategies based on the applied technical analysis tools and chosen time horizon to see their historical performance compared to B&H.
- **Current suggestion**: See what your chosen strategy suggests to do now.

## Installation

To run this project locally, follow these steps:


1. **Clone the repository**: Open your terminal and run the following command to clone the <code>main</code> branch of the repository:
```
git clone -b main https://github.com/HukovychB/TA-Project-2024.git
```

2. **Install the required packages**: You can install the required packages by running the following command (make sure you are in the correct directory in your terminal):
```
pip install -r requirements.txt
```
This command will install all the packages listed in the `requirements.txt` file.

3. **Run the Streamlit app**:
```
streamlit run app/web.py
```
5. **Open in browser**: This command will start a local web server and provide a URL (typically <code>http://localhost:8501</code>) which you can open in your web browser to view and interact with your Streamlit app.

## Dependencies
- **numpy**==2.1.0
- **pandas**==2.2.2
- **pandas_ta**==0.3.14b0
- **plotly**==5.23.0
- **pytest**==8.3.2
- **streamlit**==1.37.1
- **streamlit_lottie**==0.0.5
- **streamlit_option_menu**==0.3.13
- **yfinance**==0.2.42

## License
This project is licensed under the MIT License. See the [LICENCE](LICENCE.htm) file for details.

## Contact
For any question and concerns, please contact us at 72617770@fsv.cuni.cz or 45673694@fsv.cuni.cz.

