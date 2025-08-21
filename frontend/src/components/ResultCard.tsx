import { ExternalLink, ShoppingCart, Star } from 'lucide-react'
import type { Product } from '@/types'
import { formatPrice, getMarketplaceColor, cn } from '@/utils'

interface ResultCardProps {
  product: Product
  onWatchClick?: (product: Product) => void
}

export function ResultCard({ product, onWatchClick }: ResultCardProps) {
  const { best_price, offer_count, marketplaces } = product
  
  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 overflow-hidden">
      {/* 상품 이미지 */}
      <div className="aspect-square bg-gray-100 flex items-center justify-center">
        <div className="text-gray-400 text-4xl">📱</div>
      </div>
      
      {/* 상품 정보 */}
      <div className="p-4">
        {/* 브랜드 & 모델 */}
        <div className="flex items-center gap-2 mb-2">
          <span className="text-sm font-medium text-blue-600">{product.brand}</span>
          <span className="text-sm text-gray-500">{product.model_code}</span>
        </div>
        
        {/* 상품명 */}
        <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
          {product.name}
        </h3>
        
        {/* 최저가 */}
        {best_price && (
          <div className="mb-3">
            <div className="text-2xl font-bold text-red-600">
              {formatPrice(best_price.total_price)}
            </div>
            <div className="text-sm text-gray-500">
              배송비 포함
            </div>
          </div>
        )}
        
        {/* 마켓플레이스 배지 */}
        <div className="flex flex-wrap gap-2 mb-3">
          {marketplaces.map((marketplace) => (
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
        
        {/* 오퍼 개수 */}
        <div className="flex items-center gap-1 text-sm text-gray-500 mb-4">
          <ShoppingCart className="w-4 h-4" />
          <span>{offer_count}개 오퍼</span>
        </div>
        
        {/* 액션 버튼 */}
        <div className="flex gap-2">
          {best_price && (
            <a
              href={best_price.affiliate_url || '#'}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 px-4 rounded-md flex items-center justify-center gap-2 transition-colors"
            >
              <ExternalLink className="w-4 h-4" />
              구매하기
            </a>
          )}
          
          <button
            onClick={() => onWatchClick?.(product)}
            className="px-4 py-2 border border-gray-300 hover:border-gray-400 text-gray-700 text-sm font-medium rounded-md transition-colors"
          >
            <Star className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  )
}
