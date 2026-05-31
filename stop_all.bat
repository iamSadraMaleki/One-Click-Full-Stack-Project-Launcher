@echo off
title Stopping All Services
echo ========================================
echo    Stopping All Services
echo ========================================
echo.

echo [1] Stopping Backend on port 8081...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8081 ^| findstr LISTENING') do (
    echo     Killing process %%a
    taskkill /F /PID %%a 2>nul
)

echo.
echo [2] Stopping Frontend on port 5173...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173 ^| findstr LISTENING') do (
    echo     Killing process %%a
    taskkill /F /PID %%a 2>nul
)

echo.
echo [3] Killing any remaining Java processes...
taskkill /F /IM java.exe 2>nul

echo.
echo [4] Killing any remaining Node processes...
taskkill /F /IM node.exe 2>nul

echo.
echo ========================================
echo    ✅ All Services Stopped Successfully!
echo ========================================
timeout /t 2 /nobreak >nul
exit