import yfinance as yf
import streamlit as st
import plotly.graph_objs as go

def fetch_data(ticker_input):
    ticker_data = yf.Ticker(ticker_input)
    price = ticker_data.history(period = 'max')

    if not price.empty:
        return ticker_data
    else:
        st.error("Error: The ticker is not recognized. Please provide a valid symbol listed on Yahoo Finance (https://finance.yahoo.com/).", icon="🚨")

def create_graph(ticker_data, period):
    price_df = ticker_data.history(period = period)
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
            rangebreaks=[                 
            dict(bounds=["sat", "mon"])
            ],
            tickfont=dict(family='serif', size=12, color='linen')                
        ),
        yaxis=dict(
        showline=False,
        linecolor='dimgrey',            
        gridcolor='dimgrey',
        tickfont=dict(family='serif', size=12, color='linen')               
        )
    )

    return fig

def add_mas(fig, ticker_data, period, ma_period_short, ma_period_long):
    price_df = ticker_data.history(period=period)
    price_df['Moving_Average_short'] = price_df['Close'].rolling(window=ma_period_short).mean()
    price_df['Moving_Average_long'] = price_df['Close'].rolling(window=ma_period_long).mean()
    n_traces = len(fig.data)

    if n_traces >= 2:
        fig.data = [fig.data[-1]]

    if ma_period_short > 1:
        fig.add_trace(go.Scatter(
            x=price_df.index,
            y=price_df['Moving_Average_short'],
            mode='lines',
            line=dict(color='#FF5500', width=2),
            name=f'{ma_period_short}-Day MA'
        ))
    fig.add_trace(go.Scatter(
    x=price_df.index,
    y=price_df['Moving_Average_long'],
    mode='lines',
    line=dict(color='lightgreen', width=2),
    name=f'{ma_period_long}-Day MA'
    ))

    fig.data = list(fig.data[1:]) + [fig.data[0]]

    fig.data[-1].update(showlegend=False)

    fig.update_layout(
        legend=dict(
            x=0,          
            y=1,          
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



    

    