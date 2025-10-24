"""
日志配置 - 结构化 JSON 日志
"""
import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    配置结构化 JSON 日志
    
    Args:
        name: Logger 名称
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        logging.Logger: 配置好的 Logger
        
    使用示例:
        from app.utils.logger import setup_logger
        
        logger = setup_logger(__name__)
        logger.info("Processing task", extra={"task_id": "task_001", "step": "analyzing"})
    """
    logger = logging.getLogger(name)
    
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        
        formatter = jsonlogger.JsonFormatter(
            fmt='%(asctime)s %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    return logger
