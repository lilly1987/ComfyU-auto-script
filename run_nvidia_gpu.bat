rem Set vram state to: NORMAL_VRAM
rem --cache-lru 64 --highvram
:top
..\python_embeded\python.exe -s ..\ComfyUI\main.py --cache-classic 
pause
goto top