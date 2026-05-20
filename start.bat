@echo off
chcp 65001 >nul
echo ========================================
echo    SuperMarket v2 — Flask Backend
echo ========================================
pip install flask flask-cors 2>nul
echo.
echo Server ishga tushmoqda...
echo Brauzerda oching: http://localhost:5000
echo Toxtatish uchun: Ctrl+C
echo.
python main.py
pause
