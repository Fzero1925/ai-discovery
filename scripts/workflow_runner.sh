#!/bin/bash

# =============================================================================
# AI Discovery Workflow Runner
# 完全分离式架构，避免YAML语法问题
# =============================================================================

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
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

# 步骤1: 多源关键词分析
run_keyword_analysis() {
    log_info "Starting multi-source keyword analysis..."
    
    if python scripts/multi_source_keywords.py; then
        log_success "Multi-source keyword analysis completed"
        return 0
    else
        log_warning "Multi-source analysis failed, falling back to basic system"
        if python scripts/generate_keywords.py; then
            log_success "Fallback keyword analysis completed"
            return 0
        else
            log_warning "Fallback failed, using test system"
            python scripts/test_system.py
            return 1
        fi
    fi
}

# 步骤2: 内容生成
run_content_generation() {
    log_info "Starting content generation with hot topics support..."
    
    if python scripts/generate_content.py; then
        log_success "Content generation completed"
        return 0
    else
        log_warning "Content generation completed with existing data"
        return 1
    fi
}

# 步骤3: 性能优化
run_performance_optimization() {
    log_info "Running performance optimizations..."
    
    # 图片优化
    if python scripts/performance_optimizer.py --images-only; then
        log_success "Image optimization completed"
    else
        log_warning "Image optimization skipped"
    fi
    
    # 缓存优化
    if [ ! -f "scripts/optimized-build.sh" ]; then
        if python scripts/performance_optimizer.py --cache-only; then
            log_success "Cache optimization completed"
        else
            log_warning "Cache optimization skipped"
        fi
    fi
}

# 步骤4: SEO优化
run_seo_optimization() {
    log_info "Running SEO optimizations..."
    
    # 结构化数据优化
    if python scripts/seo_enhancer.py --structured-data-only; then
        log_success "Structured data optimization completed"
    else
        log_warning "Structured data optimization skipped"
    fi
    
    # 面包屑优化
    if python scripts/seo_enhancer.py --breadcrumbs-only; then
        log_success "Breadcrumbs optimization completed"
    else
        log_warning "Breadcrumbs optimization skipped"
    fi
    
    # 内链优化（仅对新内容）
    if [ -f "generated_files.txt" ] && [ -s "generated_files.txt" ]; then
        log_info "Optimizing internal links for new content..."
        if python scripts/seo_enhancer.py --internal-links-only; then
            log_success "Internal linking optimization completed"
        else
            log_warning "Internal linking optimization skipped"
        fi
    fi
}

# 步骤5: 构建站点
run_hugo_build() {
    log_info "Building Hugo site with performance optimizations..."
    
    # 显示Google Analytics配置（脱敏）
    if [ -n "$HUGO_PARAMS_GOOGLE_ANALYTICS_ID" ]; then
        ga_id_preview="${HUGO_PARAMS_GOOGLE_ANALYTICS_ID:0:8}***"
        log_info "Google Analytics ID: $ga_id_preview"
    fi
    
    # 使用优化构建脚本
    if [ -f "scripts/optimized-build.sh" ] && [ "$(uname)" != "MINGW"* ]; then
        log_info "Using optimized build script..."
        chmod +x scripts/optimized-build.sh
        bash scripts/optimized-build.sh
    else
        log_info "Using standard build process..."
        hugo --minify --gc --environment production
    fi
    
    # 检查构建结果
    if [ -d "public" ]; then
        log_success "Hugo build successful"
        
        # 性能指标
        html_count=$(find public -name "*.html" | wc -l)
        css_count=$(find public -name "*.css" | wc -l)
        js_count=$(find public -name "*.js" | wc -l)
        img_count=$(find public -name "*.jpg" -o -name "*.png" -o -name "*.webp" | wc -l)
        total_size=$(du -sh public 2>/dev/null | cut -f1 || echo "N/A")
        
        log_info "Performance metrics:"
        echo "  HTML files: $html_count"
        echo "  CSS files: $css_count"
        echo "  JS files: $js_count"
        echo "  Image files: $img_count"
        echo "  Total size: $total_size"
        
        return 0
    else
        log_error "Hugo build failed"
        return 1
    fi
}

