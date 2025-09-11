#!/usr/bin/env python3
"""
Send Telegram notification using existing data
"""

import json
import sys
import os

sys.path.append('.')
sys.path.append('scripts')

def main():
    try:
        # Check if notification data exists
        if os.path.exists('notification_data.json'):
            with open('notification_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            keyword_data = data.get('keyword_data', {})
            content_data = data.get('content_data', {})
            
            print("Sending detailed keyword analysis notification...")
            
            # Import and call telegram notification
            from telegram_notify import send_telegram_message, format_keyword_analysis_message
            
            message = format_keyword_analysis_message(keyword_data, content_data)
            success = send_telegram_message(message)
            if success:
                print("Enhanced notification sent successfully")
            else:
                print("Enhanced notification failed (non blocking)")
                # 不阻塞工作流
                sys.exit(0)
                
        else:
            print("No notification data available, sending basic status")
            from telegram_notify import send_telegram_message
            
            message = """📢 *AI Discovery Status* 
            
✅ System operational
🤖 Content generation in progress
🎯 Hot topics monitoring active

*Live Site*: https://ai-discovery-nu.vercel.app/"""
            
            success = send_telegram_message(message)
            if not success:
                print("Basic notification failed (non blocking)")
                sys.exit(0)
                
    except Exception as e:
        print(f"Notification error (non blocking): {e}")
        sys.exit(0)

if __name__ == "__main__":
    main()
