#!/usr/bin/env python3
"""
HyperTrend API 客户端 - 真实数据获取
基于 https://app.hypertrend.top/api
"""

import os
import json
import requests
from typing import Dict, List, Optional

class HyperTrendAPI:
    """HyperTrend API 客户端"""
    
    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = base_url or os.getenv('HYPERTREND_API_URL', 'https://app.hypertrend.top/api')
        self.token = token or os.getenv('HYPERTREND_API_TOKEN')
        self.headers = {
            'Content-Type': 'application/json'
        }
        if self.token:
            self.headers['Authorization'] = f'Bearer {self.token}'
    
    def _post(self, endpoint: str, data: Dict = None) -> Dict:
        """POST 请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=data or {}, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    def _get(self, endpoint: str) -> Dict:
        """GET 请求"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    
    # ========== 榜单接口 ==========
    
    def get_hothunter(self, page: int = 1, page_size: int = 10, type_: str = "week") -> Dict:
        """获取热点猎杀者榜单"""
        return self._post('/open/hothunter', {
            'page': page,
            'page_size': page_size,
            'type': type_
        })
    
    def get_master(self, page: int = 1, page_size: int = 10, type_: str = "week") -> Dict:
        """获取稳健大师榜单"""
        return self._post('/open/master', {
            'page': page,
            'page_size': page_size,
            'type': type_
        })
    
    def get_vertex(self, page: int = 1, page_size: int = 10, type_: str = "week") -> Dict:
        """获取量变先锋榜单"""
        return self._post('/open/vertex', {
            'page': page,
            'page_size': page_size,
            'type': type_
        })
    
    def get_hexagram(self, page: int = 1, page_size: int = 10, type_: str = "week") -> Dict:
        """获取巅峰指数(六芒星)榜单"""
        return self._post('/open/hexagram', {
            'page': page,
            'page_size': page_size,
            'type': type_
        })
    
    def get_billings(self, page: int = 1, page_size: int = 10, type_: str = "week") -> Dict:
        """获取单量统计"""
        return self._post('/open/billings', {
            'page': page,
            'page_size': page_size,
            'type': type_
        })
    
    def get_volume(self, page: int = 1, page_size: int = 10, type_: str = "week") -> Dict:
        """获取交易量统计"""
        return self._post('/open/vlm', {
            'page': page,
            'page_size': page_size,
            'type': type_
        })
    
    # ========== 个人信息接口 ==========
    
    def get_personal(self) -> Dict:
        """获取个人信息(六芒星)"""
        return self._get('/apps/personal')
    
    def get_account(self) -> Dict:
        """获取账户资产"""
        return self._get('/apps/account')
    
    def get_pnl(self) -> Dict:
        """获取收益表现"""
        return self._get('/apps/pnl')
    
    def get_positions(self) -> Dict:
        """获取持仓表现"""
        return self._get('/apps/positions')
    
    def get_history(self) -> Dict:
        """获取历史操作"""
        return self._get('/apps/history')
    
    # ========== 跟单接口 ==========
    
    def get_copy_list(self) -> Dict:
        """获取跟单列表"""
        return self._get('/trade/list')
    
    def get_copy_summary(self, type_: str = "week") -> Dict:
        """获取跟单总览"""
        return self._get(f'/trade/summary?type={type_}')
    
    def create_copy(self, copy_addr: str, mode: str = "smart", amount: float = 100, stop_loss: float = 10) -> Dict:
        """创建跟单"""
        return self._post('/trade/create', {
            'copy_addr': copy_addr,
            'mode': mode,
            'amount': amount,
            'stop_loss': stop_loss
        })
    
    def update_copy(self, copy_id: int, mode: str = "fixed", amount: float = 100, stop_loss: float = 0) -> Dict:
        """更新跟单"""
        return self._post('/trade/edit', {
            'id': copy_id,
            'mode': mode,
            'amount': amount,
            'stop_loss': stop_loss
        })
    
    def stop_copy(self, copy_id: int) -> Dict:
        """停止跟单"""
        return self._post('/trade/stop', {'id': copy_id})
    
    def get_copy_orders(self, copy_id: int) -> Dict:
        """获取跟单交易记录"""
        return self._post('/trade/orders', {'id': copy_id})
    
    # ========== 收藏接口 ==========
    
    def get_follows(self) -> Dict:
        """获取我的收藏"""
        return self._get('/apps/myfollows')
    
    def add_follow(self, address: str) -> Dict:
        """添加收藏"""
        return self._post('/apps/follow', {
            'type': 'follow',
            'fdata': address
        })
    
    def remove_follow(self, address: str) -> Dict:
        """取消收藏"""
        return self._post('/apps/follow', {
            'type': 'cancel',
            'fdata': address
        })
    
    # ========== 带单接口 ==========
    
    def get_my_bring(self) -> Dict:
        """获取带单汇总"""
        return self._get('/trade/mybring')
    
    def get_my_profit(self) -> Dict:
        """获取带单分润"""
        return self._get('/trade/myprofit')
    
    def get_my_orders(self) -> Dict:
        """获取带单订单详情"""
        return self._get('/trade/myorder')


