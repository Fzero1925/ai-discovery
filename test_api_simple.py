#!/usr/bin/env python3
import os
import requests

# Test Unsplash API
access_key = "fU_RSdecKs7yCLkwfietuN_An8Y4pDAARPjbGuWlyKQ"

try:
    print("Testing Unsplash API...")
    
    url = "https://api.unsplash.com/search/photos"
    headers = {
        'Authorization': f'Client-ID {access_key}',
        'Accept-Version': 'v1'
    }
    
    params = {
        'query': 'artificial intelligence',
        'per_page': 3,
        'orientation': 'landscape'
    }
    
    response = requests.get(url, headers=headers, params=params, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        photos = data.get('results', [])
        
        print(f"SUCCESS: API connected! Found {len(photos)} images")
        print(f"Rate limit remaining: {response.headers.get('X-Ratelimit-Remaining', 'N/A')}")
        
        for i, photo in enumerate(photos[:2], 1):
            print(f"Image {i}: {photo['description'] or 'No description'}")
            print(f"  Size: {photo['width']}x{photo['height']}")
            print(f"  Author: {photo['user']['name']}")
            
    elif response.status_code == 401:
        print("ERROR: Invalid API key")
    elif response.status_code == 403:
        print("ERROR: API rate limit exceeded")
    else:
        print(f"ERROR: API request failed: {response.status_code}")
        
except Exception as e:
    print(f"ERROR: {e}")