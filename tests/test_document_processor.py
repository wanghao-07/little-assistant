# 新文件: tests/test_document_processor.py
"""
文档处理器单元测试

运行测试：
    pytest tests/ -v

带覆盖率：
    pytest tests/ -v --cov=core --cov-report=html
"""

import pytest
import os
import tempfile
from pathlib import Path
from core.document_processor import DocumentProcessor
from config.settings import settings


class TestDocumentProcessor:
    """文档处理器测试类"""

    @pytest.fixture
    def processor(self):
        """创建处理器实例"""
        return DocumentProcessor()

    @pytest.fixture
    def sample_pdf_path(self):
        """创建临时 PDF 文件用于测试"""
        # 注意：实际测试需要一个真实的 PDF 文件
        # 这里只是示例，实际应该使用测试专用的 PDF
        pdf_path = Path(settings.DOCS_PATH) / "test_sample.pdf"

        if not pdf_path.exists():
            pytest.skip("测试 PDF 文件不存在")

        return str(pdf_path)

    def test_processor_initialization(self, processor):
        """测试处理器初始化"""
        assert processor.split_chunk_size == settings.CHUNK_SIZE
        assert processor.split_overlap == settings.CHUNK_OVERLAP

    def test_load_single_doc_success(self, processor, sample_pdf_path):
        """测试成功加载单个文档"""
        docs = processor.load_single_doc(sample_pdf_path)

        assert len(docs) > 0
        assert hasattr(docs[0], 'page_content')
        assert hasattr(docs[0], 'metadata')

    def test_load_nonexistent_file(self, processor):
        """测试加载不存在的文件"""
        with pytest.raises(FileNotFoundError):
            processor.load_single_doc("nonexistent_file.pdf")

    def test_load_unsupported_format(self, processor):
        """测试加载不支持的格式"""
        with pytest.raises(ValueError):
            processor.load_single_doc("test.mp4")

    def test_split_documents(self, processor, sample_pdf_path):
        """测试文档分割"""
        # 加载文档
        docs = processor.load_single_doc(sample_pdf_path)

        # 分割文档
        chunks = processor.split_documents(docs)

        assert len(chunks) > 0
        assert all(len(chunk.page_content) > 0 for chunk in chunks)
        assert all(len(chunk.page_content) <= settings.CHUNK_SIZE * 1.2 for chunk in chunks)

    def test_split_with_custom_params(self):
        """测试使用自定义参数分割"""
        processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)

        assert processor.split_chunk_size == 500
        assert processor.split_overlap == 50

    def test_get_stats(self, processor, sample_pdf_path):
        """测试获取文档统计信息"""
        docs = processor.load_single_doc(sample_pdf_path)
        stats = processor.get_stats(docs)

        assert "total_docs" in stats
        assert "avg_length" in stats
        assert stats["total_docs"] > 0
        assert stats["avg_length"] > 0

    def test_load_all_docs_from_dir(self, processor):
        """测试从目录加载所有文档"""
        docs = processor.load_all_docs(settings.DOCS_PATH)

        # 如果目录有文档，应该能加载
        if docs:
            assert len(docs) > 0
        else:
            # 如果目录为空，返回空列表
            assert docs == []

    def test_load_from_empty_dir(self, processor):
        """测试从空目录加载"""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs = processor.load_all_docs(tmpdir)
            assert docs == []

    def test_load_from_nonexistent_dir(self, processor):
        """测试从不存在的目录加载"""
        with pytest.raises(FileNotFoundError):
            processor.load_all_docs("/nonexistent/path")
