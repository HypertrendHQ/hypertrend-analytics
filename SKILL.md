---
name: hypertrend-analytics
description: Access and analyze HyperTrend and Hyperliquid trader data for leaderboard lookup, trader discovery, address comparison, risk-profile matching, copy-trading candidate research, market trend summaries, and data-grounded trading analysis. Use when the user asks for HyperTrend rankings, top traders, whale or address analysis, six-hexagram/gravity scores, PnL/win-rate/drawdown/volume leaderboards, or trader recommendations based on risk preference.
---

# HyperTrend Analytics

Use this skill to fetch HyperTrend leaderboard data, compare trader quality, and turn the data into cautious trading-analysis briefs. Prefer real API data over examples in the markdown files.

Do not present results as financial advice. State the data source, period, sample size, and major risks such as drawdown, leverage, short history, and API freshness.

## Fast Path

From the skill directory, use the dependency-light CLI:

```bash
python scripts/hypertrend_cli.py leaderboard --type master --period week --limit 20 --format table
python scripts/hypertrend_cli.py leaderboard --type hexagram --period allTime --limit 10 --format json
python scripts/hypertrend_cli.py risk-match --profile conservative --period week --limit 50
python scripts/hypertrend_cli.py schema --type master
```

If `python` is unavailable, try `python3`. If the environment blocks network access, ask for permission to run the command with network access instead of fabricating data.

## Data Sources

Default base URL:

```bash
https://app.hypertrend.top/api
```

Override when needed:

```bash
export HYPERTREND_API_URL="http://192.144.239.66/api"
export HYPERTREND_API_TOKEN="..."
```

The CLI automatically tries public `/open/*` endpoints first and falls back to `/apps/*` endpoints. Authenticated endpoints require `HYPERTREND_API_TOKEN`.

## Leaderboards

Use these CLI `--type` values:

| Type | Meaning | Primary fields |
| --- | --- | --- |
| `master` | Stable/master traders | `address`, `rankno`, `pnl`, `roi/rio`, `winrate/win_rate`, `drawdown`, `cross_rate`, `avalue` |
| `hothunter` | Hot opportunity hunters | `address`, `rankno`, `position`, `pnl`, `roi/rio`, `cross_rate`, `vlm`, `avalue` |
| `vertex` | High-activity/volume leaders | `address`, `rankno`, `total`, `spot`, `perpetuals`, `vlm`, `pnl`, `roi/rio`, `avalue` |
| `hexagram` | Six-hexagram/gravity quality ranking | `address`, `rankno`, `score`, `profit`, `risk`, `market`, `leverage`, `win_rate`, `footprint` |
| `billings` | Order-count statistics | `address`, `rankno`, `value`, `pnl`, `roi/rio`, `vlm`, `total`, `spot`, `perpetuals` |
| `volume` | Market volume data | `name`, `maxLeverage`, `dayNtlVlm`, `oraclePx`, `markPx` |

Valid periods are usually `day`, `week`, `month`, and `allTime`. If one period fails, retry with `week` and report the fallback.

## Analysis Workflow

1. Fetch enough rows for the task, usually 20-100.
2. Normalize fields before ranking: use `roi` or `rio` for return, `winrate` or `win_rate` for win rate, and `rankno` for leaderboard rank.
3. Screen obvious risks before recommending a trader: high drawdown, high leverage/cross rate, low account value, low trade count, short period only, and unusually concentrated PnL.
4. Compare candidates across at least two dimensions, such as PnL plus drawdown, or win rate plus volume.
5. Explain recommendations as hypotheses from data, not guarantees. Include why a strong candidate could still fail.

## Risk Matching

Use:

```bash
python scripts/hypertrend_cli.py risk-match --profile moderate --period week --limit 80
```

Profiles:

| Profile | Goal | Default filter intent |
| --- | --- | --- |
| `conservative` | Lower volatility and steadier returns | Higher win rate, lower drawdown, lower leverage |
| `moderate` | Balance return and risk | Positive PnL, controlled drawdown, acceptable leverage |
| `aggressive` | Higher return tolerance | Allows higher leverage/drawdown but still rejects extreme risk |
| `quantitative` | Data-density preference | Favors trade count, volume, and repeatability |

When outputting copy-trading candidates, include:

- Address and leaderboard rank
- Period and leaderboard type
- PnL, ROI, win rate, drawdown, leverage/cross-rate when available
- Match score and the top 2-3 reasons
- Risk warning and a suggestion to verify with fresh data before any action

## Reference Files

Read only when needed:

- `API_CLIENT.md`: Detailed endpoint notes and authenticated API examples.
- `LEADERBOARD.md`: Leaderboard concepts and output patterns.
- `COPYTRADING.md` and `PLATFORM_COPYTRADING.md`: Copy-trading flows and safety checks.
- `ADDRESS_MONITORING.md`: Address monitoring and whale-tracking scenarios.
- `USAGE_EXAMPLES.md`: Prompt and output examples.

## Safety Rules

- Never place trades, create copy-trading orders, or modify follows unless the user explicitly asks and credentials are configured.
- For any trading action, confirm the exact address, amount, mode, stop loss, and risk first.
- Avoid claiming that the agent has learned a profitable strategy from the data. Say what patterns the data suggests and what validation is still missing.
