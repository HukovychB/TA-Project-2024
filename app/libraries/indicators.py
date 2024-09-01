import streamlit as st
import plotly.graph_objs as go
import numpy as np
import pandas_ta as ta

# -------------------------------------------------------
# HOW TO ADD OTHER INDICATORS:
# -------------------------------------------------------
# 1. Modify indicators.py
# a.) Create function 'create_(indicator_name)' if it is to be displayed as a separate graph
#     or 'add_(indicator_name)' if it is to be added to the main graph
# b.) Create function 'execute_(indicator_name' if it is to be displayed
#
# 2. Modify main.py
# a.) Modify function 'execute_ta' if it is to be displayed
# b.) Modify function 'add_ta_to_df'
#
# 3. Modify web.py
# a.) Add placeholder '(indicator_name)_place' = st.empty() and execution if-statement if separate graph needs to be displayed
# b.) Add (indicator_name) to st.multiselect
# c.) Add section for parameters' choice
# d.) Add necessary variables to main.execute_ta and main.add_ta_to_df
# e.) Modify the logic of "REMOVE INDICATORS" button if separate graph is displayed


# -------------------------------------------------------
# SUPPORT
# -------------------------------------------------------
def rangebreaks(interval):
    """
    Generates range break configurations based on the specified interval.

    Args:
        interval (str): Time interval.

    Returns:
        list: A list of dictionaries defining the range breaks.
    """
    if "m" in interval or "h" in interval:
        rangebreaks = [
            dict(bounds=["sat", "mon"]),
            dict(bounds=[16, 9.5], pattern="hour"),
        ]
    else:
        rangebreaks = [
            dict(bounds=["sat", "mon"]),
        ]
    return rangebreaks


# LAYOUT OF SEPARATE INDICATOR GRAPHS
def indicator_graph_layout(fig, interval, height=400):
    """
    Updates the layout of a Plotly figure for an indicator graph.

    Args:
    fig (plotly.graph_objs._figure.Figure): Plotly figure object to update.
    interval (str): Time interval for range breaks in x-axis.
    height (int, optional): Height of the figure. Default is 400.

    Returns:
    None
    """
    fig.update_layout(
        height=height,
        dragmode="pan",
        uirevision="constant",
        xaxis=dict(
            showline=False,
            linecolor="dimgrey",
            gridcolor="black",
            rangebreaks=rangebreaks(interval),
            tickfont=dict(family="serif", size=12, color="linen"),
        ),
        yaxis=dict(
            showline=False,
            linecolor="dimgrey",
            gridcolor="dimgrey",
            tickfont=dict(family="serif", size=12, color="linen"),
        ),
        legend=dict(x=0, y=1.2, xanchor="left", yanchor="top"),
    )


# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
# INDICATOR GRAPHS
def add_mas(
    fig, ticker_data, period, interval, ma_period_short, ma_period_long, ema_chechbox
):
    """
    Adds moving averages (MA) to a Plotly figure based on the given parameters.

    Args:
        fig (plotly.graph_objs._figure.Figure): Plotly figure object to update.
        ticker_data (yfinance.Ticker object): yfinance data of the ticker.
        period (str): Period for fetching historical data.
        interval (str): Interval for historical data.
        ma_period_short (int): Period for short moving average.
        ma_period_long (int): Period for long moving average.
        ema_chechbox (bool): If True, calculates exponential moving averages (EMAs); otherwise, calculates simple moving averages (SMAs).

    Returns:
        plotly.graph_objs._figure.Figure: Updated Plotly figure object with moving averages added.
    """
    price_df = ticker_data.history(period=period, interval=interval)

    if ema_chechbox:
        price_df["Moving_Average_short"] = ta.ema(
            close=price_df["Close"], length=ma_period_short
        )
        price_df["Moving_Average_long"] = ta.ema(
            close=price_df["Close"], length=ma_period_long
        )
    else:
        price_df["Moving_Average_short"] = (
            price_df["Close"].rolling(window=ma_period_short).mean()
        )
        price_df["Moving_Average_long"] = (
            price_df["Close"].rolling(window=ma_period_long).mean()
        )

    fig.data = [trace for trace in fig.data if "MA" not in trace.name]

    if ma_period_short > 1:
        fig.add_trace(
            go.Scatter(
                x=price_df.index,
                y=price_df["Moving_Average_short"],
                mode="lines",
                line=dict(color="#FF5500", width=1),
                name=f"{ma_period_short}-MA",
            )
        )
    fig.add_trace(
        go.Scatter(
            x=price_df.index,
            y=price_df["Moving_Average_long"],
            mode="lines",
            line=dict(color="lightgreen", width=1),
            name=f"{ma_period_long}-MA",
        )
    )

    fig.data = list(fig.data[1:]) + [fig.data[0]]

    fig.data[-1].update(showlegend=False)

    return fig


