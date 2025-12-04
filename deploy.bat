@echo off
echo ========================================
echo  Live Pencil Sketch - GitHub Deploy
echo ========================================
echo.

REM Check if git is initialized
if not exist .git (
    echo Initializing Git repository...
    git init
    git branch -M main
)

echo.
echo Adding files to Git...
git add .

echo.
set /p commit_msg="Enter commit message (or press Enter for default): "
if "%commit_msg%"=="" set commit_msg=Update Live Pencil Sketch

echo.
echo Committing changes...
git commit -m "%commit_msg%"

echo.
echo.
echo ========================================
echo  NEXT STEPS:
echo ========================================
echo.
echo 1. Create a GitHub repository at:
echo    https://github.com/new
echo.
echo 2. Copy this command and replace YOUR_USERNAME:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/live-pencil-sketch.git
echo.
echo 3. Then run:
echo    git push -u origin main
echo.
echo 4. Deploy on Render:
echo    - Go to https://render.com
echo    - Click "New +" - "Web Service"
echo    - Connect your GitHub repo
echo    - Build: pip install -r requirements.txt
echo    - Start: gunicorn app:app --timeout 120 --workers 2
echo.
echo ========================================
echo.
pause
