"""Decision making engine using ChatGPT API."""

import os
import openai
from typing import Dict, List, Optional
import json


class DecisionMaker:
    """Handles automated trading decisions using ChatGPT API."""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        else:
            print("Warning: OpenAI API key not configured")
    
    def generate_trading_prompt(self, portfolio_data: Dict, market_data: Dict) -> str:
        """
        Generate a trading prompt for ChatGPT.
        
        Args:
            portfolio_data: Current portfolio information
            market_data: Current market data
        
        Returns:
            Formatted prompt string
        """
        prompt = f"""
You are managing a micro-cap stock portfolio with the following current holdings:

PORTFOLIO SUMMARY:
{json.dumps(portfolio_data, indent=2)}

CURRENT MARKET DATA:
{json.dumps(market_data, indent=2)}

Based on this information, please analyze the portfolio and provide trading recommendations.

Consider:
1. Current positions and their performance
2. Stop-loss rules (sell if price drops below stop-loss)
3. Market opportunities in micro-cap stocks
4. Risk management principles
5. Diversification needs

Please respond with specific actionable recommendations in the following format:

ACTIONS:
- HOLD [ticker]: Reason for holding
- SELL [ticker] [shares] at [price]: Reason for selling
- BUY [ticker] [shares] at [max_price] stop_loss [price]: Reason for buying

ANALYSIS:
[Your detailed analysis of the current market situation and reasoning]

Remember: This is real money trading, so be conservative and follow strict risk management.
"""
        return prompt
    
    def get_trading_decision(self, portfolio_data: Dict, market_data: Dict) -> Optional[Dict]:
        """
        Get trading decision from ChatGPT.
        
        Args:
            portfolio_data: Current portfolio information
            market_data: Current market data
        
        Returns:
            Trading decision dictionary or None if error
        """
        if not self.api_key:
            print("Cannot make automated decisions: OpenAI API key not configured")
            return None
        
        try:
            prompt = self.generate_trading_prompt(portfolio_data, market_data)
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a conservative micro-cap stock trading advisor."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            decision_text = response.choices[0].message.content
            
            # Parse the response into structured decision data
            decision = {
                "raw_response": decision_text,
                "timestamp": os.environ.get('GITHUB_RUN_ID', 'manual'),
                "actions": self._parse_actions(decision_text)
            }
            
            return decision
            
        except Exception as e:
            print(f"Error getting ChatGPT decision: {e}")
            return None
    
    def _parse_actions(self, response_text: str) -> List[Dict]:
        """
        Parse trading actions from ChatGPT response.
        
        Args:
            response_text: Raw response from ChatGPT
        
        Returns:
            List of parsed actions
        """
        # Extract trading actions from structured response text
        actions = []
        lines = response_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('- HOLD'):
                # Parse HOLD action
                parts = line.split()
                if len(parts) >= 2:
                    ticker = parts[1].rstrip(':')
                    actions.append({
                        "action": "HOLD",
                        "ticker": ticker,
                        "reason": " ".join(parts[2:])
                    })
            
            elif line.startswith('- SELL'):
                # Parse SELL action
                # Format: - SELL [ticker] [shares] at [price]: Reason
                parts = line.split()
                if len(parts) >= 5:
                    try:
                        actions.append({
                            "action": "SELL",
                            "ticker": parts[1],
                            "shares": int(parts[2]),
                            "price": float(parts[4]),
                            "reason": " ".join(parts[5:])
                        })
                    except (ValueError, IndexError):
                        continue
            
            elif line.startswith('- BUY'):
                # Parse BUY action
                # Format: - BUY [ticker] [shares] at [max_price] stop_loss [price]: Reason
                parts = line.split()
                if len(parts) >= 7:
                    try:
                        actions.append({
                            "action": "BUY",
                            "ticker": parts[1],
                            "shares": int(parts[2]),
                            "max_price": float(parts[4]),
                            "stop_loss": float(parts[6]),
                            "reason": " ".join(parts[7:])
                        })
                    except (ValueError, IndexError):
                        continue
        
        return actions
    
    def log_decision(self, decision: Dict, log_file: str = "decision_log.json"):
        """
        Log trading decision to file.
        
        Args:
            decision: Decision dictionary to log
            log_file: Path to log file
        """
        try:
            # Load existing log
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = []
            
            # Add new decision
            log_data.append(decision)
            
            # Save updated log
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f"Error logging decision: {e}")