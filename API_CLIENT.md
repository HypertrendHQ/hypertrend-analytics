---
name: hypertrend-api-client
description: HyperTrend API 客户端 - 基于真实 API 接口的数据获取和交易操作
version: 1.0.0
author: HyperTrend Team
base_url: http://192.144.239.66/api
---

# HyperTrend API 客户端

基于真实 API 接口的 HyperTrend 数据获取和交易操作。

## 🔐 认证流程

### 1. 发送验证码
```bash
POST /base/send/smscode
{
  "contact": "user@email.com",
  "sms_type": "register"
}
```

### 2. 注册
```bash
POST /base/register
{
  "wallet_address": "0x...",
  "contact": "user@email.com",
  "sms_code": "715572",
  "invite_code": "1xf4reffds"
}
```

### 3. 获取 Nonce（用于签名）
```bash
POST /base/usernonce
{
  "wallet_address": "0x..."
}
```

### 4. 登录（钱包签名）
```bash
POST /base/login
{
  "wallet_address": "0x...",
  "signature": "0x...",
  "nonce": "123456"
}
```

## 📊 榜单数据接口

### 热点猎杀者
```bash
POST /apps/hothunter
{
  "page": 1,
  "page_size": 10,
  "type": "day"  // day, week, month, allTime
}

Response:
{
  "data": [
    {
      "address": "0x...",
      "rankno": 1,
      "position": "热门项目",
      "pnl": "收益",
      "rio": "收益率",
      "cross_rate": "杠杆使用率",
      "vlm": "交易量",
      "avalue": "账户价值",
      "is_follow": true,
      "is_copy": false
    }
  ]
}
```

### 稳健大师
```bash
POST /apps/master
{
  "page": 1,
  "page_size": 10,
  "type": "week"
}

Response:
{
  "data": [
    {
      "address": "0x...",
      "rankno": 1,
      "drawdown": "最大回撤",
      "pnl": "收益",
      "winrate": "胜率",
      "rio": "收益率",
      "cross_rate": "杠杆使用率",
      "avalue": "账户价值",
      "is_follow": false,
      "is_copy": true
    }
  ]
}
```

### 量变先锋
```bash
POST /apps/vertex
{
  "page": 1,
  "page_size": 10,
  "type": "month"
}

Response:
{
  "data": [
    {
      "address": "0x...",
      "rankno": 1,
      "total": "开单数",
      "spot": "现货",
      "perpetuals": "合约",
      "vlm": "交易量",
      "pnl": "收益",
      "rio": "收益率",
      "avalue": "账户价值"
    }
  ]
}
```

### 巅峰指数（六芒星）
```bash
POST /apps/hexagram
{
  "page": 1,
  "page_size": 10,
  "type": "allTime"
}

Response:
{
  "data": [
    {
      "address": "0x...",
      "rankno": 1,
      "hexagram": {
        "收益质量": "profit",
        "风险控制": "risk",
        "市场相位": "market",
        "杠杆艺术": "leverage",
        "胜率矩阵": "winrate",
        "链上足迹": "footprint"
      },
      "is_follow": false,
      "is_copy": false
    }
  ]
}
```

### 单量统计
```bash
POST /open/billings
{
  "page": 1,
  "page_size": 10,
  "type": "day"  // day, week, month
}

Response:
{
  "data": [
    {
      "address": "0x...",
      "rankno": 1,
      "value": "总资产",
      "pnl": "收益",
      "rio": "收益率",
      "vlm": "交易量",
      "total": "开单",
      "spot": "现货",
      "perpetuals": "合约"
    }
  ],
  "sum": "交易总量",
  "total": "活跃用户"
}
```

### 交易量统计
```bash
POST /open/vlm
{
  "page": 1,
  "page_size": 10,
  "type": "allTime"
}

Response:
{
  "data": [
    {
      "name": "币种",
      "maxLeverage": "最大倍率",
      "dayNtlVlm": "交易量",
      "oraclePx": "现价格",
      "markPx": "市场价格"
    }
  ],
  "sum": "交易总量",
  "total": "活跃用户"
}
```

## 👤 个人信息接口

### 获取用户信息
```bash
GET /apps/preview

Response:
{
  "wallet_address": "0x...",
  "username": "用户名",
  "description": "语录",
  "avatar": "头像",
  "achievement": "成就",
  "follow": "收藏人数",
  "is_follow": false
}
```

### 六芒星数据
```bash
GET /apps/personal

Response:
{
  "hexagram": {
    "收益质量": "profit",
    "风险控制": "risk",
    "市场相位": "market",
    "杠杆艺术": "leverage",
    "胜率矩阵": "winrate",
    "链上足迹": "footprint"
  },
  "avatar": "头像",
  "achievement": "个人成就",
  "follow": "收藏人数",
  "is_follow": false
}
```

### 账户资产
```bash
GET /apps/account

Response:
{
  "crossMarginSummary": {
    "accountValue": "账户价值",
    "totalMarginUsed": "合约保证金使用",
    "totalNtlPos": "现货保证金使用",
    "totalRawUsd": "0.0"
  },
  "marginSummary": {
    "accountValue": "0.0",
    "totalMarginUsed": "0.0",
    "totalNtlPos": "0.0",
    "totalRawUsd": "0.0"
  }
}
```

