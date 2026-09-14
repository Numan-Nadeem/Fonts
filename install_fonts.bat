@echo off
setlocal
rem Cross-platform installer lives in install_fonts.py (works on Windows,
rem macOS and Linux). This wrapper runs it on Windows with the bundled
rem python launcher, falling back to the legacy copy-and-register logic
rem if Python is unavailable.

set "SCRIPT_DIR=%~dp0"

where py >nul 2>&1
if not errorlevel 1 (
    py "%SCRIPT_DIR%install_fonts.py" %*
    goto :end
)

where python >nul 2>&1
if not errorlevel 1 (
    python "%SCRIPT_DIR%install_fonts.py" %*
    goto :end
)

echo Python not found - falling back to legacy installer.
echo For the best experience install Python 3, or visit:
echo   https://www.python.org/downloads/windows/
echo.

rem ---------------------------------------------------------------------
rem Legacy fallback: original copy + registry approach (system-wide,
rem requires this window to be running as Administrator).
rem ---------------------------------------------------------------------
setlocal enabledelayedexpansion
echo Installing fonts...
echo This may take a while. Please wait...
echo.

set "fonts_dir=%WINDIR%\Fonts"
set "source_dir=%~dp0"

net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo Please run this script as Administrator.
    pause
    exit /b 1
)

for /r "%source_dir%" %%f in (*.ttf) do (
    echo Installing "%%~nxf"...
    copy /y "%%f" "%fonts_dir%" >nul
    reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "%%~nf (TrueType)" /t REG_SZ /d "%%~nxf" /f >nul
)

for /r "%source_dir%" %%f in (*.otf) do (
    echo Installing "%%~nxf"...
    copy /y "%%f" "%fonts_dir%" >nul
    reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "%%~nf (OpenType)" /t REG_SZ /d "%%~nxf" /f >nul
)

echo.
echo Font installation complete.
pause

:end
endlocal
