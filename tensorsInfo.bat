pushd %~dp0
:top
..\python_embeded\python.exe tensorsInfo.py %*
pause
rem goto top