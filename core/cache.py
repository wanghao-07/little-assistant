import hashlib
from typing import Optional
from config.settings import settings
from utils.logger import logger


class QueryCache:
    def __init__(self, use_cache: bool = None):
        self.use_cache = use_cache if use_cache is not None else settings.USE_CACHE
        self.cache = {}

        if self.use_cache:
            logger.info("查询缓存已启用")
        else:
            logger.info("查询缓存已禁用")

    def _generate_key(self, query: str) -> str:
        query_normalized = query.strip().lower()
        return hashlib.md5(query_normalized.encode('utf-8')).hexdigest()

    def get(self, query: str) -> Optional[dict]:
        if not self.use_cache:
            return None

        key = self._generate_key(query)
        if key in self.cache:
            logger.debug(f"缓存命中: {query[:50]}...")
            return self.cache[key]

        logger.debug(f"缓存未命中: {query[:50]}...")
        return None

    def set(self, query: str, result: dict):
        if not self.use_cache:
            return

        key = self._generate_key(query)
        self.cache[key] = result
        logger.debug(f"缓存已设置: {key[:16]}...")

    def clear(self):
        self.cache.clear()
        logger.info("缓存已清空")

    def get_stats(self) -> dict:
        return {
            "enabled": self.use_cache,
            "size": len(self.cache)
        }
