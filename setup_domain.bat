@echo off
title Mathruseva Foundation - Local Domain Setup
color 0A
echo ========================================
echo    Mathruseva Foundation
echo    Local Domain Setup
echo ========================================
echo.
echo Setting up local domain: mathruseva.local
echo.

cd /d "C:\Users\nehaj\CascadeProjects\mathruseva_foundation"

REM Add entry to hosts file
echo Adding entry to hosts file...
powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList '-Command \"Add-Content -Path \"$env:windir\System32\drivers\etc\hosts\" -Value \"127.0.0.1 mathruseva.local\"\"'"

echo.
echo Starting application on port 80...
echo You can now access: http://mathruseva.local
echo.

python -c "
import sys
sys.argv = ['secure_app.py']
exec(open('secure_app.py').read().replace('port=5000', 'port=80'))
"

pause
