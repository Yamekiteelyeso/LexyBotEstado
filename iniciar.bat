@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %errorlevel%==0 (
    py -3 -m pip install -r requirements.txt || goto error
    if not exist config.json copy config.example.json config.json >nul
    py -3 main.py
) else (
    python -m pip install -r requirements.txt || goto error
    if not exist config.json copy config.example.json config.json >nul
    python main.py
)
pause
exit /b 0
:error
echo.
echo No se pudo instalar o ejecutar LexyBotEstado.
pause
exit /b 1
