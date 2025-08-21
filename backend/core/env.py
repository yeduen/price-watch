"""
환경 변수 로드 및 설정
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트 디렉토리
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# .env 파일 로드
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(env_path)

def get_env(key: str, default: str = None) -> str:
    """환경 변수 값을 가져옵니다."""
    return os.getenv(key, default)

def get_env_bool(key: str, default: bool = False) -> bool:
    """환경 변수 값을 boolean으로 가져옵니다."""
    value = get_env(key)
    if value is None:
        return default
    return value.lower() in ('true', '1', 'yes', 'on')

def get_env_int(key: str, default: int = 0) -> int:
    """환경 변수 값을 integer로 가져옵니다."""
    value = get_env(key)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default
