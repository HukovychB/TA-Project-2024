import yfinance as yf
import streamlit as st
import plotly.graph_objs as go
import numpy as np
import pandas_ta as ta

def fetch_data(ticker_input):
    ticker_data = yf.Ticker(ticker_input)
    price = ticker_data.history(period = 'max')

    if not price.empty:
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
    
    if 'm' in interval or 'h' in interval:
        rangebreaks = [
            dict(bounds=["sat", "mon"]),  
            dict(bounds=[16, 9.5], pattern="hour"), 
        ]
    else:
        rangebreaks = [
            dict(bounds=["sat", "mon"]), 
        ]
    
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
            rangebreaks= rangebreaks,
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

def add_mas(fig, ticker_data, period, interval, ma_period_short, ma_period_long, ema_chechbox):
    price_df = ticker_data.history(period=period, interval=interval)

    if ema_chechbox:
        price_df['Moving_Average_short'] = ta.ema(close=price_df['Close'], length=ma_period_short)
        price_df['Moving_Average_long'] = ta.ema(close=price_df['Close'], length=ma_period_long)
    else:
        price_df['Moving_Average_short'] = price_df['Close'].rolling(window=ma_period_short).mean()
        price_df['Moving_Average_long'] = price_df['Close'].rolling(window=ma_period_long).mean()

    fig.data = [trace for trace in fig.data if 'MA' not in trace.name]

    if ma_period_short > 1:
        fig.add_trace(go.Scatter(
            x=price_df.index,
            y=price_df['Moving_Average_short'],
            mode='lines',
            line=dict(color='#FF5500', width=1),
            name=f'{ma_period_short}-MA'
        ))
    fig.add_trace(go.Scatter(
    x=price_df.index,
    y=price_df['Moving_Average_long'],
    mode='lines',
    line=dict(color='lightgreen', width=1),
    name=f'{ma_period_long}-MA'
    ))

    fig.data = list(fig.data[1:]) + [fig.data[0]]

    fig.data[-1].update(showlegend=False)

    return fig

def add_channels(fig, ticker_data, period, interval, trb_length, trb_width):
    price_df = ticker_data.history(period=period, interval = interval)
    price_df['Max'] = price_df['Close'].rolling(window=trb_length).max()
    price_df['Min'] = price_df['Close'].rolling(window=trb_length).min()

    condition = price_df['Max'] > price_df['Min'] * (1 + trb_width)
    price_df.loc[condition, ['Max', 'Min']] = np.nan

    fig.data = [trace for trace in fig.data if 'Range' not in trace.name]

    fig.add_trace(go.Scatter(
        x=price_df.index,
        y=price_df['Max'],
        mode='lines',
        line=dict(color='lightskyblue', width=1.5),
        name=f'{trb_length}/{trb_width}-Range Resistance'
        ))
    fig.add_trace(go.Scatter(
        x=price_df.index,
        y=price_df['Min'],
        mode='lines',
        line=dict(color='lightskyblue', width=1.5),
        name=f'{trb_length}/{trb_width}-Range Support'
        ))
    return fig  

def create_rsi(ticker_data, period, interval, rsi_length, rsi_thresholds, rsi_checkbox):
    price_df = ticker_data.history(period = period, interval = interval)
    fig = go.Figure()

    price_df.ta.rsi(length = rsi_length, append=True)

    fig.add_trace(go.Scatter(
    x=price_df.index,
    y=price_df[f'RSI_{rsi_length}'],
    mode='lines',
    line=dict(color='lime', width=1.5),
    name=f'RSI-{rsi_length}'
    ))

    lower_threshold, upper_threshold = map(int, rsi_thresholds.split('/'))

    fig.add_shape(
        type="line",
        x0=price_df.index[0],
        y0=lower_threshold,
        x1=price_df.index[-1],
        y1=lower_threshold,
        line=dict(color="#FF440B", width=1, dash="dash"),
        name=f'Lower Threshold ({lower_threshold})'
    )
    fig.add_shape(
        type="line",
        x0=price_df.index[0],
        y0=upper_threshold,
        x1=price_df.index[-1],
        y1=upper_threshold,
        line=dict(color="#FF440B", width=1, dash="dash"),
        name=f'Upper Threshold ({upper_threshold})'
    )

    if 'm' in interval or 'h' in interval:
        rangebreaks = [
            dict(bounds=["sat", "mon"]),  
            dict(bounds=[16, 9.5], pattern="hour"), 
        ]
    else:
        rangebreaks = [
            dict(bounds=["sat", "mon"]), 
        ]

    fig.update_layout(
        height = 300,
        dragmode='pan',
        uirevision='constant',
        xaxis=dict(
            showline=False,
            linecolor='dimgrey',            
            gridcolor='black',
            rangebreaks=rangebreaks,
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
            y=1.2,          
            xanchor='left',
            yanchor='top'
        )     
    )

    if rsi_checkbox:
        price_df.ta.sma(close = f"RSI_{rsi_length}", length = rsi_length, append=True)

        fig.add_trace(go.Scatter(
            x=price_df.index,
            y=price_df[f'SMA_{rsi_length}'],
            mode='lines',
            line=dict(color='#FF5500', width=1),
            name=f'{rsi_length}-MA'
        ))

    return fig 

