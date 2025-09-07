#!/usr/bin/env python3
"""
Multi-Source System Comprehensive Test Suite
测试多源热门话题检测系统的完整功能
"""

import json
import sys
import os
import time
from datetime import datetime
from pathlib import Path

# 添加模块路径
sys.path.append('.')
sys.path.append('modules')

def test_api_configurations():
    """测试API配置状态"""
    print("🔧 Testing API Configurations...")
    
    configs = {
        'Reddit API': ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USER_AGENT'],
        'News API': ['NEWS_API_KEY'],
        'Product Hunt': ['PRODUCTHUNT_TOKEN'],
        'Telegram': ['TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID'],
        'Image APIs': ['UNSPLASH_ACCESS_KEY', 'PEXELS_API_KEY', 'PIXABAY_API_KEY']
    }
    
    results = {}
    for service, required_vars in configs.items():
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            results[service] = f"❌ Missing: {', '.join(missing)}"
        else:
            results[service] = "✅ Configured"
    
    print("API Configuration Status:")
    for service, status in results.items():
        print(f"  {service}: {status}")
    
    # 计算配置完成度
    total_services = len(configs)
    configured_services = sum(1 for status in results.values() if "✅" in status)
    completion_rate = (configured_services / total_services) * 100
    
    print(f"\n📊 Configuration Completion: {completion_rate:.1f}% ({configured_services}/{total_services})")
    return results

def test_multi_source_detector():
    """测试多源检测器"""
    print("\n🔍 Testing Multi-Source Detector...")
    
    try:
        from trending_detector.multi_source_detector import MultiSourceTrendDetector
        
        detector = MultiSourceTrendDetector()
        print("✅ Multi-source detector initialized successfully")
        
        # 测试各个数据源
        sources_to_test = [
            ('HackerNews', detector.detect_hackernews_trends, 5),
            ('RSS Feeds', detector.detect_rss_trends, 5),
        ]
        
        # 只测试不需要API的数据源
        results = {}
        for source_name, detection_func, limit in sources_to_test:
            try:
                print(f"  Testing {source_name}...")
                topics = detection_func(limit=limit)
                results[source_name] = {
                    'status': '✅ Working',
                    'topics_found': len(topics),
                    'sample_topics': [t.keyword for t in topics[:2]]
                }
                print(f"    Found {len(topics)} topics")
            except Exception as e:
                results[source_name] = {
                    'status': f'❌ Error: {str(e)[:50]}...',
                    'topics_found': 0,
                    'sample_topics': []
                }
        
        # 测试Reddit和News如果有配置
        if os.getenv('REDDIT_CLIENT_ID'):
            try:
                print("  Testing Reddit API...")
                reddit_topics = detector.detect_reddit_trends(limit=3)
                results['Reddit'] = {
                    'status': '✅ Working',
                    'topics_found': len(reddit_topics),
                    'sample_topics': [t.keyword for t in reddit_topics[:2]]
                }
            except Exception as e:
                results['Reddit'] = {
                    'status': f'❌ Error: {str(e)[:50]}...',
                    'topics_found': 0,
                    'sample_topics': []
                }
        
        if os.getenv('NEWS_API_KEY'):
            try:
                print("  Testing News API...")
                news_topics = detector.detect_news_trends(limit=3)
                results['News API'] = {
                    'status': '✅ Working',
                    'topics_found': len(news_topics),
                    'sample_topics': [t.keyword for t in news_topics[:2]]
                }
            except Exception as e:
                results['News API'] = {
                    'status': f'❌ Error: {str(e)[:50]}...',
                    'topics_found': 0,
                    'sample_topics': []
                }
        
        print("Multi-Source Detection Results:")
        for source, result in results.items():
            print(f"  {source}: {result['status']}")
            if result['topics_found'] > 0:
                print(f"    Sample topics: {', '.join(result['sample_topics'])}")
        
        return results
        
    except ImportError as e:
        print(f"❌ Failed to import multi-source detector: {e}")
        return {'error': 'Import failed'}
    except Exception as e:
        print(f"❌ Unexpected error in multi-source detector: {e}")
        return {'error': f'Unexpected error: {e}'}

