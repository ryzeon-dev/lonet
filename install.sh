#!/bin/bash

if [ "$(id -u)" != "0" ]; then
  echo "Must run as root"
  exit 1
fi

mkdir build
cd build

cmake ../src/cpp/
make

mkdir -p /usr/local/share/lonet
cp libnet_if_binding.so /usr/local/share/lonet

cd ..
rm -rf ./build

python3 -m venv venv
source venv/bin/activate

python3 -m pip install pyinstaller
pyinstaller --onefile ./src/main.py --name lonet

deactivate
mkdir -p bin

cp ./dist/lonet ./bin
rm -rf ./dist ./build ./lonet.spec ./venv

cp ./bin/lonet /usr/local/bin/lonet