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
                                increasing_line_color='lightgreen',
                                decreasing_line_color='orangered',   
                                whiskerwidth=0.1))
    fig.update_layout(
        title=f"Graph {ticker_data.info.get('longName').upper()}",
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

    st.plotly_chart(fig, config=dict(scrollZoom=True))

if __name__ == '__main__':
    stock = yf.Ticker("AAPL")
    stock.history(period = 'max')



    

    