---
name: hypertrend-copytrading
description: HyperTrend 自动跟单系统 - 基于引力指数筛选优质交易者，自动复制交易，智能风险控制
version: 1.0.0
author: HyperTrend Team
homepage: https://www.hypertrend.top/
license: MIT
---

# HyperTrend CopyTrading 自动跟单系统

基于 HyperTrend 引力指数和六芒星评分的智能跟单系统。

## 🎯 核心功能

| 功能 | 描述 | 状态 |
|------|------|:----:|
| **智能筛选** | 基于引力指数自动筛选优质带单者 | ✅ |
| **自动跟单** | 实时复制目标交易者开平仓操作 | ✅ |
| **风险控制** | 多重风控机制保护本金 | ✅ |
| **收益追踪** | 实时统计跟单收益和表现 | ✅ |
| **智能调仓** | 根据市场情况动态调整仓位 | ✅ |

## 📊 跟单策略

### 策略模板

#### 保守型 (Conservative)
```json
{
  "name": "稳健收益",
  "description": "高信用分交易者，低杠杆，稳健收益",
  "filters": {
    "gravity_index_min": 800,
    "win_rate_min": 70,
    "max_leverage": 8,
    "max_drawdown": 15,
    "min_trading_days": 30
  },
  "risk_management": {
    "position_size": 0.1,
    "max_positions": 3,
    "stop_loss": 0.05,
    "take_profit": 0.15
  }
}
```

#### 平衡型 (Balanced)
```json
{
  "name": "均衡配置",
  "description": "中等风险收益比，适合大多数用户",
  "filters": {
    "gravity_index_min": 650,
    "win_rate_min": 60,
    "max_leverage": 12,
    "max_drawdown": 25,
    "min_trading_days": 14
  },
  "risk_management": {
    "position_size": 0.2,
    "max_positions": 5,
    "stop_loss": 0.08,
    "take_profit": 0.25
  }
}
```

#### 激进型 (Aggressive)
```json
{
  "name": "高收益",
  "description": "高波动，高收益潜力，高风险承受能力",
  "filters": {
    "gravity_index_min": 500,
    "win_rate_min": 55,
    "max_leverage": 20,
    "max_drawdown": 40,
    "min_trading_days": 7
  },
  "risk_management": {
    "position_size": 0.3,
    "max_positions": 8,
    "stop_loss": 0.12,
    "take_profit": 0.40
  }
}
```

## ⚙️ 配置

### 基础配置

```toml
[copytrading]
enabled = true
api_key = "your_hypertrend_api_key"
private_key = "your_wallet_private_key"  # 用于执行交易

# 默认策略
default_strategy = "balanced"

# 全局风险控制
[copytrading.global_risk]
max_total_position = 0.5        # 最大总仓位 50%
max_daily_loss = 0.05           # 最大日亏损 5%
max_drawdown = 0.20             # 最大回撤 20%
emergency_stop = true           # 紧急止损

# 跟单设置
[copytrading.settings]
check_interval = 30             # 检查间隔 (秒)
slippage_tolerance = 0.005      # 滑点容忍度 0.5%
auto_adjust_size = true         # 自动调整仓位大小
```

### 策略配置

```toml
[copytrading.strategy.conservative]
name = "稳健收益"
gravity_index_min = 800
win_rate_min = 70
max_leverage = 8
position_size = 0.1
max_positions = 3

[copytrading.strategy.balanced]
name = "均衡配置"
gravity_index_min = 650
win_rate_min = 60
max_leverage = 12
position_size = 0.2
max_positions = 5

[copytrading.strategy.aggressive]
name = "高收益"
gravity_index_min = 500
win_rate_min = 55
max_leverage = 20
position_size = 0.3
max_positions = 8
```

## 🚀 使用方法

### 1. 启动跟单系统

```
用户: 启动自动跟单，使用稳健策略

AI输出:
🤖 HyperTrend 自动跟单系统启动

策略: 稳健收益 (Conservative)
筛选条件:
├─ 引力指数 ≥ 800
├─ 胜率 ≥ 70%
├─ 最大杠杆 ≤ 8x
└─ 最大回撤 ≤ 15%

正在扫描符合条件的交易者...

✅ 发现 3 个符合条件的交易者:
├─ 0x7a3f...9d2e (引力 850, 胜率 78%, 杠杆 6x)
├─ 0x9c1b...4f8a (引力 820, 胜率 72%, 杠杆 8x)
└─ 0x3d2e...8b5c (引力 805, 胜率 75%, 杠杆 7x)

初始资金: $10,000
单仓上限: $1,000 (10%)
最大持仓: 3 个

⚠️ 风险提示:
• 加密货币交易风险高，可能损失全部本金
• 请确保了解自动跟单的风险
• 建议先用小额资金测试

确认启动跟单? (y/n)
```

