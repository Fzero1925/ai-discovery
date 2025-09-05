#!/usr/bin/env python3
"""
Unsplash API测试脚本
验证API配置是否正常工作
"""

import os
import sys
import requests
import json
from pathlib import Path

def test_unsplash_api():
    """测试Unsplash API配置"""
    print("🔍 测试Unsplash API配置...")
    
    # 获取API密钥
    access_key = os.getenv('UNSPLASH_ACCESS_KEY')
    
    if not access_key:
        print("❌ 错误：未找到UNSPLASH_ACCESS_KEY环境变量")
        print("请先配置API密钥：")
        print("  Windows: set UNSPLASH_ACCESS_KEY=你的密钥")
        print("  或添加到.env文件中")
        return False
    
    # 测试API连接
    try:
        print(f"🔑 使用API密钥: {access_key[:10]}...")
        
        # 测试搜索API
        url = "https://api.unsplash.com/search/photos"
        headers = {
            'Authorization': f'Client-ID {access_key}',
            'Accept-Version': 'v1'
        }
        
        params = {
            'query': 'artificial intelligence',
            'per_page': 3,
            'orientation': 'landscape'
        }
        
        print("🌐 测试API连接...")
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            photos = data.get('results', [])
            
            print(f"✅ API连接成功!")
            print(f"📊 搜索结果: 找到 {len(photos)} 张图片")
            print(f"💫 当前限制: {response.headers.get('X-Ratelimit-Remaining', 'N/A')} 剩余请求")
            
            # 显示图片信息
            for i, photo in enumerate(photos[:2], 1):
                print(f"  📸 图片{i}: {photo['description'] or '无描述'}")
                print(f"       📏 尺寸: {photo['width']}x{photo['height']}")
                print(f"       👤 作者: {photo['user']['name']}")
                print(f"       🔗 链接: {photo['urls']['regular']}")
            
            return True
            
        elif response.status_code == 401:
            print("❌ 认证失败：API密钥无效")
            print("请检查UNSPLASH_ACCESS_KEY是否正确")
            return False
            
        elif response.status_code == 403:
            print("❌ 权限被拒：API请求超出限制")
            print("请等待一小时后再试，或检查API配额")
            return False
            
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络连接失败: {e}")
        return False
    
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def get_rate_limit_info():
    """获取API限制信息"""
    access_key = os.getenv('UNSPLASH_ACCESS_KEY')
    
    if not access_key:
        return
        
    try:
        url = "https://api.unsplash.com/me"
        headers = {
            'Authorization': f'Client-ID {access_key}',
            'Accept-Version': 'v1'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print(f"\n📈 API使用情况:")
            print(f"  ⏰ 本小时剩余: {response.headers.get('X-Ratelimit-Remaining', 'N/A')} 请求")
            print(f"  🔄 限制重置时间: {response.headers.get('X-Ratelimit-Reset-Time', 'N/A')}")
            
    except Exception as e:
        print(f"⚠️ 无法获取限制信息: {e}")

def main():
    """主函数"""
    print("🎨 Unsplash API 测试工具")
    print("=" * 50)
    
    # 测试API
    success = test_unsplash_api()
    
    if success:
        # 获取限制信息
        get_rate_limit_info()
        
        print("\n🎉 测试完成！API配置正常")
        print("现在可以运行真实图片获取系统了")
        print("下一步: python scripts/real_image_fetcher.py")
    else:
        print("\n❌ 测试失败，请检查配置")
        print("参考: scripts/setup_unsplash_api.md")

if __name__ == "__main__":
    main()