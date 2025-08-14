#!/usr/bin/env python3
"""Generate reports and visualizations for the trading experiment."""

import os
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import json
import html

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))


def create_reports_directory():
    """Create reports directory for GitHub Pages deployment."""
    reports_dir = project_root / "reports"
    reports_dir.mkdir(exist_ok=True)
    return reports_dir


def generate_performance_chart(data_dir: Path, reports_dir: Path):
    """Generate performance chart comparing portfolio to market indices."""
    portfolio_file = data_dir / "chatgpt_portfolio_update.csv"
    
    if not portfolio_file.exists():
        print("Warning: Portfolio data not found, skipping chart generation")
        return
    
    # Load portfolio data
    df = pd.read_csv(portfolio_file)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Filter for TOTAL rows (summary data)
    total_rows = df[df['Ticker'] == 'TOTAL'].copy()
    
    if total_rows.empty:
        print("Warning: No TOTAL summary rows found in portfolio data")
        return
    
    # Create the performance chart
    plt.figure(figsize=(12, 8))
    plt.plot(total_rows['Date'], total_rows['Total Equity'], 
             label='ChatGPT Portfolio', linewidth=2, color='#2E8B57')
    
    plt.title('ChatGPT Micro-Cap Trading Experiment Performance', fontsize=16, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Portfolio Value ($)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Format x-axis dates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    
    # Save the chart
    chart_path = reports_dir / "performance_chart.png"
    plt.savefig(chart_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Performance chart saved to {chart_path}")


def generate_html_dashboard(data_dir: Path, reports_dir: Path):
    """Generate HTML dashboard for GitHub Pages."""
    portfolio_file = data_dir / "chatgpt_portfolio_update.csv"
    trade_log_file = data_dir / "chatgpt_trade_log.csv"
    
    # Load data
    portfolio_data = []
    trade_data = []
    
    if portfolio_file.exists():
        portfolio_df = pd.read_csv(portfolio_file)
        portfolio_data = portfolio_df.to_dict('records')
    
    if trade_log_file.exists():
        trade_df = pd.read_csv(trade_log_file)
        trade_data = trade_df.to_dict('records')
    
    # Generate HTML
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ChatGPT Micro-Cap Trading Experiment</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2E8B57;
            text-align: center;
            margin-bottom: 30px;
        }}
        .chart-container {{
            text-align: center;
            margin: 30px 0;
        }}
        .chart-container img {{
            max-width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #2E8B57;
        }}
        .stat-label {{
            color: #666;
            margin-top: 5px;
        }}
        .section {{
            margin: 40px 0;
        }}
        .section h2 {{
            color: #333;
            border-bottom: 2px solid #2E8B57;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f8f9fa;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 ChatGPT Micro-Cap Trading Experiment</h1>
        
        <div class="chart-container">
            <h2>Portfolio Performance</h2>
            <img src="performance_chart.png" alt="Portfolio Performance Chart">
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" id="total-equity">--</div>
                <div class="stat-label">Total Equity</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="total-trades">{len(trade_data)}</div>
                <div class="stat-label">Total Trades</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="last-updated">{datetime.now().strftime('%Y-%m-%d')}</div>
                <div class="stat-label">Last Updated</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Recent Portfolio Data</h2>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Ticker</th>
                            <th>Shares</th>
                            <th>Current Price</th>
                            <th>Total Value</th>
                            <th>P&L</th>
                        </tr>
                    </thead>
                    <tbody id="portfolio-table">
                        <!-- Portfolio data will be inserted here -->
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="section">
            <h2>📈 Recent Trades</h2>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Ticker</th>
                            <th>Action</th>
                            <th>Shares</th>
                            <th>Price</th>
                            <th>P&L</th>
                        </tr>
                    </thead>
                    <tbody id="trades-table">
                        <!-- Trade data will be inserted here -->
                    </tbody>
                </table>
            </div>
        </div>
        
        <div class="footer">
            <p>🚀 Automated trading experiment powered by ChatGPT</p>
            <p>Data updated automatically via GitHub Actions</p>
        </div>
    </div>
    
    <script>
        // Portfolio data
        const portfolioData = JSON.parse("{html.escape(json.dumps(portfolio_data[-20:] if portfolio_data else []), quote=True)}");
        const tradeData = JSON.parse("{html.escape(json.dumps(trade_data[-10:] if trade_data else []), quote=True)}");
        
        // Update total equity
        if (portfolioData.length > 0) {{
            const totalRows = portfolioData.filter(row => row.Ticker === 'TOTAL');
            if (totalRows.length > 0) {{
                const latestTotal = totalRows[totalRows.length - 1];
                document.getElementById('total-equity').textContent = '$' + latestTotal['Total Equity'];
            }}
        }}
        
        // Populate portfolio table
        const portfolioTable = document.getElementById('portfolio-table');
        portfolioData.slice(-10).forEach(row => {{
            if (row.Ticker !== 'TOTAL') {{
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${{row.Date}}</td>
                    <td>${{row.Ticker}}</td>
                    <td>${{row.Shares || '--'}}</td>
                    <td>${{row['Current Price'] ? '$' + row['Current Price'] : '--'}}</td>
                    <td>${{row['Total Value'] ? '$' + row['Total Value'] : '--'}}</td>
                    <td style="color: ${{(row.PnL || 0) >= 0 ? '#2E8B57' : '#dc3545'}}">${{row.PnL ? '$' + row.PnL : '--'}}</td>
                `;
                portfolioTable.appendChild(tr);
            }}
        }});
        
        // Populate trades table
        const tradesTable = document.getElementById('trades-table');
        tradeData.forEach(row => {{
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${{row.date}}</td>
                <td>${{row.ticker}}</td>
                <td>${{row.action}}</td>
                <td>${{row.shares}}</td>
                <td>${{row.price ? '$' + row.price : '--'}}</td>
                <td style="color: ${{(row.pnl || 0) >= 0 ? '#2E8B57' : '#dc3545'}}">${{row.pnl ? '$' + row.pnl : '--'}}</td>
            `;
            tradesTable.appendChild(tr);
        }});
    </script>
</body>
</html>
"""
    
    # Save HTML file
    html_path = reports_dir / "index.html"
    html_path.write_text(html_content)
    
    print(f"✅ HTML dashboard saved to {html_path}")


def main():
    """Generate all reports and visualizations."""
    data_dir = project_root / "Scripts and CSV Files"
    reports_dir = create_reports_directory()
    
    print("📊 Generating reports...")
    
    try:
        # Generate performance chart
        generate_performance_chart(data_dir, reports_dir)
        
        # Generate HTML dashboard
        generate_html_dashboard(data_dir, reports_dir)
        
        print("✅ All reports generated successfully")
        
    except Exception as e:
        print(f"❌ Error generating reports: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()