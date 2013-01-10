mkdir dist

python "C:\dev\pyinstaller-1.5-rc1\Makespec.py" -F -w --icon=src\uniticons\flag.ico src\Stratego.py

python "C:\dev\pyinstaller-1.5-rc1\Build.py" Stratego.spec --buildpath=src\
