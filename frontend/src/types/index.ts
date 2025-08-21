export interface Product {
  id: number
  brand: string
  model_code: string
  name: string
  gtin?: string
  best_price?: {
    price: number
    total_price: number
    marketplace: string
    seller: string
  }
  offer_count: number
  marketplaces: string[]
  created_at: string
}

export interface Offer {
  id: number
  marketplace: string
  seller: string
  price: number
  shipping_fee: number
  total_price: number
  url: string
  affiliate_url?: string
  fetched_at: string
}

export interface PriceHistory {
  id: number
  price: number
  total_price: number
  recorded_at: string
}

export interface Watch {
  id: number
  user_id: number
  product: Product
  target_price: number
  is_active: boolean
  created_at: string
}

export interface SearchResult {
  query: string
  count: number
  products: Product[]
  offers: Offer[]
  best_price?: {
    price: number
    total_price: number
    marketplace: string
    seller: string
    product_id: number
  }
}

export interface ApiResponse<T> {
  data: T
  status: number
  message?: string
}
