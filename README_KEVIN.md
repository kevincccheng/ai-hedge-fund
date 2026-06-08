# AI Hedge Fund - Kevin's Convenience Layer

This is a thin, additive layer on top of the upstream
[ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) project (forked to
[kevincccheng/ai-hedge-fund](https://github.com/kevincccheng/ai-hedge-fund)).
Nothing in the original project is modified - everything here is new files only,
following the same pattern as [TradingAgents](https://github.com/kevincccheng/TradingAgents).

The app has two processes that must run together: a Python/FastAPI backend and a
React/TypeScript frontend.

## First time setup

- **Windows:** double-click `setup.bat` (or run it from a terminal)
- **Mac:** run `./setup.sh`

This creates a Python virtual environment (`.venv`), installs backend dependencies
(via Poetry) and frontend dependencies (`npm install` in `app/frontend`), and creates
a `.env` file from `.env.kevin.example` if you don't already have one.

After setup finishes, **edit `.env` and add your API keys**.

## Daily use

- **Windows:** double-click `run.bat`
- **Mac:** run `./run.sh`

This starts the FastAPI backend (http://127.0.0.1:8000) and the React frontend
(http://localhost:5173), waits a few seconds for both to come up, and opens your
browser automatically. When you save an analysis run from the UI (it lands in
`outputs/run_*.json`), the script also converts the most recent one into a polished
PDF report in `reports/latest/` and opens it in Microsoft Edge.

If you want crash protection (output logged, partial results preserved on failure),
use `run_safe.bat` / `run_safe.sh` instead - logs go to `crash_logs/`.

## Syncing to Mac

1. `git clone https://github.com/kevincccheng/ai-hedge-fund.git`
2. Copy your `.env` file over from Windows (it's intentionally not committed to git)
3. Run `./setup.sh`, then `./run.sh`

## Things to know about API keys

- The **free** `FINANCIAL_DATASETS_API_KEY` tier only covers these tickers:
  `AAPL`, `GOOGL`, `MSFT`, `NVDA`, `TSLA`
- For Hong Kong tickers (or anything outside that free five), you need a **paid**
  financialdatasets.ai key
- In `.env`, uncomment exactly **one** model provider block:
  - Anthropic - best quality, ~$1.50-2.00/run
  - DeepSeek - excellent value, ~$0.10-0.20/run
  - OpenAI - good middle ground, ~$0.50-1.00/run
