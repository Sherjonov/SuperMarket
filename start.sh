#!/bin/bash
echo "========================================"
echo "   SuperMarket v2 — Flask Backend"
echo "========================================"
pip install flask flask-cors 2>/dev/null | tail -1
echo ""
echo "Server ishga tushmoqda..."
echo "Brauzerda oching: http://localhost:5000"
echo "Toxtatish uchun: Ctrl+C"
echo ""
python main.py
