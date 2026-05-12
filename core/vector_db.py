from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from config.settings import settings
from utils.logger import logger
import os
from typing import Optional


class VectorStore:
    def __init__(self, db_type: str = None):
        self.db_type = db_type or settings.VECTOR_DB_TYPE
        self.db_path = settings.VECTOR_DB_PATH
        self.embeddings = self._create_embeddings()
        
        logger.info(f"VectorStore 初始化 | 类型: {self.db_type}, Embedding: {settings.EMBEDDING_PROVIDER}")
    
    def _create_embeddings(self):
        provider = settings.EMBEDDING_PROVIDER.lower()
        
        if provider == "dashscope":
            return DashScopeEmbeddings(
                model=settings.EMBEDDING_MODEL,
                dashscope_api_key=settings.DASHSCOPE_API_KEY
            )
        elif provider == "openai":
            from langchain_openai import OpenAIEmbeddings
            if not settings.OPENAI_API_KEY:
                raise ValueError("使用 OpenAI Embedding 需要配置 OPENAI_API_KEY")
            return OpenAIEmbeddings(
                model=settings.EMBEDDING_MODEL,
                openai_api_key=settings.OPENAI_API_KEY
            )
        elif provider == "bge":
            from langchain_community.embeddings import HuggingFaceBgeEmbeddings
            return HuggingFaceBgeEmbeddings(
                model_name="BAAI/bge-base-zh-v1.5",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        else:
            raise ValueError(f"不支持的 Embedding 提供商: {provider}")
    
    def build_from_docs(self, chunks):
        if not chunks:
            logger.error("chunks 列表为空，无法构建向量库")
            raise ValueError("无法使用空的 chunks 列表构建向量库")
        
        logger.info(f"开始构建向量库 | 文档块数量: {len(chunks)}, 类型: {self.db_type}")
        
        if self.db_type == "chroma":
            db = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=self.db_path
            )
            logger.info(f"Chroma 向量库构建完成，保存至: {self.db_path}")
            return db
        elif self.db_type == "faiss":
            from langchain_community.vectorstores import FAISS
            db = FAISS.from_documents(
                documents=chunks,
                embedding=self.embeddings
            )
            os.makedirs(self.db_path, exist_ok=True)
            db.save_local(self.db_path)
            logger.info(f"FAISS 向量库构建完成，保存至: {self.db_path}")
            return db
        else:
            raise ValueError(f"不支持的向量库类型: {self.db_type}")
    
    def load(self):
        if self.db_type == "chroma":
            if os.path.exists(self.db_path):
                logger.info(f"加载本地 Chroma 向量库: {self.db_path}")
                return Chroma(
                    persist_directory=self.db_path,
                    embedding_function=self.embeddings
                )
            return None
        elif self.db_type == "faiss":
            from langchain_community.vectorstores import FAISS
            index_path = os.path.join(self.db_path, "index.faiss")
            if os.path.exists(index_path):
                logger.info(f"加载本地 FAISS 向量库: {self.db_path}")
                return FAISS.load_local(
                    self.db_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            return None
        return None
    
    def clear(self):
        import shutil
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)
            logger.info(f"已清空向量库: {self.db_path}")