def create_macd(ticker_data, period, interval, macd_fast, macd_slow, macd_signal):
    price_df = ticker_data.history(period = period, interval = interval)
    fig = go.Figure()

    price_df.ta.macd(close = "Close", fast = macd_fast, slow = macd_slow, signal = macd_signal, append=True)

    fig.add_trace(go.Scatter(
    x=price_df.index,
    y=price_df[f'MACD_{macd_fast}_{macd_slow}_{macd_signal}'],
    mode='lines',
    line=dict(color='lime', width=1.5),
    name='MACD_line'
    ))

    fig.add_trace(go.Scatter(
    x=price_df.index,
    y=price_df[f'MACDs_{macd_fast}_{macd_slow}_{macd_signal}'],
    mode='lines',
    line=dict(color='#FF5500', width=1.5),
    name='Singal_line'
    ))

    fig.add_trace(go.Bar(
        x=price_df.index,
        y=price_df[f'MACDh_{macd_fast}_{macd_slow}_{macd_signal}'],
        marker_color='#FF440B',
        name='MACD_Histogram'
    ))

    if 'm' in interval or 'h' in interval:
        rangebreaks = [
            dict(bounds=["sat", "mon"]),  
            dict(bounds=[16, 9.5], pattern="hour"), 
        ]
    else:
        rangebreaks = [
            dict(bounds=["sat", "mon"]), 
        ]

    fig.update_layout(
        height = 400,
        dragmode='pan',
        uirevision='constant',
        xaxis=dict(
            showline=False,
            linecolor='dimgrey',            
            gridcolor='black',
            rangebreaks=rangebreaks,
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
            y=1.2,          
            xanchor='left',
            yanchor='top'
        )     
    )

    return fig 

def create_dmi(ticker_data, period, interval, length, adx_smoothing):
    price_df = ticker_data.history(period = period, interval = interval)
    fig = go.Figure()

    price_df.ta.adx(close = "Close", length = length, lensig = adx_smoothing, append=True)

    fig.add_trace(go.Scatter(
    x=price_df.index,
    y=price_df[f'ADX_{adx_smoothing}'],
    mode='lines',
    line=dict(color='#FF5500', width=1.5),
    name='ADX'
    ))

    fig.add_trace(go.Scatter(
    x=price_df.index,
    y=price_df[f'DMP_{length}'],
    mode='lines',
    line=dict(color='lime', width=1.5),
    name='DM+'
    ))

    fig.add_trace(go.Scatter(
    x=price_df.index,
    y=price_df[f'DMN_{length}'],
    mode='lines',
    line=dict(color='#FF440B', width=1.5),
    name='DM-'
    ))

    if 'm' in interval or 'h' in interval:
        rangebreaks = [
            dict(bounds=["sat", "mon"]),  
            dict(bounds=[16, 9.5], pattern="hour"), 
        ]
    else:
        rangebreaks = [
            dict(bounds=["sat", "mon"]), 
        ]

    fig.update_layout(
        height = 400,
        dragmode='pan',
        uirevision='constant',
        xaxis=dict(
            showline=False,
            linecolor='dimgrey',            
            gridcolor='black',
            rangebreaks=rangebreaks,
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
            y=1.2,          
            xanchor='left',
            yanchor='top'
        )     
    )

    return fig 


def do_analysis():
    pass


def format_value(value):
    suffixes = ["", "K", "M", "B", "T"]
    suffix_index = 0
    while value >= 1000 and suffix_index < len(suffixes) - 1:
        value /= 1000
        suffix_index += 1
    return f"${value:.1f}{suffixes[suffix_index]}"

def html_table(data):
    html = "<table class='custom-table'>"
    for key, value in data:
        html += f"<tr><td>{key}</td><td>{value}</td></tr>"
    html += "</table>"
    return html

# if __name__ == '__main__':
#     stock = yf.Ticker("AAPL")
#     stock.history(period = 'max')



    

    