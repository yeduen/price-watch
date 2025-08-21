# =============================================================================
# Price Watch - Celery Worker Script
# =============================================================================
# 이 스크립트는 Celery 워커와 비트를 실행합니다.

Write-Host "🔄 Price Watch Celery Worker Setup" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# 현재 디렉토리를 프로젝트 루트로 변경
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $projectRoot

Write-Host "📁 Project Root: $projectRoot" -ForegroundColor Yellow

# 가상환경 확인
if (-not (Test-Path ".venv")) {
    Write-Host "❌ Virtual environment not found" -ForegroundColor Red
    Write-Host "   Please run dev.ps1 first to create virtual environment" -ForegroundColor Red
    exit 1
}

# 가상환경 활성화
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Blue
& ".\.venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# Django 프로젝트 확인
if (-not (Test-Path "backend/marketwatch/manage.py")) {
    Write-Host "❌ Django project not found" -ForegroundColor Red
    Write-Host "   Please create Django project first" -ForegroundColor Red
    exit 1
}

# 환경변수 파일 확인
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  Warning: .env file not found" -ForegroundColor Yellow
    Write-Host "   Please create .env file from .env.example" -ForegroundColor Yellow
}

# Redis 연결 확인
Write-Host "🔧 Checking Redis connection..." -ForegroundColor Blue
try {
    python -c "import redis; r = redis.Redis(host='localhost', port=6379, db=0); r.ping(); print('✅ Redis connection successful')"
    if ($LASTEXITCODE -ne 0) {
        throw "Redis connection failed"
    }
} catch {
    Write-Host "❌ Redis connection failed" -ForegroundColor Red
    Write-Host "   Please ensure Redis is running on localhost:6379" -ForegroundColor Red
    Write-Host "   Or update REDIS_URL in your .env file" -ForegroundColor Red
    exit 1
}

# Celery 설정 확인
Write-Host "🔧 Checking Celery configuration..." -ForegroundColor Blue
try {
    python -c "from marketwatch.celery import app; print('✅ Celery configuration loaded')"
    if ($LASTEXITCODE -ne 0) {
        throw "Celery configuration failed"
    }
} catch {
    Write-Host "❌ Celery configuration failed" -ForegroundColor Red
    Write-Host "   Please check your Celery configuration" -ForegroundColor Red
    exit 1
}

Write-Host "🚀 Starting Celery worker and beat..." -ForegroundColor Green
Write-Host "   Worker will process background tasks" -ForegroundColor Cyan
Write-Host "   Beat will schedule periodic tasks" -ForegroundColor Cyan
Write-Host "   Press Ctrl+C to stop both processes" -ForegroundColor Cyan
Write-Host ""

# 두 개의 PowerShell 창에서 각각 실행하는 옵션 제공
Write-Host "Choose execution mode:" -ForegroundColor Yellow
Write-Host "1. Single window (worker only)" -ForegroundColor Cyan
Write-Host "2. Single window (beat only)" -ForegroundColor Cyan
Write-Host "3. Open new windows for both" -ForegroundColor Cyan
Write-Host ""

$choice = Read-Host "Enter your choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host "🚀 Starting Celery worker..." -ForegroundColor Green
        python backend/marketwatch/manage.py celery worker -l info
    }
    "2" {
        Write-Host "🚀 Starting Celery beat..." -ForegroundColor Green
        python backend/marketwatch/manage.py celery beat -l info
    }
    "3" {
        Write-Host "🚀 Opening new windows for worker and beat..." -ForegroundColor Green
        
        # Worker 창 열기
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot'; .\.venv\Scripts\Activate.ps1; python backend/marketwatch/manage.py celery worker -l info" -WindowStyle Normal
        
        # Beat 창 열기
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$projectRoot'; .\.venv\Scripts\Activate.ps1; python backend/marketwatch/manage.py celery beat -l info" -WindowStyle Normal
        
        Write-Host "✅ Opened new windows for worker and beat" -ForegroundColor Green
        Write-Host "   You can close this window now" -ForegroundColor Cyan
    }
    default {
        Write-Host "❌ Invalid choice. Exiting..." -ForegroundColor Red
        exit 1
    }
}
