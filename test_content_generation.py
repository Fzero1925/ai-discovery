#!/usr/bin/env python3
"""
Test content generation with real images
"""

import sys
import os
from datetime import datetime

# Add scripts to path
sys.path.append('scripts')

try:
    from generate_daily_ai_content import get_ai_tool_images, generate_ai_tool_review
    
    print("Testing content generation with real images...")
    
    # Test image fetching for different tools
    test_cases = [
        ("notion ai features", "productivity"),
        ("midjourney alternatives", "image_generation"), 
        ("claude ai review", "content_creation")
    ]
    
    for keyword, category in test_cases:
        print(f"\n=== Testing: {keyword} ({category}) ===")
        
        try:
            images = get_ai_tool_images(keyword, category)
            print(f"Image result: {images}")
            
            # Generate basic tool data
            tool_data = {
                "keyword": keyword,
                "category": category, 
                "trend_score": 0.90,
                "competition_score": 0.60,
                "commercial_intent": 0.88,
                "search_volume": 15000,
                "monthly_revenue_estimate": "$150-250"
            }
            
            print("Generating article content...")
            content = generate_ai_tool_review(keyword, category, tool_data)
            
            # Check if content contains real image paths (not placeholder)
            if "placeholder" not in str(images):
                print("SUCCESS: Using real image!")
            else:
                print("WARNING: Still using placeholder image")
                
        except Exception as e:
            print(f"ERROR: {e}")
    
    print("\nTest completed!")
    
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
except Exception as e:
    print(f"ERROR: {e}")