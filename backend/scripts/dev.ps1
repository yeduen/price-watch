# =============================================================================
# Price Watch - Backend Development Script
# =============================================================================
# 이 스크립트는 백엔드 개발 환경을 설정하고 Django 서버를 실행합니다.

Write-Host "🚀 Price Watch Backend Development Setup" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# 현재 디렉토리를 프로젝트 루트로 변경
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $projectRoot

Write-Host "📁 Project Root: $projectRoot" -ForegroundColor Yellow

# 가상환경 확인 및 생성
if (-not (Test-Path ".venv")) {
    Write-Host "🔧 Creating virtual environment..." -ForegroundColor Blue
    py -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment. Please check Python installation." -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Virtual environment created successfully" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

# 가상환경 활성화
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
& ".\.venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# pip 업그레이드
Write-Host "🔧 Upgrading pip..." -ForegroundColor Blue
python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to upgrade pip" -ForegroundColor Red
    exit 1
}

# 의존성 설치
Write-Host "🔧 Installing dependencies..." -ForegroundColor Blue
pip install -r backend/requirements/requirements-dev.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green

# 환경변수 파일 확인
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Warning: .env file not found" -ForegroundColor Yellow
    Write-Host "   Please create .env file from .env.example" -ForegroundColor Yellow
    Write-Host "   Copy .env.example to .env and update the values" -ForegroundColor Yellow
}

# Django 프로젝트 확인
if (-not (Test-Path "backend/marketwatch/manage.py")) {
    Write-Host "⚠️  Warning: Django project not found in backend/marketwatch/" -ForegroundColor Yellow
    Write-Host "   Please create Django project first:" -ForegroundColor Yellow
    Write-Host "   cd backend && django-admin startproject marketwatch ." -ForegroundColor Yellow
    Write-Host "   Then run this script again" -ForegroundColor Yellow
    exit 1
}

# 데이터베이스 마이그레이션
Write-Host "🔧 Running database migrations..." -ForegroundColor Blue
python backend/marketwatch/manage.py migrate
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to run migrations" -ForegroundColor Red
    Write-Host "   Please check your database configuration" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Database migrations completed" -ForegroundColor Green

# 정적 파일 수집
Write-Host "🔧 Collecting static files..." -ForegroundColor Blue
python backend/marketwatch/manage.py collectstatic --noinput
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Warning: Failed to collect static files" -ForegroundColor Yellow
}

# 개발 서버 실행
Write-Host "🚀 Starting Django development server..." -ForegroundColor Green
Write-Host "   Server will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host ""

python backend/marketwatch/manage.py runserver 0.0.0.0:8000
