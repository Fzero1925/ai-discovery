#!/usr/bin/env python3
"""
AI Discovery Image Deduplication and Cleanup Script

Analyzes and removes duplicate images in the tools directory.
Optimizes storage space and ensures each AI tool has unique, relevant images.
"""

import os
import sys
import hashlib
import shutil
from pathlib import Path
from collections import defaultdict
from PIL import Image
import json

class ImageDuplicateCleaner:
    """Clean up duplicate and unnecessary images"""
    
    def __init__(self, images_dir: str = "static/images/tools"):
        self.images_dir = Path(images_dir)
        self.duplicate_groups = defaultdict(list)
        self.kept_files = []
        self.removed_files = []
        self.space_saved = 0
        
    def get_image_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of image file"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"Error hashing {filepath}: {e}")
            return ""
    
    def analyze_duplicates(self):
        """Find duplicate images by content hash"""
        print("🔍 Analyzing images for duplicates...")
        
        if not self.images_dir.exists():
            print(f"❌ Images directory not found: {self.images_dir}")
            return
        
        hash_to_files = defaultdict(list)
        
        # Scan all image files
        for img_file in self.images_dir.glob("*.jpg"):
            file_hash = self.get_image_hash(img_file)
            if file_hash:
                hash_to_files[file_hash].append(img_file)
        
        # Find duplicate groups
        for file_hash, files in hash_to_files.items():
            if len(files) > 1:
                self.duplicate_groups[file_hash] = files
                print(f"📋 Found {len(files)} duplicates: {[f.name for f in files]}")
        
        print(f"\n📊 Analysis complete:")
        print(f"   • Total duplicate groups: {len(self.duplicate_groups)}")
        total_duplicates = sum(len(files) - 1 for files in self.duplicate_groups.values())
        print(f"   • Total duplicate files: {total_duplicates}")
        
        return len(self.duplicate_groups) > 0
    
    def select_best_file(self, files: list) -> Path:
        """Select the best file to keep from duplicates"""
        
        def score_file(filepath: Path) -> int:
            """Score file based on naming and quality preferences"""
            score = 0
            name = filepath.stem.lower()
            
            # Prefer files from newer APIs (pexels/pixabay over placeholder)
            if 'pexels' in name or 'pixabay' in name:
                score += 10
            elif 'placeholder' in name:
                score -= 5
            
            # Prefer featured images over thumbnails
            if 'featured' in name:
                score += 5
            elif 'thumbnail' in name:
                score -= 2
            elif 'icon' in name:
                score -= 3
            
            # Prefer original over processed
            if 'webp' in str(filepath):
                score -= 1  # JPEG is better for compatibility
            
            # File size consideration (larger usually better quality)
            try:
                size = filepath.stat().st_size
                score += min(size // 10000, 5)  # Up to 5 points for size
            except:
                pass
            
            return score
        
        # Score all files and select the best one
        scored_files = [(f, score_file(f)) for f in files]
        scored_files.sort(key=lambda x: x[1], reverse=True)
        
        best_file = scored_files[0][0]
        print(f"   ✅ Keeping: {best_file.name} (score: {scored_files[0][1]})")
        
        return best_file
    
    def remove_old_versions(self):
        """Remove old placeholder and redundant files"""
        print("🧹 Removing old placeholder files...")
        
        removed_count = 0
        
        for img_file in self.images_dir.glob("*.jpg"):
            name = img_file.stem.lower()
            
            # Remove obvious old files
            should_remove = False
            reason = ""
            
            # Remove old placeholders that have real API images
            if 'placeholder' in name:
                tool_name = name.split('-')[0]
                # Check if we have a real API image for this tool
                api_files = list(self.images_dir.glob(f"{tool_name}-pexels-*.jpg")) + \
                           list(self.images_dir.glob(f"{tool_name}-pixabay-*.jpg")) + \
                           list(self.images_dir.glob(f"{tool_name}-unsplash-*.jpg"))
                
                if api_files:
                    should_remove = True
                    reason = f"has real API image: {api_files[0].name}"
            
            # Remove very small files (likely corrupted or low quality)
            if img_file.stat().st_size < 5000:  # Less than 5KB
                should_remove = True
                reason = f"file too small ({img_file.stat().st_size} bytes)"
            
            if should_remove:
                print(f"   🗑️  Removing {img_file.name}: {reason}")
                self.space_saved += img_file.stat().st_size
                self.removed_files.append(img_file.name)
                img_file.unlink()
                removed_count += 1
        
        print(f"✅ Removed {removed_count} old/redundant files")
    
    def clean_duplicates(self, dry_run=False):
        """Remove duplicate files, keeping the best version"""
        print(f"\n🧹 {'[DRY RUN] ' if dry_run else ''}Cleaning duplicate files...")
        
        for file_hash, files in self.duplicate_groups.items():
            print(f"\n📋 Processing duplicate group ({len(files)} files):")
            
            # Select best file to keep
            best_file = self.select_best_file(files)
            self.kept_files.append(best_file.name)
            
            # Remove other files
            for file in files:
                if file != best_file:
                    size = file.stat().st_size
                    self.space_saved += size
                    self.removed_files.append(file.name)
                    
                    print(f"   🗑️  {'[DRY RUN] ' if dry_run else ''}Removing: {file.name} ({size} bytes)")
                    
                    if not dry_run:
                        file.unlink()
    
    def generate_report(self) -> dict:
        """Generate cleanup report"""
        report = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "duplicate_groups_found": len(self.duplicate_groups),
            "files_removed": len(self.removed_files),
            "files_kept": len(self.kept_files),
            "space_saved_bytes": self.space_saved,
            "space_saved_mb": round(self.space_saved / (1024 * 1024), 2),
            "removed_files": self.removed_files,
            "kept_files": self.kept_files
        }
        
        return report
    
    def optimize_remaining_images(self):
        """Optimize remaining images for web performance"""
        print("\n🚀 Optimizing remaining images...")
        
        optimized_count = 0
        for img_file in self.images_dir.glob("*.jpg"):
            try:
                # Check if image needs optimization
                original_size = img_file.stat().st_size
                
                if original_size > 500000:  # > 500KB
                    # Open and optimize
                    with Image.open(img_file) as img:
                        # Convert to RGB if necessary
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                        
                        # Resize if too large
                        if img.width > 1200 or img.height > 800:
                            img.thumbnail((1200, 800), Image.Resampling.LANCZOS)
                        
                        # Save with optimization
                        img.save(img_file, format='JPEG', quality=85, optimize=True)
                        
                        new_size = img_file.stat().st_size
                        saved = original_size - new_size
                        
                        if saved > 0:
                            print(f"   ⚡ Optimized {img_file.name}: {saved} bytes saved")
                            self.space_saved += saved
                            optimized_count += 1
                            
            except Exception as e:
                print(f"   ❌ Failed to optimize {img_file.name}: {e}")
        
        print(f"✅ Optimized {optimized_count} images")
    
    def run_full_cleanup(self, dry_run=False):
        """Run complete cleanup process"""
        print("🎯 AI Discovery Image Cleanup Starting...")
        print("=" * 50)
        
        # Step 1: Analyze duplicates
        has_duplicates = self.analyze_duplicates()
        
        # Step 2: Remove old versions
        if not dry_run:
            self.remove_old_versions()
        
        # Step 3: Clean duplicates
        if has_duplicates:
            self.clean_duplicates(dry_run)
        else:
            print("✅ No duplicates found!")
        
        # Step 4: Optimize images
        if not dry_run:
            self.optimize_remaining_images()
        
        # Generate report
        report = self.generate_report()
        
        print("\n" + "=" * 50)
        print("📊 CLEANUP COMPLETE")
        print("=" * 50)
        print(f"📁 Duplicate groups: {report['duplicate_groups_found']}")
        print(f"🗑️  Files removed: {report['files_removed']}")
        print(f"✅ Files kept: {report['files_kept']}")
        print(f"💾 Space saved: {report['space_saved_mb']} MB")
        
        # Save detailed report
        report_file = Path("image_cleanup_report.json")
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"📋 Detailed report saved: {report_file}")
        
        return report


def main():
    """Command line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clean up duplicate images")
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--images-dir', default='static/images/tools', help='Images directory path')
    
    args = parser.parse_args()
    
    cleaner = ImageDuplicateCleaner(args.images_dir)
    report = cleaner.run_full_cleanup(dry_run=args.dry_run)
    
    if args.dry_run:
        print("\n🔍 This was a dry run. Use --dry-run=false to actually clean files.")


if __name__ == "__main__":
    main()