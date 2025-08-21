"""
로깅 설정 및 헬퍼
"""
import sys
import structlog
from typing import Any, Dict

def configure_logging(log_level: str = "INFO") -> None:
    """structlog를 사용한 JSON 로깅을 설정합니다."""
    
    # structlog 프로세서 설정
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ]
    
    # structlog 설정
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # 표준 라이브러리 로깅 설정
    import logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.INFO),
    )

def get_logger(name: str) -> structlog.BoundLogger:
    """로거를 가져옵니다."""
    return structlog.get_logger(name)

def log_context(**kwargs: Any) -> Dict[str, Any]:
    """로깅 컨텍스트를 생성합니다."""
    return kwargs
