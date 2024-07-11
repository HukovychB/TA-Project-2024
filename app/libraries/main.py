import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import pandas_ta as ta

from libraries import indicators as ind, constants as c

#-------------------------------------------------------
#MAIN (INITIAL INTERACTION)
#-------------------------------------------------------
def fetch_data(ticker_input, period, interval):
    ticker_data = yf.Ticker(ticker_input)
    price = ticker_data.history(period = 'max')

    if interval == '5m' and period != '1mo':
        st.error("5 minutes time frame can be used only for the time period of 1 month. Please select the correct time period.", icon="🚨")
    elif not price.empty:
        return ticker_data
    else:
        st.error("Error: The ticker is not recognized. Please provide a valid symbol listed on Yahoo Finance (https://finance.yahoo.com/).", icon="🚨")

def create_graph(ticker_data, period, interval):
    price_df = ticker_data.history(period = period, interval = interval)
    fig = go.Figure()

    fig.add_trace(go.Candlestick(x=price_df.index,
                                open=price_df['Open'],
                                high=price_df['High'],
                                low=price_df['Low'],
                                close=price_df['Close'],
                                name='Candles',
                                increasing_line_color='lime',
                                increasing_fillcolor='#3f3b3b',
                                decreasing_line_color='#FF440B',
                                decreasing_fillcolor='#3f3b3b',
                                increasing_line_width=0.75,
                                decreasing_line_width=0.75,     
                                whiskerwidth=0.1))
    
    fig.update_layout(
        title=f"Graph {ticker_data.info.get('longName')} ({ticker_data.ticker.upper()})",
        xaxis_rangeslider_visible=False,
        title_font=dict(size=32, family='serif', color='linen'),
        height=600,
        dragmode='pan',
        uirevision='constant',
        xaxis=dict(
            showline=False,
            linecolor='dimgrey',            
            gridcolor='black',
            rangebreaks= rangebreaks(interval),
            tickfont=dict(family='serif', size=12, color='linen')                
        ),
        yaxis=dict(
            showline=False,
            linecolor='dimgrey',            
            gridcolor='dimgrey',
            tickfont=dict(family='serif', size=12, color='linen')           
        ),
        legend=dict(
            x=0,          
            y=1,          
            xanchor='left',
            yanchor='top'
        )
    )

    fig.data[0].update(showlegend=False)

    return fig

#-------------------------------------------------------
#TA SECTION
#-------------------------------------------------------

def execute_ta(selected_indicators, ticker_data, period_input, interval_input, graph,
               graph_place, RSI_place, MACD_place, DMI_place,
               ma_short, ma_long, ema_checkbox, rsi_length, rsi_thresholds, rsi_checkbox, 
               macd_fast, macd_slow, macd_signal, dmi_length, adx_smoothing, trb_length, trb_width):
    if "Moving Average" in selected_indicators:
        ind.execute_ma(ticker_data, period_input, interval_input, graph,
                   ma_short, ma_long, ema_checkbox,
                   graph_place)

    if "Relative Strength Index (RSI)" in selected_indicators:  
        ind.execute_rsi(ticker_data, period_input, interval_input,
                    rsi_length, rsi_thresholds, rsi_checkbox, 
                    RSI_place)

    if "Moving Average Converge Divergence (MACD)" in selected_indicators:
        ind.execute_macd(ticker_data, period_input, interval_input,
                    macd_fast, macd_slow, macd_signal,
                    MACD_place)

    if "Directional Movement Index (DMI)" in selected_indicators:  
        ind.execute_dmi(ticker_data, period_input, interval_input,
                    dmi_length, adx_smoothing,
                    DMI_place)
    if "Trading Range Breakout" in selected_indicators:
        ind.execute_trb(ticker_data, period_input, interval_input, graph,
                    trb_length, trb_width,
                    graph_place)

#--------------------------
#ANALYSIS
#--------------------------

#SUPPORT (STATISTICS)
def calculate_num_trades(col):
    num_signals = 0
    for i in range(1, len(col)):
        if col[i] != col[i-1] and col[i] != 0 and not pd.isna(col[i]):
            num_signals += 1
    
    return num_signals

