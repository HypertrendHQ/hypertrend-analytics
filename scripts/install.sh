#!/bin/bash
# HyperTrend Analytics Skill 安装脚本

set -e

echo "🚀 安装 HyperTrend Analytics Skill..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 OpenClaw 是否安装
if ! command -v openclaw &> /dev/null; then
    echo -e "${RED}❌ 错误: OpenClaw 未安装${NC}"
    echo "请先安装 OpenClaw: https://docs.openclaw.ai"
    exit 1
fi

# 检查技能目录
SKILL_DIR="$HOME/.openclaw/skills/hypertrend-analytics"
if [ -d "$SKILL_DIR" ]; then
    echo -e "${YELLOW}⚠️ 技能已存在，是否覆盖? (y/n)${NC}"
    read -r response
    if [ "$response" != "y" ]; then
        echo "安装取消"
        exit 0
    fi
    rm -rf "$SKILL_DIR"
fi

# 创建目录
echo "📁 创建技能目录..."
mkdir -p "$SKILL_DIR"

# 下载 SKILL.md
echo "⬇️ 下载技能文件..."
if command -v curl &> /dev/null; then
    curl -fsSL \
        https://raw.githubusercontent.com/GuiPulp/hypertrend-analytics/main/SKILL.md \
        -o "$SKILL_DIR/SKILL.md"
elif command -v wget &> /dev/null; then
    wget -q \
        https://raw.githubusercontent.com/GuiPulp/hypertrend-analytics/main/SKILL.md \
        -O "$SKILL_DIR/SKILL.md"
else
    echo -e "${RED}❌ 需要 curl 或 wget${NC}"
    exit 1
fi

# 创建配置目录
mkdir -p "$SKILL_DIR/references"

# 创建示例配置文件
echo "⚙️ 创建配置文件..."
cat > "$HOME/.openclaw/hypertrend.config.toml" << 'EOF'
# HyperTrend Analytics 配置
[hypertrend]
# API Key (可选，用于私有数据)
api_key = ""

# 监控阈值
whale_threshold = 500000      # USD
liquidation_alert = 5          # %
website_timeout = 3000         # ms

# 通知设置
[hypertrend.notifications]
telegram = ""      # Telegram Chat ID
discord = ""       # Discord Webhook URL
EOF

# 设置权限
chmod 600 "$HOME/.openclaw/hypertrend.config.toml"

echo ""
echo -e "${GREEN}✅ 安装完成!${NC}"
echo ""
echo "📍 安装位置: $SKILL_DIR"
echo "⚙️  配置文件: ~/.openclaw/hypertrend.config.toml"
echo ""
echo "📝 使用示例:"
echo "   - 分析地址: '分析HL地址 0x7a3f...9d2e'"
echo "   - 鲸鱼监控: '查看今日HL鲸鱼动态'"
echo "   - 生成推文: '基于今日HL数据生成推文'"
echo ""
echo "💡 提示: 编辑配置文件添加 API Key 以获取更详细数据"
echo ""
