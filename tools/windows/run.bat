@echo off
setlocal EnableExtensions
rem Nightly job started by Task Scheduler ("fang-kham clips"). The work is done by tools\home_run.py.
cd /d "%~dp0..\.."
call :findtools
if not defined GIT echo Git not found >> collect.log & exit /b 1
if not defined NODE echo Node.js not found >> collect.log & exit /b 1
".venv\Scripts\python.exe" -X utf8 -I tools\home_run.py "%GIT%" "%NODE%" >> collect.log 2>&1 & exit /b

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
