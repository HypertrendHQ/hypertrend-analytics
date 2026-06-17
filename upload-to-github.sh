#!/bin/bash

# HyperTrend Analytics Skill - GitHub 上传脚本
# 用法: ./upload-to-github.sh

set -e

echo "🚀 HyperTrend Analytics v2.4.0 - GitHub 上传脚本"
echo "================================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查 git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ 错误: 请先安装 Git${NC}"
    echo "   Mac: brew install git"
    echo "   Linux: sudo apt-get install git"
    exit 1
fi

# 检查 gh CLI (可选)
if command -v gh &> /dev/null; then
    GH_CLI=true
    echo -e "${GREEN}✅ GitHub CLI 已安装${NC}"
else
    GH_CLI=false
    echo -e "${YELLOW}⚠️  建议安装 GitHub CLI: brew install gh${NC}"
fi

# 获取 GitHub 用户名
echo ""
echo -e "${BLUE}📝 请输入您的 GitHub 用户名:${NC}"
read -p "> " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo -e "${RED}❌ 用户名不能为空${NC}"
    exit 1
fi

# 获取仓库名
echo ""
echo -e "${BLUE}📝 请输入仓库名称 (默认: hypertrend-analytics):${NC}"
read -p "> " REPO_NAME
REPO_NAME=${REPO_NAME:-hypertrend-analytics}

echo ""
echo -e "${GREEN}📋 上传信息确认:${NC}"
echo "   GitHub 用户: $GITHUB_USERNAME"
echo "   仓库名称: $REPO_NAME"
echo "   版本: v2.4.0"
echo ""
read -p "确认上传? (y/n): " CONFIRM

if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo -e "${YELLOW}⚠️  已取消上传${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}🔄 开始上传流程...${NC}"
echo ""

# 检查是否已有 git 仓库
if [ -d ".git" ]; then
    echo -e "${YELLOW}⚠️  检测到已有 git 仓库${NC}"
    read -p "是否重新初始化? (y/n): " REINIT
    if [ "$REINIT" = "y" ] || [ "$REINIT" = "Y" ]; then
        rm -rf .git
    fi
fi

# 初始化 git
echo -e "${BLUE}📦 初始化 Git 仓库...${NC}"
git init
git branch -m main 2>/dev/null || true

# 添加所有文件
echo -e "${BLUE}📁 添加文件到仓库...${NC}"
git add .

# 提交
echo -e "${BLUE}💾 提交更改...${NC}"
git commit -m "Release v2.4.0: HyperTrend Analytics Skill

Features:
- On-chain credit analysis (Gravity Index)
- HL address analysis & whale monitoring
- Auto copytrading system
- Leaderboard rankings & tracking
- Platform copytrading via HyperTrend
- Address real-time monitoring

Complete skill package for OpenClaw AI Agent."

# 添加远程仓库
echo -e "${BLUE}🔗 配置远程仓库...${NC}"
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo ""
echo -e "${GREEN}✅ 本地仓库准备完成!${NC}"
echo ""

# 检查 GitHub CLI 是否可用
if [ "$GH_CLI" = true ]; then
    echo -e "${BLUE}🔍 检查 GitHub 认证状态...${NC}"
    if gh auth status &>/dev/null; then
        echo -e "${GREEN}✅ 已登录 GitHub${NC}"
        
        # 检查仓库是否存在
        if gh repo view "$GITHUB_USERNAME/$REPO_NAME" &>/dev/null; then
            echo -e "${YELLOW}⚠️  仓库已存在${NC}"
            read -p "是否推送到现有仓库? (y/n): " PUSH_EXISTING
            if [ "$PUSH_EXISTING" = "y" ] || [ "$PUSH_EXISTING" = "Y" ]; then
                echo -e "${BLUE}📤 推送到 GitHub...${NC}"
                git push -u origin main --force
            fi
        else
            echo -e "${BLUE}🏗️  创建 GitHub 仓库...${NC}"
            gh repo create "$REPO_NAME" --public --source=. --remote=origin --push
        fi
        
        echo ""
        echo -e "${GREEN}🎉 上传成功!${NC}"
        echo ""
        echo -e "${BLUE}📎 仓库地址:${NC}"
        echo "   https://github.com/$GITHUB_USERNAME/$REPO_NAME"
        echo ""
        echo -e "${BLUE}📦 安装命令:${NC}"
        echo "   curl -fsSL https://raw.githubusercontent.com/$GITHUB_USERNAME/$REPO_NAME/main/scripts/install.sh | bash"
        echo ""
        
        # 创建 Release
        read -p "是否创建 v2.4.0 Release? (y/n): " CREATE_RELEASE
        if [ "$CREATE_RELEASE" = "y" ] || [ "$CREATE_RELEASE" = "Y" ]; then
            echo -e "${BLUE}🏷️  创建 Release...${NC}"
            gh release create v2.4.0 \
                --title "HyperTrend Analytics v2.4.0" \
                --notes "## 🎉 HyperTrend Analytics v2.4.0

### ✨ Features
- **On-chain Credit Analysis**: Gravity Index & Hexagram scoring
- **Address Analysis**: HL position, leverage, PnL tracking
- **Whale Monitoring**: >\$500K position alerts
- **Leaderboard**: Gravity/PnL/Win rate/Copy trading rankings
- **Platform Copytrading**: Direct HyperTrend integration
- **Address Monitoring**: Real-time operation & fund tracking

### 🚀 Quick Install
\`\`\`bash
curl -fsSL https://raw.githubusercontent.com/$GITHUB_USERNAME/$REPO_NAME/main/scripts/install.sh | bash
\`\`\`"
            echo -e "${GREEN}✅ Release 创建成功!${NC}"
        fi
        
    else
        echo -e "${YELLOW}⚠️  未登录 GitHub CLI${NC}"
        echo "   运行: gh auth login"
        echo ""
        MANUAL_PUSH=true
    fi
else
    MANUAL_PUSH=true
fi

# 手动推送说明
if [ "$MANUAL_PUSH" = true ]; then
    echo ""
    echo -e "${YELLOW}📋 请手动完成以下步骤:${NC}"
    echo ""
    echo "1️⃣  在 GitHub 创建仓库:"
    echo "   访问: https://github.com/new"
    echo "   仓库名: $REPO_NAME"
    echo "   选择 Public"
    echo ""
    echo "2️⃣  推送代码:"
    echo -e "   ${BLUE}git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git${NC}"
    echo -e "   ${BLUE}git branch -M main${NC}"
    echo -e "   ${BLUE}git push -u origin main${NC}"
    echo ""
    echo "3️⃣  创建 Release (可选):"
    echo "   访问: https://github.com/$GITHUB_USERNAME/$REPO_NAME/releases/new"
    echo "   Tag: v2.4.0"
    echo "   Title: HyperTrend Analytics v2.4.0"
    echo ""
fi

echo ""
echo -e "${GREEN}✨ 完成!${NC}"
echo ""
