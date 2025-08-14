"""Trading engine for automated operations."""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from trading_script import process_portfolio, load_latest_portfolio_state, set_data_dir


def run_automated_trading():
    """Execute trading logic in automated mode."""
    # Set data directory
    data_dir = project_root / "Scripts and CSV Files"
    set_data_dir(data_dir)
    
    # Load portfolio
    portfolio_file = str(data_dir / "chatgpt_portfolio_update.csv")
    
    try:
        chatgpt_portfolio, cash = load_latest_portfolio_state(portfolio_file)
        
        # Process portfolio without user interaction
        chatgpt_portfolio, cash = process_portfolio(
            chatgpt_portfolio,
            cash,
            interactive=False
        )
        
        print(f"✅ Trading engine completed. Portfolio value: ${cash + sum([row['cost_basis'] for _, row in chatgpt_portfolio.iterrows()]):.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Trading engine error: {e}")
        return False


if __name__ == "__main__":
    success = run_automated_trading()
    sys.exit(0 if success else 1)