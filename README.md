# HyperTrend Analytics Skill

HyperTrend Analytics is an agent-ready skill for accessing and analyzing HyperTrend and Hyperliquid trader data. It helps AI agents fetch leaderboard rankings, compare wallet performance, identify high-quality trader candidates, and match copy-trading ideas to different risk profiles using real HyperTrend data instead of static examples.

The skill includes a lightweight CLI for retrieving leaderboards, exporting JSON, inspecting schemas, and ranking traders by conservative, moderate, aggressive, or quantitative preferences. It is designed to make HyperTrend market intelligence easier for agents to use while keeping analysis transparent, source-aware, and risk-conscious.

HyperTrend Analytics 是一个面向 Agent 的 HyperTrend 与 Hyperliquid 交易数据分析 Skill。它可以帮助 AI Agent 获取排行榜、比较钱包表现、发现高质量交易者，并根据不同风险偏好匹配跟单候选人。

该 Skill 内置轻量级 CLI，可用于获取榜单、导出 JSON、查看数据结构，并按保守、稳健、进取或量化偏好筛选交易者，让 Agent 更方便地使用真实 HyperTrend 数据进行透明、可追溯、风险意识更强的分析。

## 🚀 核心功能

- **🔗 引力指数 / Gravity Index** - HyperTrend 六芒星信用评分与综合交易质量评估
- **🏅 信用信誉排行 / Credit Reputation Ranking** - 基于信用分、生态分、社交信用和身份一致性的声誉榜
- **🧠 聪明钱榜单 / Smart Money Ranking** - 发现高交易量、高收益或高关注度的聪明钱地址
- **✅ 认证交易员 / Certified Traders** - 获取平台认证交易员数据，供 Agent 做候选人研究
- **👤 HL 地址分析 / HL Address Analysis** - 分析持仓、杠杆、盈亏和账户价值
- **🐋 鲸鱼监控 / Whale Monitoring** - 追踪大仓位和高价值地址动态
- **📊 地址对比 / Address Comparison** - 横向比较多个地址的交易表现
- **📝 数据推文 / Data-Backed Content** - 基于真实数据生成社交媒体内容
- **🤖 自动跟单 / Copy-Trading Research** - 智能筛选优质交易者，辅助跟单决策
- **📈 多维榜单 / Multi-Dimensional Leaderboards** - 覆盖引力、收益、胜率、带单、信用和聪明钱榜单
- **🔔 排名变化 / Ranking Changes** - 跟踪榜单排名变化和新晋地址
- **💰 平台跟单 / Platform Copy Trading** - 支持 HyperTrend 平台跟单流程研究
- **👁️ 地址监控 / Address Monitoring** - 实时追踪地址操作和资金变动
- **🎯 风险偏好匹配 / Risk-Profile Matching** - 根据保守、稳健、进取或量化偏好推荐交易者

## 📦 安装

```bash
# 克隆仓库
git clone https://github.com/HypertrendHQ/hypertrend-analytics.git

# 进入目录
cd hypertrend-analytics

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

### 公开榜单 / Public Leaderboards

```bash
# 统一 CLI（推荐给 agent 使用）
python scripts/hypertrend_cli.py leaderboard --type gravity --period week --limit 10
python scripts/hypertrend_cli.py leaderboard --type credrank --period week --limit 10
python scripts/hypertrend_cli.py leaderboard --type smartmoney --period week --limit 10
python scripts/hypertrend_cli.py leaderboard --type traders --period week --limit 10
```

支持周期：`day`、`week`、`month`、`allTime`。

CLI 类型：

| CLI Type | 中文说明 | English |
| --- | --- | --- |
| `gravity` | 引力指数榜 | Gravity Index |
| `credrank` | 信用信誉排行榜 | Credit Reputation Ranking |
| `traders` | 认证交易员，当前可能返回空数据 | Certified Traders |
| `smartmoney` | 聪明钱排行榜 | Smart Money Ranking |

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
