import sys

from core import mapOpenPorts, getSystemInterfaces, processesInodes, TCP_ROUTES, UDP_ROUTES
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
        print('    -a --all                Show network interfaces information and relative open ports')
        print('    -h --help               Show this message and exits')
        print('    -i --interfaces         Show network interfaces information')
        print('    -p --ports [tcp|udp]    Show open ports of specified protocol, if omitted show both')
        print('    -virt                   Only show virtual network interfaces')
        print('    -phy                    Only show physical network interfaces')
        print('    -v --verbose            Show verbose information')
        print('    -V --version            Show version number and exit')
        print('if no option is specified, shows concise information about network interfaces')
        sys.exit(0)

    if args.version:
        print(f'lonet {VERSION}')
        sys.exit(0)

    if args.all:
        interfaces = getSystemInterfaces()
        interfaces = sorted(interfaces, key=lambda x: x.ifIndex)

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
            ip = interface.ipv4

            print('  open ports: ')

            localTcpAddressPorts = anyAddressTcpPorts.copy()

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
        interfaces = sorted(interfaces, key=lambda x: x.ifIndex)

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
        if args.protocol is None or args.protocol.lower() == 'tcp':
            print('TCP')
            for inode, (address, port) in tcpInodePorts.items():
                process = procInodes.get(inode)

                if process is not None:
                    pid, name = process

                    print(f'{address.ljust(15)} : {str(port).ljust(5)}    {pid} -> {name}')

                else:
                    print(f'{address.ljust(15)} : {str(port).ljust(5)}')

        if args.protocol is None or args.protocol.lower() == 'udp':
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
        interfaces = sorted(interfaces, key=lambda x: x.ifIndex)

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
                print(interface.concise())

            print()