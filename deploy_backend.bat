@echo off
echo 🚀 OpenWebUI Backend Deployment Script for Windows
echo ===================================================

echo.
echo 🔍 Checking prerequisites...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.11 or later.
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if backend-render directory exists
if not exist "backend-render" (
    echo ❌ backend-render directory not found!
    echo Please run this script from your project root directory.
    pause
    exit /b 1
)

echo ✅ backend-render directory found

REM Check if requirements.txt exists
if not exist "backend-render\requirements.txt" (
    echo ❌ requirements.txt not found!
    pause
    exit /b 1
)

echo ✅ requirements.txt found

echo.
echo 🔧 Running deployment preparation script...
python deploy_backend.py

if %errorlevel% neq 0 (
    echo ❌ Deployment preparation failed!
    pause
    exit /b 1
)

echo.
echo ✅ Deployment preparation completed successfully!
echo.
echo 📋 Next steps:
echo 1. Push your code to GitHub
echo 2. Go to Render.com and create a new web service
echo 3. Connect your GitHub repository
echo 4. Use the generated render.yaml configuration
echo 5. Set your environment variables
echo 6. Deploy!
echo.
echo 📚 See COMPLETE_DEPLOYMENT_GUIDE.md for detailed instructions
echo.
pause
