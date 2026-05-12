from loguru import logger
from config.settings import settings
import os

os.makedirs(settings.LOG_PATH, exist_ok=True)

logger.add(
    f"{settings.LOG_PATH}/rag.log",
    rotation="10 MB",
    retention="7 days",
    encoding="utf-8",
    enqueue=True
)

__all__ = ["logger"]