def add_channels(fig, ticker_data, period, interval, trb_length, trb_width):
    """
    Adds trading range boundaries to a Plotly figure based on the given parameters.

    Args:
        fig (plotly.graph_objs._figure.Figure): Plotly figure object to update.
        ticker_data (yfinance.Ticker object): yfinance data of the ticker.
        period (str): Period for fetching historical data.
        interval (str): Interval for historical data.
        trb_length (int): Length of the trading range boundary window.
        trb_width (float): Width multiplier for trading range boundaries as a percentage of the support line.

    Returns:
        plotly.graph_objs._figure.Figure: Updated Plotly figure object with trading range boundaries added.
    """
    price_df = ticker_data.history(period=period, interval=interval)
    price_df["Max"] = price_df["Close"].rolling(window=trb_length).max()
    price_df["Min"] = price_df["Close"].rolling(window=trb_length).min()

    condition = price_df["Max"] > price_df["Min"] * (1 + trb_width)
    price_df.loc[condition, ["Max", "Min"]] = np.nan

    fig.data = [trace for trace in fig.data if "Range" not in trace.name]

    fig.add_trace(
        go.Scatter(
            x=price_df.index,
            y=price_df["Max"],
            mode="lines",
            line=dict(color="lightskyblue", width=1.5),
            name=f"{trb_length}/{trb_width}-Range Resistance",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=price_df.index,
            y=price_df["Min"],
            mode="lines",
            line=dict(color="lightskyblue", width=1.5),
            name=f"{trb_length}/{trb_width}-Range Support",
        )
    )
    return fig


def create_rsi(ticker_data, period, interval, rsi_length, rsi_thresholds, rsi_checkbox):
    """
    Creates a Plotly figure displaying the Relative Strength Index (RSI) and its thresholds.

    Args:
        ticker_data (yfinance.Ticker object): yfinance data of the ticker.
        period (str): Period for fetching historical data (e.g., '1y', '3mo').
        interval (str): Interval for historical data (e.g., '1d', '1h').
        rsi_length (int): Length of RSI calculation period.
        rsi_thresholds (str): Lower and upper RSI thresholds separated by '/' (e.g., '30/70').
        rsi_checkbox (bool): If True, calculates and plots the SMA of RSI.

    Returns:
        plotly.graph_objs._figure.Figure: Plotly figure object displaying RSI and its thresholds.
    """
    price_df = ticker_data.history(period=period, interval=interval)
    fig = go.Figure()

    price_df.ta.rsi(length=rsi_length, append=True)

    fig.add_trace(
        go.Scatter(
            x=price_df.index,
            y=price_df[f"RSI_{rsi_length}"],
            mode="lines",
            line=dict(color="lime", width=1.5),
            name=f"RSI-{rsi_length}",
        )
    )

    lower_threshold, upper_threshold = map(int, rsi_thresholds.split("/"))

    fig.add_shape(
        type="line",
        x0=price_df.index[0],
        y0=lower_threshold,
        x1=price_df.index[-1],
        y1=lower_threshold,
        line=dict(color="#FF440B", width=1, dash="dash"),
        name=f"Lower Threshold ({lower_threshold})",
    )
    fig.add_shape(
        type="line",
        x0=price_df.index[0],
        y0=upper_threshold,
        x1=price_df.index[-1],
        y1=upper_threshold,
        line=dict(color="#FF440B", width=1, dash="dash"),
        name=f"Upper Threshold ({upper_threshold})",
    )

    indicator_graph_layout(fig, interval, height=300)

    if rsi_checkbox:
        price_df.ta.sma(close=f"RSI_{rsi_length}", length=rsi_length, append=True)

        fig.add_trace(
            go.Scatter(
                x=price_df.index,
                y=price_df[f"SMA_{rsi_length}"],
                mode="lines",
                line=dict(color="#FF5500", width=1),
                name=f"{rsi_length}-MA",
            )
        )

    return fig


