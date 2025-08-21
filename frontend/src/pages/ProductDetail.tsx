import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ArrowLeft, ExternalLink, Star, Loader2, AlertCircle, RefreshCw } from 'lucide-react'
import { PriceChart } from '@/components/PriceChart'
import { productApi, offerApi } from '@/api/client'
import { formatPrice, formatDate, getMarketplaceColor, cn } from '@/utils'
import type { Product, Offer } from '@/types'

export function ProductDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const productId = parseInt(id!)
  
  const { data: product, isLoading: productLoading, error: productError } = useQuery({
    queryKey: ['product', productId],
    queryFn: () => productApi.getProduct(productId),
    enabled: !!productId,
  })
  
  const { data: offers, isLoading: offersLoading, error: offersError } = useQuery({
    queryKey: ['offers', productId],
    queryFn: () => offerApi.getOffers(productId),
    enabled: !!productId,
  })
  
  const isLoading = productLoading || offersLoading
  const error = productError || offersError
  
  const handleBack = () => {
    navigate(-1)
  }
  
  const handleRetry = () => {
    window.location.reload()
  }
  
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">상품 정보를 불러오는 중...</p>
        </div>
      </div>
    )
  }
  
  if (error || !product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            상품을 불러올 수 없습니다
          </h3>
          <p className="text-gray-600 mb-4">
            잠시 후 다시 시도해주세요.
          </p>
          <button
            onClick={handleRetry}
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            다시 시도
          </button>
        </div>
      </div>
    )
  }
  
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* 뒤로가기 버튼 */}
        <button
          onClick={handleBack}
          className="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-6 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          뒤로가기
        </button>
        
        {/* 상품 기본 정보 */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* 상품 이미지 */}
            <div className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
              <div className="text-gray-400 text-8xl">📱</div>
            </div>
            
            {/* 상품 정보 */}
            <div>
              <div className="flex items-center gap-2 mb-3">
                <span className="text-lg font-medium text-blue-600">{product.brand}</span>
                <span className="text-lg text-gray-500">{product.model_code}</span>
              </div>
              
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                {product.name}
              </h1>
              
              {product.best_price && (
                <div className="mb-6">
                  <div className="text-4xl font-bold text-red-600 mb-2">
                    {formatPrice(product.best_price.total_price)}
                  </div>
                  <div className="text-sm text-gray-500">
                    배송비 포함 최저가
                  </div>
                </div>
              )}
              
              <div className="space-y-3 mb-6">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-gray-600">마켓플레이스:</span>
                  <div className="flex gap-2">
                    {product.marketplaces.map((marketplace) => (
                      <span
                        key={marketplace}
                        className={cn(
                          'px-2 py-1 text-xs font-medium text-white rounded-full',
                          getMarketplaceColor(marketplace)
                        )}
                      >
                        {marketplace}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium text-gray-600">오퍼 개수:</span>
                  <span className="text-sm text-gray-900">{product.offer_count}개</span>
                </div>
                
                {product.gtin && (
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-gray-600">GTIN:</span>
                    <span className="text-sm text-gray-900 font-mono">{product.gtin}</span>
                  </div>
                )}
              </div>
              
              <div className="flex gap-3">
                <button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2">
                  <Star className="w-5 h-5" />
                  가격 모니터링
                </button>
                
                {product.best_price && (
                  <a
                    href={product.best_price.affiliate_url || '#'}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-6 py-3 border border-gray-300 hover:border-gray-400 text-gray-700 font-medium rounded-lg transition-colors flex items-center justify-center gap-2"
                  >
                    <ExternalLink className="w-5 h-5" />
                    구매하기
                  </a>
                )}
              </div>
            </div>
          </div>
        </div>
        
        {/* 가격 히스토리 차트 */}
        <div className="mb-8">
          <PriceChart productId={productId} days={30} />
        </div>
        
        {/* 오퍼 목록 */}
        {offers && offers.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">가격 비교</h3>
            <div className="space-y-3">
              {offers.map((offer) => (
                <div
                  key={offer.id}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <span
                      className={cn(
                        'px-3 py-1 text-sm font-medium text-white rounded-full',
                        getMarketplaceColor(offer.marketplace)
                      )}
                    >
                      {offer.marketplace}
                    </span>
                    <span className="text-gray-600">{offer.seller}</span>
                  </div>
                  
                  <div className="text-right">
                    <div className="text-lg font-semibold text-gray-900">
                      {formatPrice(offer.total_price)}
                    </div>
                    <div className="text-sm text-gray-500">
                      상품가 {formatPrice(offer.price)} + 배송비 {formatPrice(offer.shipping_fee)}
                    </div>
                  </div>
                  
                  <a
                    href={offer.affiliate_url || offer.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-md transition-colors flex items-center gap-2"
                  >
                    <ExternalLink className="w-4 h-4" />
                    구매
                  </a>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