# ========== 便捷函数 ==========

def get_leaderboard(leaderboard_type: str = "master", period: str = "week", limit: int = 10) -> List[Dict]:
    """
    获取榜单数据
    
    Args:
        leaderboard_type: master, hothunter, vertex, hexagram
        period: day, week, month, allTime
        limit: 返回数量
    
    Returns:
        榜单数据列表
    """
    api = HyperTrendAPI()
    
    endpoints = {
        'master': api.get_master,
        'hothunter': api.get_hothunter,
        'hothunter': api.get_hothunter,
        'vertex': api.get_vertex,
        'hexagram': api.get_hexagram
    }
    
    func = endpoints.get(leaderboard_type, api.get_master)
    result = func(page=1, page_size=limit, type_=period)
    
    if 'error' in result:
        return [{'error': result['error']}]
    
    return result.get('data', [])


def format_leaderboard(data: List[Dict], leaderboard_type: str) -> str:
    """格式化榜单输出"""
    if not data or (len(data) == 1 and 'error' in data[0]):
        error_msg = data[0].get('error', 'Unknown error') if data else 'No data'
        return f"❌ 获取数据失败: {error_msg}\n\n请检查:\n1. API Token 是否配置\n2. 网络连接是否正常\n3. API 服务是否可用"
    
    output = []
    output.append(f"🏆 HyperTrend {leaderboard_type.capitalize()} 榜单")
    output.append("=" * 50)
    output.append("")
    
    for i, item in enumerate(data[:10], 1):
        rank = item.get('rankno', i)
        address = item.get('address', 'Unknown')[:10] + '...'
        pnl = item.get('pnl', 'N/A')
        rio = item.get('rio', 'N/A')
        
        medal = {1: '🥇', 2: '🥈', 3: '🥉'}.get(rank, f'{rank}.')
        
        output.append(f"{medal} {address}")
        output.append(f"   收益: {pnl} | 收益率: {rio}")
        
        if 'winrate' in item:
            output.append(f"   胜率: {item.get('winrate', 'N/A')}")
        if 'drawdown' in item:
            output.append(f"   最大回撤: {item.get('drawdown', 'N/A')}")
        
        output.append("")
    
    return "\n".join(output)


# ========== 测试 ==========

if __name__ == '__main__':
    import sys
    
    print("🚀 HyperTrend API 客户端测试")
    print("=" * 50)
    
    # 检查配置
    token = os.getenv('HYPERTREND_API_TOKEN')
    if not token:
        print("\n⚠️  未配置 API Token")
        print("请先设置环境变量:")
        print("  export HYPERTREND_API_TOKEN='your_token'")
        sys.exit(1)
    
    print(f"\n✅ API Token 已配置")
    print(f"🌐 API 地址: https://app.hypertrend.top/api")
    
    # 测试获取榜单
    print("\n📊 测试获取稳健大师榜单...")
    api = HyperTrendAPI()
    result = api.get_master(page=1, page_size=5, type_="week")
    
    if 'error' in result:
        print(f"❌ 错误: {result['error']}")
    else:
        data = result.get('data', [])
        print(f"✅ 获取成功! 共 {len(data)} 条数据")
        print("\n" + format_leaderboard(data, "master"))
