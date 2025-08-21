import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { generateMockPriceHistory } from '@/utils'

interface PriceChartProps {
  productId?: number
  days?: number
  className?: string
}

export function PriceChart({ productId, days = 30, className }: PriceChartProps) {
  // Mock 데이터 생성 (실제로는 API에서 가져올 예정)
  const data = generateMockPriceHistory(days)
  
  const formatYAxis = (value: number) => {
    return `${(value / 10000).toFixed(0)}만원`
  }
  
  const formatTooltip = (value: number, name: string) => {
    return [
      new Intl.NumberFormat('ko-KR', {
        style: 'currency',
        currency: 'KRW',
      }).format(value),
      name === 'price' ? '상품가' : '총가격',
    ]
  }
  
  return (
    <div className={className}>
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">가격 변동 추이</h3>
        <p className="text-sm text-gray-500">최근 {days}일간의 가격 변화</p>
      </div>
      
      <div className="bg-white p-4 rounded-lg border">
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="date" 
              stroke="#666"
              fontSize={12}
              tickFormatter={(value) => {
                const date = new Date(value)
                return `${date.getMonth() + 1}/${date.getDate()}`
              }}
            />
            <YAxis 
              stroke="#666"
              fontSize={12}
              tickFormatter={formatYAxis}
            />
            <Tooltip 
              formatter={formatTooltip}
              labelFormatter={(value) => {
                const date = new Date(value)
                return date.toLocaleDateString('ko-KR', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                })
              }}
            />
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke="#3b82f6" 
              strokeWidth={2}
              dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#3b82f6', strokeWidth: 2, fill: '#fff' }}
            />
            <Line 
              type="monotone" 
              dataKey="total_price" 
              stroke="#ef4444" 
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={{ fill: '#ef4444', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6, stroke: '#ef4444', strokeWidth: 2, fill: '#fff' }}
            />
          </LineChart>
        </ResponsiveContainer>
        
        {/* 범례 */}
        <div className="flex items-center justify-center gap-6 mt-4 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-3 h-0.5 bg-blue-500"></div>
            <span className="text-gray-600">상품가</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-0.5 bg-red-500" style={{ borderTop: '2px dashed #ef4444' }}></div>
            <span className="text-gray-600">총가격 (배송비 포함)</span>
          </div>
        </div>
      </div>
    </div>
  )
}
