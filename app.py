"""Flask web application for ChatGPT Trading Experiment dashboard."""

from flask import Flask, render_template, jsonify
import pandas as pd
import plotly.graph_objects as go
import plotly.utils
from pathlib import Path
import json

app = Flask(__name__)

# Project paths
project_root = Path(__file__).resolve().parent
data_dir = project_root / "Scripts and CSV Files"


def load_portfolio_data():
    """Load portfolio data from CSV file."""
    portfolio_file = data_dir / "chatgpt_portfolio_update.csv"
    
    if portfolio_file.exists():
        df = pd.read_csv(portfolio_file)
        return df
    else:
        return pd.DataFrame()


def load_trade_data():
    """Load trade log data from CSV file."""
    trade_file = data_dir / "chatgpt_trade_log.csv"
    
    if trade_file.exists():
        df = pd.read_csv(trade_file)
        return df
    else:
        return pd.DataFrame()


@app.route('/')
def dashboard():
    """Main dashboard page."""
    # Load data
    portfolio = load_portfolio_data()
    trades = load_trade_data()
    
    # Prepare data for display
    portfolio_data = []
    performance_data = []
    latest_stats = {}
    
    if not portfolio.empty:
        # Get latest portfolio positions (non-TOTAL rows)
        latest_date = portfolio['Date'].max()
        latest_portfolio = portfolio[
            (portfolio['Date'] == latest_date) & 
            (portfolio['Ticker'] != 'TOTAL')
        ]
        portfolio_data = latest_portfolio.to_dict('records')
        
        # Get performance data (TOTAL rows)
        total_rows = portfolio[portfolio['Ticker'] == 'TOTAL'].copy()
        total_rows['Date'] = pd.to_datetime(total_rows['Date'])
        total_rows = total_rows.sort_values('Date')
        
        if not total_rows.empty:
            # Create performance chart
            try:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=total_rows['Date'],
                    y=total_rows['Total Equity'],
                    mode='lines+markers',
                    name='ChatGPT Portfolio',
                    line=dict(color='#2E8B57', width=3),
                    marker=dict(size=6)
                ))
                
                fig.update_layout(
                    title='Portfolio Performance Over Time',
                    xaxis_title='Date',
                    yaxis_title='Portfolio Value ($)',
                    template='plotly_white',
                    height=400
                )
                
                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            except Exception as e:
                print(f"Error creating Plotly figure: {e}")
                # Fallback: empty chart or error message
                fallback_fig = {
                    "data": [],
                    "layout": {
                        "title": "Error loading chart",
                        "xaxis": {"title": "Date"},
                        "yaxis": {"title": "Portfolio Value ($)"}
                    }
                }
                graphJSON = json.dumps(fallback_fig)
            try:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=total_rows['Date'],
                    y=total_rows['Total Equity'],
                    mode='lines+markers',
                    name='ChatGPT Portfolio',
                    line=dict(color='#2E8B57', width=3),
                    marker=dict(size=6)
                ))
                
                fig.update_layout(
                    title='Portfolio Performance Over Time',
                    xaxis_title='Date',
                    yaxis_title='Portfolio Value ($)',
                    template='plotly_white',
                    height=400
                )
                
                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            except Exception as e:
                print(f"Error creating Plotly figure: {e}")
                # Fallback: empty chart or error message
                fallback_fig = {
                    "data": [],
                    "layout": {
                        "title": "Error loading chart",
                        "xaxis": {"title": "Date"},
                        "yaxis": {"title": "Portfolio Value ($)"}
                    }
                }
                graphJSON = json.dumps(fallback_fig)
            
            # Latest statistics
            latest_stats = {
                'total_equity': f"${total_rows['Total Equity'].iloc[-1]:,.2f}",
                'cash_balance': f"${total_rows['Cash Balance'].iloc[-1]:,.2f}",
                'total_pnl': f"${total_rows['PnL'].iloc[-1]:,.2f}",
                'last_updated': latest_date
            }
        else:
            graphJSON = json.dumps({})
    else:
        graphJSON = json.dumps({})
    
    # Recent trades
    trade_data = []
    if not trades.empty:
        recent_trades = trades.tail(10)
        trade_data = recent_trades.to_dict('records')
    
    return render_template(
        'dashboard.html',
        portfolio=portfolio_data,
        trades=trade_data,
        graph=graphJSON,
        stats=latest_stats
    )


@app.route('/api/portfolio')
def api_portfolio():
    """API endpoint for portfolio data."""
    portfolio = load_portfolio_data()
    
    if not portfolio.empty:
        # Return recent portfolio data
        latest_date = portfolio['Date'].max()
        latest_data = portfolio[portfolio['Date'] == latest_date]
        return latest_data.to_json(orient='records')
    else:
        return jsonify([])


@app.route('/api/performance')
def api_performance():
    """API endpoint for performance data."""
    portfolio = load_portfolio_data()
    
    if not portfolio.empty:
        # Return TOTAL rows for performance tracking
        total_rows = portfolio[portfolio['Ticker'] == 'TOTAL']
        return total_rows.to_json(orient='records')
    else:
        return jsonify([])


@app.route('/api/trades')
def api_trades():
    """API endpoint for trade data."""
    trades = load_trade_data()
    
    if not trades.empty:
        return trades.to_json(orient='records')
    else:
        return jsonify([])


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'portfolio_file_exists': (data_dir / "chatgpt_portfolio_update.csv").exists(),
        'trade_file_exists': (data_dir / "chatgpt_trade_log.csv").exists()
    })


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)