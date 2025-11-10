<p align="center">
<img alt="Version Badge" src="https://img.shields.io/badge/dev--version-v1.1.0-16a085">
<img alt="Version Badge" src="https://img.shields.io/badge/release-v1.1.0-16a085">
<img alt="License Badge" src="https://img.shields.io/github/license/ryzeon-dev/bmdns?color=16a085">
<img alt="Language Badge" src="https://img.shields.io/badge/python3-16a085?logo=python&logoColor=16a085&labelColor=5a5a5a">
<img alt="Language Badge" src="https://img.shields.io/badge/c++-16a085?logo=cplusplus&logoColor=16a085&labelColor=5a5a5a">
</p>

# LONET
Linux local network information tool written in Python and C++

## Install
### Install DEB package
```commandline
wget https://github.com/ryzeon-dev/lonet/releases/download/v1.1.0/lonet_1.1.0_amd64.deb && sudo dpkg -i ./lonet_*_amd64.deb 
```

### Compile from source
run the compilation and installation script as root
```commandline
sudo bash install.sh
```

## Uninstall
run the uninstallation script as root
```commandline
sudo bash uninstall.sh
```

## Usage
```
$ lonet --help
lonet: local network information tool
usage: lonet [OPTIONS]
options:
    -a --all                Shows network interfaces information and relative open ports
    -h --help               Shows this message and exits
    -i --interfaces         Shows network interfaces information
    -p --ports [tcp|udp]    Shows open ports of specified protocol, if omitted shows both
    -virt                   Only show virtual network interfaces
    -phy                    Only show physical network interfaces
    -V --version            Shows version number and exits
if no option is specified, shows concise information about network interfaces
```
