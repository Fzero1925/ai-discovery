#!/usr/bin/env python3
"""
Update placeholder images in existing articles with real images
"""

import os
import sys
import re
sys.path.append('modules')

from image_processor.ai_tool_image_handler import AIToolImageHandler

# Priority tools to fix first
PRIORITY_TOOLS = [
    ("ChatGPT", "content-creation", "chatgpt-review-2025-09.md"),
    ("GitHub Copilot", "code-assistance", "github-copilot-review-2025-09.md"), 
    ("DALL-E 3", "image-generation", "dall-e-3-review-2025-09.md"),
    ("Grammarly", "productivity", "grammarly-review-2025-09.md"),
    ("Jasper AI", "content-creation", "jasper-ai-review-2025-09.md")
]

def update_article_images():
    """Update articles to use real images instead of placeholders"""
    
    # API keys from environment variables (secure)
    unsplash_key = os.getenv('UNSPLASH_ACCESS_KEY')
    pexels_key = os.getenv('PEXELS_API_KEY')
    pixabay_key = os.getenv('PIXABAY_API_KEY')
    
    # Validate API keys are available
    if not any([unsplash_key, pexels_key, pixabay_key]):
        print("ERROR: 至少需要配置一个图片API密钥。请设置环境变量:")
        print("- UNSPLASH_ACCESS_KEY")  
        print("- PEXELS_API_KEY")
        print("- PIXABAY_API_KEY")
        return False
    
    # Initialize image handler
    handler = AIToolImageHandler(
        unsplash_access_key=unsplash_key,
        pexels_api_key=pexels_key,
        pixabay_api_key=pixabay_key
    )
    
    success_count = 0
    
    for tool_name, category, filename in PRIORITY_TOOLS:
        try:
            print(f"\n=== Processing {tool_name} ===")
            
            # Fetch real image
            image_metadata = handler.fetch_tool_image(tool_name, category, [tool_name, "AI tool"])
            
            if image_metadata:
                print(f"SUCCESS: Generated real image: {image_metadata.filename}")
                
                # Update article file
                article_path = f"content/reviews/{filename}"
                if os.path.exists(article_path):
                    # Read article content
                    with open(article_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace placeholder image path
                    real_image_path = f"/images/tools/{image_metadata.filename}"
                    
                    # Update featured_image in frontmatter
                    tool_slug = tool_name.lower().replace(" ", "-").replace("-ai", "").replace("ai", "")
                    placeholder_pattern = f"/images/tools/{tool_slug}-placeholder.jpg"
                    
                    updated_content = content.replace(placeholder_pattern, real_image_path)
                    
                    # Also update any inline image references
                    inline_pattern = f'![{tool_name}.*]\\({placeholder_pattern}.*\\)'
                    inline_replacement = f'![{tool_name}]({real_image_path} "{tool_name} - Professional AI Tool Interface")'
                    updated_content = re.sub(inline_pattern, inline_replacement, updated_content)
                    
                    # Write back updated content
                    with open(article_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)
                    
                    print(f"SUCCESS: Updated article {filename}")
                    success_count += 1
                else:
                    print(f"WARNING: Article file not found: {filename}")
            else:
                print(f"ERROR: Failed to generate image for {tool_name}")
                
        except Exception as e:
            print(f"ERROR processing {tool_name}: {e}")
    
    print(f"\n=== Summary ===")
    print(f"Successfully updated {success_count}/{len(PRIORITY_TOOLS)} articles")
    print("Real images generated and articles updated!")
    return True

if __name__ == "__main__":
    success = update_article_images()
    if not success:
        print("Image update failed due to missing API keys.")
        exit(1)