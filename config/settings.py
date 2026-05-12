from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()


class Settings(BaseSettings):
    # LLM 配置
    DASHSCOPE_API_KEY: str = os.getenv("DASHSCOPE_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "qwen-max")
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", 0.1))
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Embedding 配置
    EMBEDDING_PROVIDER: str = os.getenv("EMBEDDING_PROVIDER", "dashscope")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-v2")
    
    # 向量库配置
    VECTOR_DB_TYPE: str = os.getenv("VECTOR_DB_TYPE", "chroma")
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "./chroma_db")
    
    # 文档处理配置
    DOCS_PATH: str = os.getenv("DOCS_PATH", "./docs")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 800))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 100))
    
    # 检索配置
    TOP_K: int = int(os.getenv("TOP_K", 5))
    USE_RERANK: bool = os.getenv("USE_RERANK", "false").lower() == "true"
    RERANK_MODEL: str = os.getenv("RERANK_MODEL", "bge-reranker-base")
    
    # 缓存配置
    USE_CACHE: bool = os.getenv("USE_CACHE", "true").lower() == "true"
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # 日志配置
    LOG_PATH: str = os.getenv("LOG_PATH", "./logs")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # API 服务配置
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    class Config:
        env_file = ".env"


settings = Settings()
