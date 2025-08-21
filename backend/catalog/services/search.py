"""
검색 서비스
"""
import asyncio
from typing import List, Dict, Any
from decimal import Decimal
from ..models import Product, Offer
from ..providers.base import provider_registry, OfferLike
from .matching import ProductMatcher


class SearchService:
    """검색 서비스"""
    
    def __init__(self):
        self.matcher = ProductMatcher()
    
    async def search_products(self, keyword: str) -> Dict[str, Any]:
        """키워드로 상품 검색"""
        # 모든 프로바이더에서 검색
        search_results = await provider_registry.search_all(keyword)
        
        # 모든 오퍼 수집
        all_offers = []
        for result in search_results:
            all_offers.extend(result.offers)
        
        if not all_offers:
            return {
                'products': [],
                'offers': [],
                'best_price': None,
                'total_count': 0
            }
        
        # 오퍼를 Product/Offer 모델로 변환
        offers = await self._convert_offers_to_models(all_offers)
        
        # 상품 매칭 실행
        matched_groups = self.matcher.match_products([
            {'product': offer.product, 'offer': offer} for offer in offers
        ])
        
        # 결과 구성
        products = []
        all_offers_list = []
        best_price = None
        
        for group in matched_groups:
            if not group:
                continue
            
            # 그룹의 대표 상품 선택 (첫 번째)
            representative_offer = group[0]
            product = representative_offer.product
            
            # 그룹의 모든 오퍼 수집
            group_offers = [item['offer'] for item in group]
            
            # 최저가 계산
            min_price_offer = min(group_offers, key=lambda x: x.price)
            total_price = min_price_offer.price + min_price_offer.shipping_fee
            
            # 전체 최저가 업데이트
            if best_price is None or total_price < best_price['total_price']:
                best_price = {
                    'price': min_price_offer.price,
                    'total_price': total_price,
                    'marketplace': min_price_offer.marketplace,
                    'seller': min_price_offer.seller,
                    'product_id': product.id
                }
            
            # 상품 정보 구성
            product_info = {
                'id': product.id,
                'brand': product.brand,
                'model_code': product.model_code,
                'name': product.name,
                'gtin': product.gtin,
                'best_price': {
                    'price': min_price_offer.price,
                    'total_price': total_price,
                    'marketplace': min_price_offer.marketplace,
                    'seller': min_price_offer.seller
                },
                'offer_count': len(group_offers),
                'marketplaces': list(set(offer.marketplace for offer in group_offers))
            }
            
            products.append(product_info)
            all_offers_list.extend(group_offers)
        
        return {
            'products': products,
            'offers': all_offers_list,
            'best_price': best_price,
            'total_count': len(products)
        }
    
    async def _convert_offers_to_models(self, offer_likes: List[OfferLike]) -> List[Offer]:
        """OfferLike를 Offer 모델로 변환"""
        offers = []
        
        for offer_like in offer_likes:
            # 상품 생성 또는 조회
            product, created = await self._get_or_create_product(offer_like)
            
            # 오퍼 생성
            offer = Offer(
                product=product,
                marketplace=offer_like.marketplace,
                seller=offer_like.seller,
                price=offer_like.price,
                shipping_fee=offer_like.shipping_fee,
                url=offer_like.url,
                affiliate_url=offer_like.affiliate_url
            )
            
            offers.append(offer)
        
        return offers
    
    async def _get_or_create_product(self, offer_like: OfferLike) -> tuple[Product, bool]:
        """상품 조회 또는 생성"""
        # 제목에서 브랜드와 모델 코드 추출
        tokens = self.matcher.extract_tokens(offer_like.title)
        
        brand = tokens.get('brand', 'Unknown')
        model_code = tokens.get('model_code', 'Unknown')
        
        # 기존 상품 조회
        try:
            product = Product.objects.get(brand=brand, model_code=model_code)
            return product, False
        except Product.DoesNotExist:
            # 새 상품 생성
            product = Product.objects.create(
                brand=brand,
                model_code=model_code,
                name=offer_like.title,
                gtin=None,  # 나중에 업데이트
                spec_hash=None  # 나중에 계산
            )
            return product, True


# 전역 검색 서비스 인스턴스
search_service = SearchService()
