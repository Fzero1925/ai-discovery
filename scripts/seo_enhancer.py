#!/usr/bin/env python3
"""
AI Discovery SEO Enhancement Suite

Advanced SEO optimization including:
- Enhanced JSON-LD structured data
- Breadcrumb navigation generation
- Internal linking optimization
- Advanced sitemap generation with priorities
"""

import os
import sys
import json
import re
import argparse
import codecs
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Optional, Set
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

# 解决Windows编码问题
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


class SEOEnhancer:
    """
    Advanced SEO optimization for AI Discovery platform
    """
    
    def __init__(self, site_root: str = ".", base_url: str = "https://ai-discovery-nu.vercel.app"):
        self.site_root = Path(site_root)
        self.base_url = base_url.rstrip('/')
        self.content_dir = self.site_root / "content"
        self.layouts_dir = self.site_root / "layouts"
        self.static_dir = self.site_root / "static"
        
        # SEO configuration
        self.seo_config = {
            'site_name': 'AI Discovery',
            'site_description': 'Your ultimate guide to AI tools and intelligent software',
            'organization_name': 'AI Discovery Team',
            'social_media': {
                'twitter': '@aidiscovery',
                'linkedin': 'https://linkedin.com/company/aidiscovery',
                'github': 'https://github.com/aidiscovery'
            },
            'logo_url': f'{base_url}/images/logo.png',
            'default_image': f'{base_url}/images/ai-discovery-og.jpg'
        }
        
        # Category priorities for sitemap
        self.category_priorities = {
            'content_creation': 0.9,
            'image_generation': 0.9,
            'code_assistance': 0.8,
            'productivity': 0.8,
            'default': 0.7
        }
        
        # Internal linking keywords
        self.internal_linking_keywords = {
            'AI tools': '/categories/',
            'content creation': '/categories/content-creation/',
            'image generation': '/categories/image-generation/', 
            'code assistance': '/categories/code-assistance/',
            'productivity tools': '/categories/productivity/',
            'artificial intelligence': '/',
            'AI software': '/',
            'ChatGPT': '/reviews/chatgpt-review/',
            'Claude': '/reviews/claude-review/',
            'Midjourney': '/reviews/midjourney-review/'
        }
    
    def enhance_all_seo(self) -> Dict[str, any]:
        """Run complete SEO enhancement suite"""
        print("🚀 Starting AI Discovery SEO Enhancement...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'enhancements': [],
            'metrics': {},
            'errors': []
        }
        
        try:
            # Step 1: Enhanced structured data
            print("📊 Generating enhanced structured data...")
            structured_data_results = self.generate_structured_data()
            results['enhancements'].append({
                'type': 'structured_data',
                'results': structured_data_results
            })
            
            # Step 2: Breadcrumb navigation
            print("🍞 Creating breadcrumb navigation...")
            breadcrumb_results = self.create_breadcrumb_system()
            results['enhancements'].append({
                'type': 'breadcrumbs',
                'results': breadcrumb_results
            })
            
            # Step 3: Internal linking optimization
            print("🔗 Optimizing internal linking...")
            internal_linking_results = self.optimize_internal_linking()
            results['enhancements'].append({
                'type': 'internal_linking',
                'results': internal_linking_results
            })
            
            # Step 4: Advanced sitemap generation
            print("🗺️ Generating advanced sitemap...")
            sitemap_results = self.generate_advanced_sitemap()
            results['enhancements'].append({
                'type': 'sitemap',
                'results': sitemap_results
            })
            
            # Step 5: Meta tags optimization
            print("🏷️ Optimizing meta tags...")
            meta_tags_results = self.optimize_meta_tags()
            results['enhancements'].append({
                'type': 'meta_tags',
                'results': meta_tags_results
            })
            
            # Step 6: Schema markup for reviews
            print("⭐ Creating review schema markup...")
            review_schema_results = self.create_review_schema()
            results['enhancements'].append({
                'type': 'review_schema',
                'results': review_schema_results
            })
            
            # Calculate SEO metrics
            results['metrics'] = self.calculate_seo_metrics()
            
            print("✅ SEO enhancement completed successfully!")
            return results
            
        except Exception as e:
            error_msg = f"SEO enhancement error: {e}"
            print(f"❌ {error_msg}")
            results['errors'].append(error_msg)
            return results
    
    def generate_structured_data(self) -> Dict[str, any]:
        """Generate comprehensive JSON-LD structured data"""
        results = {
            'files_created': 0,
            'schema_types': [],
            'errors': []
        }
        
        try:
            # Create structured data partial
            structured_data_template = """{{/* Enhanced Structured Data for AI Discovery */}}
{{ $page := . }}
{{ $site := .Site }}

{{/* Organization Schema */}}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "{{ $site.Params.organization_name | default "AI Discovery" }}",
  "url": "{{ $site.BaseURL }}",
  "logo": "{{ $site.Params.logo_url | default (printf "%s/images/logo.png" $site.BaseURL) }}",
  "description": "{{ $site.Params.description }}",
  "foundingDate": "{{ $site.Params.founding_date | default "2024" }}",
  "sameAs": [
    {{ if $site.Params.twitter }}"https://twitter.com/{{ strings.TrimPrefix "@" $site.Params.twitter }}",{{ end }}
    {{ if $site.Params.linkedin }}"{{ $site.Params.linkedin }}",{{ end }}
    {{ if $site.Params.github }}"{{ $site.Params.github }}"{{ end }}
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "email": "{{ $site.Params.email | default "contact@aidiscovery.com" }}",
    "contactType": "customer service"
  }
}
</script>

{{ if .IsHome }}
{{/* Website Schema for Homepage */}}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "{{ $site.Title }}",
  "url": "{{ $site.BaseURL }}",
  "description": "{{ $site.Params.description }}",
  "potentialAction": {
    "@type": "SearchAction",
    "target": {
      "@type": "EntryPoint",
      "urlTemplate": "{{ $site.BaseURL }}search/?q={search_term_string}"
    },
    "query-input": "required name=search_term_string"
  },
  "publisher": {
    "@type": "Organization",
    "name": "{{ $site.Params.organization_name | default "AI Discovery" }}",
    "logo": {
      "@type": "ImageObject",
      "url": "{{ $site.Params.logo_url | default (printf "%s/images/logo.png" $site.BaseURL) }}"
    }
  }
}
</script>
{{ end }}

{{ if in .Section "reviews" }}
{{/* Software Application Review Schema */}}
{{ $toolName := .Params.tool_name | default (index (split .Title " ") 0) }}
{{ $rating := .Params.rating | default 4.2 }}
{{ $category := .Params.categories | index 0 | default "AI Tools" }}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "SoftwareApplication",
    "name": "{{ $toolName }}",
    "applicationCategory": "{{ $category }}",
    "operatingSystem": "Web, Windows, macOS, Linux",
    "description": "{{ .Description | default .Summary }}"
  },
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": {{ $rating }},
    "bestRating": 5,
    "worstRating": 1
  },
  "author": {
    "@type": "Organization",
    "name": "{{ $site.Params.organization_name | default "AI Discovery Team" }}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "{{ $site.Params.organization_name | default "AI Discovery" }}",
    "logo": {
      "@type": "ImageObject",
      "url": "{{ $site.Params.logo_url | default (printf "%s/images/logo.png" $site.BaseURL) }}"
    }
  },
  "datePublished": "{{ .Date.Format "2006-01-02" }}",
  {{ if .Lastmod }}
  "dateModified": "{{ .Lastmod.Format "2006-01-02" }}",
  {{ end }}
  "reviewBody": "{{ .Summary | plainify | truncate 300 }}"
}
</script>
{{ end }}

{{ if .IsPage }}
{{/* Article Schema for individual pages */}}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{ .Title }}",
  "description": "{{ .Description | default .Summary }}",
  "author": {
    "@type": "Organization",
    "name": "{{ $site.Params.organization_name | default "AI Discovery Team" }}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "{{ $site.Params.organization_name | default "AI Discovery" }}",
    "logo": {
      "@type": "ImageObject",
      "url": "{{ $site.Params.logo_url | default (printf "%s/images/logo.png" $site.BaseURL) }}"
    }
  },
  "datePublished": "{{ .Date.Format "2006-01-02T15:04:05Z07:00" }}",
  {{ if .Lastmod }}
  "dateModified": "{{ .Lastmod.Format "2006-01-02T15:04:05Z07:00" }}",
  {{ end }}
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{{ .Permalink }}"
  },
  {{ if .Params.featured_image }}
  "image": {
    "@type": "ImageObject",
    "url": "{{ .Params.featured_image | absURL }}",
    "width": 1200,
    "height": 630
  },
  {{ end }}
  "articleSection": "{{ range .Params.categories }}{{ . }}{{ end }}",
  "keywords": "{{ range .Params.tags }}{{ . }},{{ end }}{{ range .Params.categories }}{{ . }},{{ end }}AI tools, artificial intelligence"
}
</script>
{{ end }}

{{/* Breadcrumb Schema */}}
{{ if not .IsHome }}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "{{ $site.BaseURL }}"
    }
    {{ if .Section }},
    {
      "@type": "ListItem", 
      "position": 2,
      "name": "{{ .Section | title }}",
      "item": "{{ $site.BaseURL }}{{ .Section }}/"
    }
    {{ end }}
    {{ if and .Section (ne .Section .Type) }},
    {
      "@type": "ListItem",
      "position": 3,
      "name": "{{ .Title }}",
      "item": "{{ .Permalink }}"
    }
    {{ else if .Section }},
    {
      "@type": "ListItem",
      "position": 3,
      "name": "{{ .Title }}",
      "item": "{{ .Permalink }}"
    }
    {{ end }}
  ]
}
</script>
{{ end }}"""
            
            # Save structured data partial
            partials_dir = self.layouts_dir / "partials"
            partials_dir.mkdir(parents=True, exist_ok=True)
            
            structured_data_path = partials_dir / "seo-structured-data-enhanced.html"
            with open(structured_data_path, 'w', encoding='utf-8') as f:
                f.write(structured_data_template)
            
            results['files_created'] += 1
            results['schema_types'] = ['Organization', 'WebSite', 'Review', 'Article', 'BreadcrumbList']
            print(f"  ✅ Created enhanced structured data: {structured_data_path}")
            
        except Exception as e:
            error_msg = f"Error generating structured data: {e}"
            print(f"  ❌ {error_msg}")
            results['errors'].append(error_msg)
        
        return results
    
    def create_breadcrumb_system(self) -> Dict[str, any]:
        """Create breadcrumb navigation system"""
        results = {
            'files_created': 0,
            'breadcrumb_levels': 0,
            'errors': []
        }
        
        try:
            # Create breadcrumb partial
            breadcrumb_template = """{{/* AI Discovery Breadcrumb Navigation */}}
{{ $page := . }}
{{ $site := .Site }}

{{ if not .IsHome }}
<nav aria-label="Breadcrumb" class="breadcrumb-nav">
  <ol class="breadcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">
    <li class="breadcrumb-item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <a href="/" itemprop="item">
        <span itemprop="name">🏠 Home</span>
      </a>
      <meta itemprop="position" content="1" />
    </li>
    
    {{ if .Section }}
    <li class="breadcrumb-item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      {{ $sectionTitle := .Section | title }}
      {{ if eq .Section "reviews" }}{{ $sectionTitle = "Tool Reviews" }}{{ end }}
      {{ if eq .Section "categories" }}{{ $sectionTitle = "Categories" }}{{ end }}
      {{ if eq .Section "articles" }}{{ $sectionTitle = "Articles" }}{{ end }}
      
      <a href="/{{ .Section }}/" itemprop="item">
        <span itemprop="name">{{ $sectionTitle }}</span>
      </a>
      <meta itemprop="position" content="2" />
    </li>
    {{ end }}
    
    {{ if and .Params.categories (gt (len .Params.categories) 0) }}
    {{ $category := index .Params.categories 0 }}
    <li class="breadcrumb-item" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      {{ $categoryTitle := $category | title | replaceRE "_" " " }}
      {{ if eq $category "content_creation" }}{{ $categoryTitle = "Content Creation" }}{{ end }}
      {{ if eq $category "image_generation" }}{{ $categoryTitle = "Image Generation" }}{{ end }}
      {{ if eq $category "code_assistance" }}{{ $categoryTitle = "Code Assistance" }}{{ end }}
      
      <a href="/categories/{{ $category }}/" itemprop="item">
        <span itemprop="name">{{ $categoryTitle }}</span>
      </a>
      <meta itemprop="position" content="3" />
    </li>
    {{ end }}
    
    <li class="breadcrumb-item active" itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">
      <span itemprop="name">{{ .Title }}</span>
      <meta itemprop="position" content="{{ if and .Section .Params.categories }}4{{ else if .Section }}3{{ else }}2{{ end }}" />
    </li>
  </ol>
</nav>

<style>
.breadcrumb-nav {
  margin: 1rem 0 2rem 0;
  padding: 0.75rem 1rem;
  background: #f8f9fa;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.breadcrumb {
  display: flex;
  flex-wrap: wrap;
  padding: 0;
  margin: 0;
  list-style: none;
  align-items: center;
}

.breadcrumb-item + .breadcrumb-item::before {
  content: "›";
  padding: 0 0.5rem;
  color: #6b7280;
}

.breadcrumb-item a {
  color: #3b82f6;
  text-decoration: none;
  transition: color 0.2s;
}

.breadcrumb-item a:hover {
  color: #1d4ed8;
  text-decoration: underline;
}

.breadcrumb-item.active {
  color: #374151;
  font-weight: 500;
}

@media (max-width: 640px) {
  .breadcrumb-nav {
    margin: 0.5rem 0 1rem 0;
    padding: 0.5rem 0.75rem;
    font-size: 0.8125rem;
  }
}
</style>
{{ end }}"""
            
            # Save breadcrumb partial
            partials_dir = self.layouts_dir / "partials"
            partials_dir.mkdir(parents=True, exist_ok=True)
            
            breadcrumb_path = partials_dir / "breadcrumb-navigation.html"
            with open(breadcrumb_path, 'w', encoding='utf-8') as f:
                f.write(breadcrumb_template)
            
            results['files_created'] += 1
            results['breadcrumb_levels'] = 4  # Home > Section > Category > Page
            print(f"  ✅ Created breadcrumb navigation: {breadcrumb_path}")
            
        except Exception as e:
            error_msg = f"Error creating breadcrumb system: {e}"
            print(f"  ❌ {error_msg}")
            results['errors'].append(error_msg)
        
        return results
    
    def optimize_internal_linking(self) -> Dict[str, any]:
        """Optimize internal linking throughout content"""
        results = {
            'files_processed': 0,
            'links_added': 0,
            'errors': []
        }
        
        try:
            # Find all markdown files
            if not self.content_dir.exists():
                print(f"  ⚠️ Content directory not found: {self.content_dir}")
                return results
            
            md_files = list(self.content_dir.rglob('*.md'))
            
            for md_file in md_files:
                try:
                    # Read file content
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    links_added_in_file = 0
                    
                    # Add internal links based on keywords
                    for keyword, link_url in self.internal_linking_keywords.items():
                        # Create regex pattern for the keyword
                        pattern = rf'\\b{re.escape(keyword)}\\b(?![^<]*>)(?![^\\[]*\\])'
                        
                        # Find matches that aren't already linked
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        
                        for match in matches:
                            # Only add link if not already in a link or heading
                            before_match = content[:match.start()]
                            after_match = content[match.end():]
                            
                            # Skip if already in a link
                            if '[' in before_match.split('\\n')[-1] and '](' in after_match.split('\\n')[0]:
                                continue
                            
                            # Skip if in a heading
                            line_start = before_match.rfind('\\n') + 1
                            line_content = content[line_start:match.start()]
                            if line_content.strip().startswith('#'):
                                continue
                            
                            # Add internal link (limit to 1 per keyword per file)
                            if links_added_in_file < 3:  # Limit total links per file
                                replacement = f'[{match.group()}]({link_url})'
                                content = content[:match.start()] + replacement + content[match.end():]
                                links_added_in_file += 1
                                break
                    
                    # Save modified content if changes were made
                    if content != original_content:
                        with open(md_file, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        results['links_added'] += links_added_in_file
                        print(f"  🔗 Added {links_added_in_file} internal links to {md_file.name}")
                    
                    results['files_processed'] += 1
                    
                except Exception as e:
                    error_msg = f"Error processing {md_file}: {e}"
                    print(f"  ❌ {error_msg}")
                    results['errors'].append(error_msg)
            
        except Exception as e:
            error_msg = f"Error optimizing internal linking: {e}"
            print(f"  ❌ {error_msg}")
            results['errors'].append(error_msg)
        
        return results
    
    def generate_advanced_sitemap(self) -> Dict[str, any]:
        """Generate advanced sitemap with priorities and categories"""
        results = {
            'urls_added': 0,
            'categories_mapped': 0,
            'errors': []
        }
        
        try:
            # Create sitemap configuration
            sitemap_config = """# Advanced Sitemap Configuration for Hugo

[sitemap]
  changefreq = "weekly"
  filename = "sitemap.xml"
  priority = 0.5

# Category-specific configurations
[taxonomies]
  category = "categories"
  tag = "tags"

# URL structure optimization
[permalinks]
  reviews = "/reviews/:slug/"
  articles = "/articles/:slug/"
  categories = "/categories/:slug/"

# Advanced SEO settings
[params.seo]
  enable_sitemap_index = true
  sitemap_priority_mapping = true
  category_priorities = {
    content_creation = 0.9,
    image_generation = 0.9,
    code_assistance = 0.8,
    productivity = 0.8,
    default = 0.7
  }"""
            
            # Save sitemap configuration
            sitemap_config_path = self.site_root / "sitemap-config.toml"
            with open(sitemap_config_path, 'w', encoding='utf-8') as f:
                f.write(sitemap_config)
            
            results['categories_mapped'] = len(self.category_priorities)
            print(f"  ✅ Created advanced sitemap config: {sitemap_config_path}")
            
            # Create custom sitemap template
            sitemap_template = """{{ printf "<?xml version=\\"1.0\\" encoding=\\"utf-8\\" standalone=\\"yes\\"?>" | safeHTML }}
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">

{{ range .Data.Pages }}
{{ if and (not .Draft) (not .Params.private) }}
<url>
  <loc>{{ .Permalink }}</loc>
  {{ if not .Lastmod.IsZero }}
  <lastmod>{{ .Lastmod.Format "2006-01-02T15:04:05-07:00" | safeHTML }}</lastmod>
  {{ end }}
  
  {{/* Dynamic priority based on content type and category */}}
  {{ $priority := 0.5 }}
  {{ if .IsHome }}{{ $priority = 1.0 }}{{ end }}
  {{ if in .RelPermalink "/reviews/" }}{{ $priority = 0.9 }}{{ end }}
  {{ if .Params.categories }}
    {{ range .Params.categories }}
      {{ if eq . "content_creation" }}{{ $priority = 0.9 }}{{ end }}
      {{ if eq . "image_generation" }}{{ $priority = 0.9 }}{{ end }}
      {{ if eq . "code_assistance" }}{{ $priority = 0.8 }}{{ end }}
      {{ if eq . "productivity" }}{{ $priority = 0.8 }}{{ end }}
    {{ end }}
  {{ end }}
  <priority>{{ $priority }}</priority>
  
  {{/* Change frequency based on content type */}}
  {{ $changefreq := "weekly" }}
  {{ if .IsHome }}{{ $changefreq = "daily" }}{{ end }}
  {{ if in .RelPermalink "/reviews/" }}{{ $changefreq = "monthly" }}{{ end }}
  {{ if in .RelPermalink "/articles/" }}{{ $changefreq = "weekly" }}{{ end }}
  <changefreq>{{ $changefreq }}</changefreq>
  
  {{/* Add image information if available */}}
  {{ if .Params.featured_image }}
  <image:image>
    <image:loc>{{ .Params.featured_image | absURL }}</image:loc>
    <image:caption>{{ .Params.image_alt | default .Title }}</image:caption>
    <image:title>{{ .Title }}</image:title>
  </image:image>
  {{ end }}
  
</url>
{{ end }}
{{ end }}
</urlset>"""
            
            # Save custom sitemap template
            layouts_dir = self.layouts_dir
            layouts_dir.mkdir(parents=True, exist_ok=True)
            
            sitemap_template_path = layouts_dir / "sitemap.xml"
            with open(sitemap_template_path, 'w', encoding='utf-8') as f:
                f.write(sitemap_template)
            
            results['urls_added'] = 1  # Template created
            print(f"  ✅ Created custom sitemap template: {sitemap_template_path}")
            
        except Exception as e:
            error_msg = f"Error generating advanced sitemap: {e}"
            print(f"  ❌ {error_msg}")
            results['errors'].append(error_msg)
        
        return results
    
    def optimize_meta_tags(self) -> Dict[str, any]:
        """Optimize meta tags across the site"""
        results = {
            'templates_created': 0,
            'meta_tags_enhanced': 0,
            'errors': []
        }
        
        try:
            # Enhanced meta tags partial
            meta_tags_template = """{{/* Enhanced Meta Tags for AI Discovery */}}
{{ $page := . }}
{{ $site := .Site }}

{{/* Basic Meta Tags */}}
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="X-UA-Compatible" content="IE=edge">

{{/* Title Tag */}}
{{ $title := .Title }}
{{ if .IsHome }}
  {{ $title = $site.Title }}
{{ else }}
  {{ $title = printf "%s | %s" .Title $site.Title }}
{{ end }}
<title>{{ $title }}</title>

{{/* Description */}}
{{ $description := .Description }}
{{ if not $description }}
  {{ if .IsHome }}
    {{ $description = $site.Params.description }}
  {{ else }}
    {{ $description = .Summary | plainify | truncate 155 }}
  {{ end }}
{{ end }}
<meta name="description" content="{{ $description }}">

{{/* Keywords */}}
{{ $keywords := slice }}
{{ if .Params.tags }}{{ $keywords = $keywords | append .Params.tags }}{{ end }}
{{ if .Params.categories }}{{ $keywords = $keywords | append .Params.categories }}{{ end }}
{{ $keywords = $keywords | append (slice "AI tools" "artificial intelligence" "software review" "technology") }}
<meta name="keywords" content="{{ delimit $keywords ", " }}">

{{/* Author and Publisher */}}
<meta name="author" content="{{ $site.Params.organization_name | default "AI Discovery Team" }}">
<meta name="publisher" content="{{ $site.Params.organization_name | default "AI Discovery" }}">

{{/* Robots */}}
{{ $robots := "index, follow" }}
{{ if .Draft }}{{ $robots = "noindex, nofollow" }}{{ end }}
{{ if .Params.noindex }}{{ $robots = "noindex, follow" }}{{ end }}
<meta name="robots" content="{{ $robots }}">

{{/* Canonical URL */}}
<link rel="canonical" href="{{ .Permalink }}">

{{/* Open Graph Meta Tags */}}
<meta property="og:type" content="{{ if .IsHome }}website{{ else }}article{{ end }}">
<meta property="og:title" content="{{ $title }}">
<meta property="og:description" content="{{ $description }}">
<meta property="og:url" content="{{ .Permalink }}">
<meta property="og:site_name" content="{{ $site.Title }}">
<meta property="og:locale" content="{{ $site.Language.Lang | default "en_US" }}">

{{/* Open Graph Image */}}
{{ $ogImage := $site.Params.default_image }}
{{ if .Params.featured_image }}
  {{ $ogImage = .Params.featured_image | absURL }}
{{ end }}
<meta property="og:image" content="{{ $ogImage }}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{{ .Params.image_alt | default .Title }}">

{{/* Article-specific Open Graph */}}
{{ if .IsPage }}
<meta property="article:published_time" content="{{ .Date.Format "2006-01-02T15:04:05Z07:00" }}">
{{ if .Lastmod }}
<meta property="article:modified_time" content="{{ .Lastmod.Format "2006-01-02T15:04:05Z07:00" }}">
{{ end }}
{{ range .Params.categories }}
<meta property="article:section" content="{{ . }}">
{{ end }}
{{ range .Params.tags }}
<meta property="article:tag" content="{{ . }}">
{{ end }}
<meta property="article:author" content="{{ $site.Params.organization_name | default "AI Discovery Team" }}">
{{ end }}

{{/* Twitter Card */}}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ $title }}">
<meta name="twitter:description" content="{{ $description }}">
<meta name="twitter:image" content="{{ $ogImage }}">
{{ if $site.Params.twitter }}
<meta name="twitter:site" content="{{ $site.Params.twitter }}">
<meta name="twitter:creator" content="{{ $site.Params.twitter }}">
{{ end }}

{{/* Additional Meta Tags */}}
<meta name="theme-color" content="#3b82f6">
<meta name="msapplication-TileColor" content="#3b82f6">
<meta name="application-name" content="{{ $site.Title }}">

{{/* Performance and Security */}}
<meta http-equiv="X-Content-Type-Options" content="nosniff">
<meta http-equiv="X-Frame-Options" content="DENY">
<meta http-equiv="X-XSS-Protection" content="1; mode=block">
<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">

{{/* Preconnect for Performance */}}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{{ if $site.Params.google_analytics_id }}
<link rel="preconnect" href="https://www.googletagmanager.com">
{{ end }}"""
            
            # Save enhanced meta tags partial
            partials_dir = self.layouts_dir / "partials"
            partials_dir.mkdir(parents=True, exist_ok=True)
            
            meta_tags_path = partials_dir / "seo-meta-tags-enhanced.html"
            with open(meta_tags_path, 'w', encoding='utf-8') as f:
                f.write(meta_tags_template)
            
            results['templates_created'] += 1
            results['meta_tags_enhanced'] = 15  # Count of meta tag types
            print(f"  ✅ Created enhanced meta tags: {meta_tags_path}")
            
        except Exception as e:
            error_msg = f"Error optimizing meta tags: {e}"
            print(f"  ❌ {error_msg}")
            results['errors'].append(error_msg)
        
        return results
    
    def create_review_schema(self) -> Dict[str, any]:
        """Create structured data specifically for AI tool reviews"""
        results = {
            'schema_created': 0,
            'review_types': 0,
            'errors': []
        }
        
        try:
            # Review schema partial
            review_schema_template = """{{/* AI Tool Review Schema Markup */}}
{{ if and (eq .Section "reviews") (not .IsHome) }}
{{ $toolName := .Params.tool_name | default (index (split .Title " ") 0) }}
{{ $rating := .Params.rating | default 4.2 }}
{{ $maxRating := 5 }}
{{ $minRating := 1 }}
{{ $reviewCount := .Params.review_count | default 1 }}
{{ $category := .Params.categories | index 0 | default "AI Software" }}
{{ $pricing := .Params.pricing | default "Freemium" }}

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product", 
  "name": "{{ $toolName }}",
  "description": "{{ .Description | default .Summary | plainify | truncate 200 }}",
  "category": "{{ $category | title }}",
  "brand": {
    "@type": "Brand",
    "name": "{{ $toolName }}"
  },
  {{ if .Params.featured_image }}
  "image": "{{ .Params.featured_image | absURL }}",
  {{ end }}
  "offers": {
    "@type": "Offer",
    "price": "{{ if eq $pricing "Free" }}0{{ else }}{{ .Params.price | default "20" }}{{ end }}",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "priceValidUntil": "{{ (now.AddDate 1 0 0).Format "2006-01-02" }}",
    "seller": {
      "@type": "Organization", 
      "name": "{{ $toolName }}"
    }
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": {{ $rating }},
    "bestRating": {{ $maxRating }},
    "worstRating": {{ $minRating }},
    "ratingCount": {{ $reviewCount }}
  },
  "review": {
    "@type": "Review",
    "reviewRating": {
      "@type": "Rating",
      "ratingValue": {{ $rating }},
      "bestRating": {{ $maxRating }},
      "worstRating": {{ $minRating }}
    },
    "author": {
      "@type": "Organization",
      "name": "{{ .Site.Params.organization_name | default "AI Discovery Team" }}"
    },
    "datePublished": "{{ .Date.Format "2006-01-02" }}",
    "reviewBody": "{{ .Summary | plainify | truncate 500 }}",
    "publisher": {
      "@type": "Organization", 
      "name": "{{ .Site.Title }}",
      "logo": {
        "@type": "ImageObject",
        "url": "{{ .Site.Params.logo_url | default (printf "%s/images/logo.png" .Site.BaseURL) }}"
      }
    }
  },
  {{ if .Params.key_features }}
  "additionalProperty": [
    {{ range $index, $feature := .Params.key_features }}
    {{ if $index }},{{ end }}
    {
      "@type": "PropertyValue",
      "name": "Feature {{ add $index 1 }}",
      "value": "{{ $feature }}"
    }
    {{ end }}
  ],
  {{ end }}
  "applicationCategory": "{{ $category }}",
  "operatingSystem": "{{ .Params.operating_system | default "Web, Windows, macOS, Linux" }}",
  "softwareVersion": "{{ .Params.version | default "Latest" }}"
}
</script>

{{/* FAQ Schema if FAQ section exists */}}
{{ if .Params.faq }}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {{ range $index, $faq := .Params.faq }}
    {{ if $index }},{{ end }}
    {
      "@type": "Question",
      "name": "{{ $faq.question }}",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{{ $faq.answer | plainify }}"
      }
    }
    {{ end }}
  ]
}
</script>
{{ end }}

{{ end }}"""
            
            # Save review schema partial
            partials_dir = self.layouts_dir / "partials"
            partials_dir.mkdir(parents=True, exist_ok=True)
            
            review_schema_path = partials_dir / "review-schema-markup.html"
            with open(review_schema_path, 'w', encoding='utf-8') as f:
                f.write(review_schema_template)
            
            results['schema_created'] += 1
            results['review_types'] = 3  # Product, Review, FAQ schemas
            print(f"  ✅ Created review schema markup: {review_schema_path}")
            
        except Exception as e:
            error_msg = f"Error creating review schema: {e}"
            print(f"  ❌ {error_msg}")
            results['errors'].append(error_msg)
        
        return results
    
    def calculate_seo_metrics(self) -> Dict[str, any]:
        """Calculate SEO optimization metrics"""
        metrics = {
            'schema_types_implemented': 0,
            'internal_links_density': 0,
            'meta_optimization_score': 0,
            'seo_score': 0
        }
        
        try:
            # Count schema types
            partials_dir = self.layouts_dir / "partials"
            if partials_dir.exists():
                schema_files = list(partials_dir.glob("*schema*.html"))
                metrics['schema_types_implemented'] = len(schema_files) * 2  # Estimate
            
            # Estimate internal links density
            if self.content_dir.exists():
                md_files = list(self.content_dir.rglob('*.md'))
                total_links = 0
                total_files = len(md_files)
                
                for md_file in md_files[:10]:  # Sample first 10 files
                    try:
                        with open(md_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        links = len(re.findall(r'\\[.*?\\]\\(.*?\\)', content))
                        total_links += links
                    except:
                        continue
                
                if total_files > 0:
                    metrics['internal_links_density'] = total_links / min(10, total_files)
            
            # Calculate meta optimization score
            score = 0
            templates_dir = self.layouts_dir / "partials"
            if (templates_dir / "seo-meta-tags-enhanced.html").exists():
                score += 40
            if (templates_dir / "seo-structured-data-enhanced.html").exists():
                score += 30
            if (templates_dir / "breadcrumb-navigation.html").exists():
                score += 20
            if (self.layouts_dir / "sitemap.xml").exists():
                score += 10
            
            metrics['meta_optimization_score'] = score
            metrics['seo_score'] = min(score + (metrics['internal_links_density'] * 5), 100)
            
        except Exception as e:
            print(f"⚠️ Error calculating SEO metrics: {e}")
        
        return metrics


def main():
    """Main function for CLI usage"""
    parser = argparse.ArgumentParser(description='AI Discovery SEO Enhancer')
    parser.add_argument('--structured-data-only', action='store_true',
                       help='Only generate structured data')
    parser.add_argument('--breadcrumbs-only', action='store_true',
                       help='Only create breadcrumb system')
    parser.add_argument('--internal-links-only', action='store_true',
                       help='Only optimize internal linking')
    parser.add_argument('--site-root', default='.',
                       help='Root directory of the site')
    parser.add_argument('--base-url', default='https://ai-discovery-nu.vercel.app',
                       help='Base URL of the site')
    
    args = parser.parse_args()
    
    enhancer = SEOEnhancer(args.site_root, args.base_url)
    
    try:
        if args.structured_data_only:
            print("📊 Generating structured data only...")
            results = enhancer.generate_structured_data()
            print(f"✅ Created {results['files_created']} files with {len(results['schema_types'])} schema types")
            
        elif args.breadcrumbs_only:
            print("🍞 Creating breadcrumb system only...")
            results = enhancer.create_breadcrumb_system()
            print(f"✅ Created breadcrumb system with {results['breadcrumb_levels']} levels")
            
        elif args.internal_links_only:
            print("🔗 Optimizing internal linking only...")
            results = enhancer.optimize_internal_linking()
            print(f"✅ Added {results['links_added']} internal links across {results['files_processed']} files")
            
        else:
            # Run full SEO enhancement
            results = enhancer.enhance_all_seo()
            
            # Print summary
            print("\\n📊 SEO Enhancement Summary:")
            print("=" * 40)
            for enhancement in results['enhancements']:
                print(f"✅ {enhancement['type'].replace('_', ' ').title()}")
            
            if 'metrics' in results:
                metrics = results['metrics']
                print(f"\\n🎯 SEO Score: {metrics.get('seo_score', 0)}/100")
                print(f"📊 Schema Types: {metrics.get('schema_types_implemented', 0)}")
                print(f"🔗 Avg Internal Links: {metrics.get('internal_links_density', 0):.1f} per page")
                print(f"📈 Meta Optimization: {metrics.get('meta_optimization_score', 0)}/100")
            
            if results['errors']:
                print(f"\\n⚠️ Errors encountered: {len(results['errors'])}")
                for error in results['errors'][:3]:  # Show first 3 errors
                    print(f"  • {error}")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ SEO enhancement failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()