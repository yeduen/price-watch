import { clsx, type ClassValue } from 'clsx'

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs)
}

export function formatPrice(price: number): string {
  return new Intl.NumberFormat('ko-KR', {
    style: 'currency',
    currency: 'KRW',
  }).format(price)
}

export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function getMarketplaceColor(marketplace: string): string {
  const colors: Record<string, string> = {
    '쿠팡': 'bg-orange-500',
    '11번가': 'bg-blue-500',
    'G마켓': 'bg-green-500',
    '옥션': 'bg-purple-500',
    '네이버': 'bg-green-600',
    '카카오': 'bg-yellow-500',
  }
  
  return colors[marketplace] || 'bg-gray-500'
}

export function generateMockPriceHistory(days: number = 30) {
  const data = []
  const basePrice = 1200000
  const today = new Date()
  
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)
    
    // 가격 변동 시뮬레이션 (±10%)
    const variation = (Math.random() - 0.5) * 0.2
    const price = Math.round(basePrice * (1 + variation))
    
    data.push({
      date: date.toISOString().split('T')[0],
      price,
      total_price: price + Math.round(Math.random() * 5000), // 배송비 변동
    })
  }
  
  return data
}
