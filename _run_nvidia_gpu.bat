rem Set vram state to: NORMAL_VRAM
rem  --highvram --cache-classic 
:top
..\python_embeded\python.exe -s ..\ComfyUI\main.py --cache-lru 128
pause
goto top