@echo off
chcp 65001 > nul
echo 🚀 AI Discovery Quick Push Script
echo =======================================

cd /d "%~dp0"

REM Check if Python is available
where python > nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found in PATH. Using simple git commands instead...
    echo.
    goto :simple_push
) else (
    echo ✅ Python found, using quick_push.py script...
    python scripts/quick_push.py
    goto :end
)

:simple_push
echo Using simple git push method...
echo.

REM Get commit message from user
set /p commit_msg="Enter commit message (or press Enter for auto message): "

if "%commit_msg%"=="" (
    set "commit_msg=📝 Auto-commit: Update AI Discovery project files"
)

echo.
echo Adding files...
git add .

echo Creating commit with message: %commit_msg%
git commit -m "%commit_msg%"

echo Pushing to GitHub...
git push origin main

echo.
echo ✅ Push completed successfully!

:end
echo.
echo ✅ Script execution completed!
pause