def win_lose_trades(col_signals, col_returns):
    winning_trades = 0
    losing_trades = 0
    returns_per_trade = []
    position = 1
    for i in range(1, len(col_signals)-1):
        if col_signals[i]==col_signals[i-1] and not pd.isna(col_signals[i]) and col_signals[i] != 0:
            returns_per_trade.append(col_returns[i])
            if position == 1:
                returns_per_trade.append(col_returns[i-1])
            position += 1
        elif col_signals[i]!=col_signals[i-1] and col_signals[i]!=col_signals[i+1] and col_signals[i] != 0 and not pd.isna(col_signals[i]):
            if returns_per_trade != []:
                sum_return_trade = sum(returns_per_trade)
                if sum_return_trade > 0:
                    winning_trades += 1
                else:
                    losing_trades += 1
                returns_per_trade = []
                position = 1   
            returns_per_trade.append(col_returns[i])
        else:
            if returns_per_trade != []:
                sum_return_trade = sum(returns_per_trade)
                if sum_return_trade > 0:
                    winning_trades += 1
                else:
                    losing_trades += 1
            returns_per_trade = []
            position = 1

    #Check if the last signal is added
    if returns_per_trade != []:
        if returns_per_trade != []:
            sum_return_trade = sum(returns_per_trade)
        if sum_return_trade > 0:
            winning_trades += 1
        else:
            losing_trades += 1

    #Check if the last signal's duration is 1 period
    if col_signals.iloc[-1] != col_signals.iloc[-2] and col_signals.iloc[-1] != 0:
        if col_returns.iloc[-1] > 0:
            winning_trades += 1
        else:
            losing_trades += 1

    result = [winning_trades, losing_trades]
    return result

def mean_trade_length(col_signals):
    trade_lengths = []
    current_trade_length = 0
    in_trade = False
    current_trade_value = 0

    for i in col_signals:
        if i == 1 or i == -1:
            if not in_trade:
                in_trade = True
                current_trade_length = 1
                current_trade_value = i
            elif i == current_trade_value:
                current_trade_length += 1
            else:
                trade_lengths.append(current_trade_length)
                current_trade_length = 1
                current_trade_value = i
        elif i == 0 and in_trade:
            trade_lengths.append(current_trade_length)
            in_trade = False

    if in_trade:
        trade_lengths.append(current_trade_length)

    mean = np.mean(trade_lengths)  
    return mean

#MAIN (STATISTICS)
def add_ta_to_df(ticker_data, period_input, interval_input, selected_indicators,
                ma_short, ma_long, ema_checkbox, rsi_length, rsi_thresholds,
                macd_fast, macd_slow, macd_signal, dmi_length, adx_smoothing, trb_length, trb_width, trb_num_periods_to_hold):
    price_df = ticker_data.history(period = period_input, interval = interval_input)
    
    price_df['logreturns']=np.log(price_df['Close'] / price_df['Close'].shift(1))
    
    if 'Moving Average' in selected_indicators:
        if ema_checkbox:
            price_df['Moving_Average_short'] = ta.ema(close=price_df['Close'], length=ma_short)
            price_df['Moving_Average_long'] = ta.ema(close=price_df['Close'], length=ma_long)
        else:
            price_df['Moving_Average_short'] = price_df['Close'].rolling(window=ma_short).mean()
            price_df['Moving_Average_long'] = price_df['Close'].rolling(window=ma_long).mean()
        
        price_df['MA_Signal'] = (price_df['Moving_Average_short'] >= price_df['Moving_Average_long']).shift(1).fillna(False).astype(int).replace({0: -1, 1: 1})
        price_df['MA_Signal'].iloc[:ma_long] = None
        price_df['MA_returns'] = price_df['MA_Signal']*price_df['logreturns']

    if "Relative Strength Index (RSI)" in selected_indicators:
        price_df.ta.rsi(length = rsi_length, append=True)
        lower_threshold, upper_threshold = map(int, rsi_thresholds.split('/'))

        price_df['RSI_Signal'] = price_df[f'RSI_{rsi_length}'].apply(lambda x: -1 if x > upper_threshold else (1 if x < lower_threshold else 0)).shift(1)
        price_df['RSI_Signal'].iloc[:(rsi_length+1)] = None
        price_df['RSI_returns'] = price_df['RSI_Signal']*price_df['logreturns']

    if "Moving Average Converge Divergence (MACD)" in selected_indicators:
        price_df.ta.macd(close = "Close", fast = macd_fast, slow = macd_slow, signal = macd_signal, append=True)

        price_df['MACD_Signal'] = price_df[f'MACDh_{macd_fast}_{macd_slow}_{macd_signal}'].apply(lambda x: -1 if x < 0 else (1 if x > 0 else 0)).shift(1)
        price_df['MACD_Signal'].iloc[:(macd_slow+macd_signal-1)] = None
        price_df['MACD_returns'] = price_df['MACD_Signal']*price_df['logreturns']

    if "Directional Movement Index (DMI)" in selected_indicators:
        price_df.ta.adx(close = "Close", length = dmi_length, lensig = adx_smoothing, append=True)

        price_df['DMI_Signal'] = (price_df[f'DMP_{dmi_length}'] >= price_df[f'DMN_{dmi_length}']).shift(1).fillna(False).astype(int).replace({0: -1, 1: 1})
        price_df['DMI_Signal'].iloc[:(dmi_length+1)] = None
        price_df['DMI_returns'] = price_df['DMI_Signal']*price_df['logreturns']

    if "Trading Range Breakout" in selected_indicators:
        price_df['Max'] = price_df['Close'].rolling(window=trb_length).max()
        price_df['Min'] = price_df['Close'].rolling(window=trb_length).min()

        price_df['TRB_Condition'] = (price_df['Max'] < (price_df['Min']*(1 + trb_width))).fillna(False).astype(int)

        price_df['Prev_Max'] = price_df['Max'].shift(1)
        price_df['Prev_Min'] = price_df['Min'].shift(1)

        price_df['TRB_Signal'] = price_df.apply(
            lambda row: 1 if row['Close'] > row['Prev_Max'] and row['TRB_Condition'] == 1 else
                        -1 if row['Close'] < row['Prev_Min'] and row['TRB_Condition'] == 1 else 0,
            axis=1
        ).shift(1)

        price_df['TRB_Signal'].iloc[:trb_length] = None

        modified_signal = price_df['TRB_Signal'].copy()
        #Holding period after the signal
        for i in range(1, len(modified_signal)):
            if modified_signal[i-1] == 0 and modified_signal[i] in [-1, 1]:
                value_to_keep = modified_signal[i]
                for j in range(1, trb_num_periods_to_hold):
                    if i + j < len(modified_signal) and modified_signal[i + j] == 0:
                        modified_signal[i + j] = value_to_keep
                    elif i + j < len(modified_signal) and modified_signal[i + j] == -value_to_keep:
                        break

        price_df['TRB_Signal'] = modified_signal

        price_df['TRB_returns'] = price_df['TRB_Signal']*price_df['logreturns']

    return price_df

