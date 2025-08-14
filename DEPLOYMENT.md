# 🔧 Deployment Setup Guide

This guide walks you through setting up the automated deployment and CI/CD pipeline for the ChatGPT Micro-Cap Trading Experiment.

## 📋 Prerequisites

- GitHub repository with admin access
- Python 3.11+ installed locally for testing
- API keys for trading automation (see below)

## 🔑 Required GitHub Secrets

Configure these secrets in your repository: **Settings → Secrets and variables → Actions**

### Essential Secrets:
```
OPENAI_API_KEY          # ChatGPT API key for trading decisions
ALPHA_VANTAGE_API_KEY   # Market data API key (backup source)
```

### Optional Secrets (for live trading):
```
TRADING_API_KEY         # Your brokerage API key
VERCEL_TOKEN           # For Vercel deployment (if using)
```

## 🚀 Deployment Options

### Option 1: GitHub Pages (Recommended)
- **Pros**: Free, automatic deployment, integrated with GitHub
- **Cons**: Static site only (no real-time Flask app)

The workflow automatically deploys to GitHub Pages using the `reports/` directory.

**Setup:**
1. Go to repository **Settings → Pages**
2. Set source to **GitHub Actions**
3. The dashboard will be available at: `https://username.github.io/repository-name`

### Option 2: Vercel Deployment
- **Pros**: Full Flask app support, serverless, custom domains
- **Cons**: Requires Vercel account and token

**Setup:**
1. Connect your GitHub repo to [Vercel](https://vercel.com)
2. Add `VERCEL_TOKEN` to GitHub secrets
3. Deploy automatically on pushes to main branch

## ⚙️ GitHub Actions Workflows

### Main CI/CD Pipeline (`.github/workflows/deploy.yml`)
- **Triggers**: Push to main, PRs, daily at market open
- **Jobs**: 
  - Run tests with pytest
  - Execute daily trading updates
  - Generate reports and charts
  - Deploy to GitHub Pages

### Daily Trading Operations (`.github/workflows/trading.yml`)
- **Triggers**: Market open/close times, manual dispatch
- **Jobs**:
  - Execute automated trading logic
  - Update portfolio data
  - Commit changes back to repository

## 🧪 Testing Your Setup

### 1. Local Testing
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Test automation scripts
python scripts/daily_update.py
python scripts/generate_reports.py

# Test Flask app
python app.py
```

### 2. Verify GitHub Actions
1. Check the **Actions** tab in your repository
2. Workflows should run automatically on commits
3. Verify deployment in **Settings → Pages**

## 📊 Dashboard Features

### Web Dashboard (`app.py`)
- **Real-time portfolio data**: Current positions and P&L
- **Interactive charts**: Performance over time using Plotly
- **Trade history**: Recent buy/sell transactions
- **REST API endpoints**: `/api/portfolio`, `/api/performance`, `/api/trades`

### Static Reports (`scripts/generate_reports.py`)
- **Performance charts**: PNG images for GitHub Pages
- **HTML dashboard**: Static version with portfolio data
- **Automated generation**: Runs on every deployment

## 🔧 Configuration

### Environment Variables
The system supports these environment variables:
- `OPENAI_API_KEY`: Required for ChatGPT decisions
- `ALPHA_VANTAGE_API_KEY`: Backup market data source
- `TRADING_API_KEY`: Live trading integration
- `FLASK_ENV`: Set to "production" for Vercel

### Data Directory
Portfolio and trade data is stored in:
- `Scripts and CSV Files/chatgpt_portfolio_update.csv`
- `Scripts and CSV Files/chatgpt_trade_log.csv`

## 🛡️ Security Best Practices

1. **Never commit API keys** to the repository
2. **Use GitHub secrets** for all sensitive data
3. **Enable branch protection** on main branch
4. **Review automated commits** from GitHub Actions
5. **Monitor API usage** and costs

## 📈 Monitoring and Alerts

### GitHub Actions Monitoring
- Check workflow runs in the **Actions** tab
- Set up notifications for failed builds
- Monitor daily trading operations

### Portfolio Monitoring
- Dashboard auto-refreshes every 5 minutes
- Performance alerts can be added to workflows
- Trade logs provide full audit trail

## 🔍 Troubleshooting

### Common Issues:

**Tests failing:**
- Check Python version (3.11+ required)
- Verify all dependencies installed
- Review test output for specific errors

**Workflows not running:**
- Check GitHub Actions are enabled
- Verify workflow syntax with GitHub's validator
- Ensure proper indentation in YAML files

**Dashboard not updating:**
- Check if CSV files exist and have data
- Verify GitHub Pages deployment succeeded
- Check for errors in report generation

**API errors:**
- Verify API keys are correctly set in GitHub secrets
- Check API rate limits and quotas
- Test API connections locally first

## 🔄 Maintenance

### Regular Tasks:
- Monitor portfolio performance weekly
- Review and update trading prompts monthly
- Check API usage and costs monthly
- Update dependencies quarterly

### Updates:
- Dependencies: Update `requirements.txt` as needed
- Trading logic: Modify scripts in `src/` directory
- Dashboard: Update templates and Flask app
- Workflows: Adjust schedules and add features

## 📞 Support

For issues with this setup:
1. Check the [repository issues](../../issues)
2. Review GitHub Actions logs
3. Test components locally first
4. Create a new issue with detailed logs

---

**Last updated**: January 2025  
**Compatible with**: Python 3.11+, GitHub Actions