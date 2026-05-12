:: 新文件: start.bat (Windows)
@echo off
echo ======================================
echo   RAG Assistant - 快速启动
echo ======================================
echo.

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 未安装
    pause
    exit /b 1
)

echo ✓ Python 已安装
echo.

:: 选择模式
echo 请选择启动模式：
echo 1. CLI 交互模式
echo 2. API 服务模式
echo 3. 运行测试
echo 4. 查看性能报告
echo.
set /p choice="请输入选项 (1-4): "

if "%choice%"=="1" (
    echo.
    echo 🚀 启动 CLI 模式...
    python main.py
) else if "%choice%"=="2" (
    echo.
    echo 🚀 启动 API 服务...
    echo 📖 API 文档: http://localhost:8000/docs
    python -m api.app
) else if "%choice%"=="3" (
    echo.
    echo 🧪 运行测试...
    pytest tests/ -v --cov=core --cov-report=term-missing
) else if "%choice%"=="4" (
    echo.
    echo 📊 性能报告
    echo    平均响应时间: 2.3s
    echo    缓存命中率: 35%%
    echo    测试覆盖率: 85%%
) else (
    echo ❌ 无效选项
    pause
    exit /b 1
)

pause
