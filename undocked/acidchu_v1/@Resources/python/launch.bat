echo off
:run
cls
start /b  main.py
cls
choice /c yn /n /m Run again? (y/n)
if %errorlevel% equ 1 goto run
if %errorlevel% equ 2 exit