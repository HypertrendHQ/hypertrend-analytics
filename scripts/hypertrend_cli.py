#!/usr/bin/env python3
"""Small HyperTrend data CLI for agents.

Uses only the Python standard library so the skill can work before optional
dependencies such as requests are installed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, Iterable, List, Optional, Tuple


DEFAULT_BASE_URL = "https://app.hypertrend.top/api"
LEGACY_BASE_URL = "http://192.144.239.66/api"
DEFAULT_HYPERLIQUID_LEADERBOARD_URL = "https://stats-data.hyperliquid.xyz/Mainnet/leaderboard"

LEADERBOARDS: Dict[str, Dict[str, Any]] = {
    "hyperliquid": {
        "label": "Hyperliquid Stats",
        "source": "hyperliquid_stats",
        "fields": ["rankno", "address", "accountValue", "pnl", "roi", "vlm"],
    },
    "gravity": {
        "label": "Gravity Index",
        "endpoints": ["/open/gravity"],
        "fields": ["rankno", "address", "score", "profit", "risk", "market", "leverage", "win_rate", "footprint", "pnl", "pnl30d", "roi", "value"],
    },
    "credrank": {
        "label": "Credit Ranking",
        "endpoints": ["/open/credrank"],
        "fields": ["rankno", "address", "credscore", "gravity_index", "eco_score", "social_credit", "identity_consistency"],
    },
    "traders": {
        "label": "Certified Traders",
        "endpoints": ["/open/traders"],
        "fields": ["rankno", "address", "name", "user_name", "score", "pnl", "roi", "win_rate", "drawdown", "avalue"],
    },
    "smartmoney": {
        "label": "Smart Money",
        "endpoints": ["/open/smartmoney"],
        "fields": ["rankno", "address", "vlm", "pnl", "roi", "winrate", "drawdown", "total", "follower", "value", "is_trader"],
    },
    "master": {
        "label": "Stable Master",
        "endpoints": ["/open/master", "/apps/master"],
        "fields": ["rankno", "address", "pnl", "roi", "rio", "winrate", "win_rate", "drawdown", "cross_rate", "avalue"],
    },
    "hothunter": {
        "label": "Hot Hunter",
        "endpoints": ["/open/hothunter", "/apps/hothunter"],
        "fields": ["rankno", "address", "position", "pnl", "roi", "rio", "cross_rate", "vlm", "avalue"],
    },
    "vertex": {
        "label": "Vertex",
        "endpoints": ["/open/vertex", "/apps/vertex"],
        "fields": ["rankno", "address", "total", "spot", "perpetuals", "vlm", "pnl", "roi", "rio", "avalue"],
    },
    "hexagram": {
        "label": "Hexagram",
        "endpoints": ["/open/hexagram", "/apps/hexagram"],
        "fields": ["rankno", "address", "score", "profit", "risk", "market", "leverage", "win_rate", "footprint", "is_follow", "is_copy"],
    },
    "billings": {
        "label": "Billings",
        "endpoints": ["/open/billings"],
        "fields": ["rankno", "address", "value", "pnl", "roi", "rio", "vlm", "total", "spot", "perpetuals"],
    },
    "volume": {
        "label": "Volume",
        "endpoints": ["/open/vlm"],
        "fields": ["name", "maxLeverage", "dayNtlVlm", "oraclePx", "markPx"],
    },
}

RISK_PROFILES: Dict[str, Dict[str, Any]] = {
    "conservative": {
        "label": "Conservative",
        "filters": {"min_winrate": 0.60, "max_drawdown": 0.10, "max_leverage": 5.0, "min_pnl": 0.0},
        "weights": {"winrate": 0.35, "drawdown": 0.35, "pnl": 0.20, "leverage": 0.10},
    },
    "moderate": {
        "label": "Moderate",
        "filters": {"min_winrate": 0.52, "max_drawdown": 0.20, "max_leverage": 10.0, "min_pnl": 0.0},
        "weights": {"winrate": 0.25, "drawdown": 0.30, "pnl": 0.30, "leverage": 0.15},
    },
    "aggressive": {
        "label": "Aggressive",
        "filters": {"min_winrate": 0.42, "max_drawdown": 0.40, "max_leverage": 20.0, "min_pnl": 0.0},
        "weights": {"winrate": 0.15, "drawdown": 0.20, "pnl": 0.45, "leverage": 0.20},
    },
    "quantitative": {
        "label": "Quantitative",
        "filters": {"min_winrate": 0.50, "max_drawdown": 0.25, "max_leverage": 15.0, "min_pnl": 0.0},
        "weights": {"winrate": 0.30, "drawdown": 0.20, "pnl": 0.25, "volume": 0.25},
    },
}


def env_base_url() -> str:
    return os.getenv("HYPERTREND_API_URL", DEFAULT_BASE_URL).rstrip("/")


def headers() -> Dict[str, str]:
    result = {"Content-Type": "application/json", "Accept": "application/json"}
    token = os.getenv("HYPERTREND_API_TOKEN")
    if token:
        result["Authorization"] = f"Bearer {token}"
    return result


def post_json(base_url: str, endpoint: str, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
    url = f"{base_url}{endpoint}"
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers(), method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {"ok": True, "url": url, "status": response.status, "json": json.loads(body)}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"ok": False, "url": url, "status": exc.code, "error": body[:500]}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"ok": False, "url": url, "status": None, "error": str(exc)}


def get_json(url: str, timeout: int) -> Dict[str, Any]:
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "HyperTrend-Analytics-Skill"}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            return {"ok": True, "url": url, "status": response.status, "json": json.loads(body)}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"ok": False, "url": url, "status": exc.code, "error": body[:500]}
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"ok": False, "url": url, "status": None, "error": str(exc)}


def extract_rows(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [row for row in payload if isinstance(row, dict)]
    if not isinstance(payload, dict):
        return []
    data = payload.get("data")
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        for key in ("list", "rows", "data"):
            nested = data.get(key)
            if isinstance(nested, list):
                return [row for row in nested if isinstance(row, dict)]
    for key in ("list", "rows", "result"):
        nested = payload.get(key)
        if isinstance(nested, list):
            return [row for row in nested if isinstance(row, dict)]
    return []


def fetch_hyperliquid_leaderboard(period: str, limit: int, timeout: int) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    url = os.getenv("HYPERLIQUID_STATS_LEADERBOARD_URL", DEFAULT_HYPERLIQUID_LEADERBOARD_URL)
    result = get_json(url, timeout)
    if not result["ok"]:
        raise SystemExit(f"Unable to fetch Hyperliquid stats leaderboard: {result['error']}")

    rows = []
    source_rows = result["json"].get("leaderboardRows", []) if isinstance(result["json"], dict) else []
    for index, item in enumerate(source_rows, start=1):
        if not isinstance(item, dict):
            continue
        windows = item.get("windowPerformances", [])
        performance = {}
        for window in windows:
            if isinstance(window, list) and len(window) == 2 and window[0] == period and isinstance(window[1], dict):
                performance = window[1]
                break
        rows.append(
            {
                "rankno": index,
                "address": item.get("ethAddress", ""),
                "accountValue": item.get("accountValue", ""),
                "pnl": performance.get("pnl", ""),
                "roi": performance.get("roi", ""),
                "vlm": performance.get("vlm", ""),
            }
        )
        if len(rows) >= limit:
            break

    meta = {"source_url": result["url"], "period": period, "type": "hyperliquid", "source_rows": len(source_rows)}
    return rows, meta


def fetch_leaderboard(kind: str, period: str, limit: int, timeout: int, base_url: Optional[str] = None) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    if kind not in LEADERBOARDS:
        raise SystemExit(f"Unknown leaderboard type: {kind}. Choose: {', '.join(LEADERBOARDS)}")
    if LEADERBOARDS[kind].get("source") == "hyperliquid_stats":
        return fetch_hyperliquid_leaderboard(period, limit, timeout)

    payload = {"page": 1, "page_size": limit, "type": period}
    bases = [base_url or env_base_url()]
    if bases[0] != LEGACY_BASE_URL and os.getenv("HYPERTREND_TRY_LEGACY", "0") == "1":
        bases.append(LEGACY_BASE_URL)

    attempts: List[Dict[str, Any]] = []
    first_ok: Optional[Tuple[List[Dict[str, Any]], Dict[str, Any]]] = None
    for current_base in bases:
        for endpoint in LEADERBOARDS[kind]["endpoints"]:
            result = post_json(current_base, endpoint, payload, timeout)
            attempts.append(result)
            if result["ok"]:
                rows = extract_rows(result["json"])
                meta = {"source_url": result["url"], "period": period, "type": kind, "attempts": attempts}
                if first_ok is None:
                    first_ok = (rows[:limit], meta)
                if rows:
                    return rows[:limit], meta

    if first_ok is not None:
        return first_ok

    detail = attempts[-1]["error"] if attempts else "No request attempted"
    raise SystemExit(f"Unable to fetch HyperTrend data: {detail}")


def as_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "").replace("%", "")
    if not text:
        return default
    try:
        return float(text)
    except ValueError:
        return default


def pct(value: Any) -> float:
    number = as_float(value)
    return number / 100.0 if abs(number) > 1 else number


def normalize_trader(row: Dict[str, Any]) -> Dict[str, Any]:
    roi_value = row.get("roi", row.get("rio"))
    winrate_value = row.get("winrate", row.get("win_rate"))
    cross_rate = pct(row.get("cross_rate"))
    leverage = as_float(row.get("leverage"), 0.0)
    if leverage <= 0 and cross_rate > 0:
        leverage = max(cross_rate * 100.0, 1.0)
    if leverage <= 0:
        leverage = 1.0
    return {
        "address": row.get("address", ""),
        "rank": int(as_float(row.get("rankno"), 0)),
        "pnl": as_float(row.get("pnl")),
        "roi": pct(roi_value),
        "winrate": pct(winrate_value),
        "drawdown": abs(pct(row.get("drawdown"))),
        "leverage": leverage,
        "volume": as_float(row.get("vlm")),
        "account_value": as_float(row.get("avalue", row.get("value"))),
        "raw": row,
    }


def risk_score(trader: Dict[str, Any], profile: Dict[str, Any]) -> float:
    weights = profile["weights"]
    score = 0.0
    if "winrate" in weights:
        score += min(trader["winrate"] * 100.0, 100.0) * weights["winrate"]
    if "drawdown" in weights:
        score += max(0.0, 100.0 - trader["drawdown"] * 250.0) * weights["drawdown"]
    if "pnl" in weights:
        score += min(max(trader["pnl"] / 1000.0 * 10.0, 0.0), 100.0) * weights["pnl"]
    if "leverage" in weights:
        score += max(0.0, 100.0 - trader["leverage"] * 5.0) * weights["leverage"]
    if "volume" in weights:
        score += min(max(trader["volume"] / 1_000_000.0 * 10.0, 0.0), 100.0) * weights["volume"]
    return round(score, 2)


def match_risk(rows: Iterable[Dict[str, Any]], profile_name: str) -> List[Dict[str, Any]]:
    profile = RISK_PROFILES[profile_name]
    filters = profile["filters"]
    matched: List[Dict[str, Any]] = []
    for row in rows:
        trader = normalize_trader(row)
        if not trader["address"]:
            continue
        if trader["winrate"] < filters["min_winrate"]:
            continue
        if trader["drawdown"] > filters["max_drawdown"]:
            continue
        if trader["leverage"] > filters["max_leverage"]:
            continue
        if trader["pnl"] < filters["min_pnl"]:
            continue
        trader["match_score"] = risk_score(trader, profile)
        matched.append(trader)
    matched.sort(key=lambda item: item["match_score"], reverse=True)
    return matched


def compact_address(address: Any) -> str:
    text = str(address or "")
    if len(text) <= 14:
        return text
    return f"{text[:8]}...{text[-6:]}"


def format_table(rows: List[Dict[str, Any]], kind: str, meta: Dict[str, Any]) -> str:
    fields = LEADERBOARDS[kind]["fields"]
    visible = ["rankno", "address"] + [field for field in fields if field not in ("rankno", "address")][:6]
    lines = [
        f"HyperTrend {LEADERBOARDS[kind]['label']} leaderboard",
        f"source={meta['source_url']} period={meta['period']} rows={len(rows)}",
        "",
        " | ".join(visible),
        " | ".join(["---"] * len(visible)),
    ]
    for index, row in enumerate(rows, start=1):
        values = []
        for field in visible:
            value = row.get(field, "")
            if field == "rankno" and value == "":
                value = index
            if field == "address":
                value = compact_address(value)
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False, separators=(",", ":"))[:80]
            values.append(str(value))
        lines.append(" | ".join(values))
    return "\n".join(lines)


def format_risk(matches: List[Dict[str, Any]], profile_name: str, meta: Dict[str, Any], limit: int) -> str:
    profile = RISK_PROFILES[profile_name]
    lines = [
        f"HyperTrend risk match: {profile['label']}",
        f"source={meta['source_url']} period={meta['period']} candidates={len(matches)}",
        "",
    ]
    if not matches:
        lines.append("No candidates passed the profile filters. Try a longer period or a less restrictive profile.")
        return "\n".join(lines)
    for index, trader in enumerate(matches[:limit], start=1):
        lines.extend(
            [
                f"{index}. {compact_address(trader['address'])} score={trader['match_score']}/100 rank=#{trader['rank']}",
                f"   pnl={trader['pnl']:.2f} roi={trader['roi']*100:.2f}% winrate={trader['winrate']*100:.2f}% drawdown={trader['drawdown']*100:.2f}% leverage~{trader['leverage']:.2f}x",
            ]
        )
    lines.append("")
    lines.append("Risk note: verify fresh data, position concentration, and drawdown before any copy-trading decision.")
    return "\n".join(lines)


def command_leaderboard(args: argparse.Namespace) -> None:
    rows, meta = fetch_leaderboard(args.type, args.period, args.limit, args.timeout, args.base_url)
    if args.format == "json":
        print(json.dumps({"meta": {k: v for k, v in meta.items() if k != "attempts"}, "data": rows}, ensure_ascii=False, indent=2))
    else:
        print(format_table(rows, args.type, meta))


def command_risk_match(args: argparse.Namespace) -> None:
    rows, meta = fetch_leaderboard("master", args.period, args.fetch_limit, args.timeout, args.base_url)
    matches = match_risk(rows, args.profile)
    if args.format == "json":
        payload = [{key: value for key, value in item.items() if key != "raw"} for item in matches[: args.limit]]
        print(json.dumps({"meta": {k: v for k, v in meta.items() if k != "attempts"}, "profile": args.profile, "data": payload}, ensure_ascii=False, indent=2))
    else:
        print(format_risk(matches, args.profile, meta, args.limit))


def command_schema(args: argparse.Namespace) -> None:
    if args.type not in LEADERBOARDS:
        raise SystemExit(f"Unknown leaderboard type: {args.type}. Choose: {', '.join(LEADERBOARDS)}")
    print(json.dumps(LEADERBOARDS[args.type], ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fetch and analyze HyperTrend leaderboard data.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    leaderboard = subparsers.add_parser("leaderboard", help="Fetch a leaderboard.")
    leaderboard.add_argument("--type", choices=sorted(LEADERBOARDS), default="master")
    leaderboard.add_argument("--period", default="week", choices=["day", "week", "month", "allTime"])
    leaderboard.add_argument("--limit", type=int, default=10)
    leaderboard.add_argument("--format", choices=["table", "json"], default="table")
    leaderboard.add_argument("--base-url", default=None)
    leaderboard.add_argument("--timeout", type=int, default=20)
    leaderboard.set_defaults(func=command_leaderboard)

    risk = subparsers.add_parser("risk-match", help="Rank master leaderboard traders by risk profile.")
    risk.add_argument("--profile", choices=sorted(RISK_PROFILES), default="moderate")
    risk.add_argument("--period", default="week", choices=["day", "week", "month", "allTime"])
    risk.add_argument("--fetch-limit", type=int, default=80)
    risk.add_argument("--limit", type=int, default=5)
    risk.add_argument("--format", choices=["table", "json"], default="table")
    risk.add_argument("--base-url", default=None)
    risk.add_argument("--timeout", type=int, default=20)
    risk.set_defaults(func=command_risk_match)

    schema = subparsers.add_parser("schema", help="Show known fields for a leaderboard type.")
    schema.add_argument("--type", choices=sorted(LEADERBOARDS), default="master")
    schema.set_defaults(func=command_schema)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