def calculate_statistics_buyandhold(col_returns, periods):
    stats = {}
    
    #Returns
    stats['Total Return'] = (1 + col_returns).cumprod()[-1] - 1

    stats['Ann. Mean Return'] = (1+col_returns.mean())**periods - 1
    
    #Risk
    stats['St. Dev.'] = col_returns.std() * np.sqrt(periods)

    stats['Sharpe'] = stats['Ann. Mean Return'] / stats['St. Dev.']

    negative_returns = col_returns[col_returns < 0]
    downside_deviation = negative_returns.std() * np.sqrt(periods)
    stats['Sortino'] = stats['Ann. Mean Return'] / downside_deviation

    rolling_max = (1 + col_returns).cumprod().cummax()
    daily_drawdown = (1 + col_returns).cumprod() / rolling_max - 1
    stats['Max Drawdown'] = daily_drawdown.min()

    #Equity curve
    initial_investment = 10000
    equity_curve = initial_investment * (1 + col_returns).cumprod()
    stats['Equity Curve'] = equity_curve

    return stats

def calculate_statistics(col_returns, col_signals, periods):
    stats = {}
    
    #Returns
    stats['Total Return'] = (1 + col_returns).cumprod()[-1] - 1

    stats['Ann. Mean Return'] = (1+col_returns.mean())**periods - 1
    
    #Risk
    stats['St. Dev.'] = col_returns.std() * np.sqrt(periods)

    stats['Sharpe'] = stats['Ann. Mean Return'] / stats['St. Dev.']

    negative_returns = col_returns[col_returns < 0]
    downside_deviation = negative_returns.std() * np.sqrt(periods)
    stats['Sortino'] = stats['Ann. Mean Return'] / downside_deviation

    rolling_max = (1 + col_returns).cumprod().cummax()
    daily_drawdown = (1 + col_returns).cumprod() / rolling_max - 1
    stats['Max Drawdown'] = daily_drawdown.min()
    
    #Trade statistics
    stats['Num. Trades'] = calculate_num_trades(col_signals)

    win_lose_list = win_lose_trades(col_signals, col_returns)
    stats['Win. Trades'] = win_lose_list[0]
    stats['Pct. Win. Trades'] = stats['Win. Trades'] / stats['Num. Trades']
    stats['Losing Trades'] = win_lose_list[1]
    stats['Pct. Losing Trades'] = stats['Losing Trades'] / stats['Num. Trades']
    stats['Win/Loss Ratio'] = stats['Win. Trades'] / max(1, stats['Losing Trades'])
    
    stats['Avg. Trade Duration'] = mean_trade_length(col_signals)

    if col_signals.iloc[-1] == 1:
        stats['Current Recommendation'] = 'BUY'
    elif col_signals.iloc[-1] == -1:
        stats['Current Recommendation'] = 'SELL'
    else:
        stats['Current Recommendation'] = 'NEUTRAL'

    #Equity curve
    initial_investment = 10000
    equity_curve = initial_investment * (1 + col_returns).cumprod()
    stats['Equity Curve'] = equity_curve
    
    return stats

#--------------------------