def create_macd(ticker_data, period, interval, macd_fast, macd_slow, macd_signal):
    """
    Creates a Plotly figure displaying the Moving Average Convergence Divergence (MACD) and its components.

    Args:
        ticker_data (yfinance.Ticker object): yfinance data of the ticker.
        period (str): Period for fetching historical data (e.g., '1y', '3mo').
        interval (str): Interval for historical data (e.g., '1d', '1h').
        macd_fast (int): Fast length for MACD calculation.
        macd_slow (int): Slow length for MACD calculation.
        macd_signal (int): Signal length for MACD calculation.

    Returns:
        plotly.graph_objs._figure.Figure: Plotly figure object displaying MACD, its signal line, and histogram.
    """
    price_df = ticker_data.history(period=period, interval=interval)
    fig = go.Figure()

    price_df.ta.macd(
        close="Close", fast=macd_fast, slow=macd_slow, signal=macd_signal, append=True
    )

    fig.add_trace(
        go.Scatter(
            x=price_df.index,
            y=price_df[f"MACD_{macd_fast}_{macd_slow}_{macd_signal}"],
            mode="lines",
            line=dict(color="lime", width=1.5),
            name="MACD_line",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=price_df.index,
            y=price_df[f"MACDs_{macd_fast}_{macd_slow}_{macd_signal}"],
            mode="lines",
            line=dict(color="#FF5500", width=1.5),
            name="Signal_line",
        )
    )

    fig.add_trace(
        go.Bar(
            x=price_df.index,
            y=price_df[f"MACDh_{macd_fast}_{macd_slow}_{macd_signal}"],
            marker_color="#FF440B",
            name="MACD_Histogram",
        )
    )

    indicator_graph_layout(fig, interval)

    return fig


def create_dmi(ticker_data, period, interval, length, adx_smoothing):
    """
    Creates a Plotly figure displaying the Directional Movement Index (DMI) and its components.

    Args:
        ticker_data (yfinance.Ticker object): yfinance data of the ticker.
        period (str): Period for fetching historical data (e.g., '1y', '3mo').
        interval (str): Interval for historical data (e.g., '1d', '1h').
        length (int): Length for calculating DMI.
        adx_smoothing (int): Smoothing period for ADX calculation.

    Returns:
        plotly.graph_objs._figure.Figure: Plotly figure object displaying ADX, DI+, and DI-.
    """
    price_df = ticker_data.history(period=period, interval=interval)
    fig = go.Figure()

    price_df.ta.adx(close="Close", length=length, lensig=adx_smoothing, append=True)

    fig.add_trace(
        go.Scatter(
            x=price_df.index,
            y=price_df[f"ADX_{adx_smoothing}"],
            mode="lines",
            line=dict(color="#FF5500", width=1.5),
            name="ADX",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=price_df.index,
            y=price_df[f"DMP_{length}"],
            mode="lines",
            line=dict(color="lime", width=1.5),
            name="DI+",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=price_df.index,
            y=price_df[f"DMN_{length}"],
            mode="lines",
            line=dict(color="#FF440B", width=1.5),
            name="DI-",
        )
    )

    indicator_graph_layout(fig, interval)

    return fig


# EXECUTE TA GRAPHS
def execute_ma(
    ticker_data,
    period_input,
    interval_input,
    graph,
    ma_short,
    ma_long,
    ema_checkbox,
    graph_place,
):
    """
    Executes the calculation and plotting of moving averages (MA) on a specified graph.

    Args:
        ticker_data (yfinance.Ticker object): yfinance data of the ticker.
        period_input (str): Period for fetching historical data (e.g., '1y', '3mo').
        interval_input (str): Interval for historical data (e.g., '1d', '1h').
        graph (plotly.graph_objs._figure.Figure): Plotly figure object to update.
        ma_short (int): Period for short moving average.
        ma_long (int): Period for long moving average.
        ema_checkbox (bool): If True, calculates exponential moving averages (EMAs); otherwise, calculates simple moving averages (SMAs).
        graph_place: Placeholder for displaying the graph.

    Returns:
        None
    """
    if ma_short >= ma_long:
        st.error(
            "The parameter for the short MA should be smaller than the parameter for the long MA. Please insert valid values.",
            icon="❗",
        )
    else:
        st.session_state.graph = add_mas(
            graph,
            ticker_data,
            period_input,
            interval_input,
            ma_short,
            ma_long,
            ema_checkbox,
        )
        graph_place.plotly_chart(st.session_state.graph, config=dict(scrollZoom=True))


