#!/usr/bin/env python3
"""
AI Discovery Quick Push Script Template

Copy this file, modify the commit message, and run to push changes.
Usage: 
1. Copy this template
2. Edit COMMIT_MESSAGE below
3. Run the script
"""

import os
import sys
import subprocess
import datetime
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
os.chdir(PROJECT_ROOT)

def run_command(command, description=""):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return False
        if result.stdout.strip():
            print(f"✅ {result.stdout}")
        return True
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    """Main push workflow"""
    
    # ============================================
    # 🎯 在这里修改你的提交信息！
    # ============================================
    COMMIT_MESSAGE = """feat: Your feature title here

✨ What you added:
• Feature 1 description
• Feature 2 description
• Feature 3 description

🔧 What you improved:
• Improvement 1
• Improvement 2

🐛 What you fixed:
• Fix 1
• Fix 2

📊 Impact:
• Business impact description
• Technical impact description

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
    # ============================================
    
    print("🌟 AI Discovery Quick Push Script")
    print("=" * 50)
    
    # 检查Git状态
    if not run_command("git status --porcelain", "Checking Git status"):
        return
    
    # 显示当前更改
    print("\n📋 Current Changes:")
    run_command("git status", "Displaying current status")
    
    # 确认是否继续
    print(f"\n📝 Commit Message Preview:")
    print("-" * 40)
    print(COMMIT_MESSAGE)
    print("-" * 40)
    
    confirm = input("\n❓ Continue with push? (y/N): ").lower().strip()
    if confirm not in ['y', 'yes']:
        print("❌ Push cancelled.")
        return
    
    # 添加所有文件
    if not run_command("git add .", "Adding all changes"):
        return
    
    # 创建提交
    commit_cmd = f'''git commit -m "$(cat <<'EOF'
{COMMIT_MESSAGE}
EOF
)"'''
    
    if not run_command(commit_cmd, "Creating commit"):
        return
    
    # 推送到远程仓库
    if not run_command("git push origin main", "Pushing to GitHub"):
        return
    
    # 显示推送后状态
    print("\n🎉 Push completed successfully!")
    run_command("git log --oneline -3", "Recent commits")
    
    # 显示远程URL
    result = subprocess.run("git remote get-url origin", shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"\n🔗 Repository: {result.stdout.strip()}")
    
    print(f"\n⏰ Push completed at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()