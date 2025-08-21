"""
상품 매칭 서비스
"""
import re
from typing import List, Dict, Any, Tuple
from difflib import SequenceMatcher
from decimal import Decimal
from ..models import Product, Offer


class ProductMatcher:
    """상품 매칭 서비스"""
    
    def __init__(self, threshold: float = 0.75):
        self.threshold = threshold
        # 가중치 설정
        self.weights = {
            'brand': 0.3,
            'model_code': 0.4,
            'spec_overlap': 0.2,
            'price_proximity': 0.1
        }
    
    def normalize(self, title: str) -> str:
        """제목 정규화: 소문자 변환, 괄호/특수문자 제거, 공백 정규화"""
        if not title:
            return ""
        
        # 소문자 변환
        normalized = title.lower()
        
        # 괄호와 내용 제거 (브랜드명, 모델명 등)
        normalized = re.sub(r'\([^)]*\)', '', normalized)
        normalized = re.sub(r'\[[^\]]*\]', '', normalized)
        
        # 특수문자 제거 (하이픈, 언더스코어는 공백으로 변환)
        normalized = re.sub(r'[-_]', ' ', normalized)
        normalized = re.sub(r'[^\w\s]', '', normalized)
        
        # 공백 정규화 (여러 공백을 하나로)
        normalized = re.sub(r'\s+', ' ', normalized)
        
        return normalized.strip()
    
    def extract_tokens(self, title: str) -> Dict[str, str]:
        """제목에서 토큰 추출: brand, model_code, 용량/크기, 색상"""
        normalized = self.normalize(title)
        tokens = {}
        
        # 브랜드 추출 (일반적인 브랜드명)
        brands = ['samsung', 'lg', 'apple', 'xiaomi', 'sony', 'asus', 'lenovo', 'hp', 'dell']
        for brand in brands:
            if brand in normalized:
                tokens['brand'] = brand
                break
        
        # 모델 코드 추출 (영숫자 조합, 3자리 이상)
        model_pattern = r'\b[a-zA-Z]{1,3}\d{2,4}[a-zA-Z]*\b'
        model_matches = re.findall(model_pattern, normalized)
        if model_matches:
            tokens['model_code'] = model_matches[0]
        
        # 용량/크기 추출
        capacity_patterns = [
            r'\b(\d{1,3})\s*(?:gb|tb|mb)\b',  # 저장용량
            r'\b(\d{1,2}(?:\.\d)?)\s*(?:inch|인치)\b',  # 화면크기
            r'\b(\d{1,3})\s*(?:cm|센티)\b',  # 치수
        ]
        
        for pattern in capacity_patterns:
            matches = re.findall(pattern, normalized)
            if matches:
                tokens['capacity'] = matches[0]
                break
        
        # 색상 추출
        colors = ['black', 'white', 'silver', 'gold', 'blue', 'red', 'green', 'gray', 'pink']
        for color in colors:
            if color in normalized:
                tokens['color'] = color
                break
        
        return tokens
    
    def calculate_brand_similarity(self, brand1: str, brand2: str) -> float:
        """브랜드 유사도 계산"""
        if not brand1 or not brand2:
            return 0.0
        
        if brand1.lower() == brand2.lower():
            return 1.0
        
        # 부분 일치 확인
        if brand1.lower() in brand2.lower() or brand2.lower() in brand1.lower():
            return 0.8
        
        return 0.0
    
    def calculate_model_similarity(self, model1: str, model2: str) -> float:
        """모델 코드 유사도 계산"""
        if not model1 or not model2:
            return 0.0
        
        if model1.lower() == model2.lower():
            return 1.0
        
        # SequenceMatcher를 사용한 유사도 계산
        return SequenceMatcher(None, model1.lower(), model2.lower()).ratio()
    
    def calculate_spec_overlap(self, tokens1: Dict[str, str], tokens2: Dict[str, str]) -> float:
        """스펙 중복도 계산"""
        if not tokens1 or not tokens2:
            return 0.0
        
        common_keys = set(tokens1.keys()) & set(tokens2.keys())
        if not common_keys:
            return 0.0
        
        matches = 0
        for key in common_keys:
            if tokens1[key] == tokens2[key]:
                matches += 1
        
        return matches / len(common_keys) if common_keys else 0.0
    
    def calculate_price_proximity(self, price1: Decimal, price2: Decimal) -> float:
        """가격 근접도 계산"""
        if not price1 or not price2:
            return 0.0
        
        if price1 == 0 or price2 == 0:
            return 0.0
        
        # 가격 차이의 백분율 계산
        diff = abs(price1 - price2)
        avg_price = (price1 + price2) / 2
        proximity = 1 - (diff / avg_price)
        
        return max(0.0, min(1.0, proximity))
    
    def score(self, product1: Product, product2: Product, offer1: Offer = None, offer2: Offer = None) -> float:
        """두 상품 간의 매칭 점수 계산"""
        # 토큰 추출
        tokens1 = self.extract_tokens(product1.name)
        tokens2 = self.extract_tokens(product2.name)
        
        # GTIN 동일 시 하드매칭
        if product1.gtin and product2.gtin and product1.gtin == product2.gtin:
            return 1.0
        
        # 브랜드 유사도
        brand_sim = self.calculate_brand_similarity(
            tokens1.get('brand', product1.brand),
            tokens2.get('brand', product2.brand)
        )
        
        # 모델 코드 유사도
        model_sim = self.calculate_model_similarity(
            tokens1.get('model_code', product1.model_code),
            tokens2.get('model_code', product2.model_code)
        )
        
        # 스펙 중복도
        spec_overlap = self.calculate_spec_overlap(tokens1, tokens2)
        
        # 가격 근접도 (오퍼가 있는 경우)
        price_proximity = 0.0
        if offer1 and offer2:
            price_proximity = self.calculate_price_proximity(offer1.price, offer2.price)
        
        # 가중 평균 계산
        score = (
            self.weights['brand'] * brand_sim +
            self.weights['model_code'] * model_sim +
            self.weights['spec_overlap'] * spec_overlap +
            self.weights['price_proximity'] * price_proximity
        )
        
        return score
    
    def match_products(self, candidates: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        """상품 그룹핑: 동일 상품으로 판단되는 것들을 그룹화"""
        if not candidates:
            return []
        
        groups = []
        processed = set()
        
        for i, candidate in enumerate(candidates):
            if i in processed:
                continue
            
            group = [candidate]
            processed.add(i)
            
            # 다른 후보들과 비교
            for j, other in enumerate(candidates[i+1:], i+1):
                if j in processed:
                    continue
                
                # 매칭 점수 계산
                score = self.score(
                    candidate['product'], 
                    other['product'],
                    candidate.get('offer'),
                    other.get('offer')
                )
                
                # 임계값 이상이면 같은 그룹에 추가
                if score >= self.threshold:
                    group.append(other)
                    processed.add(j)
            
            groups.append(group)
        
        return groups


def match_products_by_offers(offers: List[Offer]) -> List[List[Offer]]:
    """오퍼 리스트를 기반으로 상품 매칭"""
    matcher = ProductMatcher()
    
    # 오퍼를 상품별로 그룹화
    candidates = []
    for offer in offers:
        candidates.append({
            'product': offer.product,
            'offer': offer
        })
    
    # 매칭 실행
    groups = matcher.match_products(candidates)
    
    # 결과를 오퍼 리스트로 변환
    result = []
    for group in groups:
        result.append([item['offer'] for item in group])
    
    return result
