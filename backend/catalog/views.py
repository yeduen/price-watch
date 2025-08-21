"""
Catalog views and viewsets
"""
from django.db.models import Q
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Offer, PriceHistory, Watch
from .serializers import (
    ProductListSerializer, ProductDetailSerializer,
    OfferListSerializer, PriceHistoryListSerializer,
    WatchCreateSerializer, WatchListSerializer, WatchUpdateSerializer
)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """상품 뷰셋"""
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['brand', 'model_code', 'name', 'gtin']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """상품 검색"""
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': '검색어를 입력해주세요.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 검색 쿼리 구성
        search_query = Q()
        for term in query.split():
            search_query |= (
                Q(brand__icontains=term) |
                Q(model_code__icontains=term) |
                Q(name__icontains=term) |
                Q(gtin__icontains=term)
            )
        
        products = self.queryset.filter(search_query)
        serializer = self.get_serializer(products, many=True)
        
        return Response({
            'query': query,
            'count': products.count(),
            'results': serializer.data
        })


class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    """오퍼 뷰셋"""
    queryset = Offer.objects.select_related('product').all()
    serializer_class = OfferListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['product_id', 'marketplace']
    ordering_fields = ['price', 'fetched_at']
    ordering = ['-fetched_at']


class PriceHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """가격 히스토리 뷰셋"""
    queryset = PriceHistory.objects.select_related('offer__product').all()
    serializer_class = PriceHistoryListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['offer_id']
    ordering_fields = ['recorded_at']
    ordering = ['-recorded_at']


class WatchViewSet(viewsets.ModelViewSet):
    """가격 모니터링 뷰셋"""
    queryset = Watch.objects.select_related('product').all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user_id', 'product_id', 'is_active']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return WatchCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return WatchUpdateSerializer
        return WatchListSerializer
    
    def get_queryset(self):
        """사용자별 모니터링 목록 조회"""
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset
    
    def create(self, request, *args, **kwargs):
        """모니터링 등록"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )
    
    def destroy(self, request, *args, **kwargs):
        """모니터링 삭제"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': '모니터링이 삭제되었습니다.'}, 
            status=status.HTTP_204_NO_CONTENT
        )
