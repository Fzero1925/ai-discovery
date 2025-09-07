#!/usr/bin/env python3
"""
Simple SEO System Test
"""

import sys
sys.path.append('modules')

from seo_optimizer.advanced_seo_system import AdvancedSEOSystem

def main():
    print("Running Advanced SEO Structure Optimization Analysis...")
    
    seo_system = AdvancedSEOSystem("content")
    
    print("Generating SEO audit report...")
    audit_report = seo_system.create_seo_audit_report()
    
    print(f"\nContent Inventory Analysis:")
    inventory = audit_report["content_inventory"]
    print(f"  - Total pages: {inventory['total_pages']}")
    print(f"  - Content categories: {inventory['categories']}")
    print(f"  - Average word count: {inventory['average_word_count']:.0f}")
    print(f"  - Pages with internal links: {inventory['pages_with_internal_links']}")
    
    print(f"\nKeyword Analysis:")
    keyword_analysis = audit_report["keyword_analysis"]
    print(f"  - Total keyword clusters: {keyword_analysis['total_keyword_clusters']}")
    print(f"  - Covered clusters: {keyword_analysis['covered_clusters']}")
    print(f"  - Uncovered clusters: {keyword_analysis['uncovered_clusters']}")
    print(f"  - Total search volume: {keyword_analysis['total_search_volume']:,}/month")
    print(f"  - Missed opportunity: {keyword_analysis['missed_opportunity']:,}/month")
    
    print(f"\nPriority Recommendations:")
    for i, action in enumerate(audit_report["priority_actions"], 1):
        print(f"  {i}. {action}")
    
    print(f"\nDetailed Recommendation Counts:")
    recommendations = audit_report["recommendations"]
    print(f"  - Keyword gaps: {len(recommendations['keyword_gaps'])}")
    print(f"  - Internal linking opportunities: {len(recommendations['internal_linking'])}")
    print(f"  - Schema markup recommendations: {len(recommendations['schema_markup'])}")
    
    print(f"\nSEO optimization analysis complete!")

if __name__ == "__main__":
    main()