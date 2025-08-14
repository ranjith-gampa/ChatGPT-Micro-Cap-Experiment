"""Flask web application for ChatGPT Trading Experiment dashboard.
Optimized for Vercel deployment with minimal dependencies.
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import json
from pathlib import Path
import os

app = Flask(__name__)

# Project paths - look for CSV files in root directory for Vercel deployment
project_root = Path(__file__).resolve().parent


def load_portfolio_data():
    """Load portfolio data from CSV file."""
    portfolio_file = project_root / "chatgpt_portfolio_update.csv"
    
    try:
        if portfolio_file.exists():
            df = pd.read_csv(portfolio_file)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"Error loading portfolio data: {e}")
        return pd.DataFrame()


def load_trade_data():
    """Load trade log data from CSV file."""
    trade_file = project_root / "chatgpt_trade_log.csv"
    
    try:
        if trade_file.exists():
            df = pd.read_csv(trade_file)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"Error loading trade data: {e}")
        return pd.DataFrame()


def create_simple_chart_data(total_rows):
    """Create simple chart data without plotly dependency."""
    if total_rows.empty:
        return json.dumps({})
    
    try:
        # Convert dates to strings for JSON serialization
        dates = pd.to_datetime(total_rows['Date']).dt.strftime('%Y-%m-%d').tolist()
        values = total_rows['Total Equity'].tolist()
        
        chart_data = {
            "dates": dates,
            "values": values,
            "title": "Portfolio Performance Over Time"
        }
        return json.dumps(chart_data)
    except Exception as e:
        print(f"Error creating chart data: {e}")
        return json.dumps({})


@app.route('/')
def dashboard():
    """Main dashboard page with simplified charting."""
    # Load data
    portfolio = load_portfolio_data()
    trades = load_trade_data()
    
    # Prepare data for display
    portfolio_data = []
    chart_data = "{}"
    latest_stats = {}
    
    if not portfolio.empty:
        try:
            # Get latest portfolio positions (non-TOTAL rows)
            latest_date = portfolio['Date'].max()
            latest_portfolio = portfolio[
                (portfolio['Date'] == latest_date) & 
                (portfolio['Ticker'] != 'TOTAL')
            ]
            portfolio_data = latest_portfolio.to_dict('records')
            
            # Get performance data (TOTAL rows)
            total_rows = portfolio[portfolio['Ticker'] == 'TOTAL'].copy()
            total_rows = total_rows.sort_values('Date')
            
            if not total_rows.empty:
                # Create simple chart data
                chart_data = create_simple_chart_data(total_rows)
                
                # Latest statistics
                latest_stats = {
                    'total_equity': f"${total_rows['Total Equity'].iloc[-1]:,.2f}",
                    'cash_balance': f"${total_rows['Cash Balance'].iloc[-1]:,.2f}",
                    'total_pnl': f"${total_rows['PnL'].iloc[-1]:,.2f}",
                    'last_updated': latest_date
                }
        except Exception as e:
            print(f"Error processing portfolio data: {e}")
    
    # Recent trades
    trade_data = []
    if not trades.empty:
        try:
            recent_trades = trades.tail(10)
            trade_data = recent_trades.to_dict('records')
        except Exception as e:
            print(f"Error processing trade data: {e}")
    
    return render_template(
        'dashboard.html',
        portfolio=portfolio_data,
        trades=trade_data,
        chart_data=chart_data,
        stats=latest_stats
    )


@app.route('/api/portfolio')
def api_portfolio():
    """API endpoint for portfolio data."""
    try:
        portfolio = load_portfolio_data()
        
        if not portfolio.empty:
            # Return recent portfolio data
            latest_date = portfolio['Date'].max()
            latest_data = portfolio[portfolio['Date'] == latest_date]
            return latest_data.to_json(orient='records')
        else:
            return jsonify([])
    except Exception as e:
        print(f"Error in portfolio API: {e}")
        return jsonify([])


@app.route('/api/performance')
def api_performance():
    """API endpoint for performance data."""
    try:
        portfolio = load_portfolio_data()
        
        if not portfolio.empty:
            # Return TOTAL rows for performance tracking
            total_rows = portfolio[portfolio['Ticker'] == 'TOTAL']
            return total_rows.to_json(orient='records')
        else:
            return jsonify([])
    except Exception as e:
        print(f"Error in performance API: {e}")
        return jsonify([])


@app.route('/api/trades')
def api_trades():
    """API endpoint for trade data."""
    try:
        trades = load_trade_data()
        
        if not trades.empty:
            return trades.to_json(orient='records')
        else:
            return jsonify([])
    except Exception as e:
        print(f"Error in trades API: {e}")
        return jsonify([])


@app.route('/health')
def health_check():
    """Health check endpoint."""
    portfolio_exists = (project_root / "chatgpt_portfolio_update.csv").exists()
    trade_exists = (project_root / "chatgpt_trade_log.csv").exists()
    
    return jsonify({
        'status': 'healthy',
        'portfolio_file_exists': portfolio_exists,
        'trade_file_exists': trade_exists,
        'environment': 'vercel' if os.environ.get('VERCEL') else 'local'
    })


# Vercel expects the app to be available as a WSGI application
def handler(request):
    """Vercel handler function."""
    return app(request.environ, lambda status, headers: None)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))