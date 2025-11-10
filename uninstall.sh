#!/bin/bash

if [ "$(id -u)" != "0" ]; then
  echo "Must run as root"
  exit 1
fi

rm /usr/local/bin/lonet
rm -rf /usr/local/share/lonet