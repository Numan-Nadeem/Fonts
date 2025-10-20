@echo off
setlocal enabledelayedexpansion
echo Installing fonts...
echo This may take a while. Please wait...
echo.

set "fonts_dir=%WINDIR%\Fonts"
set "source_dir=E:\Fonts"

:: Require admin privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo Please run this script as Administrator.
    pause
    exit /b
)

:: Install .ttf fonts
for /r "%source_dir%" %%f in (*.ttf) do (
    echo Installing "%%~nxf"...
    copy "%%f" "%fonts_dir%" >nul
    reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "%%~nf (TrueType)" /t REG_SZ /d "%%~nxf" /f >nul
)

:: Install .otf fonts
for /r "%source_dir%" %%f in (*.otf) do (
    echo Installing "%%~nxf"...
    copy "%%f" "%fonts_dir%" >nul
    reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "%%~nf (OpenType)" /t REG_SZ /d "%%~nxf" /f >nul
)

echo.
echo Font installation complete.
pause
