#!/usr/bin/env python3
"""
Simple Test for Notification System
"""

import json
import sys
import os

# 添加脚本目录到Python路径
sys.path.append('.')
sys.path.append('scripts')

def test_notification():
    """测试通知系统"""
    print("Testing notification system...")
    
    try:
        # 读取已存在的数据
        with open('notification_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        keyword_data = data.get('keyword_data', {})
        content_data = data.get('content_data', {})
        
        print(f"Primary keyword: {keyword_data.get('keyword', 'N/A')}")
        print(f"Controversy score: {keyword_data.get('controversy_score', 0)}")
        print(f"Commercial value: {keyword_data.get('monthly_revenue_estimate', 'N/A')}")
        
        # 导入通知函数
        from telegram_notify import format_keyword_analysis_message
        
        # 生成消息
        message = format_keyword_analysis_message(keyword_data, content_data)
        
        print("\n" + "="*60)
        print("GENERATED NOTIFICATION MESSAGE:")
        print("="*60)
        print(message[:1000] + "..." if len(message) > 1000 else message)
        print("="*60)
        
        # 检查关键元素
        checks = {
            'Claude AI': 'Claude AI' in message,
            'Controversy Detection': 'TRENDING CONTROVERSY DETECTED' in message,
            'Commercial Intent': 'Commercial Intent' in message,
            'Revenue Potential': 'Revenue Potential' in message,
            'Keyword Selection': 'KEYWORD SELECTION RATIONALE' in message
        }
        
        print("\nCHECK RESULTS:")
        for check, passed in checks.items():
            status = "PASS" if passed else "FAIL"
            print(f"  {check}: {status}")
        
        all_passed = all(checks.values())
        print(f"\nOVERALL: {'SUCCESS' if all_passed else 'FAILED'}")
        
        return all_passed
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_notification()
    print(f"\nResult: {'SUCCESS' if success else 'FAILURE'}")
    sys.exit(0 if success else 1)