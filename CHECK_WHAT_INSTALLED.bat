@echo off
echo ========================================
echo   CHECKING INSTALLED PACKAGES
echo ========================================
echo.

echo Checking via winget...
echo.

winget list Git.Git 2>&1 | findstr /i "Git"
if errorlevel 1 (
    echo   [MISSING] Git
) else (
    echo   [OK] Git is installed
)
echo.

winget list GitHub.cli 2>&1 | findstr /i "GitHub"
if errorlevel 1 (
    echo   [MISSING] GitHub CLI
) else (
    echo   [OK] GitHub CLI is installed
)
echo.

winget list Microsoft.VisualStudioCode 2>&1 | findstr /i "VisualStudioCode"
if errorlevel 1 (
    echo   [MISSING] VS Code
) else (
    echo   [OK] VS Code is installed
)
echo.

winget list Docker.DockerDesktop 2>&1 | findstr /i "Docker"
if errorlevel 1 (
    echo   [MISSING] Docker Desktop
) else (
    echo   [OK] Docker Desktop is installed
)
echo.

winget list Python.Python.3.12 2>&1 | findstr /i "Python"
if errorlevel 1 (
    echo   [MISSING] Python 3.12
) else (
    echo   [OK] Python 3.12 is installed
)
echo.

winget list OpenJS.NodeJS.LTS 2>&1 | findstr /i "NodeJS"
if errorlevel 1 (
    echo   [MISSING] Node.js LTS
) else (
    echo   [OK] Node.js LTS is installed
)
echo.

echo ========================================
echo   CHECKING PATH AVAILABILITY
echo ========================================
echo.

where git >nul 2>&1
if errorlevel 1 (
    echo   [NOT IN PATH] Git
) else (
    echo   [IN PATH] Git
    git --version
)
echo.

where gh >nul 2>&1
if errorlevel 1 (
    echo   [NOT IN PATH] GitHub CLI
) else (
    echo   [IN PATH] GitHub CLI
    gh --version
)
echo.

where code >nul 2>&1
if errorlevel 1 (
    echo   [NOT IN PATH] VS Code
) else (
    echo   [IN PATH] VS Code
    code --version
)
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo   [NOT IN PATH] Python - may need to restart terminal
) else (
    echo   [IN PATH] Python
    python --version
)
echo.

where node >nul 2>&1
if errorlevel 1 (
    echo   [NOT IN PATH] Node.js - may need to restart terminal
) else (
    echo   [IN PATH] Node.js
    node --version
)
echo.

pause
