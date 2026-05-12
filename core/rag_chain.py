from langchain.prompts import PromptTemplate
from langchain.chains.retrieval_qa.base import RetrievalQA
from config.settings import settings
from utils.logger import logger
from typing import Dict, List


class RAGChain:
    DEFAULT_PROMPT_TEMPLATE = """
你是一个专业的智能问答助手，基于提供的文档内容回答问题。

重要原则：
1. 严格根据文档内容回答，不要编造信息
2. 如果文档中没有相关信息，请直接回复："根据提供的文档，我无法找到相关答案。"
3. 回答要简洁清晰，条理分明

文档内容：
{context}

用户问题：
{question}

你的回答：
"""
    
    @staticmethod
    def build_chain(llm, retriever, chain_type: str = "stuff"):
        prompt = PromptTemplate(
            template=RAGChain.DEFAULT_PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )
        
        logger.info(f"构建 RAG 链 | 类型: {chain_type}, Top-K: {settings.TOP_K}")
        
        if chain_type == "stuff":
            return RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                chain_type_kwargs={"prompt": prompt},
                return_source_documents=True
            )
        elif chain_type == "map_reduce":
            return RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="map_reduce",
                retriever=retriever,
                return_source_documents=True
            )
        elif chain_type == "refine":
            return RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="refine",
                retriever=retriever,
                return_source_documents=True
            )
        else:
            raise ValueError(f"不支持的链类型: {chain_type}")
    
    @staticmethod
    def format_response(result: Dict) -> Dict:
        source_docs = result.get("source_documents", [])
        
        sources = []
        for i, doc in enumerate(source_docs, 1):
            sources.append({
                "index": i,
                "content": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                "metadata": doc.metadata
            })
        
        return {
            "answer": result["result"],
            "sources": sources,
            "source_count": len(sources)
        }