def test_keyword_generation():
    """测试关键词生成"""
    print("\n📊 Testing Keyword Generation...")
    
    try:
        # 运行关键词生成脚本
        import subprocess
        result = subprocess.run([sys.executable, 'scripts/multi_source_keywords.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Multi-source keyword generation successful")
            
            # 检查生成的文件
            if os.path.exists('daily_keywords.json'):
                with open('daily_keywords.json', 'r', encoding='utf-8') as f:
                    keywords_data = json.load(f)
                
                print(f"  Generated {len(keywords_data)} keywords")
                
                # 显示示例关键词
                if keywords_data:
                    sample_keyword = keywords_data[0]
                    print(f"  Sample keyword: {sample_keyword.get('keyword', 'N/A')}")
                    print(f"  Trend score: {sample_keyword.get('trend_score', 0)}")
                    print(f"  Controversy score: {sample_keyword.get('controversy_score', 0)}")
                
                return {'status': 'success', 'keywords_count': len(keywords_data)}
            else:
                print("⚠️ Keywords file not generated")
                return {'status': 'warning', 'message': 'No keywords file'}
        else:
            print("❌ Keyword generation failed")
            print(f"Error: {result.stderr}")
            return {'status': 'failed', 'error': result.stderr}
            
    except subprocess.TimeoutExpired:
        print("⏰ Keyword generation timed out")
        return {'status': 'timeout'}
    except Exception as e:
        print(f"❌ Error in keyword generation: {e}")
        return {'status': 'error', 'message': str(e)}

def test_notification_system():
    """测试通知系统"""
    print("\n📢 Testing Notification System...")
    
    if not os.getenv('TELEGRAM_BOT_TOKEN') or not os.getenv('TELEGRAM_CHAT_ID'):
        print("⚠️ Telegram credentials not configured, skipping notification test")
        return {'status': 'skipped', 'reason': 'No Telegram credentials'}
    
    try:
        from telegram_notify import send_telegram_message, format_test_message
        
        # 发送测试消息
        test_message = format_test_message()
        success = send_telegram_message(test_message)
        
        if success:
            print("✅ Test notification sent successfully")
            return {'status': 'success'}
        else:
            print("❌ Failed to send test notification")
            return {'status': 'failed'}
            
    except Exception as e:
        print(f"❌ Error in notification system: {e}")
        return {'status': 'error', 'message': str(e)}

def test_enhanced_notification():
    """测试增强通知功能"""
    print("\n🧠 Testing Enhanced Multi-Source Notification...")
    
    if not os.path.exists('notification_data.json'):
        print("⚠️ No notification data available, creating test data...")
        
        # 创建测试数据
        test_data = {
            "keyword_data": {
                "keyword": "Claude AI",
                "trend_score": 92,
                "controversy_score": 40,
                "monthly_revenue_estimate": "$318-880",
                "difficulty": "High",
                "commercial_intent": 0.88,
                "reason": "This keyword shows high competition with growing search trends. **TRENDING CONTROVERSY DETECTED** - Recent surge in problem-related queries, making this highly valuable for capturing user attention.",
                "data_sources": ["reddit_artificial", "news_api", "rss_techcrunch"],
                "related_queries": ["claude ai problems", "claude ai worse", "claude downgrade"],
                "sentiment": "negative",
                "is_trending_topic": True
            },
            "content_data": {
                "total_topics": 15,
                "total_keywords": 8,
                "controversy_detected": True,
                "sources_used": ["reddit_artificial", "news_api", "hackernews", "rss_techcrunch"],
                "avg_controversy_score": 25.5,
                "high_value_keywords": 3
            }
        }
        
        with open('notification_data.json', 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'scripts/send_notification.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Enhanced notification sent successfully")
            print("📱 Check your Telegram for the multi-source intelligence report")
            return {'status': 'success'}
        else:
            print("❌ Enhanced notification failed")
            print(f"Error: {result.stderr}")
            return {'status': 'failed', 'error': result.stderr}
            
    except subprocess.TimeoutExpired:
        print("⏰ Notification timed out")
        return {'status': 'timeout'}
    except Exception as e:
        print(f"❌ Error in enhanced notification: {e}")
        return {'status': 'error', 'message': str(e)}

def generate_test_report(api_results, detector_results, keyword_results, notification_results, enhanced_notification_results):
    """生成测试报告"""
    print("\n" + "="*60)
    print("📋 AI DISCOVERY MULTI-SOURCE SYSTEM TEST REPORT")
    print("="*60)
    
    # API配置状态
    configured_apis = sum(1 for status in api_results.values() if "✅" in status)
    total_apis = len(api_results)
    
    print(f"\n🔧 API Configuration: {configured_apis}/{total_apis} configured")
    for service, status in api_results.items():
        priority = "🟢 Required" if service in ['Reddit API', 'News API'] else "🟡 Optional"
        print(f"  {service}: {status} ({priority})")
    
    # 数据源检测状态
    working_sources = sum(1 for result in detector_results.values() 
                         if isinstance(result, dict) and "✅" in result.get('status', ''))
    total_sources = len([r for r in detector_results.values() if isinstance(r, dict)])
    
    print(f"\n🔍 Data Source Detection: {working_sources}/{total_sources} working")
    for source, result in detector_results.items():
        if isinstance(result, dict):
            print(f"  {source}: {result['status']}")
    
    # 系统功能状态
    print(f"\n📊 System Functions:")
    print(f"  Keyword Generation: {keyword_results.get('status', 'unknown').title()}")
    print(f"  Basic Notification: {notification_results.get('status', 'unknown').title()}")
    print(f"  Enhanced Notification: {enhanced_notification_results.get('status', 'unknown').title()}")
    
    # 整体评估
    critical_components = [
        configured_apis >= 2,  # 至少2个API配置
        working_sources >= 2,   # 至少2个数据源工作
        keyword_results.get('status') == 'success',
        enhanced_notification_results.get('status') in ['success', 'skipped']
    ]
    
    system_health = sum(critical_components) / len(critical_components) * 100
    
    print(f"\n🎯 Overall System Health: {system_health:.1f}%")
    
    if system_health >= 80:
        status_emoji = "🟢"
        status_text = "EXCELLENT - System fully operational"
    elif system_health >= 60:
        status_emoji = "🟡"
        status_text = "GOOD - Minor issues detected"
    else:
        status_emoji = "🔴"
        status_text = "NEEDS ATTENTION - Critical issues found"
    
    print(f"{status_emoji} Status: {status_text}")
    
    # 下一步建议
    print(f"\n🚀 Next Steps:")
    if configured_apis < total_apis:
        print("  1. Configure missing APIs (see API_SETUP.md)")
    if working_sources < 4:
        print("  2. Verify API credentials and internet connection")
    if keyword_results.get('status') != 'success':
        print("  3. Debug keyword generation system")
    if notification_results.get('status') != 'success':
        print("  4. Test Telegram notification setup")
    
    print(f"\n📖 Documentation: API_SETUP.md")
    print(f"🌐 Live Site: https://ai-discovery-nu.vercel.app/")
    print("="*60)

def main():
    """主测试函数"""
    print("🚀 Starting AI Discovery Multi-Source System Test Suite...")
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 执行各项测试
    api_results = test_api_configurations()
    detector_results = test_multi_source_detector()
    keyword_results = test_keyword_generation()
    notification_results = test_notification_system()
    enhanced_notification_results = test_enhanced_notification()
    
    # 生成报告
    generate_test_report(api_results, detector_results, keyword_results, 
                        notification_results, enhanced_notification_results)
    
    # 清理测试文件
    cleanup_files = ['daily_keywords.json', 'notification_data.json', 'multi_source_trends.json']
    for file in cleanup_files:
        if os.path.exists(file):
            os.remove(file)
    
    print(f"\n🧹 Cleanup completed")
    print(f"✅ Test suite finished successfully")

if __name__ == "__main__":
    main()