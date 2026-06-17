# HyperTrend API 使用文档

> **版本**: v1.0  
> **更新日期**: 2026-03-16  
> **Base URL**: `https://app.hypertrend.top/api`

---

## 🚀 快速开始

### 1. 基础调用方式

所有接口均支持 HTTP POST/GET 请求，返回 JSON 格式数据。

```bash
# 示例：获取稳健大师榜单
curl -X POST "https://app.hypertrend.top/api/open/master" \
  -H "Content-Type: application/json" \
  -d '{
    "page": 1,
    "page_size": 10,
    "type": "day"
  }'
```

### 2. Python 快速示例

```python
import requests

BASE_URL = "https://app.hypertrend.top/api"

# 获取榜单数据
response = requests.post(
    f"{BASE_URL}/open/master",
    json={"page": 1, "page_size": 10, "type": "day"}
)

data = response.json()
if data['code'] == 200:
    for item in data['data']['list']:
        print(f"地址: {item['address']}, PnL: ${item['pnl']}")
```

---

## 📚 接口目录

| 类型 | 接口 | 说明 | 认证 |
|------|------|------|:----:|
| 📊 榜单 | `/open/master` | 稳健大师 | 公开 |
| 📊 榜单 | `/open/hothunter` | 热点猎杀者 | 公开 |
| 📊 榜单 | `/open/vertex` | 量变先锋 | 公开 |
| 📊 榜单 | `/open/hexagram` | 巅峰指数(六芒星) | 公开 |
| 📊 统计 | `/open/billings` | 单量统计 | 公开 |
| 📊 统计 | `/open/vlm` | 交易量统计 | 公开 |
| 👤 用户 | `/apps/personal` | 个人信息 | 需登录 |
| 👤 账户 | `/apps/account` | 账户资产 | 需登录 |
| 💰 跟单 | `/trade/list` | 跟单列表 | 需登录 |

---

## 🔓 公开接口（无需认证）

### 稳健大师榜单

获取风控优秀、回撤较低的交易者排名。

```http
POST /open/master
```

**请求参数：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|:----:|:------:|------|
| page | int | 否 | 1 | 页码 |
| page_size | int | 否 | 10 | 每页数量 |
| type | string | 否 | "day" | 时间范围: day/week/month/allTime |

**响应示例：**

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "list": [
      {
        "address": "0xa1e848251ce2e...",
        "rankno": 1,
        "drawdown": "最大回撤",
        "pnl": "-762.52",
        "winrate": "胜率",
        "rio": "收益率",
        "cross_rate": "杠杆使用率",
        "avalue": "账户价值",
        "is_follow": false,
        "is_copy": false
      }
    ],
    "page": 1,
    "page_size": 10,
    "total": 35588
  }
}
```

**字段说明：**

| 字段 | 说明 | 示例 |
|------|------|------|
| address | 钱包地址 | 0xa1e8... |
| rankno | 排名 | 1 |
| drawdown | 最大回撤 | 0.05 (5%) |
| pnl | 收益金额 | -762.52 |
| winrate | 胜率 | 0.65 (65%) |
| rio | 收益率 | 0.01 (1%) |
| cross_rate | 杠杆使用率 | 0.3 (30%) |
| avalue | 账户价值 | 100000 |
| is_follow | 是否收藏 | false |
| is_copy | 是否跟单 | false |

---

### 热点猎杀者榜单

追踪热门项目和高频交易者。

```http
POST /open/hothunter
```

**请求参数：** 同稳健大师

**响应示例：**

```json
{
  "list": [
    {
      "address": "0x7faf...",
      "rankno": 1,
      "Position": "BTC,ETH",
      "pnl": "-7.72",
      "rio": "0",
      "cross_rate": "0.5",
      "vlm": "交易量",
      "avalue": "账户价值",
      "is_follow": false,
      "is_copy": false
    }
  ]
}
```

---

### 量变先锋榜单

按交易频率和交易量排名。

```http
POST /open/vertex
```

**请求参数：** 同稳健大师

**响应示例：**

```json
{
  "list": [
    {
      "address": "0x7796...",
      "rankno": 1,
      "total": 430,
      "spot": 100,
      "perpetuals": 330,
      "vlm": "12345678",
      "pnl": "-67754.38",
      "rio": "-0.03",
      "avalue": "1000000"
    }
  ]
}
```

**字段说明：**

| 字段 | 说明 |
|------|------|
| total | 总开单数 |
| spot | 现货交易数 |
| perpetuals | 合约交易数 |
| vlm | 交易量 |

---

### 巅峰指数（六芒星）

综合评分系统，包含六个维度。

```http
POST /open/hexagram
```

**响应示例：**

```json
{
  "list": [
    {
      "address": "0x1f67...",
      "rankno": 1,
      "六芒星数据": {
        "收益质量": 85,
        "风险控制": 92,
        "市场相位": 78,
        "杠杆艺术": 88,
        "胜率矩阵": 90,
        "链上足迹": 82
      },
      "is_follow": false,
      "is_copy": false
    }
  ]
}
```

**六芒星维度说明：**

| 维度 | 说明 | 权重 |
|------|------|:----:|
| 收益质量 | 盈利稳定性和可持续性 | 高 |
| 风险控制 | 最大回撤和爆仓风险 | 高 |
| 市场相位 | 市场时机把握能力 | 中 |
| 杠杆艺术 | 杠杆使用合理性 | 中 |
| 胜率矩阵 | 交易胜率分布 | 中 |
| 链上足迹 | 链上活跃度和历史 | 低 |

---

### 单量统计

按开单数量排名。

```http
POST /open/billings
```

**响应字段：**

| 字段 | 说明 |
|------|------|
| total | 开单总数 |
| spot | 现货开单数 |
| perpetuals | 合约开单数 |
| sum | 交易总量 |
| total_users | 活跃用户总数 |

---

### 交易量统计

按交易量排名。

```http
POST /open/vlm
```

**响应字段：**

| 字段 | 说明 |
|------|------|
| name | 币种名称 |
| maxLeverage | 最大杠杆倍数 |
| dayNtlVlm | 当日交易量 |
| oraclePx | 预言机价格 |
| markPx | 标记价格 |

---

## 🔒 需要认证的接口

### 登录流程

#### 1. 获取 Nonce

```http
POST /base/usernonce
Content-Type: application/json

