# AI Hedge Fund - Kevin's Notes

Convenience layer on top of [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund)
(forked to [kevincccheng/ai-hedge-fund](https://github.com/kevincccheng/ai-hedge-fund)).
Zero modifications to any upstream file — everything here is additive.

---

## Quick start (first time)

1. Edit `.env` — add at least one API key
2. **Windows:** double-click `setup.bat` (installs Python + Node.js deps, ~3 min)
3. **Mac:** run `./setup.sh`
4. From then on: `run.bat` (Windows) or `./run.sh` (Mac) opens the app

---

## How to use the app — 10 steps

These steps reflect the actual frontend source code, not assumptions.

### Step 1 — Launch

Double-click `run.bat` (or `./run.sh` on Mac). It:
- Starts the FastAPI backend on http://127.0.0.1:8000
- Starts the React frontend on http://localhost:5173
- Seeds **Kevin's NVDA Flow** into the database on first launch only
- Opens your browser automatically

### Step 2 — Open the default flow

On the left sidebar, you'll see **"Kevin's NVDA Flow"** under the Flows list.
Click it to open the canvas in a tab.

The flow is pre-built with 9 connected nodes:
- **Stock Input** (default ticker: NVDA)
- 4 Quant Analysts: Fundamentals, Technical, Sentiment, Valuation
- 3 Legendary Investors: Warren Buffett, Charlie Munger, Michael Burry
- **Portfolio Manager** (Risk Management runs automatically in the backend)

### Step 3 — (Optional) Change the ticker

Click the **Stock Input** node on the canvas. Edit the ticker field.
- Free tier: `AAPL`, `GOOGL`, `MSFT`, `NVDA`, `TSLA`
- Multiple tickers: `NVDA,AAPL,TSLA` (comma-separated)
- HK tickers need a paid financialdatasets.ai key

### Step 4 — (Optional) Choose your model

Each agent node has an expandable **model selector** at the bottom of the card.
The default uses whatever provider+model you set in `.env`.
You can override it per-node (e.g. run Warren Buffett on Claude, others on DeepSeek).

### Step 5 — Run the analysis

Click the green **Run** button on the Stock Input node (or press Cmd+Enter / Ctrl+Enter).
The bottom panel opens automatically showing real-time progress per agent.

### Step 6 — Read the output

When all agents finish, click the **Portfolio Manager** node to see the investment decision.
The bottom panel's **Output** tab shows signals from every analyst, sorted by conviction.

### Step 7 — Save the output as JSON (optional)

In the bottom panel, there's a **"Save to File"** toggle.
Enable it before clicking Run — the output will be written to `outputs/run_<timestamp>.json`.

### Step 8 — Generate a PDF report (optional)

After saving a JSON output, run:
```
python convert_report.py
```
(This also runs automatically at the end of every `run.bat` / `run.sh` session.)
The PDF is saved to `reports/latest/TICKER_YYYY-MM-DD_HH-MM-SS.pdf` and opens in Edge.

### Step 9 — Build your own flow

To create a custom flow from scratch:
1. Click the **+ New Flow** button in the left sidebar
2. Give it a name and description
3. From the **right sidebar**, add nodes:
   - **Start Nodes**: Stock Input (individual tickers) or Portfolio Input (existing holdings)
   - **Analysts**: any of the 20 available agents — click **+** to add each one
   - **Swarms**: pre-built groups — "Data Wizards", "Market Mavericks", "Value Investors"
   - **End Nodes**: Portfolio Manager
4. Connect nodes by dragging from the right handle of one node to the left handle of the next
5. The flow auto-saves 1 second after every change

### Step 10 — Syncing to Mac

```bash
git clone https://github.com/kevincccheng/ai-hedge-fund.git
# copy your .env from Windows — it's gitignored, so not in the repo
./setup.sh
./run.sh
```

---

## API key cost guide

| Provider | Best for | Approx cost per NVDA run |
|---|---|---|
| Anthropic (Claude) | Highest quality reasoning | ~$1.50–2.00 |
| DeepSeek | Best value, nearly as good | ~$0.10–0.20 |
| OpenAI (GPT-4o) | Good middle ground | ~$0.50–1.00 |

Uncomment exactly **one** model block in `.env`. Using multiple agents multiplies cost proportionally (7 agents in the default flow = ~7× single-agent cost).

## Free ticker tier

`financialdatasets.ai` free plan covers: **AAPL, GOOGL, MSFT, NVDA, TSLA** only.
Any other ticker (including all HK stocks) requires a paid key.

## Crash-protected run

Use `run_safe.bat` / `run_safe.sh` instead of the regular launchers.
Logs everything to `crash_logs/run_<timestamp>.log` and copies any partial JSON output
from `outputs/` into `crash_logs/` if the process exits non-zero.
