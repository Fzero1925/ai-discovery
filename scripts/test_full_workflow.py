#!/usr/bin/env python3
"""
Test Full AI Discovery Workflow
测试完整的AI Discovery工作流程
"""

import json
import os
import sys
import subprocess
from pathlib import Path

def run_workflow_test():
    """运行完整工作流测试"""
    print("=== Testing Full AI Discovery Workflow ===\n")
    
    try:
        # 步骤1: 生成关键词数据
        print("Step 1: Generating keywords...")
        result = subprocess.run([sys.executable, 'scripts/test_system.py'], 
                              capture_output=True, text=True, cwd='.')
        if result.returncode != 0:
            print(f"Keywords generation failed: {result.stderr}")
            return False
        print("✅ Keywords generated successfully")
        
        # 步骤2: 检查生成的文件
        print("\nStep 2: Checking generated files...")
        
        # 检查 daily_keywords.json
        if os.path.exists('daily_keywords.json'):
            with open('daily_keywords.json', 'r', encoding='utf-8') as f:
                keywords = json.load(f)
            print(f"✅ Keywords file: {len(keywords)} keywords loaded")
            
            # 显示第一个关键词（应该是争议话题）
            if keywords:
                first_kw = keywords[0]
                print(f"   Primary keyword: {first_kw['keyword']}")
                print(f"   Controversy score: {first_kw.get('controversy_score', 0)}")
                print(f"   Commercial value: {first_kw.get('monthly_revenue_estimate', 'N/A')}")
        else:
            print("❌ Keywords file not found")
            return False
        
        # 检查 notification_data.json
        if os.path.exists('notification_data.json'):
            with open('notification_data.json', 'r', encoding='utf-8') as f:
                notification = json.load(f)
            print(f"✅ Notification data prepared")
        else:
            print("❌ Notification data not found")
            return False
        
        # 步骤3: 测试通知格式
        print("\nStep 3: Testing notification format...")
        
        # 提取数据
        keyword_data = json.dumps(notification.get('keyword_data', {}), ensure_ascii=False)
        content_data = json.dumps(notification.get('content_data', {}), ensure_ascii=False)
        
        # 测试通知脚本
        cmd = [
            sys.executable, 'scripts/telegram_notify.py',
            '--type', 'keyword_analysis',
            '--keyword-data', keyword_data,
            '--content-data', content_data
        ]
        
        print("Testing notification script (without sending)...")
        print("Command:", ' '.join(cmd[:5]), '...')
        
        # 创建测试版本（不实际发送）
        test_notification_script = """
import sys
import json

# 模拟环境变量
import os
os.environ['TELEGRAM_BOT_TOKEN'] = 'test_token'
os.environ['TELEGRAM_CHAT_ID'] = 'test_chat'

# 修改telegram_notify脚本以测试模式运行
sys.path.append('scripts')

try:
    from telegram_notify import format_keyword_analysis_message
    
    # 解析参数
    keyword_data = json.loads(sys.argv[1])
    content_data = json.loads(sys.argv[2])
    
    # 生成消息
    message = format_keyword_analysis_message(keyword_data, content_data)
    
    print("=== Generated Notification Message ===")
    print(message)
    print("=== End Message ===")
    
    # 检查关键要素
    required_elements = [
        'Claude AI',  # 关键词
        'TRENDING CONTROVERSY DETECTED',  # 争议检测
        'Commercial Intent',  # 商业价值
        'Revenue Potential',  # 收益预测
        'KEYWORD SELECTION RATIONALE'  # 选择理由
    ]
    
    missing_elements = []
    for element in required_elements:
        if element not in message:
            missing_elements.append(element)
    
    if missing_elements:
        print(f"❌ Missing elements: {missing_elements}")
        sys.exit(1)
    else:
        print("✅ All required elements present in notification")
        
except Exception as e:
    print(f"❌ Notification test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
"""
        
        # 写入测试脚本
        with open('temp_test_notification.py', 'w', encoding='utf-8') as f:
            f.write(test_notification_script)
        
        # 运行测试
        test_result = subprocess.run([
            sys.executable, 'temp_test_notification.py',
            keyword_data, content_data
        ], capture_output=True, text=True, cwd='.')
        
        if test_result.returncode == 0:
            print("✅ Notification format test passed")
            print("Sample notification preview:")
            print("-" * 50)
            print(test_result.stdout.split("=== Generated Notification Message ===")[1].split("=== End Message ===")[0])
            print("-" * 50)
        else:
            print(f"❌ Notification format test failed: {test_result.stderr}")
            print(f"STDOUT: {test_result.stdout}")
            return False
        
        # 清理临时文件
        if os.path.exists('temp_test_notification.py'):
            os.remove('temp_test_notification.py')
        
        print("\n=== Workflow Test Summary ===")
        print("✅ Keywords generation: SUCCESS")
        print("✅ Data preparation: SUCCESS") 
        print("✅ Notification format: SUCCESS")
        print("✅ All components working correctly")
        
        # 说明为什么GitHub Actions中可能失败
        print("\n=== Troubleshooting Notes ===")
        print("If GitHub Actions fails, possible reasons:")
        print("1. Missing Python dependencies in CI environment")
        print("2. Script path issues in GitHub Actions")
        print("3. Environment variable configuration")
        print("4. Unicode encoding issues in CI")
        
        print("\nTo fix, check:")
        print("• requirements.txt has all dependencies")
        print("• Script paths are correct in workflow")
        print("• Secrets are properly configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_workflow_test()
    sys.exit(0 if success else 1)