### 2. 查看跟单状态

```
用户: 查看跟单状态

AI输出:
📊 HyperTrend 跟单状态报告

运行时间: 3天 4小时 32分钟
当前策略: 稳健收益

【跟随的交易者】

🥇 0x7a3f...9d2e (主力)
├─ 引力指数: 850 (精英级)
├─ 跟随资金: $1,000
├─ 当前持仓:
│   ├─ BTC Long 0.015 BTC @ $68,200
│   └─ ETH Long 0.25 ETH @ $3,850
├─ 未实现盈亏: +$125 (+12.5%)
├─ 历史胜率: 78%
└─ 跟随表现: ✅ 优秀

🥈 0x9c1b...4f8a
├─ 引力指数: 820 (精英级)
├─ 跟随资金: $800
├─ 当前持仓:
│   └─ SOL Long 5.5 SOL @ $142.50
├─ 未实现盈亏: +$45 (+5.6%)
├─ 历史胜率: 72%
└─ 跟随表现: ✅ 良好

🥉 0x3d2e...8b5c
├─ 引力指数: 805 (精英级)
├─ 跟随资金: $600 (未满仓)
├─ 当前持仓: 空仓等待信号
├─ 未实现盈亏: $0
├─ 历史胜率: 75%
└─ 跟随表现: ⏸️ 等待开仓

【收益统计】
├─ 总投入: $2,400
├─ 当前净值: $2,570
├─ 总收益: +$170 (+7.08%)
├─ 日收益: +$45 (+1.88%)
├─ 最大回撤: 3.2%
└─ 夏普比率: 2.4

【风险控制】
├─ 总仓位: 24% ✅ (安全)
├─ 剩余资金: $7,600
├─ 日亏损: -$12 (在范围内)
└─ 风控状态: 🟢 正常

【最近操作】
14:32 - 跟随 0x7a3f 加仓 BTC +0.005 BTC
12:15 - 跟随 0x9c1b 开仓 SOL 5.5 SOL
09:48 - 0x3d2e 平仓 ETH，跟随止盈 +$28

下次检查: 14:45 (30秒后)
```

### 3. 暂停/恢复跟单

```
用户: 暂停跟单

AI输出:
⏸️ 跟单系统已暂停

当前持仓保持，不再开新仓。
已持仓:
├─ BTC Long 0.015 BTC (+$125 unrealized)
├─ ETH Long 0.25 ETH (-$12 unrealized)
└─ SOL Long 5.5 SOL (+$45 unrealized)

如需恢复，输入: 恢复跟单
```

### 4. 紧急止损

```
用户: 执行紧急止损

AI输出:
🚨 紧急止损执行中...

正在平掉所有持仓:
├─ 平仓 BTC Long 0.015 BTC @ $68,150
│   实现盈亏: +$118 (+11.8%)
├─ 平仓 ETH Long 0.25 ETH @ $3,845
│   实现盈亏: -$15 (-0.8%)
└─ 平仓 SOL Long 5.5 SOL @ $142.30
    实现盈亏: +$42 (+5.2%)

总实现盈亏: +$145 (+6.0%)
资金已转回钱包: $10,145

跟单系统已停止。
建议检查策略设置后重新开始。
```

## 🔧 核心工具

### start_copytrading(strategy)
启动自动跟单系统

**参数:**
- `strategy`: 策略名称 (conservative/balanced/aggressive)

**示例:**
```javascript
start_copytrading("conservative")
```

### stop_copytrading()
停止跟单系统，保持持仓

**示例:**
```javascript
stop_copytrading()
```

### emergency_stop()
紧急止损，平掉所有持仓

**示例:**
```javascript
emergency_stop()
```

### get_copytrading_status()
获取跟单系统状态

**返回:**
- 跟随的交易者列表
- 当前持仓
- 收益统计
- 风控状态

**示例:**
```javascript
get_copytrading_status()
```

### adjust_strategy(new_strategy)
动态调整跟单策略

**参数:**
- `new_strategy`: 新策略名称

**示例:**
```javascript
adjust_strategy("aggressive")
```