# 步骤6: 提交新内容
commit_new_content() {
    log_info "Committing generated content..."
    
    # 配置Git用户
    git config --local user.email "action@github.com"
    git config --local user.name "AI Discovery Bot"
    
    # 添加生成的文件
    if [ -f "generated_files.txt" ] && [ -s "generated_files.txt" ]; then
        while IFS= read -r file; do
            if [ -f "$file" ]; then
                git add "$file"
                log_info "Added: $file"
            fi
        done < generated_files.txt
        
        # 添加数据文件
        git add data/ 2>/dev/null || true
        
        # 检查是否有变更需要提交
        if git diff --staged --quiet; then
            log_warning "No new content to commit"
            return 0
        else
            commit_date=$(date +'%Y-%m-%d %H:%M UTC')
            commit_message="Auto-generate AI tool reviews - $commit_date

Generated by AI Discovery automation system

Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
            
            git commit -m "$commit_message"
            git push
            log_success "Content committed and pushed"
            return 0
        fi
    else
        log_warning "No content generated, skipping commit"
        return 0
    fi
}

# 步骤7: 发送智能通知
send_notification() {
    log_info "Sending enhanced notification..."
    
    if python scripts/send_notification.py; then
        log_success "Enhanced notification sent successfully"
        return 0
    else
        log_error "Notification failed"
        return 1
    fi
}

# 步骤8: 性能报告
generate_performance_report() {
    log_info "Generating performance report..."
    
    echo "Build Performance Report"
    echo "=========================="
    echo "Hugo version: $(hugo version 2>/dev/null || echo 'N/A')"
    echo "Build time: $(date)"
    
    if [ -d "public" ]; then
        page_count=$(find public -name "*.html" | wc -l)
        total_size=$(du -sh public 2>/dev/null | cut -f1 || echo "N/A")
        echo "Generated pages: $page_count"
        echo "Total size: $total_size"
    else
        echo "Generated pages: N/A"
        echo "Total size: N/A"
    fi
    
    echo "=========================="
}

# 步骤9: 清理工作
cleanup() {
    log_info "Running cleanup..."
    
    # 清理临时文件
    rm -f daily_keywords.json generated_files.txt notification_data.json enhanced_notification_data.json
    rm -f multi_source_trends.json trending_topics.json
    
    log_success "Advanced cleanup completed"
}

# 步骤0: 预构建验证
run_pre_build_validation() {
    log_info "Running pre-build validation checks..."
    
    if [ -f "scripts/pre-build-validator.sh" ]; then
        chmod +x scripts/pre-build-validator.sh
        if bash scripts/pre-build-validator.sh; then
            log_success "Pre-build validation passed"
            return 0
        else
            log_warning "Pre-build validation found issues - attempting to continue with fixes"
            return 1
        fi
    else
        log_warning "Pre-build validator not found, skipping validation"
        return 0
    fi
}

# 主执行函数
main() {
    log_info "Starting AI Discovery workflow with enhanced validation..."
    
    # 记录开始时间
    start_time=$(date +%s)
    
    # 执行预构建验证
    run_pre_build_validation
    
    # 执行步骤
    run_keyword_analysis
    run_content_generation
    run_performance_optimization
    run_seo_optimization
    
    if run_hugo_build; then
        commit_new_content
        send_notification
        generate_performance_report
    else
        log_error "Workflow failed at Hugo build step"
        cleanup
        exit 1
    fi
    
    # 清理工作
    cleanup
    
    # 计算执行时间
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    
    log_success "Workflow completed successfully in ${duration}s"
}

# 错误处理
trap 'log_error "Workflow interrupted"; cleanup; exit 1' INT TERM

# 执行主函数
main "$@"