{
  "wallet_address": "0x5B9625d826a439B1F2aC6fa86417ffb43607A1af"
}
```

**响应：**

```json
{
  "code": 200,
  "data": {
    "nonce": "1234567890"
  }
}
```

#### 2. 签名登录

使用钱包对 nonce 进行签名：

```http
POST /base/login
Content-Type: application/json

{
  "wallet_address": "0x5B9625d826a439B1F2aC6fa86417ffb43607A1af",
  "signature": "0x...",
  "nonce": "1234567890"
}
```

**响应：**

```json
{
  "code": 200,
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
      "wallet_address": "0x...",
      "username": "用户名"
    }
  }
}
```

#### 3. 使用 Token

在后续请求中添加 Header：

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

---

### 个人信息

```http
GET /apps/personal
Authorization: Bearer <token>
```

**响应示例：**

```json
{
  "code": 200,
  "data": {
    "六芒星数据": {
      "收益质量": 85,
      "风险控制": 92,
      "市场相位": 78,
      "杠杆艺术": 88,
      "胜率矩阵": 90,
      "链上足迹": 82
    },
    "avatar": "头像URL",
    "achievement": [],
    "follow": 10,
    "is_follow": false
  }
}
```

---

## ❌ 错误处理

### 错误码说明

| 状态码 | 说明 | 处理建议 |
|--------|------|----------|
| 200 | 成功 | - |
| 400 | 参数错误 | 检查请求参数格式 |
| 401 | 未授权 | 需要登录或 Token 过期 |
| 403 | 权限不足 | 检查账户权限 |
| 404 | 接口不存在 | 检查 URL 路径 |
| 500 | 服务器错误 | 稍后重试或联系支持 |

### 错误响应格式

```json
{
  "code": 400,
  "msg": "参数错误：page_size 不能超过 100",
  "data": null
}
```

---

## 💡 常见问题

### Q1: 日榜、周榜、月榜的区别？

| 类型 | 统计周期 | 更新时间 |
|------|----------|----------|
| day | 当日 00:00 - 现在 | 实时 |
| week | 本周一 00:00 - 现在 | 实时 |
| month | 本月 1 日 00:00 - 现在 | 实时 |
| allTime | 历史累计 | 实时 |

### Q2: 为什么六芒星数据为 0？

六芒星评分需要一定的交易数据积累，新用户或低频交易者可能显示为 0。建议查看周榜或月榜获取更完整的数据。

### Q3: 如何获取完整地址？

API 返回的地址是完整的，为了显示美观可以截取前 10 位和后 6 位：

```python
addr = "0x1f67d79afc8d0e7609ddba6c9b657cc635f69981"
short_addr = addr[:10] + "..." + addr[-6:]
# 结果: 0x1f67d79a...69981
```

### Q4: 请求频率限制？

当前公开接口暂无严格频率限制，但建议：
- 榜单接口：每分钟不超过 60 次
- 用户接口：每分钟不超过 30 次

---

## 🛠️ SDK 示例

### Python SDK

```python
import requests
from typing import Dict, List

class HyperTrendClient:
    def __init__(self, base_url: str = "https://app.hypertrend.top/api"):
        self.base_url = base_url
        self.token = None
    
    def get_leaderboard(self, leaderboard_type: str = "master", 
                       period: str = "day", page: int = 1, 
                       page_size: int = 10) -> Dict:
        """获取榜单数据"""
        url = f"{self.base_url}/open/{leaderboard_type}"
        response = requests.post(url, json={
            "page": page,
            "page_size": page_size,
            "type": period
        })
        return response.json()
    
    def login(self, wallet_address: str, signature: str, nonce: str) -> bool:
        """钱包签名登录"""
        url = f"{self.base_url}/base/login"
        response = requests.post(url, json={
            "wallet_address": wallet_address,
            "signature": signature,
            "nonce": nonce
        })
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 200:
                self.token = data['data']['token']
                return True
        return False

# 使用示例
client = HyperTrendClient()

# 获取稳健大师日榜
result = client.get_leaderboard("master", "day", 1, 10)
for item in result['data']['list']:
    print(f"{item['rankno']}. {item['address'][:10]}... - PnL: ${item['pnl']}")
```

---

## 📞 支持

- **GitHub**: https://github.com/GuiPulp/hypertrend-analytics
- **网站**: https://www.hypertrend.top
- **Telegram**: https://t.me/HyperTrendHQ

---

**最后更新**: 2026-03-16
