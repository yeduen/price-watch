"""
목데이터 프로바이더
"""
import asyncio
import random
from typing import List, Optional
from decimal import Decimal
from .base import BaseProvider, OfferLike, SearchResult


class MockProvider(BaseProvider):
    """목데이터 프로바이더"""
    
    def __init__(self):
        super().__init__("mock")
        self._mock_data = self._generate_mock_data()
    
    def _generate_mock_data(self) -> List[OfferLike]:
        """목데이터 생성"""
        return [
            OfferLike(
                marketplace="쿠팡",
                seller="쿠팡",
                title="삼성전자 갤럭시 S24 128GB 블랙",
                price=Decimal("1200000"),
                shipping_fee=Decimal("0"),
                url="https://mock.coupang.com/product1",
                affiliate_url="https://mock.coupang.com/affiliate1",
                image_url="https://mock.coupang.com/image1.jpg",
                description="삼성전자 갤럭시 S24 128GB 블랙 스마트폰",
                rating=4.8,
                review_count=1250
            ),
            OfferLike(
                marketplace="쿠팡",
                seller="삼성공식스토어",
                title="삼성 갤럭시 S24 128GB 블랙",
                price=Decimal("1250000"),
                shipping_fee=Decimal("0"),
                url="https://mock.coupang.com/product2",
                affiliate_url="https://mock.coupang.com/affiliate2",
                image_url="https://mock.coupang.com/image2.jpg",
                description="삼성 갤럭시 S24 128GB 블랙",
                rating=4.9,
                review_count=890
            ),
            OfferLike(
                marketplace="11번가",
                seller="11번가",
                title="삼성 갤럭시S24 128GB 블랙",
                price=Decimal("1180000"),
                shipping_fee=Decimal("3000"),
                url="https://mock.11st.co.kr/product1",
                affiliate_url="https://mock.11st.co.kr/affiliate1",
                image_url="https://mock.11st.co.kr/image1.jpg",
                description="삼성 갤럭시S24 128GB 블랙",
                rating=4.7,
                review_count=567
            ),
            OfferLike(
                marketplace="쿠팡",
                seller="애플공식스토어",
                title="Apple iPhone 15 Pro 128GB 블랙",
                price=Decimal("1500000"),
                shipping_fee=Decimal("0"),
                url="https://mock.coupang.com/product3",
                affiliate_url="https://mock.coupang.com/affiliate3",
                image_url="https://mock.coupang.com/image3.jpg",
                description="Apple iPhone 15 Pro 128GB 블랙",
                rating=4.9,
                review_count=2100
            ),
            OfferLike(
                marketplace="쿠팡",
                seller="쿠팡",
                title="LG전자 올레드 TV 65인치 4K",
                price=Decimal("2500000"),
                shipping_fee=Decimal("0"),
                url="https://mock.coupang.com/product4",
                affiliate_url="https://mock.coupang.com/affiliate4",
                image_url="https://mock.coupang.com/image4.jpg",
                description="LG전자 올레드 TV 65인치 4K UHD",
                rating=4.8,
                review_count=890
            ),
            OfferLike(
                marketplace="11번가",
                seller="LG공식스토어",
                title="LG 올레드 65인치 4K TV",
                price=Decimal("2450000"),
                shipping_fee=Decimal("5000"),
                url="https://mock.11st.co.kr/product2",
                affiliate_url="https://mock.11st.co.kr/affiliate2",
                image_url="https://mock.11st.co.kr/image2.jpg",
                description="LG 올레드 65인치 4K UHD TV",
                rating=4.9,
                review_count=456
            ),
            OfferLike(
                marketplace="쿠팡",
                seller="샤오미공식스토어",
                title="샤오미 Redmi Note 13 128GB 블루",
                price=Decimal("350000"),
                shipping_fee=Decimal("0"),
                url="https://mock.coupang.com/product5",
                affiliate_url="https://mock.coupang.com/affiliate5",
                image_url="https://mock.coupang.com/image5.jpg",
                description="샤오미 Redmi Note 13 128GB 블루",
                rating=4.6,
                review_count=234
            ),
            OfferLike(
                marketplace="쿠팡",
                seller="쿠팡",
                title="ASUS ROG 게이밍 노트북 16인치",
                price=Decimal("3200000"),
                shipping_fee=Decimal("0"),
                url="https://mock.coupang.com/product6",
                affiliate_url="https://mock.coupang.com/affiliate6",
                image_url="https://mock.coupang.com/image6.jpg",
                description="ASUS ROG 게이밍 노트북 16인치 RTX 4060",
                rating=4.7,
                review_count=123
            )
        ]
    
    async def search(self, keyword: str, **kwargs) -> SearchResult:
        """키워드로 상품 검색 (목데이터)"""
        # 실제 검색 시간 시뮬레이션
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        # 키워드 기반 필터링
        filtered_offers = []
        keyword_lower = keyword.lower()
        
        for offer in self._mock_data:
            if (keyword_lower in offer.title.lower() or 
                keyword_lower in offer.description.lower()):
                filtered_offers.append(offer)
        
        # 키워드가 없으면 모든 데이터 반환
        if not filtered_offers:
            filtered_offers = self._mock_data
        
        # 랜덤하게 일부만 반환 (검색 결과 다양성)
        if len(filtered_offers) > 5:
            filtered_offers = random.sample(filtered_offers, 5)
        
        return SearchResult(
            offers=filtered_offers,
            total_count=len(filtered_offers),
            marketplace=self.name,
            search_time=random.uniform(0.1, 0.5)
        )
    
    async def get_product_detail(self, url: str) -> Optional[OfferLike]:
        """상품 상세 정보 조회 (목데이터)"""
        await asyncio.sleep(random.uniform(0.05, 0.2))
        
        # URL에서 상품 찾기
        for offer in self._mock_data:
            if offer.url == url:
                return offer
        
        return None
    
    def is_available(self) -> bool:
        """항상 사용 가능"""
        return True


# 프로바이더 레지스트리에 등록
from .base import provider_registry
provider_registry.register(MockProvider())
