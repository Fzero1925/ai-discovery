#!/usr/bin/env python3
"""
Domain Registration Reminder System

Provides automated reminders and checklists for tasks that need to be completed
after domain registration for the AI Discovery project.
"""

import os
import sys
import json
import datetime
from typing import List, Dict
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from modules.monitoring.telegram_bot import send_telegram_notification
except ImportError:
    print("⚠️ Telegram notification module not found. Running in standalone mode.")
    send_telegram_notification = None


class DomainRegistrationReminder:
    """
    Handles domain registration reminders and post-registration tasks
    """
    
    def __init__(self):
        self.reminder_tasks = self._load_reminder_tasks()
        self.current_domain = "https://ai-discovery-nu.vercel.app"
        self.project_name = "AI Discovery"
        
    def _load_reminder_tasks(self) -> Dict[str, List[Dict]]:
        """Load the comprehensive list of tasks to complete after domain registration"""
        
        return {
            "🔴 Critical Tasks (Complete within 24 hours)": [
                {
                    "task": "Update Pexels API Configuration",
                    "description": "Pexels API keys are domain-restricted. Must regenerate API key with new domain.",
                    "current_key": "GEIG80uBUWAZYPkdLvhqSxLatgJ5Gyiu7DWxTy3veJTMGMVVkMuSWdrg",
                    "action": "Go to https://www.pexels.com/api/ → Account → Generate new key with new domain",
                    "update_locations": [
                        "GitHub Secrets: PEXELS_API_KEY",
                        "Local environment variables",
                        "Vercel environment variables"
                    ],
                    "priority": "CRITICAL"
                },
                {
                    "task": "Update DNS Configuration", 
                    "description": "Point new domain to Vercel deployment",
                    "action": "Configure DNS A records and CNAME to point to Vercel",
                    "vercel_settings": "Add domain in Vercel project settings",
                    "priority": "CRITICAL"
                },
                {
                    "task": "Update SSL Certificate",
                    "description": "Ensure HTTPS is working properly with new domain",
                    "action": "Vercel should auto-generate SSL, verify https:// works",
                    "priority": "CRITICAL"
                }
            ],
            
            "🟡 High Priority (Complete within 48 hours)": [
                {
                    "task": "Update Google Analytics Configuration",
                    "description": "Update GA4 property with new domain for accurate tracking",
                    "current_id": "G-BLX4B9G7PE",
                    "action": "Google Analytics → Admin → Property Settings → Add new domain",
                    "priority": "HIGH"
                },
                {
                    "task": "Update Google AdSense Application",
                    "description": "AdSense applications must use final production domain",
                    "action": "If AdSense not yet applied, wait for domain setup. If applied, update site URL.",
                    "priority": "HIGH"
                },
                {
                    "task": "Update Hugo Configuration",
                    "description": "Update baseURL in config.toml to reflect new domain",
                    "file": "config.toml",
                    "current_value": "https://ai-discovery-nu.vercel.app",
                    "action": "Update baseURL parameter",
                    "priority": "HIGH"
                },
                {
                    "task": "Update Sitemap and Robots.txt",
                    "description": "Search engines need updated sitemap with new domain",
                    "action": "Regenerate sitemap, submit to Google Search Console",
                    "priority": "HIGH"
                }
            ],
            
            "🟢 Standard Tasks (Complete within 1 week)": [
                {
                    "task": "Update Social Media Links",
                    "description": "Update all social media profiles with new website URL",
                    "locations": [
                        "config.toml social links",
                        "Footer website URLs",
                        "About page contact information"
                    ],
                    "priority": "STANDARD"
                },
                {
                    "task": "Update API Documentation",
                    "description": "Update any API documentation that references the old domain",
                    "action": "Search codebase for hardcoded domain references",
                    "priority": "STANDARD"
                },
                {
                    "task": "Setup Email Configuration", 
                    "description": "Configure professional email addresses with new domain",
                    "suggestions": [
                        "contact@yournewdomain.com",
                        "admin@yournewdomain.com",
                        "noreply@yournewdomain.com"
                    ],
                    "priority": "STANDARD"
                }
            ],
            
            "🔵 Optional Enhancements": [
                {
                    "task": "Setup CDN Optimization",
                    "description": "Optimize global content delivery with new domain",
                    "action": "Verify Vercel CDN is optimized for your target markets",
                    "priority": "OPTIONAL"
                },
                {
                    "task": "Domain Monitoring Setup",
                    "description": "Setup monitoring for new domain uptime and performance",
                    "tools": "Consider UptimeRobot, Pingdom, or similar services",
                    "priority": "OPTIONAL"
                }
            ]
        }
    
    def generate_reminder_checklist(self, new_domain: str = None) -> str:
        """Generate a comprehensive checklist for domain migration"""
        
        if new_domain:
            domain_text = f"your new domain: {new_domain}"
        else:
            domain_text = "your new domain"
        
        checklist = f"""
# 🌐 Domain Registration Complete! 
# Post-Registration Checklist for AI Discovery

**Current Domain:** {self.current_domain}
**New Domain:** {domain_text if new_domain else '[YOUR_NEW_DOMAIN]'}
**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        for category, tasks in self.reminder_tasks.items():
            checklist += f"## {category}\n\n"
            
            for i, task in enumerate(tasks, 1):
                checklist += f"### {i}. {task['task']}\n"
                checklist += f"**Description:** {task['description']}\n"
                
                if 'action' in task:
                    checklist += f"**Action:** {task['action']}\n"
                
                if 'current_key' in task:
                    checklist += f"**Current Key:** `{task['current_key']}`\n"
                
                if 'update_locations' in task:
                    checklist += "**Update Locations:**\n"
                    for location in task['update_locations']:
                        checklist += f"- {location}\n"
                
                if 'file' in task:
                    checklist += f"**File to Update:** `{task['file']}`\n"
                
                if 'current_value' in task:
                    checklist += f"**Current Value:** `{task['current_value']}`\n"
                
                checklist += f"**Priority:** {task['priority']}\n"
                checklist += "- [ ] Task Completed\n\n"
            
            checklist += "---\n\n"
        
        # Add important notes
        checklist += """
