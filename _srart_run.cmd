@echo off
rem set-executionPolicy remoteSigned
pushd %~dp0
:top
powershell -executionPolicy bypass -file ".\srart_run.ps1" %*
rem pause
rem goto top