#!/usr/bin/env python3
"""
Test script for AI tool image system
"""

import sys
import os
sys.path.append('modules')

try:
    from image_processor.ai_tool_image_handler import AIToolImageHandler
    
    # API keys from user
    unsplash_key = "fU_RSdecKs7yCLkwfietuN_An8Y4pDAARPjbGuWlyKQ"
    pexels_key = "GEIG80uBUWAZYPkdLvhqSxLatgJ5Gyiu7DWxTy3veJTMGMVVkMuSWdrg"
    pixabay_key = "52152560-87d638059f34cdb71e8341171"
    
    print("Initializing AI Tool Image Handler with API keys...")
    handler = AIToolImageHandler(
        unsplash_access_key=unsplash_key,
        pexels_api_key=pexels_key,
        pixabay_api_key=pixabay_key
    )
    
    print("Available APIs:", handler.available_apis)
    
    # Test fetching an image for Claude AI
    print("\nTesting image fetch for Claude AI...")
    try:
        image_metadata = handler.fetch_tool_image("Claude AI", "content-creation", ["AI assistant", "conversation interface"])
        if image_metadata:
            print(f"SUCCESS: Fetched image: {image_metadata.filename}")
        else:
            print("ERROR: No image metadata returned")
    except Exception as e:
        print(f"ERROR: Failed to fetch image: {e}")
        
    # Test fetching an image for Stable Diffusion  
    print("\nTesting image fetch for Stable Diffusion...")
    try:
        image_metadata = handler.fetch_tool_image("Stable Diffusion", "image-generation", ["AI art", "image generator"])
        if image_metadata:
            print(f"SUCCESS: Fetched image: {image_metadata.filename}")
        else:
            print("ERROR: No image metadata returned")
    except Exception as e:
        print(f"ERROR: Failed to fetch image: {e}")
    
except ImportError as e:
    print(f"IMPORT ERROR: {e}")
except Exception as e:
    print(f"ERROR: {e}")