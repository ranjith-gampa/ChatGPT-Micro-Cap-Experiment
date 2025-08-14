# Example API Keys Configuration

This file shows the format and sources for the API keys needed for automation.

## Required API Keys

### OpenAI API Key
- **Purpose**: ChatGPT trading decision making
- **Source**: [OpenAI Platform](https://platform.openai.com/api-keys)
- **Format**: `sk-proj-...` or `sk-...`
- **Usage**: 1000+ tokens per day for trading prompts
- **Cost**: ~$5-20/month depending on usage

### Alpha Vantage API Key  
- **Purpose**: Backup market data source
- **Source**: [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
- **Format**: Alphanumeric string
- **Usage**: Free tier: 25 requests/day, 5 requests/minute
- **Cost**: Free tier available, premium plans $50+/month

## Optional API Keys

### Trading/Brokerage API Key
- **Purpose**: Live trading execution (future feature)
- **Examples**: 
  - [Alpaca](https://alpaca.markets/): Commission-free API trading
  - [TD Ameritrade](https://developer.tdameritrade.com/): Full trading API
  - [Interactive Brokers](https://www.interactivebrokers.com/en/trading/ib-api.php): Professional platform
- **Note**: Currently not implemented, manual trading only

### Vercel Token (if using Vercel deployment)
- **Purpose**: Deploy Flask web dashboard
- **Source**: [Vercel Dashboard](https://vercel.com/account/tokens)
- **Format**: Long alphanumeric token
- **Cost**: Free tier available, Pro plans $20+/month

## Setting Up GitHub Secrets

1. Go to your repository on GitHub
2. Navigate to **Settings → Secrets and variables → Actions**
3. Click **New repository secret**
4. Add each secret with the exact names:

```
Secret Name: OPENAI_API_KEY
Secret Value: sk-proj-your-actual-key-here

Secret Name: ALPHA_VANTAGE_API_KEY  
Secret Value: your-alpha-vantage-key-here
```

## Testing API Keys Locally

Create a `.env` file for local testing (DO NOT commit this file):

```bash
# .env file (local testing only)
OPENAI_API_KEY=sk-proj-your-key-here
ALPHA_VANTAGE_API_KEY=your-key-here
TRADING_API_KEY=your-trading-key-here
```

Test the keys work:
```bash
# Test OpenAI
python -c "import openai; openai.api_key='your-key'; print('OpenAI key works')"

# Test Alpha Vantage
python -c "import requests; r=requests.get('https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=MSFT&apikey=your-key'); print(r.status_code)"
```

## API Usage Monitoring

### OpenAI Usage
- Monitor at: [OpenAI Usage Dashboard](https://platform.openai.com/usage)
- Set billing limits to avoid unexpected charges
- Typical usage: $1-5/day for active trading

### Alpha Vantage Usage
- Monitor at: [Alpha Vantage Dashboard](https://www.alphavantage.co/support/#support)
- Free tier should be sufficient for backup data
- Upgrade if hitting rate limits

## Security Notes

- **Never share or commit API keys**
- **Regenerate keys if compromised**
- **Use minimal permissions where possible**
- **Monitor usage for unexpected spikes**
- **Set billing alerts on paid services**

## Cost Estimates

**Minimal Setup (Free Tier):**
- GitHub Actions: Free (2000 minutes/month)
- Alpha Vantage: Free (25 requests/day)
- GitHub Pages: Free
- **Total**: OpenAI usage only (~$10-30/month)

**Full Setup:**
- OpenAI API: $10-50/month
- Alpha Vantage Pro: $50/month
- Vercel Pro: $20/month
- Live trading platform: $0-100/month
- **Total**: $80-220/month