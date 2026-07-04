@echo off
chcp 65001 > nul
title NPFJ 构建工具
echo ============================================
echo   NPFJ 项目构建脚本
echo   1. 构建前端 (Vue 3)
echo   2. PyInstaller 打包成单文件 EXE
echo ============================================
echo.

:: 设置项目根目录（脚本所在目录的上一级）
set ROOT=%~dp0..

:: Step 1: 构建前端
echo [1/2] 构建前端...
cd /d "%ROOT%\frontend"
if not exist "node_modules" (
    echo   → 安装前端依赖...
    call npm install
)
call npm run build
if %errorlevel% neq 0 (
    echo ❌ 前端构建失败
    pause
    exit /b 1
)
echo ✅ 前端构建完成 (frontend/dist/)
echo.

:: Step 2: PyInstaller 打包
echo [2/2] 打包 EXE...
cd /d "%ROOT%\backend"

:: 检查 PyInstaller
pip show pyinstaller > nul 2>&1
if %errorlevel% neq 0 (
    echo   → 安装 PyInstaller...
    pip install pyinstaller
)

echo   → 开始打包（约 1-2 分钟）...
"%APPDATA%\Python\Python313\Scripts\pyinstaller" build.spec --clean --onefile

if %errorlevel% neq 0 (
    echo ❌ 打包失败
    pause
    exit /b 1
)
echo.

:: 完成
echo ============================================
echo ✅ 打包完成！
echo   输出文件：backend\dist\NPFJ.exe
echo   双击运行后打开 http://localhost:8080
echo ============================================
pause
