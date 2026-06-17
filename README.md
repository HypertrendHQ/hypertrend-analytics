# HyperTrend Analytics Skill

基于 Hyperliquid 的链上信用分析与智能交易工具，专为 OpenClaw 设计。

## 🚀 核心功能

- **🔗 引力指数查询** - HyperTrend 六芒星信用评分系统
- **👤 HL 地址分析** - 持仓、杠杆、盈亏全面分析
- **🐋 鲸鱼监控** - 追踪 >$500K 大仓位动态
- **📊 地址对比** - 多地址交易表现横向对比
- **📝 数据推文** - 基于真实数据生成社交媒体内容
- **🤖 自动跟单** - 智能筛选并自动跟随优质交易者
- **📈 榜单系统** - 引力/收益/胜率/带单多维度榜单
- **🔔 变化追踪** - 榜单排名变化实时监控
- **💰 平台跟单** - HyperTrend 平台直接跟单交易
- **👁️ 地址监控** - 实时追踪地址操作和资金变动
- **🎯 风险偏好匹配** - 根据用户风险偏好智能推荐交易者 ⭐v2.5.0

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/hypertrend/hypertrend-analytics-skill.git

# 进入目录
cd hypertrend-analytics-skill

# 安装到 OpenClaw
mv . ~/.openclaw/skills/hypertrend-analytics

# 安装依赖
pip install requests
```

## 🆕 v2.5.0 新特性：智能风险偏好匹配

根据用户的风险偏好，智能匹配并推荐最适合的交易者。

### 风险偏好类型

| 类型 | 英文名 | 特征描述 |
|------|--------|---------|
| **保守型** | conservative | 低风险，追求稳定收益，最大回撤控制在10%以内 |
| **稳健型** | moderate | 中等风险，平衡收益与风险，最大回撤控制在20%以内 |
| **进取型** | aggressive | 高风险高收益，可接受较大回撤，追求超额收益 |
| **量化型** | quantitative | 数据驱动，关注交易频率和策略稳定性 |

### 使用方法

```bash
# 命令行使用
cd ~/.openclaw/skills/hypertrend-analytics/scripts

python3 risk_match.py conservative    # 保守型推荐
python3 risk_match.py moderate        # 稳健型推荐
python3 risk_match.py aggressive      # 进取型推荐
python3 risk_match.py quantitative    # 量化型推荐
```

### OpenClaw 对话示例

```
用户: 我是稳健型投资者，帮我推荐几个合适的交易者跟单

AI: 
============================================================
🎯 HyperTrend 智能跟单推荐
📊 风险偏好: 稳健型
📝 中等风险，平衡收益与风险，最大回撤控制在20%以内
============================================================

【推荐 #1】匹配度: 93.26/100
├─ 地址: 0xe117d3d94b30f7e7aa...
├─ 榜单排名: #24
├─ 日收益: $7156.40
├─ 胜率: 100.0%
├─ 最大回撤: 0.1%
├─ 预估杠杆: 1.0x
└─ 💡 推荐理由: 胜率高达 100.0%，稳定性优秀；
    最大回撤仅 0.1%，风控出色；
    日收益 $7156.40，盈利能力强劲

💰 跟单操作:
  查看详情: openclaw hypertrend address <地址>
  开始跟单: openclaw hypertrend copytrade <地址> --amount <金额>
```

## 📖 使用示例

详见 [SKILL.md](./SKILL.md)

## 🔧 开发路线图

- ✅ v2.0.0 - 基础跟单功能
- ✅ v2.1.0 - 鲸鱼监控系统
- ✅ v2.2.0 - 榜单系统 + 变化追踪
- ✅ v2.3.0 - 平台跟单功能
- ✅ v2.4.0 - 地址实时监控
- ✅ **v2.5.0 - 智能风险偏好匹配** 🆕
- 🚧 v2.6.0 - AI 策略分析 (开发中)
- 📋 v2.7.0 - 社交交易功能 (计划中)

## 🤝 贡献指南

欢迎提交 Pull Request！

## 📄 许可证

MIT License