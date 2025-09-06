@echo off
chcp 65001 > nul
echo 🚀 AI Discovery Quick Push Script
echo =======================================

cd /d "%~dp0"
python scripts/quick_push.py

echo.
echo ✅ Script execution completed!
pause