import axios from 'axios'
import type { SearchResult, Product, Offer, PriceHistory, Watch } from '@/types'

const apiClient = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const searchApi = {
  search: async (query: string): Promise<SearchResult> => {
    const response = await apiClient.get(`/search/?q=${encodeURIComponent(query)}`)
    return response.data
  },
}

export const productApi = {
  getProducts: async (): Promise<Product[]> => {
    const response = await apiClient.get('/products/')
    return response.data.results
  },
  
  getProduct: async (id: number): Promise<Product> => {
    const response = await apiClient.get(`/products/${id}/`)
    return response.data
  },
}

export const offerApi = {
  getOffers: async (productId?: number): Promise<Offer[]> => {
    const params = productId ? `?product_id=${productId}` : ''
    const response = await apiClient.get(`/offers/${params}`)
    return response.data.results
  },
}

export const priceHistoryApi = {
  getPriceHistory: async (offerId?: number): Promise<PriceHistory[]> => {
    const params = offerId ? `?offer_id=${offerId}` : ''
    const response = await apiClient.get(`/price-history/${params}`)
    return response.data.results
  },
}

export const watchApi = {
  getWatches: async (userId?: number): Promise<Watch[]> => {
    const params = userId ? `?user_id=${userId}` : ''
    const response = await apiClient.get(`/watches/${params}`)
    return response.data.results
  },
  
  createWatch: async (data: { user_id: number; product: number; target_price: number }): Promise<Watch> => {
    const response = await apiClient.post('/watches/', data)
    return response.data
  },
  
  updateWatch: async (id: number, data: { target_price?: number; is_active?: boolean }): Promise<Watch> => {
    const response = await apiClient.patch(`/watches/${id}/`, data)
    return response.data
  },
  
  deleteWatch: async (id: number): Promise<void> => {
    await apiClient.delete(`/watches/${id}/`)
  },
}

export default apiClient
