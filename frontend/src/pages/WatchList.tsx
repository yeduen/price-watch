import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Star, Trash2, Edit3, Loader2, AlertCircle, RefreshCw, Plus } from 'lucide-react'
import { watchApi } from '@/api/client'
import { formatPrice, formatDate } from '@/utils'
import type { Watch } from '@/types'

export function WatchList() {
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [editingWatch, setEditingWatch] = useState<Watch | null>(null)
  const [formData, setFormData] = useState({
    user_id: 1, // 임시 사용자 ID
    product: '',
    target_price: '',
  })
  
  const queryClient = useQueryClient()
  
  const { data: watches, isLoading, error, refetch } = useQuery({
    queryKey: ['watches'],
    queryFn: () => watchApi.getWatches(),
  })
  
  const deleteMutation = useMutation({
    mutationFn: (id: number) => watchApi.deleteWatch(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['watches'] })
    },
  })
  
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: any }) => watchApi.updateWatch(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['watches'] })
      setEditingWatch(null)
    },
  })
  
  const createMutation = useMutation({
    mutationFn: (data: any) => watchApi.createWatch(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['watches'] })
      setIsCreateModalOpen(false)
      setFormData({ user_id: 1, product: '', target_price: '' })
    },
  })
  
  const handleDelete = (id: number) => {
    if (confirm('정말로 이 모니터링을 삭제하시겠습니까?')) {
      deleteMutation.mutate(id)
    }
  }
  
  const handleEdit = (watch: Watch) => {
    setEditingWatch(watch)
    setFormData({
      user_id: watch.user_id,
      product: watch.product.id.toString(),
      target_price: watch.target_price.toString(),
    })
  }
  
  const handleUpdate = () => {
    if (editingWatch) {
      updateMutation.mutate({
        id: editingWatch.id,
        data: {
          target_price: parseFloat(formData.target_price),
        },
      })
    }
  }
  
  const handleCreate = () => {
    createMutation.mutate({
      user_id: formData.user_id,
      product: parseInt(formData.product),
      target_price: parseFloat(formData.target_price),
    })
  }
  
  const handleRetry = () => {
    refetch()
  }
  
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">모니터링 목록을 불러오는 중...</p>
        </div>
      </div>
    )
  }
  
  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            모니터링 목록을 불러올 수 없습니다
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
        {/* 헤더 */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">가격 모니터링</h1>
            <p className="text-gray-600">관심 상품의 가격 변동을 추적하세요</p>
          </div>
          
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            모니터링 추가
          </button>
        </div>
        
        {/* 모니터링 목록 */}
        {watches && watches.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {watches.map((watch) => (
              <div
                key={watch.id}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
              >
                {/* 상품 정보 */}
                <div className="mb-4">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-sm font-medium text-blue-600">
                      {watch.product.brand}
                    </span>
                    <span className="text-sm text-gray-500">
                      {watch.product.model_code}
                    </span>
                  </div>
                  
                  <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">
                    {watch.product.name}
                  </h3>
                </div>
                
                {/* 목표가 */}
                <div className="mb-4">
                  <div className="text-sm text-gray-600 mb-1">목표가</div>
                  <div className="text-2xl font-bold text-red-600">
                    {formatPrice(watch.target_price)}
                  </div>
                </div>
                
                {/* 현재 최저가 */}
                {watch.product.best_price && (
                  <div className="mb-4">
                    <div className="text-sm text-gray-600 mb-1">현재 최저가</div>
                    <div className="text-lg font-semibold text-gray-900">
                      {formatPrice(watch.product.best_price.total_price)}
                    </div>
                    
                    {/* 목표가 달성 여부 */}
                    {watch.product.best_price.total_price <= watch.target_price ? (
                      <div className="text-sm text-green-600 font-medium">
                        🎉 목표가 달성!
                      </div>
                    ) : (
                      <div className="text-sm text-gray-500">
                        {formatPrice(watch.product.best_price.total_price - watch.target_price)} 더 필요
                      </div>
                    )}
                  </div>
                )}
                
                {/* 상태 및 액션 */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded-full ${
                        watch.is_active
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {watch.is_active ? '활성' : '비활성'}
                    </span>
                    <span className="text-xs text-gray-500">
                      {formatDate(watch.created_at)}
                    </span>
                  </div>
                  
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleEdit(watch)}
                      className="p-2 text-gray-600 hover:text-blue-600 transition-colors"
                      title="수정"
                    >
                      <Edit3 className="w-4 h-4" />
                    </button>
                    
                    <button
                      onClick={() => handleDelete(watch.id)}
                      className="p-2 text-gray-600 hover:text-red-600 transition-colors"
                      title="삭제"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <Star className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              모니터링이 없습니다
            </h3>
            <p className="text-gray-600 mb-4">
              관심 있는 상품을 추가하여 가격 변동을 추적해보세요.
            </p>
            <button
              onClick={() => setIsCreateModalOpen(true)}
              className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-4 h-4" />
              첫 번째 모니터링 추가
            </button>
          </div>
        )}
        
        {/* 모니터링 추가 모달 */}
        {isCreateModalOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                모니터링 추가
              </h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    상품 ID
                  </label>
                  <input
                    type="number"
                    value={formData.product}
                    onChange={(e) => setFormData({ ...formData, product: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="상품 ID를 입력하세요"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    목표가
                  </label>
                  <input
                    type="number"
                    value={formData.target_price}
                    onChange={(e) => setFormData({ ...formData, target_price: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="목표가를 입력하세요"
                  />
                </div>
              </div>
              
              <div className="flex gap-3 mt-6">
                <button
                  onClick={() => setIsCreateModalOpen(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 font-medium rounded-md hover:border-gray-400 transition-colors"
                >
                  취소
                </button>
                
                <button
                  onClick={handleCreate}
                  disabled={!formData.product || !formData.target_price}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  추가
                </button>
              </div>
            </div>
          </div>
        )}
        
        {/* 모니터링 수정 모달 */}
        {editingWatch && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                모니터링 수정
              </h3>
              
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  목표가
                </label>
                <input
                  type="number"
                  value={formData.target_price}
                  onChange={(e) => setFormData({ ...formData, target_price: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <div className="flex gap-3">
                <button
                  onClick={() => setEditingWatch(null)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 font-medium rounded-md hover:border-gray-400 transition-colors"
                >
                  취소
                </button>
                
                <button
                  onClick={handleUpdate}
                  disabled={!formData.target_price}
                  className="flex-1 px-4 py-2 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  수정
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
