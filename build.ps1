venv/Scripts/python.exe -m PyInstaller `
--onefile  `
--windowed `
--clean `
--noupx `
--add-data "assets;assets" `
--add-data "map;map" `
main.py