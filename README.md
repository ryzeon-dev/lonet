# LONET
Linux local network information tool written in Python

# Install
run the installation script as root
```commandline
sudo bash install.sh
```

# Usage
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