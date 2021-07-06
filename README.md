# Overall description
Mbin is a bin tool of embedded system.
In an Embedded system,we ofen need to combine  multiple bin files,like Image,code,sound file or other data files we need.After combine them,we can burn them into our storage device like flash.You can use this tool to set bin files' offset address,set align bytes and convert specified bin file's bytes order.
#Environment
python 3.8.5
windows10
```
pip intsall tkinter
pip install os
pip install time
pip install pathlib
```
# Generate an executable file
```
pip install pyinstaller
pyintsaller -F -w .\mbin_tool.py
```
