# run.ps1 - Запуск всего приложения одной командой
param(
    [switch]$Build,
    [switch]$Down,
    [switch]$Logs,
    [string]$Service
)

Write-Host "🎌 AnimeCore Docker Launcher" -ForegroundColor Cyan
Write-Host "========================================"

if ($Down) {
    Write-Host "🛑 Останавливаю все контейнеры..." -ForegroundColor Yellow
    docker-compose down
    exit 0
}

if ($Logs) {
    if ($Service) {
        Write-Host "📋 Логи сервиса: $Service" -ForegroundColor Yellow
        docker-compose logs -f $Service
    } else {
        Write-Host "📋 Логи всех сервисов" -ForegroundColor Yellow
        docker-compose logs -f
    }
    exit 0
}

# Проверяем Docker
try {
    docker --version | Out-Null
} catch {
    Write-Host "❌ Docker не установлен!" -ForegroundColor Red
    Write-Host "Скачай Docker Desktop: https://www.docker.com/products/docker-desktop/" -ForegroundColor Yellow
    exit 1
}

# Проверяем что Docker запущен
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker Desktop не запущен!" -ForegroundColor Red
    Write-Host "Запусти Docker Desktop и попробуй снова" -ForegroundColor Yellow
    exit 1
}

if ($Build) {
    Write-Host "🔨 Сборка контейнеров..." -ForegroundColor Yellow
    docker-compose build --no-cache
}

Write-Host "🚀 Запуск приложения..." -ForegroundColor Green
docker-compose up -d

Write-Host "⏳ Ожидание запуска сервисов..." -ForegroundColor Gray

# Ждем пока бэкенд станет здоровым
$backendReady = $false
$attempts = 0
$maxAttempts = 30

while (-not $backendReady -and $attempts -lt $maxAttempts) {
    $attempts++
    try {
        $status = docker-compose ps backend --format json | ConvertFrom-Json
        if ($status.State -eq "running" -and $status.Health -eq "healthy") {
            $backendReady = $true
            Write-Host "✅ Бэкенд запущен и здоров" -ForegroundColor Green
        } else {
            Write-Host "⏳ Бэкенд запускается... ($attempts/$maxAttempts)" -ForegroundColor Gray
            Start-Sleep -Seconds 2
        }
    } catch {
        Write-Host "⏳ Ожидание бэкенда... ($attempts/$maxAttempts)" -ForegroundColor Gray
        Start-Sleep -Seconds 2
    }
}

if (-not $backendReady) {
    Write-Host "⚠️  Бэкенд долго запускается, проверьте логи: .\run.ps1 -Logs backend" -ForegroundColor Yellow
}

# Ждем фронтенд
$frontendReady = $false
$attempts = 0

while (-not $frontendReady -and $attempts -lt 20) {
    $attempts++
    try {
        $status = docker-compose ps frontend --format json | ConvertFrom-Json
        if ($status.State -eq "running") {
            $frontendReady = $true
            Write-Host "✅ Фронтенд запущен" -ForegroundColor Green
        } else {
            Write-Host "⏳ Фронтенд запускается... ($attempts/20)" -ForegroundColor Gray
            Start-Sleep -Seconds 2
        }
    } catch {
        Start-Sleep -Seconds 2
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎉 ANIMECORE УСПЕШНО ЗАПУЩЕН!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🌐 Доступные сервисы:" -ForegroundColor Yellow
Write-Host "   Frontend:  http://localhost:5173" -ForegroundColor White
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "   Admin:     http://localhost:8000/admin" -ForegroundColor White
Write-Host "   API Test:  http://localhost:8000/api/test/" -ForegroundColor White
Write-Host "   API Anime: http://localhost:8000/api/anime/anime/" -ForegroundColor White
Write-Host ""
Write-Host "🐳 Состояние контейнеров:" -ForegroundColor Yellow
docker-compose ps
Write-Host ""
Write-Host "🔧 Управление:" -ForegroundColor Yellow
Write-Host "   Остановить:    .\run.ps1 -Down" -ForegroundColor Gray
Write-Host "   Просмотр логов: .\run.ps1 -Logs [сервис]" -ForegroundColor Gray
Write-Host "   Пересобрать:   .\run.ps1 -Build" -ForegroundColor Gray
Write-Host "   Пример:        .\run.ps1 -Logs backend" -ForegroundColor Gray
Write-Host ""
Write-Host "💡 Первый запуск может занять 2-3 минуты" -ForegroundColor Magenta

# Автоматически открываем браузер
Start-Sleep -Seconds 3
Write-Host ""
Write-Host "🌐 Открываю приложение в браузере..." -ForegroundColor Cyan
Start-Process "http://localhost:5173"