from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import settings
from utils.logger import logger
import os
from typing import List
from pathlib import Path


class DocumentProcessor:
    SUPPORTED_EXTENSIONS = {'.pdf', '.docx', '.txt'}
    
    def __init__(self, chunk_size: int = None, chunk_overlap: int = None):
        self.split_chunk_size = chunk_size or settings.CHUNK_SIZE
        self.split_overlap = chunk_overlap or settings.CHUNK_OVERLAP
        logger.info(f"DocumentProcessor 初始化 | chunk_size={self.split_chunk_size}, overlap={self.split_overlap}")
    
    def load_pdf(self, file_path: str):
        try:
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            logger.debug(f"PDF 加载成功: {file_path}, 页数: {len(docs)}")
            return docs
        except Exception as e:
            logger.error(f"PDF 加载失败 {file_path}: {e}")
            raise
    
    def load_docx(self, file_path: str):
        try:
            loader = Docx2txtLoader(file_path)
            docs = loader.load()
            logger.debug(f"DOCX 加载成功: {file_path}")
            return docs
        except Exception as e:
            logger.error(f"DOCX 加载失败 {file_path}: {e}")
            raise
    
    def load_txt(self, file_path: str):
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            docs = loader.load()
            logger.debug(f"TXT 加载成功: {file_path}")
            return docs
        except UnicodeDecodeError:
            loader = TextLoader(file_path, encoding='gbk')
            docs = loader.load()
            logger.debug(f"TXT 加载成功 (GBK): {file_path}")
            return docs
        except Exception as e:
            logger.error(f"TXT 加载失败 {file_path}: {e}")
            raise
    
    def load_single_doc(self, file_path: str):
        ext = Path(file_path).suffix.lower()
        
        if ext not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"不支持的文件格式: {ext}")
        
        if ext == '.pdf':
            return self.load_pdf(file_path)
        elif ext == '.docx':
            return self.load_docx(file_path)
        elif ext == '.txt':
            return self.load_txt(file_path)
    
    def load_all_docs(self, dir_path: str):
        docs = []
        failed_files = []
        
        if not os.path.exists(dir_path):
            raise FileNotFoundError(f"文档目录不存在: {dir_path}")
        
        files = [f for f in os.listdir(dir_path) 
                 if Path(f).suffix.lower() in self.SUPPORTED_EXTENSIONS]
        
        if not files:
            logger.warning(f"在 {dir_path} 中未找到支持的文档文件")
            return []
        
        logger.info(f"找到 {len(files)} 个文档文件，开始加载...")
        
        for file in files:
            file_path = os.path.join(dir_path, file)
            try:
                logger.info(f"[{files.index(file) + 1}/{len(files)}] 加载文档：{file}")
                docs.extend(self.load_single_doc(file_path))
            except Exception as e:
                logger.error(f"加载 {file} 失败: {e}，跳过该文件")
                failed_files.append(file)
                continue
        
        if failed_files:
            logger.warning(f"以下文件加载失败: {failed_files}")
        
        logger.info(f"文档加载完成 | 成功: {len(files) - len(failed_files)}, 失败: {len(failed_files)}")
        return docs
    
    def split_documents(self, documents, chunk_size: int = None, chunk_overlap: int = None):
        size = chunk_size or self.split_chunk_size
        overlap = chunk_overlap or self.split_overlap
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=size,
            chunk_overlap=overlap,
            length_function=len,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
        )
        
        chunks = splitter.split_documents(documents)
        
        avg_length = sum(len(chunk.page_content) for chunk in chunks) / len(chunks) if chunks else 0
        logger.info(f"文档分割完成 | 片段数: {len(chunks)}, 平均长度: {avg_length:.0f} 字符")
        
        if any(len(chunk.page_content) == 0 for chunk in chunks):
            logger.warning("发现空片段，已自动过滤")
            chunks = [chunk for chunk in chunks if chunk.page_content]
        
        return chunks
    
    def get_stats(self, documents):
        if not documents:
            return {}
        
        lengths = [len(doc.page_content) for doc in documents]
        return {
            "total_docs": len(documents),
            "avg_length": sum(lengths) / len(lengths),
            "min_length": min(lengths),
            "max_length": max(lengths),
            "total_chars": sum(lengths)
        }
