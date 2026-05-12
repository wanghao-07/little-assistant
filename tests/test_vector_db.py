# 新文件: tests/test_vector_db.py
"""
向量库单元测试
"""

import pytest
import shutil
import tempfile
from core.vector_db import VectorStore
from core.document_processor import DocumentProcessor
from config.settings import settings


class TestVectorStore:
    """向量库测试类"""

    @pytest.fixture
    def temp_db_path(self):
        """创建临时数据库路径"""
        with tempfile.TemporaryDirectory() as tmpdir:
            original_path = settings.VECTOR_DB_PATH
            settings.VECTOR_DB_PATH = tmpdir
            yield tmpdir
            settings.VECTOR_DB_PATH = original_path

    @pytest.fixture
    def sample_chunks(self):
        """获取测试用的文档块"""
        processor = DocumentProcessor()
        docs = processor.load_all_docs(settings.DOCS_PATH)

        if not docs:
            pytest.skip("没有可用的测试文档")

        return processor.split_documents(docs[:5])  # 只用前5个文档加速测试

    def test_vectorstore_initialization(self, temp_db_path):
        """测试向量库初始化"""
        vs = VectorStore()
        assert vs.db_path == temp_db_path
        assert vs.embeddings is not None

    def test_build_from_docs(self, temp_db_path, sample_chunks):
        """测试从文档构建向量库"""
        vs = VectorStore()
        db = vs.build_from_docs(sample_chunks)

        assert db is not None
        assert vs.db_path == temp_db_path

    def test_build_from_empty_chunks(self, temp_db_path):
        """测试用空 chunks 构建向量库"""
        vs = VectorStore()

        with pytest.raises(ValueError):
            vs.build_from_docs([])

    def test_load_existing_db(self, temp_db_path, sample_chunks):
        """测试加载已存在的向量库"""
        vs = VectorStore()

        # 先构建
        vs.build_from_docs(sample_chunks)

        # 再加载
        loaded_db = vs.load()
        assert loaded_db is not None

    def test_load_nonexistent_db(self, temp_db_path):
        """测试加载不存在的向量库"""
        vs = VectorStore()
        loaded_db = vs.load()

        assert loaded_db is None

    def test_clear_db(self, temp_db_path, sample_chunks):
        """测试清空向量库"""
        vs = VectorStore()

        # 构建向量库
        vs.build_from_docs(sample_chunks)

        # 清空
        vs.clear()

        # 验证已清空
        assert not hasattr(vs, 'db') or vs.load() is None

    def test_unsupported_db_type(self):
        """测试不支持的向量库类型"""
        original_type = settings.VECTOR_DB_TYPE
        settings.VECTOR_DB_TYPE = "unsupported"

        with pytest.raises(ValueError):
            VectorStore()

        settings.VECTOR_DB_TYPE = original_type
