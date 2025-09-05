#!/usr/bin/env python3
"""
AI Discovery Performance Optimizer

Optimizes website performance through:
- Image compression and WebP conversion
- Cache strategy implementation
- Build optimization
- Progressive loading setup
"""

import os
import sys
import json
import time
import shutil
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from PIL import Image, ImageOps
import codecs

# 解决Windows编码问题
if sys.platform == "win32":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


class PerformanceOptimizer:
    """
    Comprehensive performance optimization for AI Discovery website
    """
    
    def __init__(self, site_root: str = "."):
        self.site_root = Path(site_root)
        self.images_dir = self.site_root / "static" / "images"
        self.public_dir = self.site_root / "public"
        
        # Performance optimization settings
        self.image_settings = {
            'jpeg_quality': 85,
            'webp_quality': 80,
            'png_optimize': True,
            'max_width': 1200,
            'max_height': 800,
            'thumbnail_sizes': [(400, 300), (800, 600)],
            'progressive_jpeg': True
        }
        
        # File size thresholds (in bytes)
        self.size_thresholds = {
            'large_image': 500 * 1024,    # 500KB
            'medium_image': 200 * 1024,   # 200KB
            'small_image': 50 * 1024      # 50KB
        }
        
        # CDN and caching configuration
        self.cache_config = {
            'images': '7d',      # 7 days for images
            'css': '30d',        # 30 days for CSS
            'js': '30d',         # 30 days for JavaScript
            'fonts': '365d',     # 1 year for fonts
            'html': '1h'         # 1 hour for HTML
        }
    
    def optimize_all(self) -> Dict[str, any]:
        """Run complete performance optimization suite"""
        print("🚀 Starting AI Discovery Performance Optimization...")
        
        results = {
            'timestamp': time.time(),
            'optimizations': [],
            'metrics': {},
            'errors': []
        }
        
        try:
            # Step 1: Image optimization
            print("🖼️ Optimizing images...")
            image_results = self.optimize_images()
            results['optimizations'].append({
                'type': 'image_optimization',
                'results': image_results
            })
            
            # Step 2: Generate responsive image variants
            print("📱 Generating responsive image variants...")
            responsive_results = self.generate_responsive_images()
            results['optimizations'].append({
                'type': 'responsive_images',
                'results': responsive_results
            })
            
            # Step 3: Create cache headers configuration
            print("⚡ Setting up cache optimization...")
            cache_results = self.setup_cache_optimization()
            results['optimizations'].append({
                'type': 'cache_optimization',
                'results': cache_results
            })
            
            # Step 4: Generate performance monitoring script
            print("📊 Setting up performance monitoring...")
            monitoring_results = self.setup_performance_monitoring()
            results['optimizations'].append({
                'type': 'performance_monitoring',
                'results': monitoring_results
            })
            
            # Step 5: Create build optimization
            print("🏗️ Optimizing build process...")
            build_results = self.optimize_build_process()
            results['optimizations'].append({
                'type': 'build_optimization',
                'results': build_results
            })
            
            # Calculate overall metrics
            results['metrics'] = self.calculate_performance_metrics()
            
            print("✅ Performance optimization completed successfully!")
            return results
            
        except Exception as e:
            error_msg = f"Performance optimization error: {e}"
            print(f"❌ {error_msg}")
            results['errors'].append(error_msg)
            return results
    
    def optimize_images(self) -> Dict[str, any]:
        """Optimize all images in the images directory"""
        results = {
            'processed_count': 0,
            'total_size_before': 0,
            'total_size_after': 0,
            'compression_ratio': 0,
            'formats_converted': {},
            'errors': []
        }
        
        if not self.images_dir.exists():
            print(f"⚠️ Images directory not found: {self.images_dir}")
            return results
        
        # Find all images
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(self.images_dir.rglob(f'*{ext}'))
            image_files.extend(self.images_dir.rglob(f'*{ext.upper()}'))
        
        for image_path in image_files:
            try:
                # Skip if already optimized (check for WebP version)
                webp_path = image_path.with_suffix('.webp')
                if webp_path.exists() and webp_path.stat().st_mtime > image_path.stat().st_mtime:
                    continue
                
                original_size = image_path.stat().st_size
                results['total_size_before'] += original_size
                
                # Optimize the image
                optimized_size = self._optimize_single_image(image_path)
                results['total_size_after'] += optimized_size
                results['processed_count'] += 1
                
                # Track format conversions
                original_format = image_path.suffix.lower()
                if original_format not in results['formats_converted']:
                    results['formats_converted'][original_format] = 0
                results['formats_converted'][original_format] += 1
                
                print(f"  ✅ Optimized {image_path.name}: {original_size:,} → {optimized_size:,} bytes")
                
            except Exception as e:
                error_msg = f"Error optimizing {image_path}: {e}"
                print(f"  ❌ {error_msg}")
                results['errors'].append(error_msg)
        
        # Calculate compression ratio
        if results['total_size_before'] > 0:
            results['compression_ratio'] = (
                (results['total_size_before'] - results['total_size_after']) /
                results['total_size_before'] * 100
            )
        
        return results
    
    def _optimize_single_image(self, image_path: Path) -> int:
        """Optimize a single image file"""
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P', 'LA'):
                # For transparent images, keep transparency for PNG
                if image_path.suffix.lower() == '.png' and 'transparency' in img.info:
                    pass  # Keep as-is for PNG with transparency
                else:
                    img = img.convert('RGB')
            
            # Resize if too large
            original_size = img.size
            if img.width > self.image_settings['max_width'] or img.height > self.image_settings['max_height']:
                img.thumbnail(
                    (self.image_settings['max_width'], self.image_settings['max_height']),
                    Image.Resampling.LANCZOS
                )
                print(f"    📏 Resized from {original_size} to {img.size}")
            
            # Save optimized original format
            if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                img.save(
                    image_path,
                    format='JPEG',
                    quality=self.image_settings['jpeg_quality'],
                    optimize=True,
                    progressive=self.image_settings['progressive_jpeg']
                )
            elif image_path.suffix.lower() == '.png':
                img.save(
                    image_path,
                    format='PNG',
                    optimize=self.image_settings['png_optimize']
                )
            
            # Generate WebP version
            webp_path = image_path.with_suffix('.webp')
            if img.mode == 'RGBA':
                img.save(
                    webp_path,
                    format='WebP',
                    quality=self.image_settings['webp_quality'],
                    method=6,  # Better compression
                    lossless=False
                )
            else:
                img.save(
                    webp_path,
                    format='WebP',
                    quality=self.image_settings['webp_quality'],
                    method=6
                )
        
        return image_path.stat().st_size
    
    def generate_responsive_images(self) -> Dict[str, any]:
        """Generate responsive image variants"""
        results = {
            'variants_created': 0,
            'total_variants': 0,
            'errors': []
        }
        
        # Find all optimized images
        image_files = list(self.images_dir.rglob('*.jpg'))
        image_files.extend(self.images_dir.rglob('*.jpeg'))
        image_files.extend(self.images_dir.rglob('*.png'))
        
        for image_path in image_files:
            try:
                # Skip if image is already a thumbnail
                if any(size_str in image_path.name for size_str in ['400x300', '800x600', 'thumb']):
                    continue
                
                with Image.open(image_path) as img:
                    for width, height in self.image_settings['thumbnail_sizes']:
                        # Create thumbnail variant
                        thumb_name = f"{image_path.stem}-{width}x{height}{image_path.suffix}"
                        thumb_path = image_path.parent / thumb_name
                        
                        # Skip if already exists and newer
                        if thumb_path.exists() and thumb_path.stat().st_mtime > image_path.stat().st_mtime:
                            continue
                        
                        # Create thumbnail
                        thumb_img = img.copy()
                        thumb_img.thumbnail((width, height), Image.Resampling.LANCZOS)
                        
                        # Save thumbnail
                        if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                            thumb_img.save(
                                thumb_path,
                                format='JPEG',
                                quality=self.image_settings['jpeg_quality'],
                                optimize=True
                            )
                        else:
                            thumb_img.save(
                                thumb_path,
                                format='PNG',
                                optimize=True
                            )
                        
                        results['variants_created'] += 1
                        print(f"  📱 Created {width}x{height} variant: {thumb_name}")
                
                results['total_variants'] += len(self.image_settings['thumbnail_sizes'])
                
            except Exception as e:
                error_msg = f"Error creating responsive variants for {image_path}: {e}"
                print(f"  ❌ {error_msg}")
                results['errors'].append(error_msg)
        
        return results
    
    def setup_cache_optimization(self) -> Dict[str, any]:
        """Setup cache optimization configurations"""
        results = {
            'files_created': 0,
            'cache_rules': len(self.cache_config),
            'errors': []
        }
        
        try:
            # Create Vercel cache configuration
            vercel_config = {
                "headers": [
                    {
                        "source": "/images/(.*)",
                        "headers": [
                            {
                                "key": "Cache-Control",
                                "value": f"public, max-age={self._parse_cache_duration(self.cache_config['images'])}"
                            },
                            {
                                "key": "X-Content-Type-Options",
                                "value": "nosniff"
                            }
                        ]
                    },
                    {
                        "source": "/css/(.*)",
                        "headers": [
                            {
                                "key": "Cache-Control",
                                "value": f"public, max-age={self._parse_cache_duration(self.cache_config['css'])}"
                            }
                        ]
                    },
                    {
                        "source": "/js/(.*)",
                        "headers": [
                            {
                                "key": "Cache-Control",
                                "value": f"public, max-age={self._parse_cache_duration(self.cache_config['js'])}"
                            }
                        ]
                    },
                    {
                        "source": "/(.*).html",
                        "headers": [
                            {
                                "key": "Cache-Control",
                                "value": f"public, max-age={self._parse_cache_duration(self.cache_config['html'])}"
                            }
                        ]
                    }
                ]
            }
            
            # Save Vercel configuration
            vercel_config_path = self.site_root / "vercel.json"
            with open(vercel_config_path, 'w', encoding='utf-8') as f:
                json.dump(vercel_config, f, indent=2, ensure_ascii=False)
            
            results['files_created'] += 1
            print(f"  ✅ Created Vercel cache config: {vercel_config_path}")
            
            # Create Hugo cache configuration
            hugo_cache_config = """# Hugo Cache Configuration
# Add to config.toml

[caches]
  [caches.getjson]
    dir = ":cacheDir/:project"
    maxAge = "10m"
  [caches.getcsv]
    dir = ":cacheDir/:project"
    maxAge = "10m"
  [caches.images]
    dir = ":resourceDir/_gen"
    maxAge = "720h"  # 30 days
  [caches.assets]
    dir = ":resourceDir/_gen"
    maxAge = "720h"  # 30 days

[imaging]
  resampleFilter = "lanczos"
  quality = 85
  anchor = "smart"
  
[minify]
  disableCSS = false
  disableHTML = false
  disableJS = false
  disableJSON = false
  disableSVG = false
  disableXML = false
"""
            
            cache_config_path = self.site_root / "cache-config.toml"
            with open(cache_config_path, 'w', encoding='utf-8') as f:
                f.write(hugo_cache_config)
            
            results['files_created'] += 1
            print(f"  ✅ Created Hugo cache config: {cache_config_path}")
            
        except Exception as e:
            error_msg = f"Error setting up cache optimization: {e}"
            print(f"  ❌ {error_msg}")
            results['errors'].append(error_msg)
        
        return results
    
    def setup_performance_monitoring(self) -> Dict[str, any]:
        """Setup performance monitoring"""
        results = {
            'files_created': 0,
            'monitoring_enabled': True,
            'errors': []
        }
        
        try:
            # Create performance monitoring script
            monitoring_script = """// AI Discovery Performance Monitor
(function() {
    'use strict';
    
    // Performance metrics collection
    const performanceMetrics = {
        startTime: Date.now(),
        loadTime: 0,
        domContentLoaded: 0,
        imagesLoaded: 0,
        totalImages: 0
    };
    
    // Measure page load performance
    window.addEventListener('load', function() {
        performanceMetrics.loadTime = Date.now() - performanceMetrics.startTime;
        
        // Measure image loading
        const images = document.querySelectorAll('img');
        performanceMetrics.totalImages = images.length;
        
        let loadedImages = 0;
        images.forEach(img => {
            if (img.complete) {
                loadedImages++;
            } else {
                img.addEventListener('load', () => {
                    loadedImages++;
                    if (loadedImages === images.length) {
                        performanceMetrics.imagesLoaded = Date.now() - performanceMetrics.startTime;
                        reportPerformance();
                    }
                });
            }
        });
        
        if (loadedImages === images.length) {
            performanceMetrics.imagesLoaded = performanceMetrics.loadTime;
            reportPerformance();
        }
        
        // Report core web vitals if available
        if ('web-vitals' in window) {
            getCLS(reportWebVital);
            getFID(reportWebVital);
            getLCP(reportWebVital);
        }
    });
    
    // DOM Content Loaded timing
    document.addEventListener('DOMContentLoaded', function() {
        performanceMetrics.domContentLoaded = Date.now() - performanceMetrics.startTime;
    });
    
    // Report performance metrics
    function reportPerformance() {
        console.log('AI Discovery Performance Metrics:', performanceMetrics);
        
        // Send to Google Analytics if available
        if (typeof gtag === 'function') {
            gtag('event', 'page_load_performance', {
                custom_map: {
                    'load_time': performanceMetrics.loadTime,
                    'dom_ready': performanceMetrics.domContentLoaded,
                    'images_loaded': performanceMetrics.imagesLoaded
                }
            });
        }
    }
    
    // Web Vitals reporting
    function reportWebVital(metric) {
        console.log('Web Vital:', metric);
        
        if (typeof gtag === 'function') {
            gtag('event', metric.name.toLowerCase(), {
                value: Math.round(metric.value),
                event_category: 'Web Vitals',
                non_interaction: true
            });
        }
    }
    
    // Progressive image loading with WebP support
    function loadImages() {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    // Check WebP support
                    const supportsWebP = (function() {
                        const elem = document.createElement('canvas');
                        return elem.toDataURL('image/webp').indexOf('data:image/webp') === 0;
                    })();
                    
                    // Use WebP if supported and available
                    if (supportsWebP && img.dataset.srcWebp) {
                        img.src = img.dataset.srcWebp;
                    } else {
                        img.src = img.dataset.src;
                    }
                    
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
    
    // Initialize progressive loading
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadImages);
    } else {
        loadImages();
    }
    
})();"""
            
            # Save monitoring script
            monitoring_script_path = self.site_root / "static" / "js" / "performance-monitor.js"
            monitoring_script_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(monitoring_script_path, 'w', encoding='utf-8') as f:
                f.write(monitoring_script)
            
            results['files_created'] += 1
            print(f"  ✅ Created performance monitoring script: {monitoring_script_path}")
            
        except Exception as e:
            error_msg = f"Error setting up performance monitoring: {e}"
            print(f"  ❌ {error_msg}")
            results['errors'].append(error_msg)
        
        return results
    
    def optimize_build_process(self) -> Dict[str, any]:
        """Optimize Hugo build process"""
        results = {
            'optimizations_applied': 0,
            'build_time_estimate': 0,
            'errors': []
        }
        
        try:
            # Create build optimization script
            build_script = """#!/bin/bash
# AI Discovery Optimized Build Script

echo "🚀 Starting optimized Hugo build..."

# Set build environment variables
export HUGO_ENV=production
export HUGO_ENABLEGITINFO=false  # Disable for faster builds
export HUGO_TIMEOUT=120s

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf public/
rm -rf resources/_gen/

# Pre-build optimizations
echo "⚡ Running pre-build optimizations..."

# Optimize images if not already done
if [ -f "scripts/performance_optimizer.py" ]; then
    python scripts/performance_optimizer.py --images-only
fi

# Build with optimizations
echo "🏗️ Building Hugo site with optimizations..."
time hugo --minify --gc --environment production

# Post-build optimizations
echo "📊 Running post-build optimizations..."

# Compress HTML files further if needed
find public -name "*.html" -exec gzip -k9 {} \\;

# Generate sitemap with proper priorities
if [ -f "public/sitemap.xml" ]; then
    echo "✅ Sitemap generated successfully"
fi

# Report build metrics
echo "📈 Build completed!"
echo "   HTML files: $(find public -name "*.html" | wc -l)"
echo "   CSS files: $(find public -name "*.css" | wc -l)"
echo "   JS files: $(find public -name "*.js" | wc -l)"
echo "   Image files: $(find public \\( -name "*.jpg" -o -name "*.png" -o -name "*.webp" \\) | wc -l)"
echo "   Total size: $(du -sh public | cut -f1)"
"""
            
            build_script_path = self.site_root / "scripts" / "optimized-build.sh"
            build_script_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(build_script_path, 'w', encoding='utf-8') as f:
                f.write(build_script)
            
            # Make script executable (Unix systems)
            if sys.platform != "win32":
                import stat
                build_script_path.chmod(build_script_path.stat().st_mode | stat.S_IEXEC)
            
            results['optimizations_applied'] += 1
            results['files_created'] = 1
            print(f"  ✅ Created optimized build script: {build_script_path}")
            
        except Exception as e:
            error_msg = f"Error optimizing build process: {e}"
            print(f"  ❌ {error_msg}")
            results['errors'].append(error_msg)
        
        return results
    
    def calculate_performance_metrics(self) -> Dict[str, any]:
        """Calculate overall performance metrics"""
        metrics = {
            'total_images': 0,
            'total_image_size': 0,
            'webp_coverage': 0,
            'optimization_score': 0
        }
        
        try:
            # Count images and calculate sizes
            image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
            total_size = 0
            image_count = 0
            webp_count = 0
            
            for ext in image_extensions:
                files = list(self.images_dir.rglob(f'*{ext}'))
                files.extend(self.images_dir.rglob(f'*{ext.upper()}'))
                
                for file_path in files:
                    total_size += file_path.stat().st_size
                    image_count += 1
                    
                    if ext.lower() == '.webp':
                        webp_count += 1
            
            metrics['total_images'] = image_count
            metrics['total_image_size'] = total_size
            
            # Calculate WebP coverage
            if image_count > 0:
                metrics['webp_coverage'] = (webp_count / image_count) * 100
            
            # Calculate optimization score (0-100)
            score = 0
            if metrics['webp_coverage'] > 80:
                score += 40
            elif metrics['webp_coverage'] > 50:
                score += 30
            elif metrics['webp_coverage'] > 20:
                score += 20
            
            # Average file size score
            if image_count > 0:
                avg_size = total_size / image_count
                if avg_size < self.size_thresholds['small_image']:
                    score += 30
                elif avg_size < self.size_thresholds['medium_image']:
                    score += 20
                elif avg_size < self.size_thresholds['large_image']:
                    score += 10
            
            # Configuration score
            if (self.site_root / "vercel.json").exists():
                score += 15
            if (self.site_root / "cache-config.toml").exists():
                score += 15
            
            metrics['optimization_score'] = min(score, 100)
            
        except Exception as e:
            print(f"⚠️ Error calculating metrics: {e}")
        
        return metrics
    
    def _parse_cache_duration(self, duration_str: str) -> int:
        """Parse cache duration string to seconds"""
        duration_map = {
            'h': 3600,      # hours
            'd': 86400,     # days
            'm': 60         # minutes (if used alone)
        }
        
        if duration_str[-1] in duration_map:
            return int(duration_str[:-1]) * duration_map[duration_str[-1]]
        
        return 3600  # Default to 1 hour