## 📋 Important Notes

### API Key Priority Order:
1. **Pexels API** - MUST be regenerated (domain-restricted)
2. **Pixabay API** - May need update (check their policy)  
3. **Unsplash API** - Usually domain-agnostic (verify in settings)

### Testing Checklist:
- [ ] New domain loads correctly
- [ ] HTTPS certificate is active
- [ ] All images load properly
- [ ] Google Analytics tracking works
- [ ] All internal links function
- [ ] Mobile responsiveness maintained
- [ ] Page load speed is optimal

### Rollback Plan:
If issues occur, keep Vercel subdomain active until all tests pass.

---

## 🚀 Business Impact

**Estimated Revenue Impact of Proper Domain Setup:**
- Professional domain increases user trust by 40-60%
- Proper SSL/HTTPS required for AdSense approval
- Custom domain essential for premium affiliate programs
- SEO benefits: Higher click-through rates with professional URL

**Target Timeline:** Complete critical tasks within 24-48 hours to minimize SEO impact.

---

Generated by AI Discovery Domain Registration Reminder System
Contact: AI Discovery Development Team
"""
        
        return checklist
    
    def save_checklist_to_file(self, new_domain: str = None, filename: str = None) -> str:
        """Save the checklist to a markdown file"""
        
        if not filename:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"domain_migration_checklist_{timestamp}.md"
        
        filepath = project_root / filename
        
        checklist_content = self.generate_reminder_checklist(new_domain)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(checklist_content)
        
        return str(filepath)
    
    def send_telegram_reminder(self, new_domain: str = None) -> bool:
        """Send domain registration reminder via Telegram"""
        
        if not send_telegram_notification:
            print("⚠️ Telegram notifications not available")
            return False
        
        message = f"""
