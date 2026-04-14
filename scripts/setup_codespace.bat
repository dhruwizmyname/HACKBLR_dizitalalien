@echo off
setlocal EnableExtensions EnableDelayedExpansion

set "ROOT_DIR=%~dp0.."
pushd "%ROOT_DIR%"

echo Installing Python dependencies...
py -m pip install --upgrade pip
if errorlevel 1 goto :error
py -m pip install -r requirements.txt
if errorlevel 1 goto :error

where gh >nul 2>&1
if not errorlevel 1 (
  gh extension list | findstr /C:"github/gh-copilot" >nul
  if errorlevel 1 (
    echo Installing GitHub Copilot CLI extension...
    gh extension install github/gh-copilot
    if errorlevel 1 goto :error
  )
)

where docker >nul 2>&1
if not errorlevel 1 (
  if not exist "qdrant_storage" mkdir "qdrant_storage"

  set "CONTAINER_ID="
  for /f "delims=" %%i in ('docker ps -aq -f "name=^hackblr-qdrant$"') do set "CONTAINER_ID=%%i"

  if defined CONTAINER_ID (
    set "RUNNING="
    for /f "delims=" %%i in ('docker inspect -f "{{.State.Running}}" hackblr-qdrant 2^>nul') do set "RUNNING=%%i"
    if /I not "!RUNNING!"=="true" (
      echo Starting existing Qdrant container...
      docker start hackblr-qdrant >nul
      if errorlevel 1 goto :error
    )
  ) else (
    echo Creating Qdrant container...
    docker run -d --name hackblr-qdrant -p 6333:6333 -p 6334:6334 -v "%CD%\qdrant_storage:/qdrant/storage" qdrant/qdrant >nul
    if errorlevel 1 goto :error
  )
)

echo Setup complete.
popd
exit /b 0

:error
echo Setup failed.
popd
exit /b 1
