#!/bin/bash
#
# HyperTrend API 数据获取脚本
# 用于从 OpenClaw Skill 调用真实数据
#

set -e

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
API_SCRIPT="$SCRIPT_DIR/hypertrend_api.py"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo '{"error": "Python3 not found"}'
    exit 1
fi

# 检查依赖
if ! python3 -c "import requests" 2>/dev/null; then
    echo '{"error": "requests module not found. Please install: pip3 install requests"}'
    exit 1
fi

# 检查 API Token
if [ -z "$HYPERTREND_API_TOKEN" ]; then
    echo '{"error": "HYPERTREND_API_TOKEN not set"}'
    exit 1
fi

# 解析参数
COMMAND="${1:-help}"
LEADERBOARD_TYPE="${2:-master}"
PERIOD="${3:-week}"
LIMIT="${4:-10}"

case "$COMMAND" in
    leaderboard)
        python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from hypertrend_api import get_leaderboard, format_leaderboard

data = get_leaderboard('$LEADERBOARD_TYPE', '$PERIOD', $LIMIT)
print(format_leaderboard(data, '$LEADERBOARD_TYPE'))
"
        ;;
    
    master)
        python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from hypertrend_api import HyperTrendAPI, format_leaderboard

api = HyperTrendAPI()
result = api.get_master(page=1, page_size=$LIMIT, type_='$PERIOD')
if 'error' in result:
    print(f\"❌ 错误: {result['error']}\")
else:
    data = result.get('data', [])
    print(format_leaderboard(data, 'master'))
"
        ;;
    
    hothunter)
        python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from hypertrend_api import HyperTrendAPI, format_leaderboard

api = HyperTrendAPI()
result = api.get_hothunter(page=1, page_size=$LIMIT, type_='$PERIOD')
if 'error' in result:
    print(f\"❌ 错误: {result['error']}\")
else:
    data = result.get('data', [])
    print(format_leaderboard(data, 'hothunter'))
"
        ;;
    
    hexagram)
        python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from hypertrend_api import HyperTrendAPI, format_leaderboard

api = HyperTrendAPI()
result = api.get_hexagram(page=1, page_size=$LIMIT, type_='$PERIOD')
if 'error' in result:
    print(f\"❌ 错误: {result['error']}\")
else:
    data = result.get('data', [])
    print(format_leaderboard(data, 'hexagram'))
"
        ;;
    
    personal)
        python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from hypertrend_api import HyperTrendAPI
import json

api = HyperTrendAPI()
result = api.get_personal()
if 'error' in result:
    print(f\"❌ 错误: {result['error']}\")
else:
    print(json.dumps(result, indent=2, ensure_ascii=False))
"
        ;;
    
    account)
        python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from hypertrend_api import HyperTrendAPI
import json

api = HyperTrendAPI()
result = api.get_account()
if 'error' in result:
    print(f\"❌ 错误: {result['error']}\")
else:
    print(json.dumps(result, indent=2, ensure_ascii=False))
"
        ;;
    
    copylist)
        python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from hypertrend_api import HyperTrendAPI
import json

api = HyperTrendAPI()
result = api.get_copy_list()
if 'error' in result:
    print(f\"❌ 错误: {result['error']}\")
else:
    print(json.dumps(result, indent=2, ensure_ascii=False))
"
        ;;
    
    test)
        python3 "$API_SCRIPT"
        ;;
    
    help|*)
        echo "HyperTrend API 数据获取脚本"
        echo ""
        echo "用法:"
        echo "  $0 leaderboard [type] [period] [limit]  - 获取榜单"
        echo "  $0 master [period] [limit]              - 稳健大师榜"
        echo "  $0 hothunter [period] [limit]          - 热点猎杀者榜"
        echo "  $0 hexagram [period] [limit]           - 巅峰指数榜"
        echo "  $0 personal                             - 个人信息"
        echo "  $0 account                              - 账户资产"
        echo "  $0 copylist                             - 跟单列表"
        echo "  $0 test                                 - 测试API连接"
        echo ""
        echo "参数:"
        echo "  type: master, hothunter, vertex, hexagram"
        echo "  period: day, week, month, allTime"
        echo "  limit: 数字 (默认10)"
        echo ""
        echo "示例:"
        echo "  $0 master week 10"
        echo "  $0 hothunter day 5"
        echo "  $0 hexagram allTime 20"
        ;;
esac
