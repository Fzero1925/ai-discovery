/**
 * AI Discovery Performance Optimization Suite
 * 
 * Advanced performance monitoring and optimization for better Core Web Vitals
 * and enhanced user experience.
 */

class PerformanceOptimizer {
    constructor() {
        this.metrics = {
            lcp: null,
            fid: null,
            cls: null,
            fcp: null,
            ttfb: null
        };
        
        this.thresholds = {
            lcp: { good: 2500, poor: 4000 },
            fid: { good: 100, poor: 300 },
            cls: { good: 0.1, poor: 0.25 },
            fcp: { good: 1800, poor: 3000 },
            ttfb: { good: 600, poor: 1500 }
        };
        
        this.init();
    }
    
    init() {
        // Wait for page to be interactive
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.startMonitoring());
        } else {
            this.startMonitoring();
        }
    }
    
    startMonitoring() {
        console.log('🚀 Performance monitoring started');
        
        this.measureCoreWebVitals();
        this.optimizeResourceLoading();
        this.setupIntersectionObservers();
        this.optimizeFonts();
        this.detectSlowConnections();
        this.monitorJavaScriptPerformance();
        
        // Report after 5 seconds
        setTimeout(() => this.generatePerformanceReport(), 5000);
    }
    
    measureCoreWebVitals() {
        // Use Web Vitals library if available, otherwise implement basic versions
        if (typeof webVitals !== 'undefined') {
            webVitals.getLCP(this.onLCP.bind(this));
            webVitals.getFID(this.onFID.bind(this));
            webVitals.getCLS(this.onCLS.bind(this));
            webVitals.getFCP(this.onFCP.bind(this));
            webVitals.getTTFB(this.onTTFB.bind(this));
        } else {
            this.measureCoreWebVitalsBasic();
        }
    }
    
    measureCoreWebVitalsBasic() {
        // Basic LCP measurement
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                this.onLCP({ value: lastEntry.startTime });
            });
            observer.observe({ entryTypes: ['largest-contentful-paint'] });
        }
        
        // Basic FCP measurement
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                if (entries.length > 0) {
                    this.onFCP({ value: entries[0].startTime });
                }
                observer.disconnect();
            });
            observer.observe({ entryTypes: ['paint'] });
        }
        
        // TTFB from Navigation Timing
        if ('performance' in window && 'timing' in performance) {
            const ttfb = performance.timing.responseStart - performance.timing.requestStart;
            this.onTTFB({ value: ttfb });
        }
    }
    
    onLCP(metric) {
        this.metrics.lcp = metric.value;
        this.logMetric('LCP (Largest Contentful Paint)', metric.value, 'ms', this.thresholds.lcp);
        this.trackAnalyticsMetric('lcp', metric.value);
    }
    
    onFID(metric) {
        this.metrics.fid = metric.value;
        this.logMetric('FID (First Input Delay)', metric.value, 'ms', this.thresholds.fid);
        this.trackAnalyticsMetric('fid', metric.value);
    }
    
    onCLS(metric) {
        this.metrics.cls = metric.value;
        this.logMetric('CLS (Cumulative Layout Shift)', metric.value, '', this.thresholds.cls);
        this.trackAnalyticsMetric('cls', metric.value * 1000); // Convert for GA
    }
    
    onFCP(metric) {
        this.metrics.fcp = metric.value;
        this.logMetric('FCP (First Contentful Paint)', metric.value, 'ms', this.thresholds.fcp);
        this.trackAnalyticsMetric('fcp', metric.value);
    }
    
    onTTFB(metric) {
        this.metrics.ttfb = metric.value;
        this.logMetric('TTFB (Time To First Byte)', metric.value, 'ms', this.thresholds.ttfb);
        this.trackAnalyticsMetric('ttfb', metric.value);
    }
    
    logMetric(name, value, unit, threshold) {
        const status = value < threshold.good ? '✅ Good' : 
                      value < threshold.poor ? '⚠️ Needs Improvement' : '❌ Poor';
        
        console.log(`📊 ${name}: ${Math.round(value)}${unit} (${status})`);
    }
    
    trackAnalyticsMetric(metricName, value) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'web_vitals', {
                event_category: 'Performance',
                event_label: metricName.toUpperCase(),
                value: Math.round(value),
                custom_map: {
                    [metricName]: Math.round(value)
                }
            });
        }
    }
    
    optimizeResourceLoading() {
        // Prefetch important pages
        this.prefetchImportantPages();
        
        // Optimize third-party scripts
        this.optimizeThirdPartyScripts();
        
        // Enable resource hints
        this.addResourceHints();
        
        // Optimize CSS delivery
        this.optimizeCSSDelivery();
    }
    
    prefetchImportantPages() {
        const importantPages = [
            '/categories/content-creation/',
            '/categories/image-generation/',
            '/categories/code-assistance/',
            '/categories/productivity/'
        ];
        
        // Only prefetch on good connections
        if (this.isGoodConnection()) {
            importantPages.forEach(page => {
                const link = document.createElement('link');
                link.rel = 'prefetch';
                link.href = page;
                document.head.appendChild(link);
            });
            
            console.log('🔗 Prefetched important category pages');
        }
    }
    
    optimizeThirdPartyScripts() {
        // Delay non-critical third-party scripts
        const thirdPartyScripts = document.querySelectorAll('script[src*="googleapis.com"], script[src*="googletagmanager.com"]');
        
        thirdPartyScripts.forEach(script => {
            if (!script.hasAttribute('async') && !script.hasAttribute('defer')) {
                script.async = true;
            }
        });
        
        console.log(`⚡ Optimized ${thirdPartyScripts.length} third-party scripts`);
    }
    
    addResourceHints() {
        const hints = [
            { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
            { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: true },
            { rel: 'preconnect', href: 'https://www.googletagmanager.com' },
            { rel: 'dns-prefetch', href: 'https://api.unsplash.com' },
            { rel: 'dns-prefetch', href: 'https://api.pexels.com' },
            { rel: 'dns-prefetch', href: 'https://pixabay.com' }
        ];
        
        hints.forEach(hint => {
            if (!document.querySelector(`link[href="${hint.href}"]`)) {
                const link = document.createElement('link');
                link.rel = hint.rel;
                link.href = hint.href;
                if (hint.crossorigin) link.crossOrigin = 'anonymous';
                document.head.appendChild(link);
            }
        });
        
        console.log('🔗 Added resource hints for better connection performance');
    }
    
    optimizeCSSDelivery() {
        // Identify critical CSS (above-the-fold content)
        const criticalSelectors = [
            '.site-header', '.navbar', '.article-header', 
            '.article-title', '.article-meta', '.article-image'
        ];
        
        // Mark non-critical CSS for later loading
        const stylesheets = document.querySelectorAll('link[rel="stylesheet"]');
        stylesheets.forEach(link => {
            if (link.href.includes('non-critical') || link.media === 'print') {
                link.media = 'print';
                link.onload = () => link.media = 'all';
            }
        });
    }
    
    setupIntersectionObservers() {
        // Optimize heavy content sections
        const heavySections = document.querySelectorAll('.internal-links-section, .related-tools, .comparison-tools');
        
        if (heavySections.length > 0 && 'IntersectionObserver' in window) {
            const sectionObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.optimizeSectionContent(entry.target);
                        sectionObserver.unobserve(entry.target);
                    }
                });
            }, {
                rootMargin: '50px 0px'
            });
            
            heavySections.forEach(section => sectionObserver.observe(section));
        }
    }
    
    optimizeSectionContent(section) {
        // Lazy load section-specific content
        const images = section.querySelectorAll('img[data-src]');
        images.forEach(img => {
            if (img.dataset.src) {
                img.src = img.dataset.src;
                delete img.dataset.src;
            }
        });
        
        console.log(`🖼️ Optimized content for section: ${section.className}`);
    }
    
    optimizeFonts() {
        // Ensure fonts are loaded efficiently
        if ('fonts' in document) {
            // Preload critical fonts
            const criticalFonts = ['Inter-400', 'Inter-500', 'Inter-600'];
            
            criticalFonts.forEach(font => {
                document.fonts.load(`1em ${font.replace('-', ' ')}`);
            });
            
            document.fonts.ready.then(() => {
                console.log('✅ Critical fonts loaded');
            });
        }
        
        // Add font-display: swap to existing font links
        const fontLinks = document.querySelectorAll('link[href*="fonts.googleapis.com"]');
        fontLinks.forEach(link => {
            if (!link.href.includes('display=swap')) {
                link.href += link.href.includes('?') ? '&display=swap' : '?display=swap';
            }
        });
    }
    
    detectSlowConnections() {
        if ('connection' in navigator) {
            const connection = navigator.connection;
            const isSlowConnection = connection.effectiveType === 'slow-2g' || 
                                   connection.effectiveType === '2g' || 
                                   connection.downlink < 1;
            
            if (isSlowConnection) {
                document.documentElement.classList.add('slow-connection');
                this.enableSlowConnectionOptimizations();
                console.log('🐌 Slow connection detected: Enabling optimizations');
            }
        }
    }
    
    enableSlowConnectionOptimizations() {
        // Disable auto-playing content
        const videos = document.querySelectorAll('video[autoplay]');
        videos.forEach(video => {
            video.removeAttribute('autoplay');
            video.preload = 'none';
        });
        
        // Reduce image quality
        const images = document.querySelectorAll('img[data-src-low]');
        images.forEach(img => {
            if (img.dataset.srcLow) {
                img.dataset.src = img.dataset.srcLow;
            }
        });
        
        // Defer non-essential scripts
        const nonEssentialScripts = document.querySelectorAll('script[data-defer-slow]');
        nonEssentialScripts.forEach(script => {
            script.defer = true;
        });
    }
    
    isGoodConnection() {
        if ('connection' in navigator) {
            const connection = navigator.connection;
            return connection.effectiveType === '4g' && connection.downlink > 2;
        }
        return true; // Assume good connection if we can't detect
    }
    
    monitorJavaScriptPerformance() {
        // Monitor long tasks
        if ('PerformanceObserver' in window) {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    if (entry.duration > 50) {
                        console.warn(`⚠️ Long task detected: ${Math.round(entry.duration)}ms`);
                        
                        if (typeof gtag !== 'undefined') {
                            gtag('event', 'long_task', {
                                event_category: 'Performance',
                                value: Math.round(entry.duration)
                            });
                        }
                    }
                });
            });
            
            try {
                observer.observe({ entryTypes: ['longtask'] });
            } catch (e) {
                console.log('Long task monitoring not supported');
            }
        }
        
        // Monitor memory usage
        if ('memory' in performance) {
            const checkMemory = () => {
                const memory = performance.memory;
                const memoryUsage = memory.usedJSHeapSize / memory.totalJSHeapSize;
                
                if (memoryUsage > 0.8) {
                    console.warn('⚠️ High memory usage detected:', Math.round(memoryUsage * 100) + '%');
                }
            };
            
            setTimeout(checkMemory, 10000); // Check after 10 seconds
        }
    }
    
    generatePerformanceReport() {
        const report = {
            timestamp: new Date().toISOString(),
            metrics: this.metrics,
            grades: {},
            recommendations: []
        };
        
        // Grade each metric
        Object.keys(this.metrics).forEach(metricName => {
            const value = this.metrics[metricName];
            if (value !== null) {
                const threshold = this.thresholds[metricName];
                if (value < threshold.good) {
                    report.grades[metricName] = 'good';
                } else if (value < threshold.poor) {
                    report.grades[metricName] = 'needs-improvement';
                } else {
                    report.grades[metricName] = 'poor';
                }
            }
        });
        
        // Generate recommendations
        this.generateRecommendations(report);
        
        console.log('📊 Performance Report:', report);
        
        // Send to analytics
        this.sendPerformanceReport(report);
        
        return report;
    }
    
    generateRecommendations(report) {
        if (report.grades.lcp === 'poor') {
            report.recommendations.push('Optimize largest contentful paint by compressing images and improving server response time');
        }
        
        if (report.grades.cls === 'poor') {
            report.recommendations.push('Reduce layout shifts by setting explicit dimensions for images and ads');
        }
        
        if (report.grades.fid === 'poor') {
            report.recommendations.push('Improve first input delay by reducing JavaScript execution time');
        }
        
        if (report.grades.ttfb === 'poor') {
            report.recommendations.push('Improve server response time by optimizing backend performance');
        }
    }
    
    sendPerformanceReport(report) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'performance_report', {
                event_category: 'Performance',
                event_label: 'Core Web Vitals Report',
                custom_map: {
                    'lcp_grade': report.grades.lcp || 'unknown',
                    'fid_grade': report.grades.fid || 'unknown',
                    'cls_grade': report.grades.cls || 'unknown'
                }
            });
        }
    }
    
    // Public method to get current performance state
    getPerformanceState() {
        return {
            metrics: this.metrics,
            timestamp: Date.now()
        };
    }
}

// Initialize performance optimization
const performanceOptimizer = new PerformanceOptimizer();

// Make it globally accessible
window.PerformanceOptimizer = performanceOptimizer;

// Export performance state for debugging
window.getPerformanceState = () => performanceOptimizer.getPerformanceState();

console.log('⚡ AI Discovery Performance Optimizer initialized');