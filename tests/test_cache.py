# 新文件: tests/test_cache.py
"""
缓存模块单元测试
"""

import pytest
from core.cache import QueryCache


class TestQueryCache:
    """缓存测试类"""

    @pytest.fixture
    def cache(self):
        """创建缓存实例"""
        return QueryCache(use_cache=True)

    def test_cache_set_and_get(self, cache):
        """测试缓存设置和获取"""
        query = "什么是 LangChain?"
        result = {"answer": "LangChain 是一个框架", "sources": []}

        cache.set(query, result)
        retrieved = cache.get(query)

        assert retrieved == result

    def test_cache_miss(self, cache):
        """测试缓存未命中"""
        result = cache.get("nonexistent query")
        assert result is None

    def test_cache_key_normalization(self, cache):
        """测试缓存键的标准化"""
        query1 = "什么是 LangChain?"
        query2 = "什么是 langchain? "  # 大小写和空格不同

        result = {"answer": "test"}
        cache.set(query1, result)

        # 应该能命中缓存
        retrieved = cache.get(query2)
        assert retrieved == result

    def test_cache_clear(self, cache):
        """测试清空缓存"""
        cache.set("query1", {"answer": "test1"})
        cache.set("query2", {"answer": "test2"})

        cache.clear()

        assert cache.get("query1") is None
        assert cache.get("query2") is None

    def test_cache_disabled(self):
        """测试禁用缓存"""
        cache = QueryCache(use_cache=False)

        cache.set("query", {"answer": "test"})
        result = cache.get("query")

        assert result is None

    def test_cache_stats(self, cache):
        """测试缓存统计"""
        cache.set("query1", {"answer": "test1"})
        cache.set("query2", {"answer": "test2"})

        stats = cache.get_stats()

        assert stats["enabled"] is True
        assert stats["size"] == 2
