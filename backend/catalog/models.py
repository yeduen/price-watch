"""
Catalog domain models
"""
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    """상품 모델"""
    brand = models.CharField(max_length=100, help_text="브랜드명")
    model_code = models.CharField(max_length=100, help_text="모델 코드")
    name = models.CharField(max_length=500, help_text="상품명")
    gtin = models.CharField(max_length=50, blank=True, null=True, help_text="GTIN (Global Trade Item Number)")
    spec_hash = models.CharField(max_length=64, blank=True, null=True, help_text="상품 스펙 해시")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalog_product'
        unique_together = [['brand', 'model_code']]
        indexes = [
            models.Index(fields=['brand', 'model_code']),
            models.Index(fields=['gtin']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model_code} - {self.name}"

    @property
    def display_name(self):
        """표시용 상품명"""
        return f"{self.brand} {self.model_code}"


class Offer(models.Model):
    """상품 오퍼 모델"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='offers',
        help_text="연결된 상품"
    )
    marketplace = models.CharField(max_length=50, help_text="마켓플레이스명 (쿠팡, 11번가 등)")
    seller = models.CharField(max_length=100, help_text="판매자명")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        validators=[MinValueValidator(Decimal('0'))],
        help_text="상품 가격"
    )
    shipping_fee = models.DecimalField(
        max_digits=6, 
        decimal_places=0, 
        default=Decimal('0'),
        validators=[MinValueValidator(Decimal('0'))],
        help_text="배송비"
    )
    coupon_hint = models.TextField(blank=True, null=True, help_text="쿠폰 정보")
    url = models.URLField(max_length=1000, help_text="상품 URL")
    affiliate_url = models.URLField(max_length=1000, blank=True, null=True, help_text="제휴 링크")
    fetched_at = models.DateTimeField(auto_now_add=True, help_text="수집 시각")

    class Meta:
        db_table = 'catalog_offer'
        indexes = [
            models.Index(fields=['product_id', 'marketplace', '-fetched_at']),
            models.Index(fields=['marketplace', '-fetched_at']),
        ]
        ordering = ['-fetched_at']

    def __str__(self):
        return f"{self.product.display_name} - {self.marketplace} ({self.price:,}원)"

    @property
    def total_price(self):
        """총 가격 (가격 + 배송비)"""
        return self.price + self.shipping_fee


class PriceHistory(models.Model):
    """가격 히스토리 모델"""
    offer = models.ForeignKey(
        Offer, 
        on_delete=models.CASCADE, 
        related_name='price_history',
        help_text="연결된 오퍼"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        validators=[MinValueValidator(Decimal('0'))],
        help_text="기록된 가격"
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        validators=[MinValueValidator(Decimal('0'))],
        help_text="기록된 총 가격"
    )
    recorded_at = models.DateTimeField(auto_now_add=True, help_text="기록 시각")

    class Meta:
        db_table = 'catalog_pricehistory'
        indexes = [
            models.Index(fields=['offer_id', '-recorded_at']),
            models.Index(fields=['-recorded_at']),
        ]
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.offer} - {self.price:,}원 ({self.recorded_at.strftime('%Y-%m-%d %H:%M')})"


class Watch(models.Model):
    """가격 모니터링 모델"""
    user_id = models.BigIntegerField(help_text="사용자 ID")
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='watches',
        help_text="모니터링할 상품"
    )
    target_price = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        validators=[MinValueValidator(Decimal('0'))],
        help_text="목표 가격"
    )
    is_active = models.BooleanField(default=True, help_text="활성화 여부")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'catalog_watch'
        indexes = [
            models.Index(fields=['user_id', 'product_id']),
            models.Index(fields=['user_id', '-created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"User {self.user_id} - {self.product.display_name} (목표: {self.target_price:,}원)"
