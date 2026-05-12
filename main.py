from core.document_processor import DocumentProcessor
from core.vector_db import VectorStore
from core.llm_engine import LLMEngine
from core.rag_chain import RAGChain
from core.cache import QueryCache
from core.monitor import monitor
from config.settings import settings
from utils.logger import logger
import time


def initialize_system():
    logger.info("="*50)
    logger.info("开始初始化 RAG 系统")
    logger.info("="*50)
    
    processor = DocumentProcessor()
    docs = processor.load_all_docs(settings.DOCS_PATH)
    
    if not docs:
        logger.error(f"在 {settings.DOCS_PATH} 目录下未找到任何文档")
        raise ValueError(f"未找到任何文档，请确保 {settings.DOCS_PATH} 目录下有 PDF/DOCX/TXT 文件")
    
    stats = processor.get_stats(docs)
    logger.info(f"文档统计: {stats}")
    
    chunks = processor.split_documents(docs)
    
    if not chunks:
        logger.error("文档分割后得到空的 chunks 列表")
        raise ValueError("文档分割失败")

    logger.info(f"成功加载并分割文档，共 {len(chunks)} 个 chunks")

    vs = VectorStore()
    db = vs.load()
    if not db:
        logger.info("未找到本地向量库，开始构建...")
        db = vs.build_from_docs(chunks)
    else:
        logger.info("使用本地向量库")

    llm = LLMEngine.get_chat_model()

    retriever = db.as_retriever(search_kwargs={"k": settings.TOP_K})
    chain = RAGChain.build_chain(llm, retriever)
    
    logger.info("="*50)
    logger.info("系统初始化完成")
    logger.info("="*50)
    
    return chain


def chat_loop(chain):
    cache = QueryCache()
    
    print("\n" + "="*60)
    print("RAG 智能问答系统已启动")
    print(f"性能监控: 启用")
    print(f"查询缓存: {'启用' if cache.use_cache else '禁用'}")
    print("输入 'quit' 退出, 'stats' 查看统计, 'clear' 清空缓存")
    print("="*60 + "\n")
    
    while True:
        try:
            q = input("请输入问题：").strip()
            
            if not q:
                continue
            
            if q.lower() in ["quit", "exit", "q"]:
                print("\n再见！")
                break
            
            if q.lower() == "stats":
                metrics = monitor.get_metrics()
                cache_stats = cache.get_stats()
                print(f"\n性能统计:")
                print(f"   查询次数: {metrics['query_count']}")
                print(f"   平均响应时间: {metrics['avg_query_time']:.2f}s")
                print(f"   缓存数量: {cache_stats['size']} 条")
                print()
                continue
            
            if q.lower() == "clear":
                cache.clear()
                monitor.reset()
                print("缓存和统计已清空\n")
                continue
            
            cached_result = cache.get(q)
            if cached_result:
                print(f"\n[缓存] 回答：{cached_result['answer']}\n")
                monitor.record_query(0, cache_hit=True)
                continue
            
            start_time = time.time()
            res = chain.invoke({"query": q})
            elapsed_time = time.time() - start_time
            
            formatted = RAGChain.format_response(res)
            print(f"\n回答：{formatted['answer']}\n")
            print(f"参考来源 ({formatted['source_count']} 个):")
            for i, source in enumerate(formatted['sources'], 1):
                print(f"   {i}. {source['content'][:100]}...")
            print(f"\n耗时: {elapsed_time:.2f}s")
            print("-" * 60 + "\n")
            
            cache.set(q, formatted)
            monitor.record_query(elapsed_time, cache_hit=False)
            
        except KeyboardInterrupt:
            print("\n\n再见！")
            break
        except Exception as e:
            logger.error(f"查询出错: {e}")
            print(f"\n出错了: {e}\n请重试或联系管理员\n")


if __name__ == "__main__":
    try:
        chain = initialize_system()
        chat_loop(chain)
    except Exception as e:
        logger.error(f"系统启动失败: {e}")
        print(f"\n系统启动失败: {e}")
        exit(1)
