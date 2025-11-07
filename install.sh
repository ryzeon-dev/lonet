#!/bin/bash

if [ "$(id -u)" != "0" ]; then
  echo "Must run as root"
  exit 1
fi

python3 -m venv venv
source venv/bin/activate

python3 -m pip install pyinstaller
pyinstaller --onefile ./src/main.py --name lonet

deactivate
mkdir -p bin

cp ./dist/lonet ./bin
rm -rf ./dist ./build ./lonet.spec ./venv

cp ./bin/lonet /usr/local/bin/lonet