@echo off
REM Quick deployment setup script for Windows
REM Run: setup_deployment.bat

echo.
echo ==========================================
echo Movie Recommender - Deployment Setup
echo ==========================================
echo.

REM 1. Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)
echo SUCCESS: Python found
echo.

REM 2. Install dependencies
echo [2/5] Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo SUCCESS: Dependencies installed
echo.

REM 3. Create .env file
echo [3/5] Setting up environment...
if not exist .env (
    copy .env.example .env >nul
    echo SUCCESS: .env file created
    echo.
    echo IMPORTANT: Edit .env with your settings:
    echo   - Generate SECRET_KEY using command below
    echo   - Set DEBUG=False
    echo   - Set ALLOWED_HOSTS to your domain
    echo.
    echo To generate SECRET_KEY, run:
    echo   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    echo.
) else (
    echo SUCCESS: .env file already exists
    echo.
)

REM 4. Run migrations and collect static
echo [4/5] Running migrations...
python manage.py migrate --noinput >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Migration failed
    pause
    exit /b 1
)
echo SUCCESS: Migrations complete
echo.

echo [5/5] Collecting static files...
python manage.py collectstatic --noinput >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Static file collection failed
    pause
    exit /b 1
)
echo SUCCESS: Static files collected
echo.

REM Final check
python manage.py check >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo SETUP COMPLETE!
    echo ==========================================
    echo.
    echo Next steps:
    echo 1. Edit .env file with your settings
    echo 2. Test locally: python manage.py runserver
    echo 3. See DEPLOYMENT.md for deployment options
    echo.
    echo Deployment options:
    echo   - Heroku (easiest)
    echo   - Docker (flexible)
    echo   - AWS EC2 or other VPS
    echo   - DigitalOcean App Platform
    echo.
) else (
    echo.
    echo ==========================================
    echo SOME CHECKS FAILED
    echo ==========================================
    echo.
    echo Please review the errors above and try again.
    echo.
)

pause
