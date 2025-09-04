#!/usr/bin/env python3
"""
AI Discovery 主控制系统
整合所有自动化模块，实现一键运营管理
"""

import os
import sys
import json
import codecs
import argparse
import subprocess
from datetime import datetime
from typing import Dict, List

# 解决Windows编码问题
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

class MasterControl:
    """AI Discovery 主控制器"""
    
    def __init__(self):
        self.scripts_dir = "scripts"
        self.data_dir = "data"
        self.logs_dir = "logs"
        
        # 确保目录存在
        for dir_name in [self.data_dir, self.logs_dir]:
            os.makedirs(dir_name, exist_ok=True)
        
        # 系统模块
        self.modules = {
            'content_generation': 'generate_daily_ai_content.py',
            'trends_analysis': 'ai_trends_analyzer.py', 
            'seo_optimization': 'seo_optimizer.py',
            'revenue_tracking': 'revenue_tracker.py',
            'telegram_notify': 'notify_ai_discovery.py'
        }

    def log_operation(self, operation: str, status: str, details: str = ""):
        """记录操作日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'status': status,
            'details': details
        }
        
        log_file = f"{self.logs_dir}/master_control_{datetime.now().strftime('%Y%m%d')}.log"
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"⚠️ 日志记录失败: {e}")

    def run_module(self, module_name: str, args: List[str] = None) -> Dict:
        """运行指定模块"""
        if module_name not in self.modules:
            return {'success': False, 'error': f'未知模块: {module_name}'}
        
        script_path = f"{self.scripts_dir}/{self.modules[module_name]}"
        
        if not os.path.exists(script_path):
            return {'success': False, 'error': f'脚本不存在: {script_path}'}
        
        try:
            cmd = [sys.executable, script_path] + (args or [])
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            
            success = result.returncode == 0
            
            self.log_operation(
                operation=module_name,
                status='success' if success else 'error',
                details=result.stdout if success else result.stderr
            )
            
            return {
                'success': success,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except Exception as e:
            error_msg = f'模块执行异常: {e}'
            self.log_operation(operation=module_name, status='error', details=error_msg)
            return {'success': False, 'error': error_msg}

    def daily_automation(self) -> Dict:
        """每日自动化任务序列"""
        print("🚀 开始AI Discovery每日自动化任务...")
        
        results = {
            'start_time': datetime.now().isoformat(),
            'tasks': {},
            'overall_success': True
        }
        
        # 任务序列（按优先级排序）
        tasks = [
            ('trends_analysis', ['--limit', '6', '--save'], '市场趋势分析'),
            ('content_generation', ['--count', '1', '--focus-high-revenue'], 'AI工具内容生成'),
            ('seo_optimization', ['--sitemap', '--robots'], 'SEO优化'),
            ('revenue_tracking', ['--daily'], '收益跟踪分析')
        ]
        
        for module, args, description in tasks:
            print(f"📋 执行: {description}")
            
            try:
                result = self.run_module(module, args)
                results['tasks'][module] = {
                    'description': description,
                    'success': result['success'],
                    'details': result.get('stdout', '') or result.get('error', '')
                }
                
                if result['success']:
                    print(f"✅ {description} - 完成")
                else:
                    print(f"❌ {description} - 失败: {result.get('error', '未知错误')}")
                    results['overall_success'] = False
                    
            except Exception as e:
                error_msg = f"任务执行异常: {e}"
                print(f"❌ {description} - {error_msg}")
                results['tasks'][module] = {
                    'description': description,
                    'success': False,
                    'details': error_msg
                }
                results['overall_success'] = False
        
        # 发送Telegram通知
        print("📱 发送每日报告...")
        notify_result = self.run_module('telegram_notify', [
            '--type', 'ai_tools_daily',
            '--status', 'success' if results['overall_success'] else 'error',
            '--generated', 'true' if results['tasks'].get('content_generation', {}).get('success') else 'false'
        ])
        
        results['notification'] = notify_result
        results['end_time'] = datetime.now().isoformat()
        
        # 保存执行结果
        results_file = f"{self.data_dir}/daily_automation_{datetime.now().strftime('%Y%m%d')}.json"
        try:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ 结果保存失败: {e}")
        
        print(f"📊 自动化任务完成 - 总体状态: {'✅ 成功' if results['overall_success'] else '❌ 部分失败'}")
        return results

    def system_health_check(self) -> Dict:
        """系统健康检查"""
        print("🔍 执行系统健康检查...")
        
        health = {
            'timestamp': datetime.now().isoformat(),
            'modules_status': {},
            'data_integrity': {},
            'overall_health': 'healthy'
        }
        
        # 检查各模块脚本
        for module, script in self.modules.items():
            script_path = f"{self.scripts_dir}/{script}"
            if os.path.exists(script_path):
                try:
                    # 测试模块是否可执行
                    result = subprocess.run([sys.executable, script_path, '--help'], 
                                          capture_output=True, timeout=10)
                    health['modules_status'][module] = 'healthy' if result.returncode == 0 else 'error'
                except subprocess.TimeoutExpired:
                    health['modules_status'][module] = 'timeout'
                except Exception:
                    health['modules_status'][module] = 'error'
            else:
                health['modules_status'][module] = 'missing'
        
        # 检查数据文件
        critical_files = [
            'trending_ai_tools_cache.json',
            'revenue_tracking.json',
            'seo_audit_latest.json'
        ]
        
        for file in critical_files:
            file_path = f"{self.data_dir}/{file}"
            if os.path.exists(file_path):
                try:
                    stat = os.stat(file_path)
                    age_hours = (datetime.now().timestamp() - stat.st_mtime) / 3600
                    health['data_integrity'][file] = 'fresh' if age_hours < 48 else 'stale'
                except:
                    health['data_integrity'][file] = 'error'
            else:
                health['data_integrity'][file] = 'missing'
        
        # 评估整体健康度
        module_issues = sum(1 for status in health['modules_status'].values() if status != 'healthy')
        data_issues = sum(1 for status in health['data_integrity'].values() if status not in ['fresh', 'stale'])
        
        if module_issues > 2 or data_issues > 1:
            health['overall_health'] = 'critical'
        elif module_issues > 0 or data_issues > 0:
            health['overall_health'] = 'warning'
        
        # 显示检查结果
        print(f"\n📋 系统健康报告:")
        print(f"整体状态: {health['overall_health'].upper()}")
        
        print("\n🔧 模块状态:")
        for module, status in health['modules_status'].items():
            icon = {'healthy': '✅', 'error': '❌', 'timeout': '⏱️', 'missing': '❓'}.get(status, '❓')
            print(f"  {icon} {module}: {status}")
        
        print("\n📁 数据状态:")
        for file, status in health['data_integrity'].items():
            icon = {'fresh': '🟢', 'stale': '🟡', 'error': '❌', 'missing': '❓'}.get(status, '❓')
            print(f"  {icon} {file}: {status}")
        
        return health

    def revenue_dashboard(self) -> Dict:
        """收益仪表板"""
        print("💰 生成收益仪表板...")
        
        dashboard = {
            'generated_at': datetime.now().isoformat(),
            'revenue_summary': {},
            'performance_metrics': {},
            'recommendations': []
        }
        
        try:
            # 运行收益跟踪
            revenue_result = self.run_module('revenue_tracking', ['--report'])
            
            if revenue_result['success']:
                dashboard['revenue_summary']['status'] = 'success'
                dashboard['revenue_summary']['details'] = revenue_result['stdout']
            else:
                dashboard['revenue_summary']['status'] = 'error'
                dashboard['revenue_summary']['error'] = revenue_result.get('error', '未知错误')
            
            # 运行SEO分析
            seo_result = self.run_module('seo_optimization', ['--audit'])
            
            if seo_result['success']:
                dashboard['performance_metrics']['seo_status'] = 'success'
                # 从输出中提取关键指标（简化实现）
                output = seo_result['stdout']
                if '平均SEO评分' in output:
                    dashboard['performance_metrics']['seo_score'] = 'extracted_from_output'
            
            # 发送仪表板通知
            self.run_module('telegram_notify', [
                '--type', 'revenue_update'
            ])
            
        except Exception as e:
            dashboard['error'] = str(e)
        
        return dashboard

def main():
    parser = argparse.ArgumentParser(description='AI Discovery 主控制系统')
    parser.add_argument('--daily', action='store_true', help='执行每日自动化任务')
    parser.add_argument('--health', action='store_true', help='系统健康检查')
    parser.add_argument('--revenue', action='store_true', help='收益仪表板')
    parser.add_argument('--module', help='运行指定模块')
    parser.add_argument('--args', nargs='*', help='模块参数')
    
    args = parser.parse_args()
    
    controller = MasterControl()
    
    try:
        if args.daily:
            result = controller.daily_automation()
            return result['overall_success']
            
        elif args.health:
            health = controller.system_health_check()
            return health['overall_health'] != 'critical'
            
        elif args.revenue:
            dashboard = controller.revenue_dashboard()
            return 'error' not in dashboard
            
        elif args.module:
            result = controller.run_module(args.module, args.args)
            if result['success']:
                print(result['stdout'])
            else:
                print(f"❌ 错误: {result.get('error', '未知错误')}", file=sys.stderr)
            return result['success']
            
        else:
            print("AI Discovery 自动化变现系统 🚀")
            print("")
            print("可用操作:")
            print("  --daily    执行每日自动化任务")
            print("  --health   系统健康检查")
            print("  --revenue  收益仪表板")
            print("  --module   运行指定模块")
            print("")
            print("系统模块:")
            for module, script in controller.modules.items():
                status = "✅" if os.path.exists(f"scripts/{script}") else "❌"
                print(f"  {status} {module}: {script}")
            
            return True
            
    except Exception as e:
        print(f"❌ 主控制器错误: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)