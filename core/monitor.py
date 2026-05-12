import time
from functools import wraps
from utils.logger import logger


class PerformanceMonitor:
    def __init__(self):
        self.metrics = {
            "query_count": 0,
            "total_query_time": 0,
            "avg_query_time": 0,
            "cache_hits": 0,
            "cache_misses": 0
        }

    def timer(self, operation_name: str):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                elapsed_time = time.time() - start_time

                logger.info(f"[{operation_name}] 耗时: {elapsed_time:.2f}s")

                metric_key = f"{operation_name}_time"
                self.metrics[metric_key] = elapsed_time

                return result

            return wrapper

        return decorator

    def record_query(self, elapsed_time: float, cache_hit: bool = False):
        self.metrics["query_count"] += 1
        self.metrics["total_query_time"] += elapsed_time
        self.metrics["avg_query_time"] = (
                self.metrics["total_query_time"] / self.metrics["query_count"]
        )

        if cache_hit:
            self.metrics["cache_hits"] += 1
        else:
            self.metrics["cache_misses"] += 1

    def get_metrics(self) -> dict:
        return self.metrics.copy()

    def reset(self):
        self.metrics = {
            "query_count": 0,
            "total_query_time": 0,
            "avg_query_time": 0,
            "cache_hits": 0,
            "cache_misses": 0
        }
        logger.info("性能指标已重置")


monitor = PerformanceMonitor()
