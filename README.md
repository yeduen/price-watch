# 온라인 쇼핑 최저가 자동 검색기 (Price Watch)

동일 상품을 다중 마켓에서 탐색하여 최저가를 산출하고, 제휴 링크를 제공하며, 가격 변동 시 알림을 보내는 온라인 쇼핑 최저가 검색 서비스입니다.

## 🎯 주요 기능

- **다중 마켓 검색**: 쿠팡, 11번가 등 주요 마켓플레이스에서 동일 상품 검색
- **최저가 산출**: 배송비, 쿠폰 등을 고려한 체감가 계산
- **제휴 링크**: 수익 창출을 위한 제휴 링크 제공
- **가격 모니터링**: 설정한 목표가 도달 시 이메일/푸시 알림
- **브라우저 확장**: 현재 페이지 상품의 최저가 정보 사이드패널 제공

## 🏗 프로젝트 구조

```
price-watch/
├── backend/                 # Django 백엔드
│   ├── marketwatch/        # Django 프로젝트 루트
│   ├── apps/               # Django 앱들
│   │   ├── core/          # 공통 유틸, 예외, 설정
│   │   ├── catalog/       # 상품, 오퍼, 매칭
│   │   ├── affiliate/     # 제휴 링크/리포트
│   │   └── alerts/        # 감시/알림
│   ├── requirements/       # Python 의존성
│   ├── scripts/           # Windows PowerShell 스크립트
│   └── tests/             # 테스트 코드
├── frontend/               # React 프론트엔드
│   ├── src/               # 소스 코드
│   └── public/            # 정적 파일
├── extensions/             # 브라우저 확장
│   └── chrome/            # Chrome 확장 (Manifest V3)
├── ops/                    # 배포/운영 도구
│   ├── docker/            # Docker 설정
│   └── ci/                # CI/CD 설정
└── docs/                   # API 명세, ERD, 설계 문서
```

## 🚀 빠른 시작 (Windows)

### 1. 백엔드 실행

```powershell
# 가상환경 생성 및 활성화
py -m venv .venv
.\.venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r backend/requirements/requirements-dev.txt

# 데이터베이스 마이그레이션
python backend/manage.py migrate

# 개발 서버 실행
python backend/manage.py runserver 0.0.0.0:8000
```

또는 스크립트 사용:
```powershell
.\backend\scripts\dev.ps1
```

### 2. 프론트엔드 실행

```powershell
cd frontend
npm install
npm run dev
```

또는 스크립트 사용:
```powershell
.\backend\scripts\fe.ps1
```

### 3. Celery 워커 실행 (백그라운드 작업)

```powershell
.\backend\scripts\worker.ps1
```

### 4. 브라우저 확장 로드

1. Chrome에서 `chrome://extensions/` 접속
2. 개발자 모드 활성화
3. "압축해제된 확장 프로그램을 로드합니다" 클릭
4. `extensions/chrome` 폴더 선택

## 🔧 환경 설정

`.env.example` 파일을 참고하여 `.env` 파일을 생성하고 필요한 환경변수를 설정하세요:

- `APP_ENV`: 환경 (local/dev/prod)
- `SECRET_KEY`: Django 시크릿 키
- `DB_URL`: PostgreSQL 데이터베이스 URL
- `REDIS_URL`: Redis URL
- `AFFIL_COUPANG_KEY`: 쿠팡 제휴 API 키
- `AFFIL_11ST_KEY`: 11번가 제휴 API 키

## 📚 API 문서

- API 명세: `docs/api.md`
- 데이터베이스 설계: `docs/erd.md`

## 🧪 테스트

```powershell
# 백엔드 테스트
python backend/manage.py test

# 프론트엔드 테스트
cd frontend
npm test
```

## 📝 개발 가이드

- **백엔드**: Django REST Framework 기반 API 개발
- **프론트엔드**: React + TypeScript + Vite
- **데이터베이스**: PostgreSQL + Redis
- **배포**: Docker + AWS EC2

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
