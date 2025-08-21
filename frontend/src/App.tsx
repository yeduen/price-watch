import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Search } from '@/pages/Search'
import { ProductDetail } from '@/pages/ProductDetail'
import { WatchList } from '@/pages/WatchList'

// React Query 클라이언트 생성
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 5 * 60 * 1000, // 5분
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          <Route path="/" element={<Search />} />
          <Route path="/products/:id" element={<ProductDetail />} />
          <Route path="/watches" element={<WatchList />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  )
}

export default App
