"""
Catalog admin configuration
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Offer, PriceHistory, Watch


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """상품 관리"""
    list_display = ['brand', 'model_code', 'name', 'gtin', 'created_at']
    list_filter = ['brand', 'created_at']
    search_fields = ['brand', 'model_code', 'name', 'gtin']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('기본 정보', {
            'fields': ('brand', 'model_code', 'name')
        }),
        ('상세 정보', {
            'fields': ('gtin', 'spec_hash'),
            'classes': ('collapse',)
        }),
        ('시스템 정보', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """오퍼 관리"""
    list_display = ['product', 'marketplace', 'seller', 'price', 'shipping_fee', 'total_price_display', 'fetched_at']
    list_filter = ['marketplace', 'fetched_at']
    search_fields = ['product__name', 'product__brand', 'product__model_code', 'seller']
    readonly_fields = ['fetched_at']
    ordering = ['-fetched_at']
    
    def total_price_display(self, obj):
        """총 가격 표시"""
        return format_html('<strong>{:,}원</strong>', obj.total_price)
    total_price_display.short_description = '총 가격'
    
    fieldsets = (
        ('상품 정보', {
            'fields': ('product',)
        }),
        ('오퍼 정보', {
            'fields': ('marketplace', 'seller', 'price', 'shipping_fee', 'coupon_hint')
        }),
        ('링크', {
            'fields': ('url', 'affiliate_url')
        }),
        ('시스템 정보', {
            'fields': ('fetched_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    """가격 히스토리 관리"""
    list_display = ['offer', 'price', 'total_price', 'recorded_at']
    list_filter = ['recorded_at']
    search_fields = ['offer__product__name', 'offer__product__brand']
    readonly_fields = ['recorded_at']
    ordering = ['-recorded_at']
    
    fieldsets = (
        ('오퍼 정보', {
            'fields': ('offer',)
        }),
        ('가격 정보', {
            'fields': ('price', 'total_price')
        }),
        ('시스템 정보', {
            'fields': ('recorded_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    """가격 모니터링 관리"""
    list_display = ['user_id', 'product', 'target_price', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['product__name', 'product__brand', 'product__model_code']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('사용자 정보', {
            'fields': ('user_id',)
        }),
        ('모니터링 정보', {
            'fields': ('product', 'target_price', 'is_active')
        }),
        ('시스템 정보', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
