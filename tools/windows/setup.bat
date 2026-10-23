@echo off
setlocal EnableExtensions
title fang-kham : one-time setup
echo ==========================================================
echo   fang-kham : one-time setup for this computer
echo   (collects new clips every night at 23:00)
echo ==========================================================
echo.
where winget >nul 2>nul
if errorlevel 1 goto nowinget
call :findtools
if defined GIT goto havegit
echo [1/6] Installing Git ...
winget install -e --id Git.Git --source winget --accept-source-agreements --accept-package-agreements
:havegit
call :findtools
if defined PY goto havepy
echo [2/6] Installing Python ...
winget install -e --id Python.Python.3.12 --source winget --scope user --accept-source-agreements --accept-package-agreements
:havepy
call :findtools
if defined NODE goto havenode
echo [3/6] Installing Node.js ...
winget install -e --id OpenJS.NodeJS.LTS --source winget --accept-source-agreements --accept-package-agreements
:havenode
call :findtools
if not defined GIT goto missing
if not defined PY goto missing
if not defined NODE goto missing

set "HOME_DIR=%USERPROFILE%\fang-kham"
echo [4/6] Getting the website files into %HOME_DIR% ...
if not exist "%HOME_DIR%\.git" "%GIT%" clone https://github.com/Jiradeem/fang-kham.git "%HOME_DIR%"
if not exist "%HOME_DIR%\.git" goto failed
cd /d "%HOME_DIR%"
if not exist ".venv\Scripts\python.exe" "%PY%" -m venv .venv
".venv\Scripts\python.exe" -m pip install --quiet --upgrade pip yt-dlp yt-dlp-ejs
if errorlevel 1 goto failed
"%GIT%" config user.name "fang-kham home computer"
"%GIT%" config user.email "actions@users.noreply.github.com"

echo.
echo [5/6] Sign in to GitHub. A browser window may open: choose "Sign in with your browser"
echo       and log in as Jiradeem, then come back here.
"%GIT%" push --dry-run origin main
if errorlevel 1 goto nologin

echo [6/6] Scheduling the nightly job (every day at 23:00) ...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$a = New-ScheduledTaskAction -Execute '%HOME_DIR%\tools\windows\run.bat'; $t = New-ScheduledTaskTrigger -Daily -At 23:00; $s = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable -AllowStartIfOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 9); Register-ScheduledTask -TaskName 'fang-kham clips' -Action $a -Trigger $t -Settings $s -Force | Out-Null"
if errorlevel 1 goto failed

echo.
echo ==========================================================
echo   DONE. The computer will collect clips every night at 23:00
echo   (leave it switched on and plugged in).
echo   Log file: %HOME_DIR%\collect.log
echo ==========================================================
echo.
choice /C YN /M "Start a first collection now (it runs for up to 7 hours)"
if errorlevel 2 goto end
schtasks /Run /TN "fang-kham clips" >nul
echo Started. It runs in the background; you can close this window.
echo Progress is written to %HOME_DIR%\collect.log
goto end

:nowinget
echo winget was not found. Please install "App Installer" from the Microsoft Store, then run this file again.
goto end
:missing
echo Something did not install. Close this window and run setup.bat again.
echo If it still fails, send a photo of this window to Claude.
goto end
:nologin
echo Could not sign in to GitHub. Run setup.bat again and sign in as Jiradeem.
goto end
:failed
echo Setup stopped because of an error. Send a photo of this window to Claude.
:end
echo.
pause
exit /b 0

:findtools
set "GIT="
set "PY="
set "NODE="
if exist "%ProgramFiles%\Git\cmd\git.exe" set "GIT=%ProgramFiles%\Git\cmd\git.exe"
if not defined GIT for /f "delims=" %%G in ('where git 2^>nul') do if not defined GIT set "GIT=%%G"
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
if not defined PY if exist "%ProgramFiles%\Python312\python.exe" set "PY=%ProgramFiles%\Python312\python.exe"
if exist "%ProgramFiles%\nodejs\node.exe" set "NODE=%ProgramFiles%\nodejs\node.exe"
if not defined NODE for /f "delims=" %%N in ('where node 2^>nul') do if not defined NODE set "NODE=%%N"
exit /b 0
