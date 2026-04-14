@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT_DIR=%~dp0.."
pushd "%ROOT_DIR%"

:: 1. Check Python Dependencies
echo Checking Python dependencies...
:: Read through requirements.txt and check if each package is installed
for /f "tokens=1 delims==<>" %%a in (requirements.txt) do (
    py -m pip show %%a >nul 2>&1
    if errorlevel 1 (
        echo Package %%a missing. Installing requirements...
        py -m pip install -r requirements.txt
        goto :next_step
    )
)
echo Python dependencies are already up to date.

:next_step
:: 2. Check GitHub Copilot CLI Extension
where gh >nul 2>&1
if not errorlevel 1 (
    gh extension list | findstr /C:"github/gh-copilot" >nul
    if errorlevel 1 (
        echo Installing GitHub Copilot CLI extension...
        gh extension install github/gh-copilot
    ) else (
        echo GitHub Copilot CLI already installed.
    )
)

:: 3. Docker & Qdrant Configuration
where docker >nul 2>&1
if not errorlevel 1 (
    if not exist "qdrant_storage" mkdir "qdrant_storage"
    
    :: Check if the hackblr-qdrant container exists
    docker ps -aq -f "name=^hackblr-qdrant$" >nul
    if not errorlevel 1 (
        :: Check if the container is currently running
        for /f "delims=" %%i in ('docker inspect -f "{{.State.Running}}" hackblr-qdrant 2^>nul') do set "RUNNING=%%i"
        if /I "!RUNNING!"=="false" (
            echo Starting Qdrant...
            docker start hackblr-qdrant >nul
        ) else (
            echo Qdrant container is already running.
        )
    ) else (
        echo Creating new Qdrant container...
        docker run -d --name hackblr-qdrant -p 6333:6333 -p 6334:6334 -v "%CD%\qdrant_storage:/qdrant/storage" qdrant/qdrant >nul
    )
)

echo Setup check complete.
popd
exit /b 0

:error
echo Setup failed.
popd
exit /b 1
