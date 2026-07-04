@echo off
chcp 65001 >nul
REM ============================================================
REM  NPFJ 构建脚本（Windows）
REM  用法: 双击 build.bat
REM  输出: NPFJ-交付包.zip（不含 node_modules 和源码）
REM ============================================================

echo 📦 NPFJ 构建开始...

REM 1. 构建前端
echo 🔧 构建前端...
cd frontend
call npm install --silent
call npm run build
cd ..

REM 2. 检查 dist
if not exist "frontend\dist" (
    echo ❌ 前端构建失败
    pause
    exit /b 1
)

REM 3. 创建交付目录
echo 🗜️ 打包交付物...
mkdir _dist
copy run.py _dist\ >nul
xcopy /E /I /Q backend _dist\backend >nul
xcopy /E /I /Q frontend\dist _dist\frontend\dist >nul
xcopy /E /I /Q docs _dist\docs >nul

REM 清理 __pycache__
for /d /r "_dist\backend" %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d" >nul

REM 打包
powershell Compress-Archive -Path "_dist\*" -DestinationPath "NPFJ-交付包.zip" -Force

rmdir /s /q _dist >nul

echo ✅ 构建完成！交付包: NPFJ-交付包.zip
pause
