"""
프로바이더 공통 인터페이스
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class OfferLike(BaseModel):
    """오퍼 유사 스키마 (프로바이더 응답용)"""
    marketplace: str = Field(..., description="마켓플레이스명")
    seller: str = Field(..., description="판매자명")
    title: str = Field(..., description="상품 제목")
    price: Decimal = Field(..., description="상품 가격")
    shipping_fee: Decimal = Field(0, description="배송비")
    url: str = Field(..., description="상품 URL")
    affiliate_url: Optional[str] = Field(None, description="제휴 링크")
    image_url: Optional[str] = Field(None, description="상품 이미지 URL")
    description: Optional[str] = Field(None, description="상품 설명")
    rating: Optional[float] = Field(None, description="평점")
    review_count: Optional[int] = Field(None, description="리뷰 수")
    
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }


class SearchResult(BaseModel):
    """검색 결과 스키마"""
    offers: List[OfferLike] = Field(default_factory=list, description="검색된 오퍼 목록")
    total_count: int = Field(0, description="총 검색 결과 수")
    marketplace: str = Field(..., description="검색한 마켓플레이스")
    search_time: float = Field(..., description="검색 소요 시간(초)")


class BaseProvider(ABC):
    """프로바이더 기본 클래스"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    async def search(self, keyword: str, **kwargs) -> SearchResult:
        """키워드로 상품 검색"""
        pass
    
    @abstractmethod
    async def get_product_detail(self, url: str) -> Optional[OfferLike]:
        """상품 상세 정보 조회"""
        pass
    
    def get_name(self) -> str:
        """프로바이더명 반환"""
        return self.name
    
    def is_available(self) -> bool:
        """프로바이더 사용 가능 여부"""
        return True
    
    def get_rate_limit_info(self) -> dict:
        """속도 제한 정보"""
        return {
            'requests_per_minute': 60,
            'requests_per_hour': 1000,
            'cooldown_seconds': 0
        }


class ProviderRegistry:
    """프로바이더 레지스트리"""
    
    def __init__(self):
        self._providers: dict = {}
    
    def register(self, provider: BaseProvider):
        """프로바이더 등록"""
        self._providers[provider.get_name()] = provider
    
    def get_provider(self, name: str) -> Optional[BaseProvider]:
        """프로바이더 조회"""
        return self._providers.get(name)
    
    def get_all_providers(self) -> List[BaseProvider]:
        """모든 프로바이더 조회"""
        return list(self._providers.values())
    
    def get_available_providers(self) -> List[BaseProvider]:
        """사용 가능한 프로바이더만 조회"""
        return [p for p in self._providers.values() if p.is_available()]
    
    async def search_all(self, keyword: str, **kwargs) -> List[SearchResult]:
        """모든 프로바이더에서 검색"""
        results = []
        for provider in self.get_available_providers():
            try:
                result = await provider.search(keyword, **kwargs)
                results.append(result)
            except Exception as e:
                # 로깅 추가 필요
                continue
        return results


# 전역 프로바이더 레지스트리
provider_registry = ProviderRegistry()
