#!/bin/sh

python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
pyinstaller main.py -n reviewpln
rm -rf ./build ./venv
mkdir ~/.local/bin 2>/dev/null
ln -s $(pwd)/dist/reviewpln/reviewpln ~/.local/bin/
deactivate
