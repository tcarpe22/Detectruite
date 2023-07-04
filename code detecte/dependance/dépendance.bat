@echo off

set "repertoire=%~dp0"

cd %repertoire%


pip install -r requirements.txt



python message.py

python -i Fish_track.py

exit