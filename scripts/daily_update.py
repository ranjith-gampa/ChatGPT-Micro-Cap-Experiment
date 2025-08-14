#!/usr/bin/env python3
"""Daily trading update script for automated operations."""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from trading_script import process_portfolio, daily_results, load_latest_portfolio_state, set_data_dir


def main():
    """Run daily portfolio update in non-interactive mode."""
    # Set data directory to Scripts and CSV Files
    data_dir = project_root / "Scripts and CSV Files"
    set_data_dir(data_dir)
    
    # Load current portfolio state
    portfolio_file = str(data_dir / "chatgpt_portfolio_update.csv")
    
    try:
        chatgpt_portfolio, cash = load_latest_portfolio_state(portfolio_file)
        
        # Process portfolio in non-interactive mode
        chatgpt_portfolio, cash = process_portfolio(
            chatgpt_portfolio, 
            cash, 
            interactive=False
        )
        
        # Generate and print daily results
        daily_results(chatgpt_portfolio, cash)
        
        print("✅ Daily portfolio update completed successfully")
        
    except Exception as e:
        print(f"❌ Error during daily update: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()