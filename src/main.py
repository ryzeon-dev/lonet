import sys

from core import mapOpenPorts, getSystemInterfaces, processesInodes, networkToInterface, TCP_ROUTES, UDP_ROUTES
from argparser import ArgParser

VERSION = 'v1.0.0'

if __name__ == '__main__':
    argv = sys.argv

    args = ArgParser()
    args.parse(argv[1:])

    if args.help:
        print('lonet: local network information tool')
        print('usage: lonet [OPTIONS]')
        print('options:')
        print('    -a --all                Shows network interfaces information and relative open ports')
        print('    -h --help               Shows this message and exits')
        print('    -i --interfaces         Shows network interfaces information')
        print('    -p --ports [tcp|udp]    Shows open ports of specified protocol, if omitted shows both')
        print('    -virt                   Only show virtual network interfaces')
        print('    -phy                    Only show physical network interfaces')
        print('    -v --verbose            Showd verbose information7')
        print('    -V --version            Shows version number and exits')
        print('if no option is specified, shows concise information about network interfaces')
        sys.exit(0)

    if args.version:
        print(f'lonet {VERSION}')
        sys.exit(0)

    if args.all:
        interfaces = getSystemInterfaces()
        interfaces = networkToInterface(interfaces)

        interfaces = sorted(interfaces, key=lambda x: x.name)

        tcpInodePorts, tcpAddressPorts = mapOpenPorts(TCP_ROUTES)
        udpInodePorts, udpAddressPorts = mapOpenPorts(UDP_ROUTES)

        anyAddressTcpPorts = tcpPorts if (tcpPorts := tcpAddressPorts.get('0.0.0.0')) is not None else set()
        anyAddressUdpPorts = udpPorts if (udpPorts := udpAddressPorts.get('0.0.0.0')) is not None else set()

        for interface in interfaces:
            if args.virtual and not args.physical:
                if interface.type == 'physical':
                    continue

            elif args.physical and not args.virtual:
                if interface.type == 'virtual':
                    continue

            if args.verbose:
                print(interface.verbose())
            else:
                print(interface.pretty())
            ip = interface.ip

            localTcpAddressPorts = anyAddressTcpPorts.copy()

            print('  open ports: ')

            if ip in tcpAddressPorts:
                localTcpAddressPorts.update(tcpAddressPorts.get(ip))
            print(f'    tcp: {", ".join(str(p) for p in sorted(localTcpAddressPorts))}')

            localUdpAddressPorts = anyAddressUdpPorts.copy()

            if ip in udpAddressPorts:
                localUdpAddressPorts.update(udpAddressPorts.get(ip))
            print(f'    udp: {", ".join(str(p) for p in sorted(localUdpAddressPorts))}')

            print()

    elif args.interfaces:
        interfaces = getSystemInterfaces()
        interfaces = networkToInterface(interfaces)

        for interface in interfaces:
            if args.virtual and not args.physical:
                if interface.type == 'physical':
                    continue

            elif args.physical and not args.virtual:
                if interface.type == 'virtual':
                    continue

            if args.verbose:
                print(interface.verbose())
            else:
                print(interface.pretty())
            print()

    elif args.ports:
        tcpInodePorts, _ = mapOpenPorts(TCP_ROUTES)
        udpInodePorts, _ = mapOpenPorts(UDP_ROUTES)

        procInodes = processesInodes()

        print('ADDRESS         : PORT     PID -> NAME')

        print('TCP')
        for inode, (address, port) in tcpInodePorts.items():
            process = procInodes.get(inode)

            if process is not None:
                pid, name = process

                print(f'{address.ljust(15)} : {str(port).ljust(5)}    {pid} -> {name}')

            else:
                print(f'{address.ljust(15)} : {str(port).ljust(5)}')

        print('UDP')
        for inode, (address, port) in udpInodePorts.items():
            process = procInodes.get(inode)

            if process is not None:
                pid, name = process

                print(f'{address.ljust(15)} : {str(port).ljust(5)}    {pid} -> {name}')

            else:
                print(f'{address.ljust(15)} : {str(port).ljust(5)}')

    else:
        interfaces = getSystemInterfaces()
        interfaces = networkToInterface(interfaces)
        interfaces = sorted(interfaces, key=lambda x: x.name)

        for interface in interfaces:
            if args.virtual and not args.physical:
                if interface.type == 'physical':
                    continue

            elif args.physical and not args.virtual:
                if interface.type == 'virtual':
                    continue

            if args.verbose:
                print(interface.concise())
            else:
                print(interface.verbose())
            print()