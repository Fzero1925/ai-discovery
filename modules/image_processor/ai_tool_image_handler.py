"""
AI Tool Image Handler

Automatically fetches and processes high-quality images for AI tool reviews.
Integrates with Unsplash API for relevant, professional images.
"""

import os
import re
import json
import time
import hashlib
import requests
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from PIL import Image, ImageOps
import urllib.parse


@dataclass
class ImageMetadata:
    """Container for image metadata and SEO information"""
    filename: str
    alt_text: str
    caption: str
    photographer: str
    source_url: str
    license_info: str
    width: int
    height: int
    file_size: int
    keywords: List[str]


class AIToolImageHandler:
    """
    Handles automatic image fetching, processing, and optimization for AI tool reviews
    Supports multiple image APIs: Unsplash, Pexels, and Pixabay with intelligent failover
    """
    
    def __init__(self, unsplash_access_key: Optional[str] = None, 
                 pexels_api_key: Optional[str] = None,
                 pixabay_api_key: Optional[str] = None):
        """
        Initialize the multi-API image handler
        
        Args:
            unsplash_access_key: Unsplash API access key. If None, will try to get from environment.
            pexels_api_key: Pexels API key. If None, will try to get from environment.
            pixabay_api_key: Pixabay API key. If None, will try to get from environment.
        """
        # API keys
        self.unsplash_key = unsplash_access_key or os.getenv('UNSPLASH_ACCESS_KEY')
        self.pexels_key = pexels_api_key or os.getenv('PEXELS_API_KEY')
        self.pixabay_key = pixabay_api_key or os.getenv('PIXABAY_API_KEY')
        
        # API endpoints
        self.api_endpoints = {
            'unsplash': "https://api.unsplash.com",
            'pexels': "https://api.pexels.com/v1",
            'pixabay': "https://pixabay.com/api/"
        }
        
        # API availability check
        self.available_apis = self._check_api_availability()
        
        self.images_dir = Path("static/images/tools")
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # Image quality settings
        self.image_settings = {
            'max_width': 1200,
            'max_height': 800,
            'quality': 85,
            'format': 'JPEG',
            'thumbnail_size': (400, 300)
        }
        
        # AI tool category to search term mapping
        self.category_keywords = {
            'content_creation': [
                'artificial intelligence writing',
                'AI content creation workspace',
                'digital content editing',
                'creative writing technology',
                'text generation interface'
            ],
            'image_generation': [
                'AI art generation',
                'digital art creation',
                'creative AI interface',
                'computer graphics design',
                'artificial intelligence artwork'
            ],
            'code_assistance': [
                'programming development',
                'code editor interface',
                'software development workspace',
                'coding assistance technology',
                'developer tools interface'
            ],
            'productivity': [
                'productivity workspace',
                'business automation',
                'digital workflow management',
                'efficient workplace technology',
                'professional task management'
            ]
        }
    
    def _check_api_availability(self) -> List[str]:
        """Check which APIs have valid keys configured"""
        available = []
        
        if self.unsplash_key:
            available.append('unsplash')
        if self.pexels_key:
            available.append('pexels')  
        if self.pixabay_key:
            available.append('pixabay')
            
        return available
    
    def fetch_tool_image(self, tool_name: str, category: str, keywords: List[str] = None) -> Optional[ImageMetadata]:
        """
        Fetch a relevant image for an AI tool using intelligent API rotation
        
        Args:
            tool_name: Name of the AI tool
            category: Tool category (content_creation, image_generation, etc.)
            keywords: Additional keywords for image search
            
        Returns:
            ImageMetadata object or None if no suitable image found
        """
        if not self.available_apis:
            print("WARNING: No API keys configured. Set UNSPLASH_ACCESS_KEY, PEXELS_API_KEY, or PIXABAY_API_KEY environment variables.")
            return self._generate_placeholder_image(tool_name, category)
        
        # Try each available API in priority order
        api_priority = ['unsplash', 'pexels', 'pixabay']
        available_apis = [api for api in api_priority if api in self.available_apis]
        
        for api_name in available_apis:
            try:
                print(f"Trying {api_name.title()} API for {tool_name}...")
                
                # Build search query
                search_terms = self._build_search_query(tool_name, category, keywords)
                
                # Search for images using the appropriate API
                images = self._search_images(api_name, search_terms)
                
                if not images:
                    print(f"No images found on {api_name.title()} for {tool_name}. Trying next API...")
                    continue
                
                # Select best image
                selected_image = self._select_best_image_multi_api(images, tool_name, category, api_name)
                
                # Download and process image
                image_metadata = self._download_and_process_image_multi_api(selected_image, tool_name, category, api_name)
                
                print(f"SUCCESS: Processed image for {tool_name} using {api_name.title()}")
                return image_metadata
                
            except Exception as e:
                print(f"ERROR: {api_name.title()} API failed for {tool_name}: {e}")
                continue
        
        # All APIs failed, generate placeholder
        print(f"WARNING: All APIs failed for {tool_name}. Generating placeholder.")
        return self._generate_placeholder_image(tool_name, category)
    
    def _build_search_query(self, tool_name: str, category: str, keywords: List[str] = None) -> str:
        """Build optimized search query for Unsplash"""
        
        # Get category-specific keywords
        category_terms = self.category_keywords.get(category, ['technology', 'digital workspace'])
        
        # Build query components
        query_parts = []
        
        # Add category keywords
        query_parts.extend(category_terms[:2])  # Use top 2 category keywords
        
        # Add generic AI/tech terms
        tech_terms = ['technology', 'digital', 'modern', 'professional']
        query_parts.extend(tech_terms[:1])
        
        # Add custom keywords if provided
        if keywords:
            query_parts.extend(keywords[:2])
        
        # Join with OR operator for broader results
        search_query = ' OR '.join(query_parts)
        
        return search_query[:100]  # Limit query length
    
    def _search_unsplash_images(self, query: str, per_page: int = 10) -> List[Dict]:
        """Search Unsplash for images"""
        
        headers = {
            'Authorization': f'Client-ID {self.unsplash_key}'
        }
        
        params = {
            'query': query,
            'per_page': per_page,
            'order_by': 'relevance',
            'orientation': 'landscape',
            'content_filter': 'high',
            'color': 'any'
        }
        
        response = requests.get(
            f"{self.api_endpoints['unsplash']}/search/photos",
            headers=headers,
            params=params,
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        return data.get('results', [])
    
    def _search_images(self, api_name: str, query: str, per_page: int = 10) -> List[Dict]:
        """Universal image search method for all APIs"""
        if api_name == 'unsplash':
            return self._search_unsplash_images(query, per_page)
        elif api_name == 'pexels':
            return self._search_pexels_images(query, per_page)
        elif api_name == 'pixabay':
            return self._search_pixabay_images(query, per_page)
        else:
            raise ValueError(f"Unsupported API: {api_name}")
    
    def _search_pexels_images(self, query: str, per_page: int = 10) -> List[Dict]:
        """Search Pexels for images"""
        headers = {
            'Authorization': self.pexels_key
        }
        
        params = {
            'query': query,
            'per_page': per_page,
            'orientation': 'landscape',
            'size': 'large'
        }
        
        response = requests.get(
            f"{self.api_endpoints['pexels']}/search",
            headers=headers,
            params=params,
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        return data.get('photos', [])
    
    def _search_pixabay_images(self, query: str, per_page: int = 10) -> List[Dict]:
        """Search Pixabay for images"""
        params = {
            'key': self.pixabay_key,
            'q': query,
            'per_page': per_page,
            'orientation': 'horizontal',
            'category': 'computer,education',
            'image_type': 'photo',
            'safesearch': 'true',
            'order': 'popular'
        }
        
        response = requests.get(
            self.api_endpoints['pixabay'],
            params=params,
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        return data.get('hits', [])
    
    def _select_best_image_multi_api(self, images: List[Dict], tool_name: str, category: str, api_name: str) -> Dict:
        """Select the most appropriate image from search results for any API"""
        
        def score_image_universal(img: Dict) -> float:
            score = 0.0
            
            # Get dimensions based on API
            if api_name == 'unsplash':
                width = img.get('width', 0)
                height = img.get('height', 0)
            elif api_name == 'pexels':
                width = img.get('width', 0)
                height = img.get('height', 0)
            elif api_name == 'pixabay':
                width = img.get('webformatWidth', 0)
                height = img.get('webformatHeight', 0)
            else:
                width = height = 0
            
            # Resolution score
            if width >= 1920 and height >= 1080:
                score += 2.0
            elif width >= 1200 and height >= 800:
                score += 1.5
            elif width >= 800 and height >= 600:
                score += 1.0
            
            # API-specific engagement metrics
            if api_name == 'unsplash':
                likes = img.get('likes', 0)
                downloads = img.get('downloads', 0)
                score += min(likes / 1000, 2.0)
                score += min(downloads / 10000, 1.0)
            elif api_name == 'pexels':
                # Pexels doesn't have likes, but photographer quality can be a factor
                photographer = img.get('photographer', '')
                if photographer:
                    score += 0.5
            elif api_name == 'pixabay':
                likes = img.get('likes', 0)
                downloads = img.get('downloads', 0)
                views = img.get('views', 0)
                score += min(likes / 100, 2.0)
                score += min(downloads / 1000, 1.0)
                score += min(views / 10000, 0.5)
            
            # Description relevance check
            description = ""
            if api_name == 'unsplash':
                description = (img.get('description', '') or img.get('alt_description', '') or '').lower()
            elif api_name == 'pexels':
                description = (img.get('alt', '') or '').lower()
            elif api_name == 'pixabay':
                description = (img.get('tags', '') or '').lower()
            
            tech_keywords = ['technology', 'digital', 'ai', 'artificial', 'computer', 'software']
            for keyword in tech_keywords:
                if keyword in description:
                    score += 0.5
            
            # Avoid overly specific content
            avoid_terms = ['logo', 'brand', 'company', 'advertisement']
            for term in avoid_terms:
                if term in description:
                    score -= 1.0
            
            return score
        
        # Score and sort images
        scored_images = [(img, score_image_universal(img)) for img in images]
        scored_images.sort(key=lambda x: x[1], reverse=True)
        
        # Return the best image
        return scored_images[0][0] if scored_images else images[0]
    
    def _download_and_process_image_multi_api(self, image_data: Dict, tool_name: str, category: str, api_name: str) -> ImageMetadata:
        """Download and process the selected image from any API"""
        
        # Generate filename
        safe_name = re.sub(r'[^a-zA-Z0-9]', '-', tool_name.lower())
        
        # Get image ID based on API
        if api_name == 'unsplash':
            image_id = image_data.get('id', 'unknown')
        elif api_name == 'pexels':
            image_id = str(image_data.get('id', 'unknown'))
        elif api_name == 'pixabay':
            image_id = str(image_data.get('id', 'unknown'))
        else:
            image_id = 'unknown'
        
        filename = f"{safe_name}-{api_name}-{image_id}.jpg"
        filepath = self.images_dir / filename
        
        # Get download URL based on API
        if api_name == 'unsplash':
            download_url = image_data['urls']['regular']
            # Trigger download for Unsplash analytics
            if 'links' in image_data and 'download_location' in image_data['links']:
                try:
                    requests.get(
                        image_data['links']['download_location'],
                        headers={'Authorization': f'Client-ID {self.unsplash_key}'},
                        timeout=5
                    )
                except:
                    pass  # Don't fail if analytics request fails
        elif api_name == 'pexels':
            download_url = image_data['src']['large']
        elif api_name == 'pixabay':
            download_url = image_data['webformatURL']
        else:
            raise ValueError(f"Unsupported API: {api_name}")
        
        # Download actual image
        img_response = requests.get(download_url, timeout=30)
        img_response.raise_for_status()
        
        # Process and optimize image
        with Image.open(requests.get(download_url, stream=True).raw) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            if img.width > self.image_settings['max_width'] or img.height > self.image_settings['max_height']:
                img.thumbnail(
                    (self.image_settings['max_width'], self.image_settings['max_height']),
                    Image.Resampling.LANCZOS
                )
            
            # Optimize and save
            img.save(
                filepath,
                format=self.image_settings['format'],
                quality=self.image_settings['quality'],
                optimize=True
            )
        
        # Generate metadata
        return self._create_image_metadata_multi_api(image_data, filename, tool_name, category, api_name)
    
    def _create_image_metadata_multi_api(self, image_data: Dict, filename: str, tool_name: str, category: str, api_name: str) -> ImageMetadata:
        """Create comprehensive metadata for the image from any API"""
        
        # Generate SEO-friendly alt text
        alt_text = self._generate_alt_text(tool_name, category, image_data)
        
        # Generate caption
        caption = f"Professional {category.replace('_', ' ')} interface showcasing {tool_name} capabilities"
        
        # Get photographer and source info based on API
        if api_name == 'unsplash':
            photographer = image_data.get('user', {}).get('name', 'Unknown')
            source_url = image_data.get('links', {}).get('html', '')
            license_info = "Unsplash License"
        elif api_name == 'pexels':
            photographer = image_data.get('photographer', 'Unknown')
            source_url = image_data.get('url', '')
            license_info = "Pexels License"
        elif api_name == 'pixabay':
            photographer = image_data.get('user', 'Unknown')
            source_url = image_data.get('pageURL', '')
            license_info = "Pixabay License"
        else:
            photographer = 'Unknown'
            source_url = ''
            license_info = 'Unknown License'
        
        # Get image dimensions
        filepath = self.images_dir / filename
        with Image.open(filepath) as img:
            width, height = img.size
            file_size = os.path.getsize(filepath)
        
        # Generate keywords for SEO
        keywords = self._generate_seo_keywords(tool_name, category)
        
        return ImageMetadata(
            filename=filename,
            alt_text=alt_text,
            caption=caption,
            photographer=photographer,
            source_url=source_url,
            license_info=license_info,
            width=width,
            height=height,
            file_size=file_size,
            keywords=keywords
        )
    
    def _select_best_image(self, images: List[Dict], tool_name: str, category: str) -> Dict:
        """Select the most appropriate image from search results"""
        
        def score_image(img: Dict) -> float:
            score = 0.0
            
            # Resolution score (prefer high-quality images)
            width = img.get('width', 0)
            height = img.get('height', 0)
            if width >= 1920 and height >= 1080:
                score += 2.0
            elif width >= 1200 and height >= 800:
                score += 1.5
            elif width >= 800 and height >= 600:
                score += 1.0
            
            # Likes and downloads score
            likes = img.get('likes', 0)
            downloads = img.get('downloads', 0)
            score += min(likes / 1000, 2.0)  # Cap at 2.0 points
            score += min(downloads / 10000, 1.0)  # Cap at 1.0 points
            
            # Description relevance (if available)
            description = (img.get('description', '') or '').lower()
            alt_description = (img.get('alt_description', '') or '').lower()
            
            tech_keywords = ['technology', 'digital', 'ai', 'artificial', 'computer', 'software']
            for keyword in tech_keywords:
                if keyword in description or keyword in alt_description:
                    score += 0.5
            
            # Avoid overly specific or branded content
            avoid_terms = ['logo', 'brand', 'company', 'advertisement']
            for term in avoid_terms:
                if term in description or term in alt_description:
                    score -= 1.0
            
            return score
        
        # Score and sort images
        scored_images = [(img, score_image(img)) for img in images]
        scored_images.sort(key=lambda x: x[1], reverse=True)
        
        # Return the best image
        return scored_images[0][0] if scored_images else images[0]
    
    def _download_and_process_image(self, image_data: Dict, tool_name: str, category: str) -> ImageMetadata:
        """Download and process the selected image"""
        
        # Generate filename
        safe_name = re.sub(r'[^a-zA-Z0-9]', '-', tool_name.lower())
        image_id = image_data.get('id', 'unknown')
        filename = f"{safe_name}-{image_id}.jpg"
        filepath = self.images_dir / filename
        
        # Download image
        download_url = image_data['urls']['regular']  # High quality but reasonable size
        
        # Trigger download for Unsplash analytics
        if 'links' in image_data and 'download_location' in image_data['links']:
            requests.get(
                image_data['links']['download_location'],
                headers={'Authorization': f'Client-ID {self.unsplash_key}'},
                timeout=5
            )
        
        # Download actual image
        img_response = requests.get(download_url, timeout=30)
        img_response.raise_for_status()
        
        # Process and optimize image
        with Image.open(requests.get(download_url, stream=True).raw) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            if img.width > self.image_settings['max_width'] or img.height > self.image_settings['max_height']:
                img.thumbnail(
                    (self.image_settings['max_width'], self.image_settings['max_height']),
                    Image.Resampling.LANCZOS
                )
            
            # Optimize and save
            img.save(
                filepath,
                format=self.image_settings['format'],
                quality=self.image_settings['quality'],
                optimize=True
            )
        
        # Generate metadata
        return self._create_image_metadata(image_data, filename, tool_name, category)
    
    def _create_image_metadata(self, image_data: Dict, filename: str, tool_name: str, category: str) -> ImageMetadata:
        """Create comprehensive metadata for the image"""
        
        # Generate SEO-friendly alt text
        alt_text = self._generate_alt_text(tool_name, category, image_data)
        
        # Generate caption
        caption = f"Professional {category.replace('_', ' ')} interface showcasing {tool_name} capabilities"
        
        # Get photographer info
        photographer = image_data.get('user', {}).get('name', 'Unknown')
        source_url = image_data.get('links', {}).get('html', '')
        
        # Get image dimensions
        filepath = self.images_dir / filename
        with Image.open(filepath) as img:
            width, height = img.size
            file_size = os.path.getsize(filepath)
        
        # Generate keywords for SEO
        keywords = self._generate_seo_keywords(tool_name, category)
        
        return ImageMetadata(
            filename=filename,
            alt_text=alt_text,
            caption=caption,
            photographer=photographer,
            source_url=source_url,
            license_info="Unsplash License",
            width=width,
            height=height,
            file_size=file_size,
            keywords=keywords
        )
    
    def _generate_alt_text(self, tool_name: str, category: str, image_data: Dict) -> str:
        """Generate SEO-optimized alt text"""
        
        # Base alt text components
        alt_components = []
        
        # Add tool name and category
        alt_components.append(f"{tool_name} AI tool interface")
        alt_components.append(f"{category.replace('_', ' ')} software")
        
        # Add contextual description
        context_map = {
            'content_creation': 'text generation and writing assistance',
            'image_generation': 'visual content creation and design',
            'code_assistance': 'programming support and development',
            'productivity': 'workflow optimization and automation'
        }
        
        context = context_map.get(category, 'AI-powered functionality')
        alt_components.append(f"showcasing {context}")
        
        # Join components naturally
        alt_text = f"{alt_components[0]} for {alt_components[2]}"
        
        # Limit length for SEO best practices
        return alt_text[:125] if len(alt_text) > 125 else alt_text
    
    def _generate_seo_keywords(self, tool_name: str, category: str) -> List[str]:
        """Generate SEO keywords for the image"""
        
        keywords = [
            tool_name.lower(),
            f"{tool_name} interface",
            f"AI {category.replace('_', ' ')}",
            "artificial intelligence",
            "software interface",
            "technology platform"
        ]
        
        # Add category-specific keywords
        category_keywords_map = {
            'content_creation': ['writing AI', 'content generation', 'text creation'],
            'image_generation': ['AI art', 'image creation', 'visual generation'],
            'code_assistance': ['code AI', 'programming assistant', 'development tools'],
            'productivity': ['productivity AI', 'workflow automation', 'business tools']
        }
        
        if category in category_keywords_map:
            keywords.extend(category_keywords_map[category])
        
        return keywords[:10]  # Limit for practical use
    
    def _generate_placeholder_image(self, tool_name: str, category: str) -> ImageMetadata:
        """Generate a placeholder image when API fails"""
        
        # Create a simple colored placeholder
        filename = f"{re.sub(r'[^a-zA-Z0-9]', '-', tool_name.lower())}-placeholder.jpg"
        filepath = self.images_dir / filename
        
        # Category color mapping
        colors = {
            'content_creation': '#4F46E5',    # Indigo
            'image_generation': '#EC4899',    # Pink
            'code_assistance': '#10B981',     # Emerald
            'productivity': '#F59E0B'         # Amber
        }
        
        color = colors.get(category, '#6B7280')  # Default gray
        
        # Create placeholder image
        img = Image.new('RGB', (800, 600), color)
        img.save(filepath, format='JPEG', quality=85)
        
        return ImageMetadata(
            filename=filename,
            alt_text=f"{tool_name} AI tool interface placeholder",
            caption=f"Placeholder image for {tool_name} {category.replace('_', ' ')} tool",
            photographer="AI Discovery",
            source_url="",
            license_info="Generated placeholder",
            width=800,
            height=600,
            file_size=os.path.getsize(filepath),
            keywords=[tool_name.lower(), category, 'AI tool', 'placeholder']
        )


def main():
    """Test the image handler"""
    handler = AIToolImageHandler()
    
    # Test with a sample tool
    metadata = handler.fetch_tool_image("ChatGPT", "content_creation")
    
    if metadata:
        print(f"✅ Generated image: {metadata.filename}")
        print(f"📝 Alt text: {metadata.alt_text}")
        print(f"📏 Dimensions: {metadata.width}x{metadata.height}")
        print(f"📊 File size: {metadata.file_size} bytes")


if __name__ == "__main__":
    main()