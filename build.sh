#!/bin/sh

rm -rf ./venv
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
pyinstaller main.py -n reviewpln
mkdir ~/.local/share/bin 2>/dev/null
rm ~/.local/share/bin/reviewpln 2>/dev/null
ln -s $(pwd)/dist/reviewpln/reviewpln ~/.local/share/bin/
deactivate