### set_risk_limits(limits)
设置风险控制参数

**参数:**
- `limits`: 风险限制对象

**示例:**
```javascript
set_risk_limits({
  max_daily_loss: 0.03,
  max_drawdown: 0.15
})
```

## 🛡️ 风险控制

### 多层风控机制

1. **交易者筛选层**
   - 引力指数门槛
   - 胜率要求
   - 历史回撤限制
   - 最低交易天数

2. **资金管理层**
   - 单仓上限
   - 总仓位上限
   - 杠杆倍数限制
   - 分散投资要求

3. **实时监控层**
   - 日亏损限制
   - 最大回撤监控
   - 异常交易检测
   - 流动性检查

4. **紧急保护层**
   - 自动止损
   - 黑天鹅保护
   - 系统故障保护
   - 手动紧急停止

### 风控触发条件

| 级别 | 条件 | 操作 |
|------|------|------|
| 🟡 警告 | 单日亏损 >3% | 降低仓位50% |
| 🟠 注意 | 单日亏损 >5% | 暂停开新仓 |
| 🔴 危险 | 回撤 >15% | 减仓至30% |
| 🚨 紧急 | 回撤 >20% | 全部平仓停止 |

## 📈 收益统计

### 统计指标

- **总收益率**: (当前净值 - 初始资金) / 初始资金
- **日收益率**: 24小时收益变化
- **最大回撤**: 从高点到低点的最大跌幅
- **夏普比率**: 收益/风险比
- **胜率**: 盈利交易次数 / 总交易次数
- **盈亏比**: 平均盈利 / 平均亏损

### 报告生成

```
用户: 生成周度跟单报告

AI输出:
📊 HyperTrend 跟单周报
统计周期: 2026-03-02 至 2026-03-09

【总体表现】
├─ 初始资金: $10,000
├─ 期末净值: $11,250
├─ 总收益: +$1,250 (+12.5%)
├─ 日均收益: +$178 (+1.78%)
├─ 最大回撤: 4.2%
├─ 夏普比率: 2.8
└─ 胜率: 68%

【分交易者表现】
├─ 0x7a3f...9d2e: +$680 (+68% weight)
├─ 0x9c1b...4f8a: +$420 (+34% weight)
└─ 0x3d2e...8b5c: +$150 (+12% weight)

【交易统计】
├─ 总交易: 23笔
├─ 盈利: 16笔 (69.6%)
├─ 亏损: 7笔 (30.4%)
├─ 平均持仓: 2.3天
└─ 平均杠杆: 7.5x

【风险指标】
├─ 最大日亏损: -$85 (-0.85%)
├─ 连续亏损天数: 1天
├─ 波动率: 12.3%
└─ Beta系数: 0.85 (相对市场)

【本周亮点】
✅ 成功跟随 BTC 反弹行情
✅ 及时止损 ETH 下跌
✅ 捕捉到 SOL 突破机会

【改进建议】
💡 可适当增加仓位至15%
💡 关注新增的高分交易者
💡 考虑加入趋势策略

下周展望: 继续当前策略，关注市场变化
```

## 🎨 最佳实践

### 新手建议

1. **从小额开始**
   - 初始资金: $500-$1000
   - 熟悉系统后再增加

2. **选择稳健策略**
   - 先用保守型策略测试
   - 了解风险后再调整

3. **定期复盘**
   - 每周查看收益报告
   - 分析成功/失败原因

### 进阶技巧

1. **组合策略**
   - 70% 稳健 + 30% 激进
   - 分散风险提高收益

2. **动态调整**
   - 牛市提高仓位
   - 熊市降低风险

3. **多交易所配置**
   - Hyperliquid 主力
   - 其他所对冲风险

## ⚠️ 风险提示

**自动跟单存在以下风险：**

1. **市场风险**
   - 加密货币价格波动大
   - 可能损失全部本金

2. **策略风险**
   - 历史表现不代表未来
   - 策略可能失效

3. **技术风险**
   - 系统故障可能
   - 网络延迟影响

4. **流动性风险**
   - 极端行情可能无法成交
   - 滑点可能导致亏损

**请确保：**
- 只用闲置资金投资
- 了解所有风险
- 设置合理的止损
- 不要投入无法承受损失的资金

## 📞 支持与反馈

- Telegram: https://t.me/HyperTrendHQ
- Discord: https://discord.gg/MEFA8Rbq
- Email: support@hypertrend.top

---

**自动跟单有风险，投资需谨慎！**
