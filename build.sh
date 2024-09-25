#!/bin/sh

rm -rf ./venv
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
pyinstaller main.py -n reviewpln
mkdir ~/.local/bin 2>/dev/null
rm ~/.local/bin/reviewpln
ln -s $(pwd)/dist/reviewpln/reviewpln ~/.local/bin/
deactivate
