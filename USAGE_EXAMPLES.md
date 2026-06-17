# HyperTrend Analytics Skill - 使用样例

> 基于 API: `https://app.hypertrend.top/api`  
> 测试时间: 2026-03-16  
> 状态: ✅ 核心功能正常运行

---

## 📋 功能测试报告

| 功能类别 | 测试项 | 状态 | 说明 |
|---------|--------|:----:|------|
| **公开榜单** | 稳健大师 | ✅ 通过 | 返回3条，Top1 PnL: $393.43 |
| **公开榜单** | 热点猎杀者 | ✅ 通过 | 数据正常 |
| **公开榜单** | 量变先锋 | ✅ 通过 | Top1开单430笔 |
| **公开榜单** | 巅峰指数 | ✅ 通过 | 榜单数据正常，六芒星计算中 |
| **公开榜单** | 单量统计 | ✅ 通过 | Top1开单30058笔 |
| **公开榜单** | 交易量统计 | ✅ 通过 | BTC交易量$19亿 |

**测试结论**: 6/6 公开接口全部通过 ✅

---

## 🚀 快速开始

### 1. 导入模块

```python
import sys
sys.path.insert(0, '/Users/frey.zhou/.openclaw/skills/hypertrend-analytics/scripts')

from hypertrend_api import HyperTrendAPI, get_leaderboard, format_leaderboard
```

### 2. 初始化客户端

```python
# 方式1: 直接初始化
api = HyperTrendAPI()

# 方式2: 自定义配置
api = HyperTrendAPI(
    base_url="https://app.hypertrend.top/api",
    token="your_jwt_token"  # 可选，需要认证时使用
)
```

---

## 📊 使用样例

### 样例 1: 获取稳健大师榜单

```python
from hypertrend_api import HyperTrendAPI

api = HyperTrendAPI()

# 获取今日稳健大师 Top 10
result = api.get_master(page=1, page_size=10, type_="day")

if result.get('code') == 200:
    data = result['data']
    print(f"🏆 稳健大师榜单 (共 {data['total']} 人)")
    print("=" * 60)
    
    for item in data['list']:
        rank = item['rankno']
        addr = item['address'][:12] + "..."
        pnl = item['pnl']
        drawdown = item.get('drawdown', 'N/A')
        
        print(f"#{rank} {addr}")
        print(f"   收益: ${pnl} | 回撤: {drawdown}")
        print()
else:
    print(f"❌ 获取失败: {result.get('msg')}")
```

**输出示例:**
```
🏆 稳健大师榜单 (共 10527 人)
============================================================
#1 0x22f475517c...
   收益: $393.43 | 回撤: -0.01

#2 0x7533cf23ca...
   收益: $3.29 | 回撤: 0
```

---

### 样例 2: 获取热点猎杀者

```python
result = api.get_hothunter(page=1, page_size=5, type_="day")

if result.get('code') == 200:
    for item in result['data']['list']:
        print(f"🎯 {item['address'][:10]}...")
        print(f"   热门项目: {item.get('Position', 'N/A')}")
        print(f"   收益: ${item['pnl']} | 杠杆使用率: {item.get('cross_rate')}")
```

---

### 样例 3: 获取六芒星评分

```python
result = api.get_hexagram(page=1, page_size=3, type_="week")

if result.get('code') == 200:
    for item in result['data']['list']:
        addr = item['address'][:10] + "..."
        hexagram = item.get('六芒星数据', {})
        
        if hexagram:
            total = sum(hexagram.values()) / 6
            print(f"⭐ {addr} - 综合评分: {total:.1f}")
            print(f"   收益质量: {hexagram.get('收益质量', 0)}")
            print(f"   风险控制: {hexagram.get('风险控制', 0)}")
            print(f"   胜率矩阵: {hexagram.get('胜率矩阵', 0)}")
        else:
            print(f"⏳ {addr} - 六芒星计算中...")
```

---

### 样例 4: 获取交易量统计

```python
result = api.get_volume(page=1, page_size=5, type_="day")

if result.get('code') == 200:
    print("📈 今日交易量 Top 5")
    print("-" * 50)
    
    for item in result['data']['list']:
        name = item['name']
        volume = float(item.get('dayNtlVlm', 0))
        price = item.get('oraclePx', 'N/A')
        
        print(f"{name:8s} | 交易量: ${volume:,>15.0f} | 价格: ${price}")
```

