#!/usr/bin/env python3
"""
HyperTrend 风险偏好匹配与跟单推荐系统
根据用户风险偏好推荐合适的交易者
"""

import requests
import json
import sys
from typing import Dict, List, Optional

BASE_URL = "https://app.hypertrend.top/api"

# 风险偏好配置
RISK_PROFILES = {
    "conservative": {
        "name": "保守型",
        "description": "低风险偏好，追求稳定收益，最大回撤控制在10%以内",
        "filters": {
            "max_drawdown": 0.10,  # 最大回撤 < 10%
            "min_winrate": 0.60,   # 胜率 > 60%
            "max_leverage": 5,     # 杠杆 < 5x
            "min_pnl": 0,          # 盈利 > 0
        },
        "weight": {
            "winrate": 0.4,        # 胜率权重最高
            "drawdown": 0.3,       # 回撤控制
            "pnl": 0.2,            # 收益
            "leverage": 0.1,       # 杠杆
        }
    },
    "moderate": {
        "name": "稳健型",
        "description": "中等风险，平衡收益与风险，最大回撤控制在20%以内",
        "filters": {
            "max_drawdown": 0.20,
            "min_winrate": 0.55,
            "max_leverage": 10,
            "min_pnl": 0,
        },
        "weight": {
            "winrate": 0.3,
            "pnl": 0.3,
            "drawdown": 0.25,
            "leverage": 0.15,
        }
    },
    "aggressive": {
        "name": "进取型",
        "description": "高风险高收益，可接受较大回撤，追求超额收益",
        "filters": {
            "max_drawdown": 0.40,
            "min_winrate": 0.45,
            "max_leverage": 20,
            "min_pnl": 100,        # 至少盈利 $100
        },
        "weight": {
            "pnl": 0.4,            # 收益权重最高
            "winrate": 0.2,
            "drawdown": 0.2,
            "leverage": 0.2,
        }
    },
    "quantitative": {
        "name": "量化型",
        "description": "数据驱动，关注交易频率和策略稳定性",
        "filters": {
            "max_drawdown": 0.25,
            "min_winrate": 0.50,
            "min_trades": 20,      # 最少交易次数
        },
        "weight": {
            "winrate": 0.35,
            "trade_freq": 0.25,    # 交易频率
            "pnl": 0.25,
            "drawdown": 0.15,
        }
    }
}

def fetch_leaderboard(leaderboard_type: str = "master", page_size: int = 50) -> List[Dict]:
    """获取榜单数据"""
    try:
        url = f"{BASE_URL}/open/{leaderboard_type}"
        response = requests.post(
            url,
            json={"page": 1, "page_size": page_size, "type": "day"},
            timeout=10
        )
        data = response.json()
        if data.get("code") == 200:
            return data.get("data", {}).get("list", [])
        return []
    except Exception as e:
        print(f"Error fetching leaderboard: {e}", file=sys.stderr)
        return []

def parse_trader_data(trader: Dict) -> Dict:
    """解析交易者数据"""
    try:
        pnl = float(trader.get("pnl", 0))
        
        # drawdown 可能是负数字符串，如 "-0.01"
        drawdown_val = float(trader.get("drawdown", "0"))
        drawdown = abs(drawdown_val) / 100 if drawdown_val else 0
        
        # win_rate 是数字字符串，如 "100"
        winrate = float(trader.get("win_rate", "0")) / 100
        
        # roi 是数字字符串
        rio = float(trader.get("roi", "0")) / 100
        
        # cross_rate 是数字字符串
        cross_rate = float(trader.get("cross_rate", "0")) / 100
        
        # 估算杠杆（从 cross_rate 推算，cross_rate 0.1 = 10x 杠杆）
        leverage = cross_rate * 100 if cross_rate > 0 else 1
        
        return {
            "address": trader.get("address", "Unknown"),
            "rank": trader.get("rankno", 0),
            "pnl": pnl,
            "drawdown": drawdown,
            "winrate": winrate,
            "roi": rio,
            "cross_rate": cross_rate,
            "leverage": leverage,
            "account_value": float(trader.get("avalue", 0)),
            "is_following": trader.get("is_follow", False),
            "is_copying": trader.get("is_copy", False),
        }
    except Exception as e:
        print(f"Error parsing trader data: {e}", file=sys.stderr)
        return None

def calculate_match_score(trader: Dict, profile: Dict) -> float:
    """计算匹配分数 (0-100)"""
    weights = profile["weight"]
    score = 0.0
    
    if "winrate" in weights:
        winrate_score = min(trader["winrate"] * 100, 100)
        score += winrate_score * weights["winrate"]
    
    if "drawdown" in weights:
        drawdown_score = max(0, 100 - trader["drawdown"] * 100 * 2)
        score += drawdown_score * weights["drawdown"]
    
    if "pnl" in weights:
        pnl_score = min(max(trader["pnl"] / 1000 * 10, 0), 100)
        score += pnl_score * weights["pnl"]
    
    if "leverage" in weights:
        if profile["name"] == "保守型":
            leverage_score = max(0, 100 - trader["leverage"] * 10)
        else:
            leverage_score = min(trader["leverage"] * 5, 100)
        score += leverage_score * weights["leverage"]
    
    return round(score, 2)

