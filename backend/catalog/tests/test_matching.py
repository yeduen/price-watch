"""
매칭 서비스 테스트
"""
import pytest
from decimal import Decimal
from django.test import TestCase
from ..models import Product, Offer
from ..services.matching import ProductMatcher


class ProductMatcherTest(TestCase):
    """상품 매칭 테스트"""
    
    def setUp(self):
        """테스트 데이터 설정"""
        # 테스트 상품 생성
        self.product1 = Product.objects.create(
            brand="삼성",
            model_code="S24",
            name="삼성 갤럭시 S24 128GB 블랙",
            gtin="1234567890123"
        )
        
        self.product2 = Product.objects.create(
            brand="삼성",
            model_code="S24",
            name="삼성전자 갤럭시 S24 128GB 블랙",
            gtin="1234567890123"
        )
        
        self.product3 = Product.objects.create(
            brand="Apple",
            model_code="iPhone15",
            name="Apple iPhone 15 Pro 128GB 블랙",
            gtin="9876543210987"
        )
        
        # 테스트 오퍼 생성
        self.offer1 = Offer.objects.create(
            product=self.product1,
            marketplace="쿠팡",
            seller="쿠팡",
            price=Decimal("1200000"),
            shipping_fee=Decimal("0"),
            url="https://test1.com"
        )
        
        self.offer2 = Offer.objects.create(
            product=self.product2,
            marketplace="11번가",
            seller="11번가",
            price=Decimal("1180000"),
            shipping_fee=Decimal("3000"),
            url="https://test2.com"
        )
        
        self.offer3 = Offer.objects.create(
            product=self.product3,
            marketplace="쿠팡",
            seller="애플공식스토어",
            price=Decimal("1500000"),
            shipping_fee=Decimal("0"),
            url="https://test3.com"
        )
        
        self.matcher = ProductMatcher(threshold=0.75)
    
    def test_normalize(self):
        """제목 정규화 테스트"""
        title = "삼성전자 갤럭시 S24 (128GB) 블랙 스마트폰"
        normalized = self.matcher.normalize(title)
        expected = "삼성전자 갤럭시 s24 128gb 블랙 스마트폰"
        self.assertEqual(normalized, expected)
    
    def test_extract_tokens(self):
        """토큰 추출 테스트"""
        title = "삼성전자 갤럭시 S24 128GB 블랙"
        tokens = self.matcher.extract_tokens(title)
        
        self.assertEqual(tokens['brand'], 'samsung')
        self.assertEqual(tokens['model_code'], 'S24')
        self.assertEqual(tokens['capacity'], '128')
        self.assertEqual(tokens['color'], 'black')
    
    def test_calculate_brand_similarity(self):
        """브랜드 유사도 계산 테스트"""
        # 동일 브랜드
        sim1 = self.matcher.calculate_brand_similarity("삼성", "삼성")
        self.assertEqual(sim1, 1.0)
        
        # 다른 브랜드
        sim2 = self.matcher.calculate_brand_similarity("삼성", "Apple")
        self.assertEqual(sim2, 0.0)
        
        # 부분 일치
        sim3 = self.matcher.calculate_brand_similarity("삼성", "삼성전자")
        self.assertEqual(sim3, 0.8)
    
    def test_calculate_model_similarity(self):
        """모델 코드 유사도 계산 테스트"""
        # 동일 모델
        sim1 = self.matcher.calculate_model_similarity("S24", "S24")
        self.assertEqual(sim1, 1.0)
        
        # 유사한 모델
        sim2 = self.matcher.calculate_model_similarity("S24", "S24+")
        self.assertGreater(sim2, 0.8)
        
        # 다른 모델
        sim3 = self.matcher.calculate_model_similarity("S24", "iPhone15")
        self.assertLess(sim3, 0.5)
    
    def test_calculate_spec_overlap(self):
        """스펙 중복도 계산 테스트"""
        tokens1 = {'brand': 'samsung', 'model_code': 'S24', 'capacity': '128'}
        tokens2 = {'brand': 'samsung', 'model_code': 'S24', 'color': 'black'}
        
        overlap = self.matcher.calculate_spec_overlap(tokens1, tokens2)
        expected = 2 / 3  # brand, model_code 일치
        self.assertEqual(overlap, expected)
    
    def test_calculate_price_proximity(self):
        """가격 근접도 계산 테스트"""
        # 동일 가격
        proximity1 = self.matcher.calculate_price_proximity(
            Decimal("1000000"), Decimal("1000000")
        )
        self.assertEqual(proximity1, 1.0)
        
        # 10% 차이
        proximity2 = self.matcher.calculate_price_proximity(
            Decimal("1000000"), Decimal("1100000")
        )
        self.assertAlmostEqual(proximity2, 0.9, places=1)
    
    def test_score_gtin_match(self):
        """GTIN 동일 시 하드매칭 테스트"""
        score = self.matcher.score(self.product1, self.product2)
        self.assertEqual(score, 1.0)
    
    def test_score_brand_model_match(self):
        """브랜드+모델 일치 시 높은 점수 테스트"""
        score = self.matcher.score(self.product1, self.product2, self.offer1, self.offer2)
        self.assertGreater(score, 0.8)
    
    def test_score_different_products(self):
        """다른 상품 시 낮은 점수 테스트"""
        score = self.matcher.score(self.product1, self.product3, self.offer1, self.offer3)
        self.assertLess(score, 0.5)
    
    def test_match_products(self):
        """상품 그룹핑 테스트"""
        candidates = [
            {'product': self.product1, 'offer': self.offer1},
            {'product': self.product2, 'offer': self.offer2},
            {'product': self.product3, 'offer': self.offer3}
        ]
        
        groups = self.matcher.match_products(candidates)
        
        # GTIN이 동일한 product1과 product2는 같은 그룹에 있어야 함
        self.assertEqual(len(groups), 2)
        
        # 첫 번째 그룹에는 product1과 product2가 있어야 함
        first_group = groups[0]
        self.assertEqual(len(first_group), 2)
        
        # 두 번째 그룹에는 product3가 있어야 함
        second_group = groups[1]
        self.assertEqual(len(second_group), 1)


@pytest.mark.django_db
class ProductMatcherPytestTest:
    """pytest 기반 매칭 테스트"""
    
    def test_empty_candidates(self):
        """빈 후보 리스트 테스트"""
        matcher = ProductMatcher()
        result = matcher.match_products([])
        assert result == []
    
    def test_single_candidate(self):
        """단일 후보 테스트"""
        matcher = ProductMatcher()
        candidates = [{'product': Product(), 'offer': None}]
        result = matcher.match_products(candidates)
        assert len(result) == 1
        assert len(result[0]) == 1
