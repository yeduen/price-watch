"""
프로바이더 테스트
"""
import pytest
from decimal import Decimal
from django.test import TestCase
from ..providers.mock import MockProvider
from ..providers.base import OfferLike, SearchResult


class MockProviderTest(TestCase):
    """목데이터 프로바이더 테스트"""
    
    def setUp(self):
        """테스트 설정"""
        self.provider = MockProvider()
    
    def test_provider_name(self):
        """프로바이더명 테스트"""
        self.assertEqual(self.provider.get_name(), "mock")
    
    def test_provider_availability(self):
        """프로바이더 사용 가능 여부 테스트"""
        self.assertTrue(self.provider.is_available())
    
    def test_mock_data_generation(self):
        """목데이터 생성 테스트"""
        mock_data = self.provider._mock_data
        
        self.assertGreater(len(mock_data), 0)
        self.assertIsInstance(mock_data[0], OfferLike)
        
        # 첫 번째 상품 확인
        first_offer = mock_data[0]
        self.assertEqual(first_offer.marketplace, "쿠팡")
        self.assertEqual(first_offer.seller, "쿠팡")
        self.assertIn("갤럭시 S24", first_offer.title)
        self.assertEqual(first_offer.price, Decimal("1200000"))
    
    @pytest.mark.asyncio
    async def test_search_with_keyword(self):
        """키워드 검색 테스트"""
        result = await self.provider.search("갤럭시")
        
        self.assertIsInstance(result, SearchResult)
        self.assertEqual(result.marketplace, "mock")
        self.assertGreater(result.total_count, 0)
        
        # 갤럭시 관련 상품이 검색되어야 함
        galaxy_offers = [o for o in result.offers if "갤럭시" in o.title]
        self.assertGreater(len(galaxy_offers), 0)
    
    @pytest.mark.asyncio
    async def test_search_without_keyword(self):
        """키워드 없이 검색 테스트"""
        result = await self.provider.search("")
        
        self.assertIsInstance(result, SearchResult)
        self.assertGreater(result.total_count, 0)
        # 빈 키워드 시 모든 데이터 반환
        self.assertGreaterEqual(len(result.offers), 5)
    
    @pytest.mark_asyncio
    async def test_search_nonexistent_keyword(self):
        """존재하지 않는 키워드 검색 테스트"""
        result = await self.provider.search("존재하지않는상품")
        
        self.assertIsInstance(result, SearchResult)
        # 존재하지 않는 키워드 시 모든 데이터 반환
        self.assertGreater(result.total_count, 0)
    
    @pytest.mark.asyncio
    async def test_get_product_detail(self):
        """상품 상세 정보 조회 테스트"""
        # 존재하는 URL
        url = "https://mock.coupang.com/product1"
        offer = await self.provider.get_product_detail(url)
        
        self.assertIsNotNone(offer)
        self.assertEqual(offer.url, url)
        self.assertEqual(offer.marketplace, "쿠팡")
        
        # 존재하지 않는 URL
        nonexistent_url = "https://nonexistent.com/product"
        offer = await self.provider.get_product_detail(nonexistent_url)
        
        self.assertIsNone(offer)
    
    def test_rate_limit_info(self):
        """속도 제한 정보 테스트"""
        rate_limit = self.provider.get_rate_limit_info()
        
        self.assertIn('requests_per_minute', rate_limit)
        self.assertIn('requests_per_hour', rate_limit)
        self.assertIn('cooldown_seconds', rate_limit)
        
        self.assertEqual(rate_limit['requests_per_minute'], 60)
        self.assertEqual(rate_limit['requests_per_hour'], 1000)


@pytest.mark.asyncio
class MockProviderAsyncTest:
    """비동기 프로바이더 테스트"""
    
    @pytest.fixture
    def provider(self):
        return MockProvider()
    
    async def test_search_performance(self, provider):
        """검색 성능 테스트"""
        import time
        
        start_time = time.time()
        result = await provider.search("갤럭시")
        end_time = time.time()
        
        search_time = end_time - start_time
        
        # 검색 시간이 1초 이하여야 함
        assert search_time < 1.0
        assert result.search_time < 1.0
    
    async def test_search_result_structure(self, provider):
        """검색 결과 구조 테스트"""
        result = await provider.search("갤럭시")
        
        # 필수 필드 확인
        assert hasattr(result, 'offers')
        assert hasattr(result, 'total_count')
        assert hasattr(result, 'marketplace')
        assert hasattr(result, 'search_time')
        
        # 데이터 타입 확인
        assert isinstance(result.offers, list)
        assert isinstance(result.total_count, int)
        assert isinstance(result.marketplace, str)
        assert isinstance(result.search_time, float)
    
    async def test_offer_structure(self, provider):
        """오퍼 구조 테스트"""
        result = await provider.search("갤럭시")
        
        if result.offers:
            offer = result.offers[0]
            
            # 필수 필드 확인
            assert hasattr(offer, 'marketplace')
            assert hasattr(offer, 'seller')
            assert hasattr(offer, 'title')
            assert hasattr(offer, 'price')
            assert hasattr(offer, 'url')
            
            # 데이터 타입 확인
            assert isinstance(offer.marketplace, str)
            assert isinstance(offer.seller, str)
            assert isinstance(offer.title, str)
            assert isinstance(offer.price, Decimal)
            assert isinstance(offer.url, str)
