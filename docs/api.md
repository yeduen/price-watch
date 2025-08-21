# Price Watch API 명세

## 개요

Price Watch API는 온라인 쇼핑 최저가 검색 및 모니터링 서비스를 위한 RESTful API입니다.

## 기본 정보

- **Base URL**: `http://localhost:8000/api/v1/`
- **Content-Type**: `application/json`
- **인증**: JWT Token (Bearer)
- **버전**: v1

## 인증

### JWT 토큰 발급

```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "username": "user@example.com",
  "password": "password123"
}
```

**응답:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "user@example.com",
    "email": "user@example.com"
  }
}
```

### 토큰 갱신

```http
POST /api/v1/auth/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 상품 검색

### 상품 검색

```http
GET /api/v1/search?q={query}&marketplace={marketplace}&limit={limit}
Authorization: Bearer {token}
```

**쿼리 파라미터:**
- `q` (필수): 검색할 상품명 또는 키워드
- `marketplace` (선택): 특정 마켓플레이스 (coupang, 11st, gmarket, auction)
- `limit` (선택): 결과 개수 (기본값: 20, 최대: 100)

**응답:**
```json
{
  "query": "삼성 갤럭시 S24",
  "total_count": 15,
  "best_price": {
    "price": 1200000,
    "shipping_fee": 0,
    "total_price": 1200000,
    "marketplace": "coupang",
    "seller": "삼성전자 공식몰"
  },
  "products": [
    {
      "id": 1,
      "name": "삼성 갤럭시 S24 128GB",
      "brand": "삼성",
      "model_code": "SM-S921N",
      "gtin": "8806092521234",
      "image_url": "https://...",
      "offers": [
        {
          "id": 1,
          "marketplace": "coupang",
          "seller": "삼성전자 공식몰",
          "price": 1200000,
          "shipping_fee": 0,
          "coupon_hint": "신용카드 5% 할인",
          "url": "https://...",
          "affiliate_url": "https://...",
          "fetched_at": "2024-01-15T10:30:00Z"
        }
      ]
    }
  ]
}
```

## 상품 관리

### 상품 상세 조회

```http
GET /api/v1/products/{id}/
Authorization: Bearer {token}
```

**응답:**
```json
{
  "id": 1,
  "name": "삼성 갤럭시 S24 128GB",
  "brand": "삼성",
  "model_code": "SM-S921N",
  "gtin": "8806092521234",
  "specifications": {
    "storage": "128GB",
    "color": "블랙",
    "screen_size": "6.2인치"
  },
  "image_url": "https://...",
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "offers": [...],
  "price_history": [
    {
      "date": "2024-01-15",
      "lowest_price": 1200000,
      "highest_price": 1250000,
      "average_price": 1225000
    }
  ]
}
```

### 상품 가격 히스토리

```http
GET /api/v1/products/{id}/price-history/?days={days}
Authorization: Bearer {token}
```

**쿼리 파라미터:**
- `days`: 조회할 일수 (기본값: 30, 최대: 365)

## 가격 모니터링

### 가격 감시 등록

```http
POST /api/v1/watches/
Authorization: Bearer {token}
Content-Type: application/json

{
  "product_id": 1,
  "target_price": 1100000,
  "notification_email": true,
  "notification_push": false
}
```

**응답:**
```json
{
  "id": 1,
  "product": {
    "id": 1,
    "name": "삼성 갤럭시 S24 128GB"
  },
  "target_price": 1100000,
  "current_price": 1200000,
  "notification_email": true,
  "notification_push": false,
  "is_active": true,
  "created_at": "2024-01-15T11:00:00Z"
}
```

### 가격 감시 목록

```http
GET /api/v1/watches/
Authorization: Bearer {token}
```

### 가격 감시 수정

```http
PATCH /api/v1/watches/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
  "target_price": 1050000,
  "is_active": false
}
```

### 가격 감시 삭제

```http
DELETE /api/v1/watches/{id}/
Authorization: Bearer {token}
```

## 오퍼 관리

### 오퍼 목록 조회

```http
GET /api/v1/offers/?product_id={product_id}&marketplace={marketplace}
Authorization: Bearer {token}
```

**쿼리 파라미터:**
- `product_id`: 상품 ID
- `marketplace`: 마켓플레이스 필터

### 오퍼 상세 조회

```http
GET /api/v1/offers/{id}/
Authorization: Bearer {token}
```

## 마켓플레이스

### 지원 마켓플레이스 목록

```http
GET /api/v1/marketplaces/
Authorization: Bearer {token}
```

**응답:**
```json
[
  {
    "id": "coupang",
    "name": "쿠팡",
    "logo_url": "https://...",
    "is_active": true,
    "last_sync": "2024-01-15T10:30:00Z"
  },
  {
    "id": "11st",
    "name": "11번가",
    "logo_url": "https://...",
    "is_active": true,
    "last_sync": "2024-01-15T10:25:00Z"
  }
]
```

## 사용자 관리

### 사용자 프로필

```http
GET /api/v1/users/profile/
Authorization: Bearer {token}
```

### 사용자 프로필 수정

```http
PATCH /api/v1/users/profile/
Authorization: Bearer {token}
Content-Type: application/json

{
  "email": "newemail@example.com",
  "notification_preferences": {
    "email": true,
    "push": false,
    "sms": false
  }
}
```

## 에러 응답

### 에러 형식

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "입력 데이터가 유효하지 않습니다.",
    "details": {
      "field_name": ["이 필드는 필수입니다."]
    }
  }
}
```

### HTTP 상태 코드

- `200`: 성공
- `201`: 생성됨
- `400`: 잘못된 요청
- `401`: 인증 실패
- `403`: 권한 없음
- `404`: 리소스 없음
- `429`: 요청 제한 초과
- `500`: 서버 오류

## 요청 제한

- **인증된 사용자**: 1000 requests/hour
- **미인증 사용자**: 100 requests/hour
- **검색 API**: 500 requests/hour

## 웹훅 (선택사항)

### 가격 알림 웹훅 등록

```http
POST /api/v1/webhooks/
Authorization: Bearer {token}
Content-Type: application/json

{
  "url": "https://your-domain.com/webhook",
  "events": ["price_drop", "watch_triggered"],
  "secret": "your-webhook-secret"
}
```

## SDK 및 라이브러리

### Python SDK

```bash
pip install pricewatch-sdk
```

```python
from pricewatch import PriceWatchClient

client = PriceWatchClient(api_key="your-api-key")
results = client.search("삼성 갤럭시 S24")
```

### JavaScript SDK

```bash
npm install pricewatch-sdk
```

```javascript
import { PriceWatchClient } from 'pricewatch-sdk';

const client = new PriceWatchClient('your-api-key');
const results = await client.search('삼성 갤럭시 S24');
```

## 지원 및 문의

- **API 문서**: `/api/docs/`
- **개발자 포럼**: [GitHub Discussions](https://github.com/your-repo/discussions)
- **이메일**: api-support@pricewatch.com
