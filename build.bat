echo on
setlocal enabledelayedexpansion
SET arg=
for %%f in (UiInit\*.py) do SET arg=!arg! --hidden-import UiInit.%%~nf
pyinstaller -F Main.py %arg% --add-data "AGENCYR.TTF;."