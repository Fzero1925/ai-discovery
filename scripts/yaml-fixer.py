#!/usr/bin/env python3
"""
YAML Syntax Auto-Fixer for AI Discovery
自动修复Markdown文件中的YAML front matter语法问题
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import List, Tuple, Dict

class YAMLFixer:
    def __init__(self):
        self.fixed_files: List[str] = []
        self.error_files: List[str] = []
        self.total_fixes = 0
        
    def fix_quote_issues(self, front_matter: str) -> Tuple[str, int]:
        """修复引号相关的YAML问题"""
        fixes_count = 0
        fixed_yaml = front_matter
        
        # 1. 修复单引号内包含撇号的问题
        patterns = [
            # title字段修复
            (r"title:\s*'([^']*'[^']*)'", r'title: "\1"'),
            # description字段修复 
            (r"description:\s*'([^']*'[^']*)'", r'description: "\1"'),
            # 其他可能包含撇号的字段
            (r"alt_text:\s*'([^']*'[^']*)'", r'alt_text: "\1"'),
            (r"image_alt:\s*'([^']*'[^']*)'", r'image_alt: "\1"'),
        ]
        
        for pattern, replacement in patterns:
            new_yaml, count = re.subn(pattern, replacement, fixed_yaml)
            if count > 0:
                fixed_yaml = new_yaml
                fixes_count += count
                
        # 2. 修复嵌套引号问题
        # 将 "text "inner" text" 修复为 "text \"inner\" text"
        nested_quotes_pattern = r'"([^"]*)"([^"]*)"([^"]*)"'
        if re.search(nested_quotes_pattern, fixed_yaml):
            fixed_yaml = re.sub(nested_quotes_pattern, r'"\1\"\2\"\3"', fixed_yaml)
            fixes_count += 1
            
        return fixed_yaml, fixes_count
    
    def fix_structure_issues(self, front_matter: str) -> Tuple[str, int]:
        """修复YAML结构问题"""
        fixes_count = 0
        fixed_yaml = front_matter
        
        # 1. 确保title在前面
        lines = fixed_yaml.split('\n')
        title_line = None
        title_index = -1
        
        for i, line in enumerate(lines):
            if line.strip().startswith('title:'):
                title_line = line
                title_index = i
                break
        
        if title_line and title_index > 0:
            # 将title移到第一行
            lines.pop(title_index)
            lines.insert(0, title_line)
            fixed_yaml = '\n'.join(lines)
            fixes_count += 1
            
        # 2. 修复缩进问题
        lines = fixed_yaml.split('\n')
        for i, line in enumerate(lines):
            # 确保数组项正确缩进
            if re.match(r'^-\s+\w', line):
                lines[i] = '- ' + line.lstrip('- ')
                fixes_count += 1
                
        fixed_yaml = '\n'.join(lines)
        return fixed_yaml, fixes_count
    
    def validate_yaml(self, yaml_content: str) -> bool:
        """验证YAML语法是否正确"""
        try:
            yaml.safe_load(yaml_content)
            return True
        except yaml.YAMLError:
            return False
    
    def fix_file(self, file_path: Path) -> bool:
        """修复单个文件的YAML问题"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 提取front matter
            parts = content.split('---')
            if len(parts) < 3:
                return False  # 没有front matter
                
            front_matter = parts[1]
            
            # 检查是否需要修复
            if self.validate_yaml(front_matter):
                return True  # 已经是有效的YAML
                
            # 进行修复
            fixed_yaml = front_matter
            total_file_fixes = 0
            
            # 应用各种修复
            fixed_yaml, quote_fixes = self.fix_quote_issues(fixed_yaml)
            fixed_yaml, struct_fixes = self.fix_structure_issues(fixed_yaml)
            
            total_file_fixes = quote_fixes + struct_fixes
            
            # 验证修复结果
            if self.validate_yaml(fixed_yaml) and total_file_fixes > 0:
                # 重新组装文件内容
                new_content = '---' + fixed_yaml + '---' + '---'.join(parts[2:])
                
                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                    
                self.fixed_files.append(str(file_path))
                self.total_fixes += total_file_fixes
                
                print(f"Fixed {total_file_fixes} issues in: {file_path}")
                return True
            elif self.validate_yaml(fixed_yaml):
                print(f"No fixes needed for: {file_path}")
                return True
            else:
                self.error_files.append(str(file_path))
                print(f"Could not fix YAML in: {file_path}")
                return False
                
        except Exception as e:
            self.error_files.append(str(file_path))
            print(f"❌ Error processing {file_path}: {e}")
            return False
    
    def fix_all_files(self, content_dir: str = "content") -> Dict:
        """修复所有内容文件中的YAML问题"""
        content_path = Path(content_dir)
        
        if not content_path.exists():
            print(f"Content directory not found: {content_dir}")
            return {"success": False, "message": "Content directory not found"}
            
        # 查找所有markdown文件
        md_files = list(content_path.rglob("*.md"))
        
        if not md_files:
            print("No markdown files found")
            return {"success": True, "files_processed": 0}
            
        print(f"Processing {len(md_files)} markdown files...")
        
        # 处理每个文件
        success_count = 0
        for md_file in md_files:
            if self.fix_file(md_file):
                success_count += 1
                
        # 生成报告
        result = {
            "success": True,
            "files_processed": len(md_files),
            "files_fixed": len(self.fixed_files),
            "files_with_errors": len(self.error_files),
            "total_fixes_applied": self.total_fixes,
            "fixed_files": self.fixed_files,
            "error_files": self.error_files
        }
        
        # 输出摘要
        print("\n" + "="*50)
        print("YAML Fix Summary Report")
        print("="*50)
        print(f"Files processed: {result['files_processed']}")
        print(f"Files fixed: {result['files_fixed']}")
        print(f"Total fixes applied: {result['total_fixes_applied']}")
        print(f"Files with errors: {result['files_with_errors']}")
        
        if self.error_files:
            print("\nFiles that could not be fixed:")
            for file in self.error_files:
                print(f"  ERROR: {file}")
                
        print("="*50)
        
        return result

def main():
    """主函数"""
    # 解析命令行参数
    content_dir = sys.argv[1] if len(sys.argv) > 1 else "content"
    
    print("AI Discovery YAML Auto-Fixer")
    print("="*50)
    
    fixer = YAMLFixer()
    result = fixer.fix_all_files(content_dir)
    
    # 根据结果设置退出代码
    if result["success"] and result["files_with_errors"] == 0:
        print("All YAML fixes completed successfully!")
        sys.exit(0)
    elif result["success"] and result["files_with_errors"] > 0:
        print("Some files could not be fixed automatically")
        sys.exit(1)
    else:
        print("YAML fixing failed")
        sys.exit(1)

if __name__ == "__main__":
    main()