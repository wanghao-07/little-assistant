from langchain_community.llms import Tongyi
from config.settings import settings
from utils.logger import logger


class LLMEngine:
    @staticmethod
    def get_chat_model(model_name: str = None, temperature: float = None):
        model = model_name or settings.LLM_MODEL
        temp = temperature or settings.TEMPERATURE
        
        if model.startswith("gpt"):
            return LLMEngine._get_openai_model(model, temp)
        else:
            return LLMEngine._get_tongyi_model(model, temp)
    
    @staticmethod
    def _get_tongyi_model(model_name: str, temperature: float):
        if not settings.DASHSCOPE_API_KEY:
            raise ValueError("使用通义千问需要配置 DASHSCOPE_API_KEY")
        
        logger.info(f"使用通义千问模型: {model_name}, temperature: {temperature}")
        return Tongyi(
            model_name=model_name,
            temperature=temperature,
            dashscope_api_key=settings.DASHSCOPE_API_KEY,
            max_tokens=2000
        )
    
    @staticmethod
    def _get_openai_model(model_name: str, temperature: float):
        from langchain_openai import ChatOpenAI
        
        if not settings.OPENAI_API_KEY:
            raise ValueError("使用 OpenAI 需要配置 OPENAI_API_KEY")
        
        logger.info(f"使用 OpenAI 模型: {model_name}, temperature: {temperature}")
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            openai_api_key=settings.OPENAI_API_KEY,
            max_tokens=2000
        )
    
    @staticmethod
    def compare_models(test_question: str):
        results = {}
        
        try:
            tongyi = LLMEngine.get_chat_model("qwen-turbo")
            results["qwen-turbo"] = tongyi.invoke(test_question)
        except Exception as e:
            results["qwen-turbo"] = f"Error: {e}"
        
        try:
            qwen_max = LLMEngine.get_chat_model("qwen-max")
            results["qwen-max"] = qwen_max.invoke(test_question)
        except Exception as e:
            results["qwen-max"] = f"Error: {e}"
        
        if settings.OPENAI_API_KEY:
            try:
                gpt = LLMEngine.get_chat_model("gpt-3.5-turbo")
                results["gpt-3.5-turbo"] = gpt.invoke(test_question)
            except Exception as e:
                results["gpt-3.5-turbo"] = f"Error: {e}"
        
        return results