def filter_and_rank_traders(traders: List[Dict], profile_key: str) -> List[Dict]:
    """根据风险偏好筛选和排序交易者"""
    profile = RISK_PROFILES.get(profile_key, RISK_PROFILES["moderate"])
    filters = profile["filters"]
    
    filtered = []
    for trader_data in traders:
        trader = parse_trader_data(trader_data)
        if not trader:
            continue
        
        if trader["drawdown"] > filters.get("max_drawdown", 1.0):
            continue
        if trader["winrate"] < filters.get("min_winrate", 0):
            continue
        if trader["leverage"] > filters.get("max_leverage", 100):
            continue
        if trader["pnl"] < filters.get("min_pnl", -999999):
            continue
        
        trader["match_score"] = calculate_match_score(trader, profile)
        trader["risk_profile"] = profile["name"]
        filtered.append(trader)
    
    filtered.sort(key=lambda x: x["match_score"], reverse=True)
    return filtered

def generate_recommendation(trader: Dict, rank: int) -> str:
    """生成推荐理由"""
    reasons = []
    
    if trader["winrate"] > 0.70:
        reasons.append(f"胜率高达 {trader['winrate']*100:.1f}%，稳定性优秀")
    elif trader["winrate"] > 0.60:
        reasons.append(f"胜率 {trader['winrate']*100:.1f}%，表现良好")
    
    if trader["drawdown"] < 0.10:
        reasons.append(f"最大回撤仅 {trader['drawdown']*100:.1f}%，风控出色")
    elif trader["drawdown"] < 0.20:
        reasons.append(f"回撤控制 {trader['drawdown']*100:.1f}%，风险可控")
    
    if trader["pnl"] > 1000:
        reasons.append(f"日收益 ${trader['pnl']:.2f}，盈利能力强劲")
    elif trader["pnl"] > 100:
        reasons.append(f"日收益 ${trader['pnl']:.2f}，持续盈利")
    
    if trader["leverage"] < 5:
        reasons.append("低杠杆操作，风险较低")
    elif trader["leverage"] > 15:
        reasons.append("高杠杆激进策略，适合高风险偏好")
    
    return "；".join(reasons) if reasons else "综合表现均衡，值得跟踪"

def format_output(traders: List[Dict], profile_key: str, limit: int = 5) -> str:
    """格式化输出结果"""
    profile = RISK_PROFILES.get(profile_key, RISK_PROFILES["moderate"])
    
    output = []
    output.append("=" * 60)
    output.append(f"🎯 HyperTrend 智能跟单推荐")
    output.append(f"📊 风险偏好: {profile['name']}")
    output.append(f"📝 {profile['description']}")
    output.append("=" * 60)
    output.append("")
    
    if not traders:
        output.append("⚠️ 未找到符合条件的交易者")
        return "\n".join(output)
    
    for i, trader in enumerate(traders[:limit], 1):
        output.append(f"【推荐 #{i}】匹配度: {trader['match_score']}/100")
        output.append(f"├─ 地址: {trader['address'][:20]}...")
        output.append(f"├─ 榜单排名: #{trader['rank']}")
        output.append(f"├─ 日收益: ${trader['pnl']:.2f}")
        output.append(f"├─ 胜率: {trader['winrate']*100:.1f}%")
        output.append(f"├─ 最大回撤: {trader['drawdown']*100:.1f}%")
        output.append(f"├─ 预估杠杆: {trader['leverage']:.1f}x")
        output.append(f"└─ 💡 推荐理由: {generate_recommendation(trader, i)}")
        output.append("")
    
    output.append("=" * 60)
    output.append("💰 跟单操作:")
    output.append(f"  查看详情: openclaw hypertrend address <地址>")
    output.append(f"  开始跟单: openclaw hypertrend copytrade <地址> --amount <金额>")
    output.append("=" * 60)
    
    return "\n".join(output)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 risk_match.py <风险偏好>")
        print("")
        print("可选风险偏好:")
        for key, profile in RISK_PROFILES.items():
            print(f"  {key}: {profile['name']} - {profile['description']}")
        sys.exit(1)
    
    profile_key = sys.argv[1].lower()
    
    if profile_key not in RISK_PROFILES:
        print(f"❌ 未知的风险偏好: {profile_key}")
        print(f"✅ 可选: {', '.join(RISK_PROFILES.keys())}")
        sys.exit(1)
    
    print(f"🔍 正在为您匹配 '{RISK_PROFILES[profile_key]['name']}' 风格的交易者...")
    print("")
    
    traders = fetch_leaderboard("master", page_size=50)
    if not traders:
        print("❌ 获取榜单数据失败")
        sys.exit(1)
    
    matched = filter_and_rank_traders(traders, profile_key)
    print(format_output(matched, profile_key))

if __name__ == "__main__":
    main()