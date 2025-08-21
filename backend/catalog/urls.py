"""
Catalog app URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'catalog'

# 뷰셋 라우터 설정
router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'offers', views.OfferViewSet)
router.register(r'price-history', views.PriceHistoryViewSet)
router.register(r'watches', views.WatchViewSet)

urlpatterns = [
    # 뷰셋 URL
    path('', include(router.urls)),
    
    # 검색 엔드포인트 (별도 액션)
    path('search/', views.ProductViewSet.as_view({'get': 'search'}), name='product-search'),
]
