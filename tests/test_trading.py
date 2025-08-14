"""Basic tests for trading functionality."""

import pytest
import sys
from pathlib import Path
import pandas as pd

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from src.data_fetcher import DataFetcher
from src.decision_maker import DecisionMaker
import trading_script


class TestDataFetcher:
    """Test data fetching functionality."""
    
    def test_data_fetcher_initialization(self):
        """Test that DataFetcher can be initialized."""
        fetcher = DataFetcher()
        assert fetcher is not None
    
    def test_get_current_price_basic(self):
        """Test basic price fetching functionality."""
        fetcher = DataFetcher()
        # Test with a major stock that should always have data
        price = fetcher.get_current_price("AAPL")
        # Price should be a positive number or None (if market closed/error)
        assert price is None or (isinstance(price, float) and price > 0)


class TestDecisionMaker:
    """Test decision making functionality."""
    
    def test_decision_maker_initialization(self):
        """Test that DecisionMaker can be initialized."""
        decision_maker = DecisionMaker()
        assert decision_maker is not None
    
    def test_generate_trading_prompt(self):
        """Test prompt generation."""
        decision_maker = DecisionMaker()
        
        portfolio_data = {
            "cash": 100.0,
            "positions": [
                {"ticker": "TEST", "shares": 10, "cost_basis": 50.0}
            ]
        }
        
        market_data = {
            "TEST": {"price": 5.5, "change": 0.1}
        }
        
        prompt = decision_maker.generate_trading_prompt(portfolio_data, market_data)
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "PORTFOLIO SUMMARY" in prompt
        assert "CURRENT MARKET DATA" in prompt


class TestTradingScript:
    """Test core trading script functionality."""
    
    def test_trading_script_import(self):
        """Test that trading_script module can be imported."""
        assert trading_script is not None
        assert hasattr(trading_script, 'process_portfolio')
        assert hasattr(trading_script, 'daily_results')
    
    def test_process_portfolio_with_empty_data(self):
        """Test portfolio processing with empty data."""
        # Create empty portfolio
        empty_portfolio = pd.DataFrame(columns=['ticker', 'shares', 'buy_price', 'stop_loss', 'cost_basis'])
        cash = 100.0
        
        try:
            # This should not crash
            result_portfolio, result_cash = trading_script.process_portfolio(
                empty_portfolio, 
                cash, 
                interactive=False
            )
            
            assert isinstance(result_portfolio, pd.DataFrame)
            assert isinstance(result_cash, float)
            assert result_cash == cash  # Cash should remain unchanged
            
        except Exception as e:
            # If there's an exception, it should be a controlled one
            assert "weekend" in str(e).lower() or "market" in str(e).lower()


if __name__ == "__main__":
    pytest.main([__file__])