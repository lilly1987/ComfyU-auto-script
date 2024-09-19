rem Set vram state to: NORMAL_VRAM
rem  --highvram --cache-classic --cache-lru 128
:top
..\python_embeded\python.exe -s ..\ComfyUI\main.py --cache-classic 
pause
goto top