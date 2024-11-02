# utils.py (or any file where you want to keep utility functions)

import yfinance as yf

def get_stock_tickers():
    # Fetch the stock tickers using the Tickers class
    tickers = yf.Ticker("MSFT")  # Empty string fetches all tickers, but you might want to limit it
    ticker_list = []
    print(tickers)
    # This will get the tickers from the Yahoo Finance dataset
    for ticker in tickers.tickers:
        ticker_list.append((ticker.ticker, ticker.ticker))
    print(ticker_list)
    return ticker_list[:100]  # Limit to the first 100 tickers for performance