🌐 **DOMAIN REGISTRATION REMINDER**

**Project:** AI Discovery
**Status:** Domain registration detected
**New Domain:** {new_domain or '[UPDATE_REQUIRED]'}

🔴 **CRITICAL TASKS (24hrs):**
• Regenerate Pexels API key with new domain
• Update DNS configuration  
• Verify SSL certificate

🟡 **HIGH PRIORITY (48hrs):**
• Update Google Analytics domain
• Update Hugo config.toml baseURL
• Submit new sitemap to search engines

📋 **Full checklist generated**
Run: `python scripts/domain_registration_reminder.py --checklist`

⚠️ **Remember:** Pexels API MUST be regenerated for new domain!
"""
        
        try:
            success = send_telegram_notification(
                message, 
                notification_type="domain_reminder"
            )
            return success
        except Exception as e:
            print(f"❌ Failed to send Telegram reminder: {e}")
            return False
    
    def check_current_domain_status(self) -> Dict:
        """Check the current domain configuration status"""
        
        status = {
            "current_domain": self.current_domain,
            "config_file_domain": None,
            "vercel_domain": "ai-discovery-nu.vercel.app",
            "needs_update": False,
            "api_keys_status": {
                "unsplash": bool(os.getenv('UNSPLASH_ACCESS_KEY')),
                "pexels": bool(os.getenv('PEXELS_API_KEY')),
                "pixabay": bool(os.getenv('PIXABAY_API_KEY'))
            }
        }
        
        # Check config.toml for current baseURL
        config_file = project_root / "config.toml"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Simple regex to find baseURL
                    import re
                    match = re.search(r'baseURL\s*=\s*"([^"]+)"', content)
                    if match:
                        status["config_file_domain"] = match.group(1)
            except Exception as e:
                print(f"⚠️ Could not read config.toml: {e}")
        
        return status


def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Domain Registration Reminder System")
    parser.add_argument('--checklist', action='store_true', help='Generate migration checklist')
    parser.add_argument('--domain', type=str, help='New domain name')
    parser.add_argument('--telegram', action='store_true', help='Send Telegram notification')
    parser.add_argument('--status', action='store_true', help='Check current domain status')
    
    args = parser.parse_args()
    
    reminder = DomainRegistrationReminder()
    
    if args.status:
        print("🔍 Checking current domain configuration...")
        status = reminder.check_current_domain_status()
        print(json.dumps(status, indent=2))
        return
    
    if args.checklist:
        print("📋 Generating domain migration checklist...")
        filepath = reminder.save_checklist_to_file(args.domain)
        print(f"✅ Checklist saved to: {filepath}")
        
        # Also display the checklist
        checklist = reminder.generate_reminder_checklist(args.domain)
        print("\n" + "="*60)
        print(checklist)
    
    if args.telegram:
        print("📱 Sending Telegram reminder...")
        success = reminder.send_telegram_reminder(args.domain)
        if success:
            print("✅ Telegram reminder sent successfully")
        else:
            print("❌ Failed to send Telegram reminder")
    
    if not any(vars(args).values()):
        # No arguments provided, show help and current status
        print("🌐 AI Discovery Domain Registration Reminder")
        print("=" * 50)
        
        status = reminder.check_current_domain_status()
        print(f"Current domain: {status['current_domain']}")
        print(f"Config domain: {status['config_file_domain']}")
        
        print("\nUsage examples:")
        print("  python domain_registration_reminder.py --checklist")
        print("  python domain_registration_reminder.py --domain 'ai-discovery.com' --checklist")
        print("  python domain_registration_reminder.py --telegram --domain 'ai-discovery.com'")
        print("  python domain_registration_reminder.py --status")
        
        print("\n⚠️  REMINDER: When you register your domain, run:")
        print("     python domain_registration_reminder.py --checklist --telegram --domain 'YOUR_NEW_DOMAIN'")


if __name__ == "__main__":
    main()