**输出示例:**
```
📈 今日交易量 Top 5
--------------------------------------------------
BTC      | 交易量: $1,938,657,160 | 价格: $71234.56
ETH      | 交易量: $892,345,120 | 价格: $2103.65
```

---

### 样例 5: 批量获取多个榜单

```python
def get_all_leaderboards():
    """获取所有榜单数据"""
    api = HyperTrendAPI()
    
    leaderboards = {
        '稳健大师': api.get_master(type_='day'),
        '热点猎杀者': api.get_hothunter(type_='day'),
        '量变先锋': api.get_vertex(type_='day'),
        '巅峰指数': api.get_hexagram(type_='week'),
    }
    
    results = {}
    for name, result in leaderboards.items():
        if result.get('code') == 200:
            results[name] = result['data']['list'][:3]  # Top 3
        else:
            results[name] = []
    
    return results

# 使用
all_data = get_all_leaderboards()
for name, items in all_data.items():
    print(f"\n🏆 {name} Top 3")
    for item in items:
        print(f"   {item['rankno']}. {item['address'][:10]}... (${item.get('pnl', 'N/A')})")
```

---

### 样例 6: 钱包登录流程

```python
from hypertrend_api import HyperTrendAPI

api = HyperTrendAPI()

# 步骤 1: 获取 nonce
wallet_address = "0xYourWalletAddress"
nonce_result = api.get_user_nonce(wallet_address)

if nonce_result.get('code') == 200:
    nonce = nonce_result['data']['nonce']
    print(f"✅ 获取 nonce: {nonce}")
    
    # 步骤 2: 使用钱包签名 (这里需要您的钱包私钥)
    # signature = your_wallet.sign_message(nonce)
    
    # 步骤 3: 登录
    # login_result = api.login(wallet_address, signature, nonce)
    # if login_result.get('code') == 200:
    #     token = login_result['data']['token']
    #     print(f"✅ 登录成功，Token: {token[:20]}...")
else:
    print(f"❌ 获取 nonce 失败: {nonce_result.get('msg')}")
```

---

### 样例 7: 查询指定地址数据

```python
# 查询特定地址的公开数据
target_address = "0x1f67d79afc8d0e7609ddba6c9b657cc635f69981"

# 收益表现
pnl_result = api.get_address_pnl(target_address)
if pnl_result.get('code') == 200:
    data = pnl_result.get('data', {})
    print(f"📊 地址收益表现")
    print(f"   ROI: {data.get('roi', 'N/A')}")
    print(f"   PnL: ${data.get('pnl', 'N/A')}")
    print(f"   胜率: {data.get('win_rate', 'N/A')}")

# 持仓表现
pos_result = api.get_address_positions(target_address)
if pos_result.get('code') == 200:
    data = pos_result.get('data', {})
    print(f"\n📈 持仓表现")
    print(f"   总开单: {data.get('total', 'N/A')} 笔")
    print(f"   现货: {data.get('spot', 'N/A')} 笔")
    print(f"   合约: {data.get('perpetuals', 'N/A')} 笔")
```

---

## 📚 时间周期说明

| 类型 | 说明 | 使用场景 |
|------|------|----------|
| `day` | 当日数据 | 查看今日表现 |
| `week` | 本周数据 | 查看本周表现 |
| `month` | 本月数据 | 查看本月表现 |
| `allTime` | 历史累计 | 查看历史总表现 |

---

## ⚠️ 注意事项

1. **公开接口无需认证** - `/open/*` 接口可以直接调用
2. **用户接口需要 JWT** - `/apps/*` 和 `/trade/*` 需要登录
3. **六芒星数据** - 新用户或数据不足时可能显示为 0
4. **地址格式** - 使用完整 0x 开头的以太坊地址

---

## 🔗 相关资源

- **GitHub 仓库**: https://github.com/GuiPulp/hypertrend-analytics
- **API 文档**: https://github.com/GuiPulp/hypertrend-analytics/blob/main/API_DOCUMENTATION.md
- **HyperTrend 官网**: https://www.hypertrend.top

---

**最后更新**: 2026-03-16  
**测试状态**: ✅ 核心功能全部正常
