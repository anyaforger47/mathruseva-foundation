@echo off
echo Testing Mathruseva Foundation Launcher
echo.
echo Current directory: %CD%
echo.

cd /d "C:\Users\nehaj\CascadeProjects\mathruseva_foundation"
echo Changed to: %CD%
echo.

echo Testing Python...
python --version
echo.

echo Testing secure_app.py exists...
if exist secure_app.py (
    echo secure_app.py found
) else (
    echo secure_app.py NOT found
)
echo.

echo Testing import...
python -c "print('Python test successful')"
echo.

echo Testing Flask import...
python -c "import flask; print('Flask import successful')"
echo.

echo Starting application in 3 seconds...
timeout /t 3 /nobreak

python secure_app.py

pause
