# Vercel Deployment Guide

This repository has been optimized for Vercel deployment to address the 250MB function size limit.

## Files Created for Vercel Optimization

### `.vercelignore`
Excludes large files and directories not needed for the web app:
- PDF documentation files (~864KB)
- Research images and assets
- Source code files only needed for automation
- Test files and development directories
- GitHub workflow files

### `requirements-vercel.txt`
Minimal dependencies for the web dashboard:
- flask==2.3.3 (web framework)
- pandas==2.0.3 (data processing)

This reduces the deployment size significantly compared to the full requirements.txt which includes heavy packages like matplotlib, plotly, numpy, yfinance, etc.

### Optimized `app.py`
- Removed plotly dependency (was causing size issues)
- Uses Chart.js for lightweight client-side charting
- Simplified error handling
- Reads CSV files from root directory instead of subdirectories
- Added Vercel-specific configurations

### Updated `vercel.json`
- Added maxLambdaSize limit
- Added function timeout configuration
- Production environment settings

## Deployment Instructions

1. **Vercel CLI Deployment:**
   ```bash
   vercel --prod
   ```

2. **GitHub Integration:**
   The deployment will automatically use the optimized configuration and exclude large files.

3. **Environment Variables:**
   Set `FLASK_ENV=production` in Vercel dashboard if not automatically detected.

## Size Optimization Results

- **Before:** ~250MB+ (exceeded Vercel limit)
- **After:** <50MB (well within Vercel limit)

## Files Included in Deployment

- `app.py` (Flask web application)
- `templates/dashboard.html` (web interface)
- `chatgpt_portfolio_update.csv` (data file)
- `chatgpt_trade_log.csv` (data file)
- `requirements-vercel.txt` (minimal dependencies)
- `vercel.json` (deployment configuration)

## Monitoring

The deployed app includes:
- `/health` endpoint for monitoring
- Error handling for missing data files
- Graceful fallbacks for chart rendering failures

## Backup Strategy

The full application with all features remains available in the repository. The Vercel deployment is optimized for web dashboard functionality only.