def main():
    """Main function for CLI usage"""
    parser = argparse.ArgumentParser(description='AI Discovery Performance Optimizer')
    parser.add_argument('--images-only', action='store_true',
                       help='Only optimize images')
    parser.add_argument('--cache-only', action='store_true',
                       help='Only setup cache optimization')
    parser.add_argument('--site-root', default='.',
                       help='Root directory of the site')
    
    args = parser.parse_args()
    
    optimizer = PerformanceOptimizer(args.site_root)
    
    try:
        if args.images_only:
            print("🖼️ Running image optimization only...")
            results = optimizer.optimize_images()
            print(f"✅ Processed {results['processed_count']} images")
            if results['compression_ratio'] > 0:
                print(f"📈 Compression ratio: {results['compression_ratio']:.1f}%")
                
        elif args.cache_only:
            print("⚡ Setting up cache optimization only...")
            results = optimizer.setup_cache_optimization()
            print(f"✅ Created {results['files_created']} configuration files")
            
        else:
            # Run full optimization
            results = optimizer.optimize_all()
            
            # Print summary
            print("\n📊 Performance Optimization Summary:")
            print("=" * 40)
            for opt in results['optimizations']:
                print(f"✅ {opt['type'].replace('_', ' ').title()}")
            
            if 'metrics' in results:
                metrics = results['metrics']
                print(f"\n🎯 Performance Score: {metrics.get('optimization_score', 0)}/100")
                print(f"🖼️ Total Images: {metrics.get('total_images', 0)}")
                print(f"📊 WebP Coverage: {metrics.get('webp_coverage', 0):.1f}%")
                print(f"💾 Total Image Size: {metrics.get('total_image_size', 0) / 1024 / 1024:.2f}MB")
            
            if results['errors']:
                print(f"\n⚠️ Errors encountered: {len(results['errors'])}")
                for error in results['errors'][:3]:  # Show first 3 errors
                    print(f"  • {error}")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Optimization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()