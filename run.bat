@echo off
echo 🎌 AnimeCore Docker Launcher
echo ========================================

REM Проверяем аргументы
if "%1%"=="down" (
    echo 🛑 Останавливаю все контейнеры...
    docker-compose down
    pause
    exit /b 0
)

if "%1%"=="logs" (
    if not "%2%"=="" (
        echo 📋 Логи сервиса: %2%
        docker-compose logs -f %2%
    ) else (
        echo 📋 Логи всех сервисов
        docker-compose logs -f
    )
    pause
    exit /b 0
)

if "%1%"=="build" (
    echo 🔨 Сборка контейнеров...
    docker-compose build --no-cache
)

echo 🚀 Запуск приложения...
docker-compose up -d

echo ⏳ Ожидание запуска сервисов...

REM Небольшая пауза
timeout /t 10 /nobreak > nul

echo.
echo ========================================
echo 🎉 ANIMECORE УСПЕШНО ЗАПУЩЕН!
echo ========================================
echo.
echo 🌐 Доступные сервисы:
echo    Frontend:  http://localhost:5173
echo    Backend:   http://localhost:8000
echo    Admin:     http://localhost:8000/admin
echo    API Test:  http://localhost:8000/api/test/
echo.
echo 🐳 Состояние контейнеров:
docker-compose ps
echo.
echo 🔧 Управление:
echo    Остановить:    run.bat down
echo    Просмотр логов: run.bat logs [сервис]
echo    Пересобрать:   run.bat build
echo.
echo 💡 Первый запуск может занять 2-3 минуты
echo.

REM Автоматически открываем браузер
timeout /t 3 /nobreak > nul
start http://localhost:5173

echo Нажми любую клавишу для просмотра логов или Ctrl+C для выхода...
pause
docker-compose logs -f