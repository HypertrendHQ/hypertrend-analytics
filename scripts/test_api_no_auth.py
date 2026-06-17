#!/usr/bin/env python3
"""
HyperTrend API 无认证测试脚本
测试公开接口（无需 Token）
"""

import requests
import json

BASE_URL = "http://192.144.239.66/api"

def test_open_billings():
    """测试单量统计（公开接口）"""
    print("📊 测试 /open/billings (单量统计)...")
    try:
        response = requests.post(
            f"{BASE_URL}/open/billings",
            json={"page": 1, "page_size": 5, "type": "week"},
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功!")
            print(f"数据条数: {len(data.get('data', []))}")
            if data.get('data'):
                print(f"\n🥇 第一名:")
                first = data['data'][0]
                for k, v in first.items():
                    print(f"   {k}: {v}")
            return True
        else:
            print(f"❌ 错误: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

def test_open_vlm():
    """测试交易量统计（公开接口）"""
    print("\n📊 测试 /open/vlm (交易量统计)...")
    try:
        response = requests.post(
            f"{BASE_URL}/open/vlm",
            json={"page": 1, "page_size": 5, "type": "week"},
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功!")
            return True
        else:
            print(f"❌ 错误: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

def test_apps_without_auth():
    """测试榜单接口（可能需要认证）"""
    print("\n📊 测试 /apps/master (稳健大师)...")
    try:
        response = requests.post(
            f"{BASE_URL}/apps/master",
            json={"page": 1, "page_size": 3, "type": "week"},
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功! 无需认证")
            return True
        elif response.status_code == 401:
            print(f"⚠️  需要认证 (401)")
            return False
        else:
            print(f"⚠️  状态码: {response.status_code}")
            print(f"响应: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

def test_open_quotes():
    """测试名人名言（公开接口）"""
    print("\n📊 测试 /open/quotes (名人名言)...")
    try:
        response = requests.get(
            f"{BASE_URL}/open/quotes",
            timeout=15
        )
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功!")
            if isinstance(data, dict) and 'content' in data:
                print(f"名言: {data['content']}")
                print(f"作者: {data.get('name', 'Unknown')}")
            return True
        else:
            print(f"⚠️  状态码: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 连接错误: {e}")
        return False

if __name__ == '__main__':
    print("🚀 HyperTrend API 无认证测试")
    print("=" * 50)
    print(f"API 地址: {BASE_URL}")
    print("=" * 50)
    
    results = []
    
    # 测试公开接口
    results.append(("open/billings", test_open_billings()))
    results.append(("open/vlm", test_open_vlm()))
    results.append(("open/quotes", test_open_quotes()))
    
    # 测试可能需要认证的接口
    results.append(("apps/master", test_apps_without_auth()))
    
    print("\n" + "=" * 50)
    print("📋 测试结果汇总:")
    print("=" * 50)
    for endpoint, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{endpoint:20s} {status}")
    
    print("\n💡 说明:")
    print("   - ✅ 通过: 接口可以无认证访问")
    print("   - ❌ 失败: 接口需要认证或有网络问题")
    print("   - 公开接口(open/*)通常可以无认证访问")
    print("   - 用户接口(apps/*)可能需要 Token")
