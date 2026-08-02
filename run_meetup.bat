@echo off
setlocal

cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
) else (
    set "PYTHON=py"
)

set "DJANGO_SETTINGS_MODULE=meetup_site.settings_sqlite"

echo Using %PYTHON%
echo Using %DJANGO_SETTINGS_MODULE%
echo.

%PYTHON% manage.py migrate --noinput
if errorlevel 1 (
    echo.
    echo Failed to apply migrations.
    exit /b 1
)

%PYTHON% manage.py runserver
set "EXIT_CODE=%ERRORLEVEL%"

endlocal & exit /b %EXIT_CODE%