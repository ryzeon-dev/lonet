<p align="center">
<img alt="Version Badge" src="https://img.shields.io/badge/dev--version-v2.2.1-16a085">
<img alt="Version Badge" src="https://img.shields.io/badge/release-v2.2.1-16a085">
<img alt="License Badge" src="https://img.shields.io/github/license/ryzeon-dev/bmdns?color=16a085">
<img alt="Language Badge" src="https://img.shields.io/badge/python3-16a085?logo=python&logoColor=16a085&labelColor=5a5a5a">
<img alt="Language Badge" src="https://img.shields.io/badge/c++-16a085?logo=cplusplus&logoColor=16a085&labelColor=5a5a5a">
</p>

# LONET
Linux local network information tool written in Python and C++

## Install
### Install DEB package
```commandline
wget https://github.com/ryzeon-dev/lonet/releases/download/v2.2.1/lonet_2.2.1_amd64.deb && sudo dpkg -i ./lonet_2.2.1_amd64.deb 
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
    -a --all                Show all available information
    -A --arp                Show arp table
    -h --help               Show this message and exits
    -i --interface IFACE    Show information about requested interface
    -I --interfaces         Show network interfaces information
    -j --json               Use JSON output
    -O --open-connections   Show open connections (IPv4 only)
    -p --ports [tcp|udp]    Show open ports of specified protocol, if omitted show both
    -phy                    Only show physical network interfaces
    -virt                   Only show virtual network interfaces
    -r --routes             Show system routes
    -v --verbose            Show verbose information
    -V --version            Show version number and exit
if no option is specified, shows concise information about network interfaces
```