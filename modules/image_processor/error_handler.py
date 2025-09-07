"""
Enhanced Error Handler for Image Processing System
提供更强大的错误处理、重试机制和日志记录功能
"""

import time
import logging
import requests
from typing import Callable, Optional, Any, Dict
from functools import wraps

class ImageProcessingErrorHandler:
    """图片处理系统增强错误处理器"""
    
    def __init__(self, log_level=logging.INFO):
        self.logger = self._setup_logger(log_level)
        self.api_stats = {
            'unsplash': {'calls': 0, 'failures': 0, 'success_rate': 0},
            'pexels': {'calls': 0, 'failures': 0, 'success_rate': 0},
            'pixabay': {'calls': 0, 'failures': 0, 'success_rate': 0}
        }
    
    def _setup_logger(self, level) -> logging.Logger:
        """设置日志系统"""
        logger = logging.getLogger("ImageProcessing")
        logger.setLevel(level)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def with_retry(self, max_attempts: int = 3, delay_base: int = 2, 
                   exceptions: tuple = (requests.RequestException, ConnectionError)):
        """重试装饰器"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                last_exception = None
                
                for attempt in range(max_attempts):
                    try:
                        result = func(*args, **kwargs)
                        if attempt > 0:
                            self.logger.info(f"{func.__name__} succeeded on attempt {attempt + 1}")
                        return result
                        
                    except exceptions as e:
                        last_exception = e
                        wait_time = delay_base ** attempt
                        
                        self.logger.warning(
                            f"{func.__name__} failed on attempt {attempt + 1}/{max_attempts}: {e}"
                        )
                        
                        if attempt < max_attempts - 1:
                            self.logger.info(f"Retrying in {wait_time} seconds...")
                            time.sleep(wait_time)
                        else:
                            self.logger.error(f"{func.__name__} failed after {max_attempts} attempts")
                
                raise last_exception
            return wrapper
        return decorator
    
    def track_api_usage(self, api_name: str, success: bool = True):
        """追踪API使用统计"""
        if api_name in self.api_stats:
            self.api_stats[api_name]['calls'] += 1
            if not success:
                self.api_stats[api_name]['failures'] += 1
            
            # 计算成功率
            stats = self.api_stats[api_name]
            stats['success_rate'] = (
                (stats['calls'] - stats['failures']) / stats['calls'] * 100
                if stats['calls'] > 0 else 0
            )
    
    def get_api_statistics(self) -> Dict:
        """获取API使用统计"""
        return self.api_stats.copy()
    
    def log_performance_metrics(self, operation: str, duration: float, success: bool = True):
        """记录性能指标"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"[PERFORMANCE] {operation}: {duration:.2f}s - {status}")
    
    def assess_image_quality(self, image_path: str, min_width: int = 800, 
                           min_height: int = 600, min_size_kb: int = 50) -> Dict:
        """评估图片质量"""
        try:
            from PIL import Image
            import os
            
            with Image.open(image_path) as img:
                width, height = img.size
                file_size = os.path.getsize(image_path) / 1024  # KB
                
                quality_score = 0
                issues = []
                
                # 检查分辨率
                if width >= min_width and height >= min_height:
                    quality_score += 40
                else:
                    issues.append(f"Low resolution: {width}x{height}")
                
                # 检查文件大小
                if file_size >= min_size_kb:
                    quality_score += 30
                else:
                    issues.append(f"Small file size: {file_size:.1f}KB")
                
                # 检查纵横比
                aspect_ratio = width / height
                if 1.3 <= aspect_ratio <= 2.0:  # 适合横向布局
                    quality_score += 30
                else:
                    issues.append(f"Poor aspect ratio: {aspect_ratio:.2f}")
                
                return {
                    'score': quality_score,
                    'width': width,
                    'height': height,
                    'file_size_kb': file_size,
                    'aspect_ratio': aspect_ratio,
                    'issues': issues,
                    'grade': self._get_quality_grade(quality_score)
                }
                
        except Exception as e:
            self.logger.error(f"Quality assessment failed: {e}")
            return {'score': 0, 'issues': [f"Assessment failed: {e}"], 'grade': 'F'}
    
    def _get_quality_grade(self, score: int) -> str:
        """根据分数获取质量等级"""
        if score >= 90:
            return 'A'
        elif score >= 75:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 40:
            return 'D'
        else:
            return 'F'
    
    def create_error_report(self) -> Dict:
        """创建错误报告"""
        return {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'api_statistics': self.get_api_statistics(),
            'recommendations': self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> list:
        """生成优化建议"""
        recommendations = []
        
        for api, stats in self.api_stats.items():
            if stats['calls'] > 0:
                if stats['success_rate'] < 80:
                    recommendations.append(
                        f"Consider improving {api.title()} API reliability "
                        f"(current success rate: {stats['success_rate']:.1f}%)"
                    )
                elif stats['success_rate'] > 95:
                    recommendations.append(
                        f"{api.title()} API performing excellently "
                        f"({stats['success_rate']:.1f}% success rate)"
                    )
        
        return recommendations

# 全局错误处理器实例
error_handler = ImageProcessingErrorHandler()

# 便捷装饰器
def with_retry(max_attempts: int = 3, delay_base: int = 2):
    """便捷的重试装饰器"""
    return error_handler.with_retry(max_attempts, delay_base)

def track_performance(operation_name: str):
    """性能跟踪装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                raise e
            finally:
                duration = time.time() - start_time
                error_handler.log_performance_metrics(operation_name, duration, success)
        return wrapper
    return decorator