"""
Catalog serializers
"""
from rest_framework import serializers
from .models import Product, Offer, PriceHistory, Watch


class ProductListSerializer(serializers.ModelSerializer):
    """상품 목록 시리얼라이저"""
    best_price = serializers.SerializerMethodField()
    offer_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'brand', 'model_code', 'name', 'best_price', 'offer_count', 'created_at']
    
    def get_best_price(self, obj):
        """최저가 조회"""
        best_offer = obj.offers.order_by('price').first()
        if best_offer:
            return {
                'price': best_offer.price,
                'total_price': best_offer.total_price,
                'marketplace': best_offer.marketplace,
                'seller': best_offer.seller
            }
        return None
    
    def get_offer_count(self, obj):
        """오퍼 개수"""
        return obj.offers.count()


class ProductDetailSerializer(serializers.ModelSerializer):
    """상품 상세 시리얼라이저"""
    offers = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'brand', 'model_code', 'name', 'gtin', 'spec_hash', 'offers', 'created_at', 'updated_at']
    
    def get_offers(self, obj):
        """최신 오퍼 목록"""
        from .serializers import OfferListSerializer
        return OfferListSerializer(obj.offers.order_by('-fetched_at')[:10], many=True).data


class OfferListSerializer(serializers.ModelSerializer):
    """오퍼 목록 시리얼라이저"""
    product_brand = serializers.CharField(source='product.brand', read_only=True)
    product_model = serializers.CharField(source='product.model_code', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = Offer
        fields = [
            'id', 'product_brand', 'product_model', 'product_name',
            'marketplace', 'seller', 'price', 'shipping_fee', 'total_price',
            'coupon_hint', 'url', 'affiliate_url', 'fetched_at'
        ]


class PriceHistoryListSerializer(serializers.ModelSerializer):
    """가격 히스토리 목록 시리얼라이저"""
    marketplace = serializers.CharField(source='offer.marketplace', read_only=True)
    seller = serializers.CharField(source='offer.seller', read_only=True)
    
    class Meta:
        model = PriceHistory
        fields = ['id', 'marketplace', 'seller', 'price', 'total_price', 'recorded_at']


class WatchCreateSerializer(serializers.ModelSerializer):
    """가격 모니터링 생성 시리얼라이저"""
    class Meta:
        model = Watch
        fields = ['user_id', 'product', 'target_price']


class WatchListSerializer(serializers.ModelSerializer):
    """가격 모니터링 목록 시리얼라이저"""
    product_brand = serializers.CharField(source='product.brand', read_only=True)
    product_model = serializers.CharField(source='product.model_code', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    current_best_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Watch
        fields = [
            'id', 'product_brand', 'product_model', 'product_name',
            'target_price', 'current_best_price', 'is_active', 'created_at'
        ]
    
    def get_current_best_price(self, obj):
        """현재 최저가"""
        best_offer = obj.product.offers.order_by('price').first()
        if best_offer:
            return {
                'price': best_offer.price,
                'total_price': best_offer.total_price,
                'marketplace': best_offer.marketplace
            }
        return None


class WatchUpdateSerializer(serializers.ModelSerializer):
    """가격 모니터링 수정 시리얼라이저"""
    class Meta:
        model = Watch
        fields = ['target_price', 'is_active']
