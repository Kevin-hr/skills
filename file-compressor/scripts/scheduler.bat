@echo off
chcp 65001 >nul
REM 文件: scheduler.bat
REM 用途: 手动触发文件压缩任务

echo ============================================
echo       File Compressor - 手动执行
echo ============================================
echo.

REM 设置默认目标目录（可根据需要修改）
set TARGET_DIR=C:\Users\52648\Downloads

REM 询问目标目录
set /p USER_DIR="请输入目标目录 (直接回车使用默认目录 %TARGET_DIR%): "
if not "%USER_DIR%"=="" set TARGET_DIR=%USER_DIR%

echo.
echo 目标目录: %TARGET_DIR%
echo.

REM 询问运行模式
echo 选择运行模式:
echo   [1] 预览模式 (只显示将要压缩的文件)
echo   [2] 执行模式 (执行压缩)
choice /c 12 /n /m "请选择: "

if errorlevel 2 set MODE=auto
if errorlevel 1 set MODE=preview

echo.
echo 运行模式: %MODE%
echo.

REM 执行压缩脚本
python "%~dp0compress.py" --target "%TARGET_DIR%" --mode %MODE%

echo.
pause
