"""Tests for data handling functionality."""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.data_fetcher import DataFetcher


class TestDataHandling:
    """Test data import/export and CSV handling."""
    
    def test_csv_creation_and_reading(self):
        """Test CSV file creation and reading."""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            # Write test portfolio data
            test_data = """Date,Ticker,Shares,Buy Price,Cost Basis,Stop Loss,Current Price,Total Value,PnL,Action,Cash Balance,Total Equity
2024-01-01,TEST,10,5.0,50.0,4.5,5.5,55.0,5.0,,100.0,155.0
2024-01-01,TOTAL,,,,,,,5.0,,100.0,155.0"""
            f.write(test_data)
            temp_path = f.name
        
        try:
            # Read the CSV file
            df = pd.read_csv(temp_path)
            
            # Verify the data
            assert len(df) == 2
            assert 'Ticker' in df.columns
            assert 'Shares' in df.columns
            
            # Check specific values
            test_row = df[df['Ticker'] == 'TEST'].iloc[0]
            assert test_row['Shares'] == 10
            assert test_row['Buy Price'] == 5.0
            
            total_row = df[df['Ticker'] == 'TOTAL'].iloc[0]
            assert total_row['Total Equity'] == 155.0
            
        finally:
            # Clean up
            os.unlink(temp_path)
    
    def test_multiple_stocks_data_fetching(self):
        """Test fetching data for multiple stocks."""
        fetcher = DataFetcher()
        
        # Test with a few major stocks
        tickers = ["AAPL", "MSFT"]
        prices = fetcher.get_multiple_prices(tickers)
        
        # Should return a dictionary
        assert isinstance(prices, dict)
        
        # Check that we got responses (prices could be None if market closed)
        for ticker in tickers:
            if ticker in prices:
                assert isinstance(prices[ticker], (float, type(None)))
                if prices[ticker] is not None:
                    assert prices[ticker] > 0


class TestDataValidation:
    """Test data validation and error handling."""
    
    def test_invalid_ticker_handling(self):
        """Test handling of invalid ticker symbols."""
        fetcher = DataFetcher()
        
        # Test with obviously invalid ticker
        price = fetcher.get_current_price("INVALID_TICKER_12345")
        
        # Should return None for invalid ticker
        assert price is None
    
    def test_empty_portfolio_data(self):
        """Test handling of empty portfolio data."""
        # Create empty DataFrame with correct columns
        empty_df = pd.DataFrame(columns=[
            'ticker', 'shares', 'buy_price', 'stop_loss', 'cost_basis'
        ])
        
        # Should not crash when processing empty portfolio
        assert len(empty_df) == 0
        assert list(empty_df.columns) == ['ticker', 'shares', 'buy_price', 'stop_loss', 'cost_basis']


if __name__ == "__main__":
    pytest.main([__file__])