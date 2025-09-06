#!/usr/bin/env python3
"""
Batch remove "Review" terms from AI Discovery content files
Replace with SEO-friendly alternatives
"""

import os
import re
import glob
from pathlib import Path

# SEO-friendly replacements for "Review"
REVIEW_REPLACEMENTS = {
    "Complete {} Review": "{} Complete Guide",
    "{} Review 2025": "{} Analysis: Complete 2025 Guide", 
    "{} Comprehensive Review": "{} Comprehensive Guide",
    "{} Ultimate Review": "{} Ultimate Guide",
    "{} Detailed Review": "{} Detailed Analysis",
    "{} Review": "{} Guide",
    "review": "guide",
    "Review": "Guide",
    "reviews": "guides", 
    "Reviews": "Guides"
}

def update_file_content(filepath):
    """Update a single file, removing Review terms"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        updated = False
        
        # Apply replacements
        for old_pattern, new_pattern in REVIEW_REPLACEMENTS.items():
            if '{}' in old_pattern:
                # Pattern with placeholder - use regex
                # Convert to regex pattern
                regex_pattern = old_pattern.replace('{}', r'([A-Z][a-zA-Z\s\-\.]+)')
                def replace_func(match):
                    tool_name = match.group(1)
                    return new_pattern.format(tool_name)
                
                new_content = re.sub(regex_pattern, replace_func, content)
                if new_content != content:
                    content = new_content
                    updated = True
            else:
                # Direct string replacement
                new_content = content.replace(old_pattern, new_pattern)
                if new_content != content:
                    content = new_content
                    updated = True
        
        # Write back if changed
        if updated:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated: {filepath}")
            return True
        else:
            print(f"No changes: {filepath}")
            return False
            
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    """Main execution"""
    print("Removing 'Review' terms from AI Discovery content...")
    print("=" * 60)
    
    # Files to update
    content_patterns = [
        "content/**/*.md",
        "layouts/**/*.html"
    ]
    
    updated_files = 0
    total_files = 0
    
    for pattern in content_patterns:
        files = glob.glob(pattern, recursive=True)
        for filepath in files:
            # Skip certain files
            if any(skip in filepath for skip in ['_index.md', '.git', 'node_modules']):
                continue
                
            total_files += 1
            if update_file_content(filepath):
                updated_files += 1
    
    print("=" * 60)
    print(f"Summary:")
    print(f"   Total files processed: {total_files}")
    print(f"   Files updated: {updated_files}")
    print(f"   Files unchanged: {total_files - updated_files}")
    print("\nReview term removal completed!")

if __name__ == "__main__":
    main()