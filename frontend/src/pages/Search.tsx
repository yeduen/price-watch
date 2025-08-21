import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Search as SearchIcon, Loader2, AlertCircle, RefreshCw } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { ResultCard } from '@/components/ResultCard'
import { searchApi } from '@/api/client'
import type { Product } from '@/types'

export function Search() {
  const [query, setQuery] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const navigate = useNavigate()
  
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['search', searchTerm],
    queryFn: () => searchApi.search(searchTerm),
    enabled: !!searchTerm,
    staleTime: 5 * 60 * 1000, // 5분
  })
  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      setSearchTerm(query.trim())
    }
  }
  
  const handleWatchClick = (product: Product) => {
    navigate(`/products/${product.id}`)
  }
  
  const handleRetry = () => {
    refetch()
  }
  
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* 검색 헤더 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🛒 Price Watch
          </h1>
          <p className="text-lg text-gray-600">
            온라인 쇼핑 최저가 자동 검색기
          </p>
        </div>
        
        {/* 검색 폼 */}
        <form onSubmit={handleSearch} className="max-w-2xl mx-auto mb-8">
          <div className="flex gap-2">
            <div className="flex-1 relative">
              <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="상품명, 브랜드, 모델명을 입력하세요..."
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button
              type="submit"
              disabled={!query.trim() || isLoading}
              className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                '검색'
              )}
            </button>
          </div>
        </form>
        
        {/* 검색 결과 */}
        {searchTerm && (
          <div>
            <div className="mb-6">
              <h2 className="text-2xl font-semibold text-gray-900">
                "{searchTerm}" 검색 결과
              </h2>
              {data && (
                <p className="text-gray-600">
                  총 {data.count}개의 상품을 찾았습니다.
                </p>
              )}
            </div>
            
            {/* 로딩 상태 */}
            {isLoading && (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
                <span className="ml-2 text-gray-600">검색 중...</span>
              </div>
            )}
            
            {/* 에러 상태 */}
            {error && (
              <div className="text-center py-12">
                <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  검색 중 오류가 발생했습니다
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
            )}
            
            {/* 결과가 없는 경우 */}
            {!isLoading && !error && data && data.count === 0 && (
              <div className="text-center py-12">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  검색 결과가 없습니다
                </h3>
                <p className="text-gray-600">
                  다른 키워드로 검색해보세요.
                </p>
              </div>
            )}
            
            {/* 검색 결과 그리드 */}
            {!isLoading && !error && data && data.count > 0 && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {data.products.map((product) => (
                  <ResultCard
                    key={product.id}
                    product={product}
                    onWatchClick={handleWatchClick}
                  />
                ))}
              </div>
            )}
          </div>
        )}
        
        {/* 초기 상태 */}
        {!searchTerm && (
          <div className="text-center py-12">
            <div className="text-6xl mb-4">📱</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              상품을 검색해보세요
            </h3>
            <p className="text-gray-600">
              상품명, 브랜드, 모델명으로 검색하면<br />
              여러 마켓플레이스의 최저가를 비교할 수 있습니다.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
