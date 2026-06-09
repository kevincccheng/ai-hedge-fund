#!/usr/bin/env python3
"""
Seed Kevin's default NVDA analysis flow into the ai-hedge-fund database.
Safe to re-run: only creates the flow when the database has NO flows yet.
Called automatically by run.bat / run.sh after the backend starts.
"""

import json
import sys
import time
import urllib.error
import urllib.request

API_BASE = "http://127.0.0.1:8000"
MAX_RETRIES = 20   # 20 x 2s = 40s max wait
RETRY_DELAY = 2    # seconds between retries

FLOW_NAME = "Kevin's NVDA Flow"
FLOW_DESCRIPTION = (
    "Analyses NVDA using 4 quant analysts (Fundamentals, Technical, Sentiment, Valuation) "
    "plus 3 legendary investors (Warren Buffett, Charlie Munger, Michael Burry). "
    "Change the ticker in the Stock Input node to analyse any stock from the free tier: "
    "AAPL, GOOGL, MSFT, NVDA, TSLA. Risk management runs automatically inside the backend."
)


# ---------------------------------------------------------------------------
# HTTP helpers (no third-party deps — stdlib only)
# ---------------------------------------------------------------------------

def _http_get(path: str):
    url = f"{API_BASE}{path}"
    with urllib.request.urlopen(url, timeout=5) as resp:
        return json.loads(resp.read())


def _http_post(path: str, body: dict):
    url = f"{API_BASE}{path}"
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


# ---------------------------------------------------------------------------
# Backend readiness check
# ---------------------------------------------------------------------------

def wait_for_backend() -> bool:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            _http_get("/flows/")
            print("[seed_flow] Backend is ready.")
            return True
        except Exception:
            if attempt < MAX_RETRIES:
                print(f"[seed_flow] Waiting for backend to start... ({attempt}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)
    print(f"[seed_flow] Backend not reachable after {MAX_RETRIES * RETRY_DELAY}s. Skipping seed.")
    return False


# ---------------------------------------------------------------------------
# Flow definition
# ---------------------------------------------------------------------------
# Node IDs use deterministic 6-char suffixes (kevin0-kevin8) so the backend's
# extract_base_agent_key() correctly strips them to recover the agent key.
# e.g. "warren_buffett_kevin5" → agent key "warren_buffett"
# ---------------------------------------------------------------------------

STOCK_ID   = "stock-analyzer-node_kevin0"
FUND_ID    = "fundamentals_analyst_kevin1"
TECH_ID    = "technical_analyst_kevin2"
SENT_ID    = "sentiment_analyst_kevin3"
VALU_ID    = "valuation_analyst_kevin4"
WB_ID      = "warren_buffett_kevin5"
CM_ID      = "charlie_munger_kevin6"
MB_ID      = "michael_burry_kevin7"
PM_ID      = "portfolio_manager_kevin8"

ANALYST_IDS = [FUND_ID, TECH_ID, SENT_ID, VALU_ID, WB_ID, CM_ID, MB_ID]


def _node(nid: str, ntype: str, x: float, y: float, name: str, description: str, internal_state: dict | None = None) -> dict:
    data: dict = {"name": name, "description": description, "status": "Idle"}
    if internal_state:
        data["internal_state"] = internal_state
    return {"id": nid, "type": ntype, "position": {"x": x, "y": y}, "data": data}


def _edge(source: str, target: str) -> dict:
    return {
        "id": f"{source}-{target}",
        "source": source,
        "target": target,
        "markerEnd": {"type": "ArrowClosed"},
    }


def build_flow_payload() -> dict:
    # Vertical layout: Stock Input on the left, 7 agent nodes in the middle column
    # (spaced 175px apart), Portfolio Manager on the right.
    nodes = [
        _node(
            STOCK_ID, "stock-analyzer-node", 50, 600,
            "Stock Input",
            "Enter individual stocks and connect this node to Analysts to generate insights.",
            internal_state={
                "tickers": "NVDA",
                "runMode": "single",
                "initialCash": "100000",
            },
        ),
        _node(FUND_ID, "agent-node", 500,   75, "Fundamentals Analyst",
              "Financial Statement Specialist — Delves into financial statements and economic "
              "indicators to assess the intrinsic value of companies through fundamental analysis."),
        _node(TECH_ID, "agent-node", 500,  250, "Technical Analyst",
              "Chart Pattern Specialist — Focuses on chart patterns and market trends to make "
              "investment decisions, often using technical indicators and price action analysis."),
        _node(SENT_ID, "agent-node", 500,  425, "Sentiment Analyst",
              "Market Sentiment Specialist — Gauges market sentiment and investor behavior to "
              "predict market movements and identify opportunities through behavioral analysis."),
        _node(VALU_ID, "agent-node", 500,  600, "Valuation Analyst",
              "Company Valuation Specialist — Specializes in determining the fair value of "
              "companies, using various valuation models and financial metrics."),
        _node(WB_ID,   "agent-node", 500,  775, "Warren Buffett",
              "The Oracle of Omaha — Seeks companies with strong fundamentals and competitive "
              "advantages through value investing and long-term ownership."),
        _node(CM_ID,   "agent-node", 500,  950, "Charlie Munger",
              "The Rational Thinker — Advocates for value investing with a focus on quality "
              "businesses and long-term growth through rational decision-making."),
        _node(MB_ID,   "agent-node", 500, 1125, "Michael Burry",
              "The Big Short Contrarian — Makes contrarian bets, often shorting overvalued "
              "markets and investing in undervalued assets through deep fundamental analysis."),
        _node(PM_ID,   "portfolio-manager-node", 1050, 600,
              "Portfolio Manager",
              "Generates investment decisions based on input from Analysts. "
              "Risk management runs automatically in the backend."),
    ]

    edges = (
        [_edge(STOCK_ID, aid) for aid in ANALYST_IDS]
        + [_edge(aid, PM_ID) for aid in ANALYST_IDS]
    )

    # Viewport: slight zoom-out + upward offset to frame the tall graph
    viewport = {"x": 20, "y": 60, "zoom": 0.65}

    return {
        "name": FLOW_NAME,
        "description": FLOW_DESCRIPTION,
        "nodes": nodes,
        "edges": edges,
        "viewport": viewport,
        "data": {
            "nodeStates": {
                STOCK_ID: {
                    "tickers": "NVDA",
                    "runMode": "single",
                    "initialCash": "100000",
                }
            }
        },
        "is_template": False,
        "tags": ["kevin", "nvda", "default"],
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    if not wait_for_backend():
        sys.exit(0)  # Non-fatal — user can still use the app manually

    try:
        flows = _http_get("/flows/")
    except Exception as exc:
        print(f"[seed_flow] Could not fetch flows: {exc}. Skipping seed.")
        return

    if flows:
        print(f"[seed_flow] {len(flows)} flow(s) already exist — skipping seed.")
        return

    payload = build_flow_payload()
    try:
        created = _http_post("/flows/", payload)
        print(f"[seed_flow] Created default flow \"{created['name']}\" (id={created['id']})")
        print("[seed_flow] Open it from the left sidebar and click Run.")
    except Exception as exc:
        print(f"[seed_flow] Failed to create default flow: {exc}")


if __name__ == "__main__":
    main()