def execute_trb(
    ticker_data, period_input, interval_input, graph, trb_length, trb_width, graph_place
):
    """
    Executes the calculation and plotting of trading range boundaries (TRB) on a specified graph.

    Args:
        ticker_data (yfinance.Ticker object): yfinance data of the ticker.
        period_input (str): Period for fetching historical data (e.g., '1y', '3mo').
        interval_input (str): Interval for historical data (e.g., '1d', '1h').
        graph (plotly.graph_objs._figure.Figure): Plotly figure object to update.
        trb_length (int): Length of the trading range boundary window.
        trb_width (float): Width multiplier for trading range boundaries.
        graph_place: Placeholder for displaying the graph.

    Returns:
        None
    """
    st.session_state.graph = add_channels(
        graph, ticker_data, period_input, interval_input, trb_length, trb_width
    )
    graph_place.plotly_chart(st.session_state.graph, config=dict(scrollZoom=True))


def execute_rsi(
    ticker_data,
    period_input,
    interval_input,
    rsi_length,
    rsi_thresholds,
    rsi_checkbox,
    RSI_place,
):
    """
    Executes the calculation and plotting of the Relative Strength Index (RSI) on a specified graph.

    Args:
        ticker_data (yfinance.Ticker object): yfinance data of the ticker.
        period_input (str): Period for fetching historical data (e.g., '1y', '3mo').
        interval_input (str): Interval for historical data (e.g., '1d', '1h').
        rsi_length (int): Length of RSI calculation period.
        rsi_thresholds (str): Lower and upper RSI thresholds separated by '/' (e.g., '30/70').
        rsi_checkbox (bool): If True, calculates and plots the SMA of RSI.
        RSI_place: Placeholder for displaying the RSI graph.

    Returns:
        None
    """
    rsi_graph = create_rsi(
        ticker_data,
        period_input,
        interval_input,
        rsi_length,
        rsi_thresholds,
        rsi_checkbox,
    )
    RSI_place.plotly_chart(rsi_graph, config=dict(scrollZoom=True))


def execute_macd(
    ticker_data,
    period_input,
    interval_input,
    macd_fast,
    macd_slow,
    macd_signal,
    MACD_place,
):
    """
    Executes the calculation and plotting of the Moving Average Convergence Divergence (MACD) on a specified graph.

    Args:
        ticker_data (yfinance.Ticker object): yfinance data of the ticker.
        period_input (str): Period for fetching historical data (e.g., '1y', '3mo').
        interval_input (str): Interval for historical data (e.g., '1d', '1h').
        macd_fast (int): Fast length for MACD calculation.
        macd_slow (int): Slow length for MACD calculation.
        macd_signal (int): Signal length for MACD calculation.
        MACD_place: Placeholder for displaying the MACD graph.

    Returns:
        None
    """
    if macd_fast >= macd_slow:
        st.error(
            "The parameter for the fast MA should be smaller than the parameter for the slow MA. Please insert valid values.",
            icon="❗",
        )
    else:
        macd_graph = create_macd(
            ticker_data, period_input, interval_input, macd_fast, macd_slow, macd_signal
        )
        MACD_place.plotly_chart(macd_graph, config=dict(scrollZoom=True))


def execute_dmi(
    ticker_data, period_input, interval_input, dmi_length, adx_smoothing, DMI_place
):
    """
    Executes the calculation and plotting of the Directional Movement Index (DMI) on a specified graph.

    Args:
        ticker_data (yfinance.Ticker object): yfinance data of the ticker.
        period_input (str): Period for fetching historical data (e.g., '1y', '3mo').
        interval_input (str): Interval for historical data (e.g., '1d', '1h').
        dmi_length (int): Length for calculating DMI.
        adx_smoothing (int): Smoothing period for ADX calculation.
        DMI_place: Placeholder for displaying the DMI graph.

    Returns:
        None
    """
    dmi_graph = create_dmi(
        ticker_data, period_input, interval_input, dmi_length, adx_smoothing
    )
    DMI_place.plotly_chart(dmi_graph, config=dict(scrollZoom=True))