#SUPPORT (STYLES)
def color_high_green(val, reference):
    if val > reference:
        color = 'lime'  
    elif val < reference:
        color = '#FF440B'
    else:
        color = '#f2e1e1'
    return f'color: {color}'
            
def color_high_red(val, reference):
    if val > reference:
        color = '#FF440B'  
    elif val < reference:
        color = 'lime'
    else:
        color = '#f2e1e1'
    return f'color: {color}'

def get_bh_value(value, df):
    for col in df.columns[0:6]:
        if value in df[col].values:
            return df.loc['B&H', col]

def color_recommendation(val):
    if val == 'BUY':
        return 'color: lime'
    elif val == 'SELL':
        return 'color: #FF440B'
    else:
        return ''

#MAIN (FINAL DATA FRAME + STYLES) 
def do_ta_analysis(price_df):
    signal_columns = [col for col in price_df.columns if col.endswith('_Signal')]

    ta_statistics = pd.DataFrame()

    #ADD B&H    
    statistics_bh = calculate_statistics_buyandhold(price_df['logreturns'], 252)
    statistics_for_df_bh = {key: value for key, value in statistics_bh.items() if key != 'Equity Curve'}
    statistics_df_bh = pd.DataFrame(statistics_for_df_bh, index=[0])
    statistics_df_bh.index = ['B&H']
    ta_statistics = pd.concat([ta_statistics, statistics_df_bh])

    #ADD INDICATORS
    for col_signals in signal_columns:
        indicator = col_signals.split('_')[0]
        col_returns = indicator + '_returns'
        statistics = calculate_statistics(price_df[col_returns], price_df[col_signals], 252)
        statistics_for_df = {key: value for key, value in statistics.items() if key != 'Equity Curve'}
        statistics_df = pd.DataFrame(statistics_for_df, index=[0])
        statistics_df.index = [indicator]
        ta_statistics = pd.concat([ta_statistics, statistics_df])

    return ta_statistics

def apply_styles_df(ta_statistics):
    ta_statistics_styled = ta_statistics.style.applymap(lambda val: color_high_green(val, get_bh_value(val, ta_statistics)), subset=['Total Return',
                                                                                                                                'Ann. Mean Return',
                                                                                                                                'Sharpe',
                                                                                                                                'Sortino',
                                                                                                                                'Max Drawdown'])
    
    ta_statistics_styled = ta_statistics_styled.applymap(lambda val: color_high_red(val, get_bh_value(val, ta_statistics)), subset = ['St. Dev.'])
    ta_statistics_styled = ta_statistics_styled.format(c.styles_statistics_df)
    ta_statistics_styled = ta_statistics_styled.applymap(lambda x: color_recommendation(x), subset = ['Current Recommendation'])

    return ta_statistics_styled

def current_recommendation(ta_statistics):
    recommendation_counts = ta_statistics['Current Recommendation'].value_counts()
    buy_count = recommendation_counts.get('BUY', 0)
    sell_count = recommendation_counts.get('SELL', 0)
    neutral_count = recommendation_counts.get('NEUTRAL', 0)

    if buy_count == sell_count or buy_count == neutral_count or sell_count == neutral_count:
        recommendation = "NEUTRAL"
    else:
        recommendation = recommendation_counts.idxmax()

    if recommendation == 'BUY':
        background_color = 'green'
    elif recommendation == 'SELL':
        background_color = 'red'
    else:
        background_color = '#FF5500'

    st.markdown("<h4 style='text-align: center; font-size: 20px; font-family: serif;'>CURRENT TRADE RECOMMENDATION BASED ON THE SELECTED INDICATORS:</h4>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; font-size: 35px; font-family: serif; background-color: {background_color}; border-radius: 15px; padding: 10px;'>{recommendation}</h2>", unsafe_allow_html=True)   

#-------------------------------------------------------
#INFO SECTION
#-------------------------------------------------------

def format_value(value):
    suffixes = ["", "K", "M", "B", "T"]
    suffix_index = 0
    while value >= 1000 and suffix_index < len(suffixes) - 1:
        value /= 1000
        suffix_index += 1
    return f"${value:.1f}{suffixes[suffix_index]}"

def html_table(data):
    html = "<div id='custom-table' class='custom-table'>"
    
    html += "<div id='table-top' class='table-top'>"
    html += f"<div class='table-top-cell' style='width:129px; text-align:center;'>{data[0][0]}</div>"
    html += f"<div class='table-top-cell' style='border:none;'>{data[0][1]}</div>"
    html += "</div>"
    
    html += "<div id='table-middle' class='table-middle'>"
    for key, value in data[1:]:
        html += f"<div class='table-row'><div class='table-left'>{key}</div>"
        html += f"<div class='table-right'>{value}</div></div>"
    html += "</div>"
    
    html += "</div>"
    return html




    

    