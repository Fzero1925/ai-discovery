#!/bin/bash

# =============================================================================
# AI Discovery Pre-Build Validator
# 构建前系统验证脚本 - 预防语法错误和资源缺失
# =============================================================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[VALIDATOR]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_check() {
    echo -e "${CYAN}[CHECK]${NC} $1"
}

# 全局变量
VALIDATION_ERRORS=0
VALIDATION_WARNINGS=0
VALIDATION_FIXES=0

# 1. YAML语法验证
validate_yaml_syntax() {
    log_check "Validating YAML syntax in content files..."
    
    local yaml_errors=0
    local yaml_files=0
    
    # 检查所有markdown文件的front matter
    while IFS= read -r -d '' file; do
        yaml_files=$((yaml_files + 1))
        
        # 使用Python验证YAML语法
        if python -c "
import yaml
import sys

try:
    with open('$file', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取front matter
    parts = content.split('---')
    if len(parts) >= 3:
        front_matter = parts[1]
        try:
            yaml.safe_load(front_matter)
            print('YAML_OK')
        except yaml.YAMLError as e:
            print(f'YAML_ERROR: {e}')
            sys.exit(1)
    else:
        print('NO_FRONTMATTER')
except Exception as e:
    print(f'FILE_ERROR: {e}')
    sys.exit(1)
" 2>/dev/null | grep -q "YAML_ERROR"; then
            log_error "YAML syntax error in: $file"
            yaml_errors=$((yaml_errors + 1))
            VALIDATION_ERRORS=$((VALIDATION_ERRORS + 1))
        fi
        
    done < <(find content -name "*.md" -print0 2>/dev/null)
    
    if [ $yaml_errors -eq 0 ]; then
        log_success "YAML syntax validation passed ($yaml_files files checked)"
    else
        log_error "Found $yaml_errors YAML syntax errors in $yaml_files files"
    fi
}

# 2. Hugo模板语法验证
validate_hugo_templates() {
    log_check "Validating Hugo template syntax..."
    
    # 使用Hugo dry-run检查模板语法
    if hugo --renderToMemory --logLevel info --quiet 2>/dev/null; then
        log_success "Hugo template syntax validation passed"
    else
        log_error "Hugo template syntax errors detected"
        VALIDATION_ERRORS=$((VALIDATION_ERRORS + 1))
        
        # 尝试获取详细错误信息
        log_info "Detailed Hugo validation output:"
        hugo --renderToMemory --logLevel debug 2>&1 | head -20 || true
    fi
}

# 3. 关键资源存在性检查
validate_critical_resources() {
    log_check "Checking critical resource availability..."
    
    local missing_resources=0
    
    # 检查关键目录
    local critical_dirs=("content" "layouts" "static" "data")
    for dir in "${critical_dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            log_warning "Critical directory missing: $dir"
            missing_resources=$((missing_resources + 1))
            VALIDATION_WARNINGS=$((VALIDATION_WARNINGS + 1))
        fi
    done
    
    # 检查关键配置文件
    local critical_files=("config.toml" "requirements.txt")
    for file in "${critical_files[@]}"; do
        if [ ! -f "$file" ]; then
            log_warning "Critical file missing: $file"
            missing_resources=$((missing_resources + 1))
            VALIDATION_WARNINGS=$((VALIDATION_WARNINGS + 1))
        fi
    done
    
    # 检查Hugo可执行性
    if ! command -v hugo >/dev/null 2>&1; then
        log_error "Hugo binary not found or not executable"
        VALIDATION_ERRORS=$((VALIDATION_ERRORS + 1))
    else
        local hugo_version=$(hugo version 2>/dev/null || echo "unknown")
        log_success "Hugo available: $hugo_version"
    fi
    
    if [ $missing_resources -eq 0 ]; then
        log_success "All critical resources available"
    fi
}

# 4. 内容质量快速检查
validate_content_quality() {
    log_check "Running content quality checks..."
    
    local quality_issues=0
    
    # 检查是否有空文件
    while IFS= read -r -d '' file; do
        if [ ! -s "$file" ]; then
            log_warning "Empty content file detected: $file"
            quality_issues=$((quality_issues + 1))
            VALIDATION_WARNINGS=$((VALIDATION_WARNINGS + 1))
        fi
    done < <(find content -name "*.md" -print0 2>/dev/null)
    
    # 检查是否有过短的文章
    while IFS= read -r -d '' file; do
        if [ -f "$file" ]; then
            local word_count=$(wc -w < "$file" 2>/dev/null || echo 0)
            if [ "$word_count" -lt 500 ]; then
                log_warning "Short content detected: $file ($word_count words)"
                quality_issues=$((quality_issues + 1))
                VALIDATION_WARNINGS=$((VALIDATION_WARNINGS + 1))
            fi
        fi
    done < <(find content -name "*.md" -print0 2>/dev/null)
    
    if [ $quality_issues -eq 0 ]; then
        log_success "Content quality checks passed"
    fi
}

# 5. YAML语法自动修复
auto_fix_yaml_quotes() {
    log_check "Attempting automatic YAML fixes..."
    
    local fixed_files=0
    
    # 创建Python修复脚本
    python -c "
import os
import re
from pathlib import Path

def fix_yaml_quotes(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取front matter
        parts = content.split('---')
        if len(parts) >= 3:
            front_matter = parts[1]
            
            # 修复撇号问题：单引号包围含撇号的字符串改为双引号
            fixed_front_matter = re.sub(
                r\"title: '([^']*'[^']*)'\",'title: \"\1\"',
                front_matter
            )
            
            # 修复其他可能的引号问题
            fixed_front_matter = re.sub(
                r\"description: '([^']*'[^']*)'\",'description: \"\1\"',
                fixed_front_matter
            )
            
            if fixed_front_matter != front_matter:
                # 重新组装文件
                new_content = '---' + fixed_front_matter + '---' + '---'.join(parts[2:])
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f'FIXED: {file_path}')
                return True
        
        return False
    except Exception as e:
        print(f'ERROR fixing {file_path}: {e}')
        return False

# 处理所有markdown文件
content_dir = Path('content')
fixed_count = 0

if content_dir.exists():
    for md_file in content_dir.rglob('*.md'):
        if fix_yaml_quotes(md_file):
            fixed_count += 1

print(f'FIXED_COUNT: {fixed_count}')
" | grep -E "(FIXED:|FIXED_COUNT:)" | while read line; do
        if [[ "$line" =~ FIXED_COUNT:\ ([0-9]+) ]]; then
            fixed_files="${BASH_REMATCH[1]}"
        elif [[ "$line" =~ FIXED:\ (.+) ]]; then
            log_success "Auto-fixed YAML in: ${BASH_REMATCH[1]}"
        fi
    done
    
    if [ "$fixed_files" -gt 0 ]; then
        log_success "Automatically fixed $fixed_files YAML files"
        VALIDATION_FIXES=$((VALIDATION_FIXES + fixed_files))
    fi
}

# 6. 生成验证报告
generate_validation_report() {
    log_info "Generating validation report..."
    
    echo ""
    echo "=================================="
    echo "Pre-Build Validation Report"
    echo "=================================="
    echo "Timestamp: $(date)"
    echo "Git commit: $(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
    echo ""
    echo "Results:"
    echo "  Errors: $VALIDATION_ERRORS"
    echo "  Warnings: $VALIDATION_WARNINGS"
    echo "  Auto-fixes applied: $VALIDATION_FIXES"
    echo ""
    
    if [ $VALIDATION_ERRORS -eq 0 ]; then
        echo "✅ Validation Status: PASSED"
        echo "🚀 Ready for Hugo build"
    else
        echo "❌ Validation Status: FAILED"
        echo "🛑 Build should be stopped"
    fi
    
    echo "=================================="
}

# 主函数
main() {
    log_info "Starting pre-build validation..."
    echo "=================================="
    
    # 记录开始时间
    start_time=$(date +%s)
    
    # 执行所有验证步骤
    validate_critical_resources
    validate_yaml_syntax
    validate_hugo_templates  
    validate_content_quality
    auto_fix_yaml_quotes
    
    # 生成报告
    generate_validation_report
    
    # 计算执行时间
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    
    log_info "Validation completed in ${duration}s"
    
    # 根据错误数量确定退出状态
    if [ $VALIDATION_ERRORS -gt 0 ]; then
        log_error "Validation failed with $VALIDATION_ERRORS errors"
        exit 1
    else
        log_success "Pre-build validation passed successfully"
        exit 0
    fi
}

# 信号处理
trap 'log_error "Validation interrupted"; exit 1' INT TERM

# 执行主函数
main "$@"