@echo off

set "repertoire=%~dp0"

cd %repertoire%/code detecte/dependance

pip install -r requirements.txt

cd ..
cd ..

python setup.py build

cd %repertoire%/code detecte/dependance

python message.py

exit
