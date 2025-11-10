#!/bin/bash

if [ "$(id -u)" != "0" ]; then
  echo "Must run as root"
  exit 1
fi

echo "Preparing to compile C++ source"
mkdir build
cd build

echo "Building Makefile"
cmake ../src/cpp/ &> /dev/null

if [ "$?" != "0" ]; then
  echo "Error while building Makefile. Exiting"
  exit 1
fi

echo "Compiling..."
make &> /dev/null
if [ "$?" != "0" ]; then
  echo "Error while compiling C++ source. Exiting"
  exit 1
fi

echo "Installing C++ shared object "
mkdir -p /usr/local/share/lonet
cp libnet_if_binding.so /usr/local/share/lonet

cd ..
rm -rf ./build

echo "Creating Python3 virtual environment"
python3 -m venv venv
source venv/bin/activate

echo "Installing pyinstaller dependency into venv"
python3 -m pip install pyinstaller &> /dev/null

if [ "$?" != "0" ]; then
  echo "Cannot install pyinstaller. Exiting"
  exit 1
fi

echo "Compiling python source..."
pyinstaller --onefile ./src/main.py --name lonet &> /dev/null
if [ "$?" != "0" ]; then
  echo "Error while compiling python source. Exiting"
  exit 1
fi

deactivate
mkdir -p bin

cp ./dist/lonet ./bin
rm -rf ./dist ./build ./lonet.spec ./venv

echo "Installing compiled binary"
cp ./bin/lonet /usr/local/bin/lonet