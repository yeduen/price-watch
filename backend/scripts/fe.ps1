# =============================================================================
# Price Watch - Frontend Development Script
# =============================================================================
# 이 스크립트는 프론트엔드 개발 환경을 설정하고 개발 서버를 실행합니다.

Write-Host "🎨 Price Watch Frontend Development Setup" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# 현재 디렉토리를 프로젝트 루트로 변경
$projectRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $projectRoot

Write-Host "📁 Project Root: $projectRoot" -ForegroundColor Yellow

# frontend 디렉토리로 이동
if (-not (Test-Path "frontend")) {
    Write-Host "❌ Frontend directory not found" -ForegroundColor Red
    Write-Host "   Please create frontend directory first" -ForegroundColor Red
    exit 1
}

Set-Location "frontend"
Write-Host "📁 Frontend Directory: $(Get-Location)" -ForegroundColor Yellow

# package.json 확인
if (-not (Test-Path "package.json")) {
    Write-Host "⚠️  Warning: package.json not found" -ForegroundColor Yellow
    Write-Host "   Please initialize frontend project first:" -ForegroundColor Yellow
    Write-Host "   npm init -y" -ForegroundColor Yellow
    Write-Host "   npm install react react-dom @types/react @types/react-dom" -ForegroundColor Yellow
    Write-Host "   npm install --save-dev vite @vitejs/plugin-react typescript" -ForegroundColor Yellow
    Write-Host "   Then run this script again" -ForegroundColor Yellow
    exit 1
}

# node_modules 확인 및 설치
if (-not (Test-Path "node_modules")) {
    Write-Host "🔧 Installing npm dependencies..." -ForegroundColor Blue
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install npm dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "✅ Dependencies already installed" -ForegroundColor Green
}

# 의존성 업데이트 확인
Write-Host "🔧 Checking for dependency updates..." -ForegroundColor Blue
npm outdated
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All dependencies are up to date" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some dependencies may be outdated" -ForegroundColor Yellow
    Write-Host "   Run 'npm update' to update them" -ForegroundColor Yellow
}

# 개발 서버 실행
Write-Host "🚀 Starting frontend development server..." -ForegroundColor Green
Write-Host "   Server will be available at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Cyan
Write-Host ""

# package.json의 scripts 확인
$packageJson = Get-Content "package.json" | ConvertFrom-Json
if ($packageJson.scripts.dev) {
    npm run dev
} elseif ($packageJson.scripts.start) {
    npm start
} else {
    Write-Host "❌ No dev or start script found in package.json" -ForegroundColor Red
    Write-Host "   Please add a dev script to package.json:" -ForegroundColor Red
    Write-Host "   \"scripts\": { \"dev\": \"vite\" }" -ForegroundColor Red
    exit 1
}