### 收益表现
```bash
GET /apps/pnl

Response:
{
  "roi": "收益率",
  "pnl": "盈亏",
  "drawdown": "最大回撤",
  "win_rate": "胜率",
  "unrealized_pnl": "未实现盈亏"
}
```

### 持仓表现
```bash
GET /apps/positions

Response:
{
  "vlm": "交易量",
  "total": "开单数",
  "spot": "现货数",
  "perpetuals": "合约数",
  "cross_rate": "杠杆率",
  "avg_time": "平均持仓时间",
  "avg_pnl": "平均盈亏",
  "closedPnl": "已关闭盈亏"
}
```

### 历史操作
```bash
GET /apps/history

Response:
{
  "data": [
    {
      "time": "时间戳",
      "coin": "币种",
      "dir": "方向",
      "px": "价格",
      "sz": "数量",
      "closedPnl": "已关闭盈亏"
    }
  ]
}
```

## 🤝 收藏功能

### 收藏/取消收藏
```bash
POST /apps/follow
{
  "type": "follow",  // follow 或 cancel
  "fdata": "0x..."
}
```

### 我的收藏
```bash
GET /apps/myfollows

Response:
{
  "data": [
    {
      "address": "0x...",
      "user_name": "用户",
      "level": "交易等级",
      "achievement": "成就",
      "average": "六芒星综合指数",
      "is_follow": true
    }
  ]
}
```

## 💰 跟单交易接口

### 创建跟单
```bash
POST /trade/create
{
  "copy_addr": "0x...",
  "mode": "smart",  // fixed 固定金额, smart 智能
  "amount": 100,
  "stop_loss": 10
}
```

### 更新跟单
```bash
POST /trade/edit
{
  "id": 1,
  "mode": "fixed",
  "amount": 100,
  "stop_loss": 0
}
```

### 停止跟单
```bash
POST /trade/stop
{
  "id": 1
}
```

### 跟单列表
```bash
GET /trade/list

Response:
{
  "data": [
    {
      "address": "0x...",
      "user_name": "用户名",
      "description": "语录",
      "avatar": "头像",
      "id": "跟单id",
      "ctime": "开始时间戳",
      "mode": "模式",
      "amount": "数量",
      "pnl": "盈亏",
      "pnl_rate": "收益率",
      "unrealized": "未实现盈亏",
      "value": "账户价值"
    }
  ]
}
```

### 跟单总览
```bash
GET /trade/summary?type=week

Response:
{
  "address": "0x...",
  "pnl": "盈亏",
  "pnl_rate": "收益率",
  "unrealized": "未实现盈亏",
  "value": "账户价值",
  "withdraw": "可提现",
  "data": "曲线数据"
}
```

### 跟单交易记录
```bash
POST /trade/orders
{
  "id": 1
}

Response:
{
  "data": [
    {
      "time": "时间戳",
      "coin": "币种",
      "leverage": "杠杆",
      "dir": "多空",
      "px": "价格",
      "sz": "数量",
      "closedPnl": "盈亏",
      "value": "价值",
      "fee": "手续费",
      "unrealized": "未实现盈亏"
    }
  ]
}
```

### 跟单提币
```bash
POST /trade/withdraw
{
  "amount": 100
}
```

## 💼 带单功能

### 带单汇总
```bash
GET /trade/mybring

Response:
{
  "address": "0x...",
  "copy_pnl": "带单收益",
  "copy_roi": "带单收益率",
  "win_rate": "胜率",
  "pnl_rate": "盈亏比",
  "copy_cnt": "带单数量",
  "copy_sum": "带单资金规模"
}
```

### 带单分润
```bash
GET /trade/myprofit

Response:
{
  "profit": "带单总分润",
  "withdraw": "已提现",
  "available": "可提现",
  "locked": "未结算",
  "profit_rate": "分润比例"
}
```

### 带单订单详情
```bash
GET /trade/myorder

Response:
{
  "data": [
    {
      "coin": "币种",
      "leverage": "杠杆",
      "dir": "多空",
      "value": "价值",
      "pnl": "盈亏",
      "copy_value": "跟单价值",
      "copy_pnl": "跟单盈亏",
      "profit_rate": "带单分润率",
      "copy_cnt": "跟随人数",
      "cprice": "开仓价",
      "eprice": "平仓价",
      "ctime": "创建时间",
      "etime": "平仓时间"
    }
  ]
}
```

### 分润提现
```bash
POST /trade/mywithdraw
{
  "amount": 100
}
```

## 🔧 使用示例

### 获取榜单数据
```javascript
// 获取稳健大师榜单
const response = await fetch('http://192.144.239.66/api/apps/master', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    page: 1,
    page_size: 10,
    type: 'week'
  })
});

const data = await response.json();
console.log(data.data); // 榜单数据
```

### 创建跟单
```javascript
// 跟随某个地址
const response = await fetch('http://192.144.239.66/api/trade/create', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    copy_addr: '0x...',
    mode: 'smart',
    amount: 100,
    stop_loss: 10
  })
});
```

## 📝 更新日志

### v1.0.0 (2026-03-11)
- ✅ 基于真实 API 文档创建
- ✅ 包含所有榜单接口
- ✅ 包含跟单交易接口
- ✅ 包含个人信息接口
- ✅ 包含带单功能接口

---

**注意：此 API 文档基于 http://192.144.239.66/api，为内网/测试地址。生产环境请使用正式域名。**
