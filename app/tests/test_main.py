import pytest

from app.libraries import main


def test_fetch_data():
    assert main.fetch_data("AAPL", "1y", "1d").history(period="max").empty == False
    assert main.fetch_data("MSFT", "1mo", "5m").history(period="max").empty == False
    assert main.fetch_data("nvda", "max", "1wk").history(period="max").empty == False
    assert main.fetch_data("btc-usd", "ytd", "1h").history(period="max").empty == False

    assert main.fetch_data("AAPL", "1y", "5m") == 1
    assert main.fetch_data("nvda", "max", "5m") == 1


def test_color_high_green():
    assert main.color_high_green(100, 100) == "color: #f2e1e1"
    assert main.color_high_green(100, 101) == "color: #FF440B"
    assert main.color_high_green(100, 99) == "color: lime"


def test_color_high_red():
    assert main.color_high_red(100, 100) == "color: #f2e1e1"
    assert main.color_high_red(100, 101) == "color: lime"
    assert main.color_high_red(100, 99) == "color: #FF440B"


def test_color_recommendation():
    assert main.color_recommendation("BUY") == "color: lime"
    assert main.color_recommendation("SELL") == "color: #FF440B"
    assert main.color_recommendation("Hold") == ""
    assert main.color_recommendation("Strong Buy") == ""
    assert main.color_recommendation("fdfsdf") == ""
    assert main.color_recommendation("buy") == ""
