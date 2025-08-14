"""Data fetching utilities for market data."""

import yfinance as yf
import pandas as pd
from typing import Dict, List, Optional
import requests
import os


class DataFetcher:
    """Handles fetching market data from various sources."""
    
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    def get_stock_data(self, ticker: str, period: str = "1d") -> Optional[pd.DataFrame]:
        """
        Fetch stock data using yfinance.
        
        Args:
            ticker: Stock ticker symbol
            period: Data period (1d, 5d, 1mo, etc.)
        
        Returns:
            DataFrame with stock data or None if error
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period=period)
            return data
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None
    
    def get_current_price(self, ticker: str) -> Optional[float]:
        """
        Get current stock price.
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            Current price or None if error
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            if not data.empty:
                return float(data['Close'].iloc[-1])
            return None
        except Exception as e:
            print(f"Error fetching current price for {ticker}: {e}")
            return None
    
    def get_multiple_prices(self, tickers: List[str]) -> Dict[str, float]:
        """
        Get current prices for multiple tickers.
        
        Args:
            tickers: List of ticker symbols
        
        Returns:
            Dictionary mapping ticker to current price
        """
        prices = {}
        for ticker in tickers:
            price = self.get_current_price(ticker)
            if price is not None:
                prices[ticker] = price
        return prices
    
    def get_market_data_alpha_vantage(self, ticker: str) -> Optional[Dict]:
        """
        Fetch data using Alpha Vantage API (backup/alternative source).
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            Market data dictionary or None if error
        """
        if not self.alpha_vantage_key:
            print("Alpha Vantage API key not configured")
            return None
        
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': ticker,
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'Global Quote' in data:
                quote = data['Global Quote']
                return {
                    'symbol': quote.get('01. symbol'),
                    'price': float(quote.get('05. price', 0)),
                    'change': float(quote.get('09. change', 0)),
                    'change_percent': quote.get('10. change percent'),
                }
            
            return None
            
        except Exception as e:
            print(f"Error fetching Alpha Vantage data for {ticker}: {e}")
            return None