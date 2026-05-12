from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import time

from core.document_processor import DocumentProcessor
from core.vector_db import VectorStore
from core.llm_engine import LLMEngine
from core.rag_chain import RAGChain
from core.cache import QueryCache
from core.monitor import monitor
from config.settings import settings
from utils.logger import logger


app = FastAPI(
    title="RAG 智能问答系统",
    description="基于 LangChain + 通义千问的企业级 RAG 问答系统",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_chain = None
query_cache = None


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    top_k: Optional[int] = Field(5, ge=1, le=20)
    use_cache: Optional[bool] = Field(True)


class SourceDocument(BaseModel):
    index: int = Field(...)
    content: str = Field(...)
    metadata: dict = Field(...)


class QueryResponse(BaseModel):
    success: bool = Field(...)
    answer: str = Field(...)
    sources: List[SourceDocument] = Field(...)
    source_count: int = Field(...)
    response_time: float = Field(...)
    cache_hit: bool = Field(False)


class RebuildRequest(BaseModel):
    docs_path: Optional[str] = Field(None)


class SystemStatus(BaseModel):
    status: str = Field(...)
    vector_db_loaded: bool = Field(...)
    cache_size: int = Field(...)
    metrics: dict = Field(...)


class MetricsResponse(BaseModel):
    metrics: dict = Field(...)
    cache: dict = Field(...)


@app.on_event("startup")
async def startup_event():
    global rag_chain, query_cache

    logger.info("启动 RAG 系统...")

    try:
        processor = DocumentProcessor()
        docs = processor.load_all_docs(settings.DOCS_PATH)

        if not docs:
            logger.warning("未找到文档")
            rag_chain = None
            query_cache = QueryCache()
            return

        chunks = processor.split_documents(docs)

        vs = VectorStore()
        db = vs.load()
        if not db:
            logger.info("构建向量库...")
            db = vs.build_from_docs(chunks)

        llm = LLMEngine.get_chat_model()
        retriever = db.as_retriever(search_kwargs={"k": settings.TOP_K})
        rag_chain = RAGChain.build_chain(llm, retriever)

        query_cache = QueryCache()

        logger.info("RAG 系统初始化完成")

    except Exception as e:
        logger.error(f"系统初始化失败: {e}")
        raise


@app.get("/")
async def root():
    return {
        "name": "RAG 智能问答系统",
        "version": "1.0.0",
        "status": "运行中",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "正常",
        "timestamp": time.time()
    }


@app.post("/api/v1/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    if rag_chain is None:
        raise HTTPException(status_code=503, detail="系统未初始化")
    
    start_time = time.time()
    
    try:
        cache_hit = False
        if request.use_cache and query_cache:
            cached_result = query_cache.get(request.question)
            if cached_result:
                cache_hit = True
                elapsed_time = time.time() - start_time
                monitor.record_query(elapsed_time, cache_hit=True)
                
                return QueryResponse(
                    success=True,
                    answer=cached_result["answer"],
                    sources=cached_result["sources"],
                    source_count=cached_result["source_count"],
                    response_time=elapsed_time,
                    cache_hit=True
                )
        
        result = rag_chain.invoke({"query": request.question})
        formatted = RAGChain.format_response(result)
        
        elapsed_time = time.time() - start_time
        
        if query_cache:
            query_cache.set(request.question, formatted)
        
        monitor.record_query(elapsed_time, cache_hit=False)
        
        return QueryResponse(
            success=True,
            answer=formatted["answer"],
            sources=formatted["sources"],
            source_count=formatted["source_count"],
            response_time=elapsed_time,
            cache_hit=False
        )
        
    except Exception as e:
        logger.error(f"查询失败: {e}")
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@app.get("/api/v1/status", response_model=SystemStatus)
async def get_status():
    return SystemStatus(
        status="运行中",
        vector_db_loaded=rag_chain is not None,
        cache_size=query_cache.get_stats()["size"] if query_cache else 0,
        metrics=monitor.get_metrics()
    )


@app.post("/api/v1/rebuild")
async def rebuild_vectordb(request: RebuildRequest = None, background_tasks: BackgroundTasks = None):
    docs_path = request.docs_path if request else settings.DOCS_PATH
    
    def rebuild_task():
        try:
            logger.info("开始重建向量库...")
            
            vs = VectorStore()
            vs.clear()
            
            processor = DocumentProcessor()
            docs = processor.load_all_docs(docs_path)
            chunks = processor.split_documents(docs)
            
            db = vs.build_from_docs(chunks)
            
            global rag_chain
            llm = LLMEngine.get_chat_model()
            retriever = db.as_retriever(search_kwargs={"k": settings.TOP_K})
            rag_chain = RAGChain.build_chain(llm, retriever)
            
            if query_cache:
                query_cache.clear()
            
            logger.info("向量库重建完成")
            
        except Exception as e:
            logger.error(f"向量库重建失败: {e}")
    
    if background_tasks:
        background_tasks.add_task(rebuild_task)
        return {"message": "重建任务已启动，将在后台执行"}
    else:
        rebuild_task()
        return {"message": "向量库重建完成"}


@app.delete("/api/v1/cache")
async def clear_cache():
    if query_cache:
        query_cache.clear()
        monitor.reset()
        return {"message": "缓存和统计已清空"}
    return {"message": "缓存未启用"}


@app.get("/api/v1/metrics", response_model=MetricsResponse)
async def get_metrics():
    return MetricsResponse(
        metrics=monitor.get_metrics(),
        cache=query_cache.get_stats() if query_cache else {"enabled": False}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "success": False,
        "error": "请求失败",
        "detail": exc.detail
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"未处理的异常: {exc}")
    return {
        "success": False,
        "error": "服务器内部错误",
        "detail": str(exc)
    }


if __name__ == "__main__":
    import uvicorn
    
    print("="*60)
    print("启动 RAG 智能问答系统 API 服务")
    print("="*60)
    print(f"API 文档: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    print(f"健康检查: http://{settings.API_HOST}:{settings.API_PORT}/health")
    print("="*60)
    
    uvicorn.run(
        "api.app:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level="info"
    )
