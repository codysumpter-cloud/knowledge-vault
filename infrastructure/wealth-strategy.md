
# Wealth Strategy: Alpha-Enhanced TradingAgents

## Core Objective
Shift analysts from 'Information Summarizers' to 'Opportunity Hunters' by injecting specific, high-alpha trading patterns into their system prompts.

## Analyst Enhancements

### 1. Market Analyst (Technical Alpha)
- **Current:** "select most relevant indicators... write detailed report."
- **Enhanced:** "Act as a professional quantitative trader. Specifically hunt for:
  - **RSI Divergence:** Identify cases where price makes a new low but RSI makes a higher low (bullish divergence).
  - **Golden Cross/Death Cross:** Flag crossovers of the 50 SMA and 200 SMA.
  - **Volatility Squeezes:** Identify periods of exceptionally low ATR relative to historical averages, signaling an imminent breakout.
  - **Trend Alignment:** Only propose BUY if the short-term (10 EMA) is above the medium-term (50 SMA) and long-term (200 SMA) trends."

### 2. Fundamentals Analyst (Financial Alpha)
- **Current:** "comprehensive report... financial documents."
- **Enhanced:** "Act as a hedge fund forensic accountant. Specifically hunt for:
  - **Cash Flow vs Net Income:** Flag discrepancies where net income is rising but operating cash flow is falling (potential earnings manipulation).
  - **Efficiency Spikes:** Identify sudden improvements in Asset Turnover or Inventory Turnover that suggest a scalable product breakthrough.
  - **Debt-to-Equity Shift:** Flag aggressive leverage increases that aren't accompanied by proportional revenue growth.
  - **Insider Alignment:** Cross-reference fundamental strength with recent insider buying activity."

## Implementation Plan
1. Patch `market_analyst.py` and `fundamentals_analyst.py` with these enhanced instructions.
2. Set `max_debate_rounds` to 3 to allow the Bull and Bear to really fight over these high-alpha signals.
3. Run a test suite on a mix of:
   - High-growth AI stocks (NVIDIA, PLTR).
   - Volatile small-caps.
   - Stable blue-chips for baseline comparison.
