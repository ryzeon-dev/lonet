import sys
import json

from core import (
    mapOpenPorts, getSystemInterfaces, processesInodes, TCP_ROUTES, UDP_ROUTES, scanIpv4Routes, readArpTable,
    tcp4Connections, udp4Connections, LOCALHOST_IP
)
from argparser import ArgParser

VERSION = 'v2.2.1'

def printAllIfaceInfo(interface, args):
    jfmt = {}
    if args.virtual and not args.physical:
        if interface.type == 'physical':
            return False, {}

    elif args.physical and not args.virtual:
        if interface.type == 'virtual':
            return False, {}

    if args.verbose:
        if args.json:
            jfmt = interface.jsonVerbose()

        else:
            print(interface.verbose())
    else:
        if args.json:
            jfmt = interface.jsonPretty()

        else:
            print(interface.pretty())

    ip = interface.ipv4

    if args.json:
        jfmt['open_ports'] = {}
    else:
        print('  open ports: ')

    tcpInodePorts, tcpAddressPorts = mapOpenPorts(TCP_ROUTES)
    udpInodePorts, udpAddressPorts = mapOpenPorts(UDP_ROUTES)

    anyAddressTcpPorts = tcpPorts if (tcpPorts := tcpAddressPorts.get('0.0.0.0')) is not None else set()
    anyAddressUdpPorts = udpPorts if (udpPorts := udpAddressPorts.get('0.0.0.0')) is not None else set()

    localTcpAddressPorts = anyAddressTcpPorts.copy()

    if ip in tcpAddressPorts:
        localTcpAddressPorts.update(tcpAddressPorts.get(ip))

    if args.json:
        jfmt['open_ports']['tcp'] = sorted(localTcpAddressPorts)
    else:
        print(f'    tcp: {", ".join(str(p) for p in sorted(localTcpAddressPorts))}')

    localUdpAddressPorts = anyAddressUdpPorts.copy()

    if ip in udpAddressPorts:
        localUdpAddressPorts.update(udpAddressPorts.get(ip))

    if args.json:
        jfmt['open_ports']['udp'] = sorted(localUdpAddressPorts)
    else:
        print(f'    udp: {", ".join(str(p) for p in sorted(localUdpAddressPorts))}')
    ipv4Routes = scanIpv4Routes()

    interfaceIPv4Routes = ipv4Routes.get(interface.name)

    if args.json:
        jfmt['routes'] = []

    if interfaceIPv4Routes:
        if not args.json:
            print('  routes:')

        for route in interfaceIPv4Routes:
            from_, to_, flags = route

            if args.json:
                jfmt['routes'].append({
                    'from' : from_,
                    'to' : to_,
                    'flags': flags
                })
                
            else:
                print(f'    {from_} -> {to_}')
                print(f'      flags: {", ".join(flags)}')

    arpTable = readArpTable()
    relatedArpEntries = arpTable.get(interface.name)

    if args.json:
        jfmt['arp_table'] = []

    if relatedArpEntries is not None:
        if not args.json:
            print('  arp:')

        for entry in relatedArpEntries:
            ip, address, type, flags = entry

            if args.json:
                jfmt['arp_table'].append({
                    'ip': ip,
                    'address' : address,
                    'type' : type,
                    'flags' : flags
                })
                
            else:
                print(f'    {ip} -> {address}')
                print(f'      type: {type}')
                print(f'      flags: {flags}')

    return True, jfmt

def printRouteInfo(interface, ifaceRoutes, args):
    jfmt = []
    if not args.json:
        print(interface)

    for route in ifaceRoutes:
        from_, to_, flags = route

        if args.json:
            jfmt.append({
                'from' : from_,
                'to' : to_,
                'flags' : flags
            })

        else:
            print(f'  {from_} -> {to_}')
            print(f'    flags: {", ".join(flags)}')

    return jfmt

def printArpEntries(interface, arpEntries, args):
    jfmt = []

    if not args.json:
        print(f'interface {interface}:')

    for entry in arpEntries:
        ip, address, type, flags = entry

        if args.json:
            jfmt.append({
                'ip' : ip,
                'address' : address,
                'type' : type,
                'flags': flags.split(', ')
            })

        else:
            print(f'  {ip} -> {address}')
            print(f'    type: {type}')
            print(f'    flags: {flags}')

    if args.json:
        return jfmt

def printIfaceInfo(interface, args):
    jfmt = {}

    if args.virtual and not args.physical:
        if interface.type == 'physical':
            return False, {}

    elif args.physical and not args.virtual:
        if interface.type == 'virtual':
            return False, {}

    if args.verbose:
        if args.json:
            jfmt = interface.jsonVerbose()
        else:
            print(interface.verbose())

    else:
        if args.json:
            jfmt = interface.jsonConcise()
        else:
            print(interface.concise())

    return True, jfmt

def all(args):
    jfmt = {}

    interfaces = getSystemInterfaces()
    interfaces = sorted(interfaces, key=lambda x: x.ifIndex)

    if (ifaceName := args.interface) is not None:
        found = False

        for interface in interfaces:
            if interface.name == ifaceName:
                ok, jInfo = printAllIfaceInfo(interface, args)

                if args.json:
                    jfmt[interface.name] = jInfo
                found = True
                break

        if not found:
            print(f'Error: interface `{ifaceName}` not found')
            sys.exit(1)

        print(json.dumps(jfmt))
        sys.exit(0)

    for interface in interfaces:
        ok, jInfo = printAllIfaceInfo(interface, args)

        if args.json:
            jfmt[interface.name] = jInfo

        else:
            if ok:
                print()
    if args.json:
        print(json.dumps(jfmt))

if __name__ == '__main__':
    argv = sys.argv

    args = ArgParser()
    args.parse(argv[1:])

    if args.help:
        print('lonet: local network information tool')
        print('usage: lonet [OPTIONS]')
        print('options:')
        print('    -a --all                Show all available information')
        print('    -A --arp                Show arp table')
        print('    -h --help               Show this message and exits')
        print('    -i --interface IFACE    Show information about requested interface')
        print('    -I --interfaces         Show network interfaces information')
        print('    -j --json               Use JSON output')
        print('    -O --open-connections   Show open connections (IPv4 only)')
        print('    -p --ports [tcp|udp]    Show open ports of specified protocol, if omitted show both')
        print('    -phy                    Only show physical network interfaces')
        print('    -virt                   Only show virtual network interfaces')
        print('    -r --routes             Show system routes')
        print('    -v --verbose            Show verbose information')
        print('    -V --version            Show version number and exit')
        print('if no option is specified, shows concise information about network interfaces')
        sys.exit(0)

    if args.version:
        print(f'lonet {VERSION}')
        sys.exit(0)

    if args.all:
        all(args)

    elif args.interfaces:
        interfaces = getSystemInterfaces()
        interfaces = sorted(interfaces, key=lambda x: x.ifIndex)

        if (ifaceName := args.interface) is not None:
            found = False

            for interface in interfaces:
                if interface.name == ifaceName:

                    if args.verbose:
                        if args.json:
                            print(json.dumps({
                                interface.name : interface.jsonVerbose()
                            }))
                            
                        else:
                            print(interface.verbose())

                    else:
                        if args.json:
                            print(json.dumps({
                                interface.name: interface.jsonPretty()
                            }))
                            
                        else:
                            print(interface.verbose())

                    found = True
                    break

            if not found:
                print(f'Error: interface `{ifaceName}` not found')
                sys.exit(1)

            sys.exit(0)

        jfmt = {}
        for interface in interfaces:
            if args.virtual and not args.physical:
                if interface.type == 'physical':
                    continue

            elif args.physical and not args.virtual:
                if interface.type == 'virtual':
                    continue

            if args.verbose:
                if args.json:
                    jfmt[interface.name] = interface.jsonVerbose()
                else:
                    print(interface.verbose())

            else:
                if args.json:
                    jfmt[interface.name] = interface.jsonPretty()
                else:
                    print(interface.verbose())

            if not args.json:
                print()

        if args.json:
            print(json.dumps(jfmt))

    elif args.ports:
        jfmt = {}
        tcpInodePorts, _ = mapOpenPorts(TCP_ROUTES)
        udpInodePorts, _ = mapOpenPorts(UDP_ROUTES)

        procInodes = processesInodes()

        if not args.json:
            print('ADDRESS         : PORT     PID -> NAME')

        if args.protocol is None or args.protocol.lower() == 'tcp':
            if args.json:
                jfmt['tcp'] = []
            else:
                print('TCP')

            for inode, (address, port) in tcpInodePorts.items():
                process = procInodes.get(inode)

                if process is not None:
                    pid, name = process

                    if args.json:
                        jfmt['tcp'].append({
                            'address' : address,
                            'port' : port,
                            'pid' : pid,
                            'process_name' : name
                        })
                    else:
                        print(f'{address.ljust(15)} : {str(port).ljust(5)}    {pid} -> {name}')

                else:
                    if args.json:
                        jfmt['tcp'].append({
                            'address': address,
                            'port': port,
                            'pid': None,
                            'process_name': None
                        })
                    else:
                        print(f'{address.ljust(15)} : {str(port).ljust(5)}')

        if args.protocol is None or args.protocol.lower() == 'udp':
            if args.json:
                jfmt['udp'] = []
            else:
                print('UDP')

            for inode, (address, port) in udpInodePorts.items():
                process = procInodes.get(inode)

                if process is not None:
                    pid, name = process

                    if args.json:
                        jfmt['udp'].append({
                            'address': address,
                            'port': port,
                            'pid': pid,
                            'process_name': name
                        })
                    else:
                        print(f'{address.ljust(15)} : {str(port).ljust(5)}    {pid} -> {name}')

                else:
                    if args.json:
                        jfmt['udp'].append({
                            'address': address,
                            'port': port,
                            'pid': None,
                            'process_name': None
                        })
                    else:
                        print(f'{address.ljust(15)} : {str(port).ljust(5)}')

        if args.json:
            print(json.dumps(jfmt))

    elif args.routes:
        jfmt = {}
        routes = scanIpv4Routes()

        if (ifaceName := args.interface):
            for interface, ifaceRoutes in routes.items():
                if interface == ifaceName:
                    ifaceRoutes = printRouteInfo(interface, ifaceRoutes, args)

                    if args.json:
                        jfmt[ifaceName] = ifaceRoutes

                    break

            if args.json:
                print(json.dumps(jfmt))

            sys.exit(0)

        for interface, ifaceRoutes in routes.items():
            routeInfo = printRouteInfo(interface, ifaceRoutes, args)

            if args.json:
                jfmt[interface] = routeInfo
            else:
                print()

        if args.json:
            print(json.dumps(jfmt))

    elif args.arp:
        jfmt = {}
        arpTable = readArpTable()

        if (ifaceName := args.interface):
            for interface, arpEntries in arpTable.items():
                if interface == ifaceName:
                    arpEntries = printArpEntries(interface, arpEntries, args)

                    if args.json:
                        jfmt[ifaceName] = arpEntries

                    break

            if args.json:
                print(json.dumps(jfmt))

            sys.exit(0)

        for interface, arpEntries in arpTable.items():
            arpEntries = printArpEntries(interface, arpEntries, args)

            if args.json:
                jfmt[interface] = arpEntries
            else:
                print()

        if args.json:
            print(json.dumps(jfmt))

    elif args.openConnections:
        jfmt = {}

        tcpOpenConnections = tcp4Connections()
        udpOpenConnections = udp4Connections()

        if args.json:
            jfmt['tcp'] = []
        else:
            print('TCP')

        for connection in tcpOpenConnections:
            if connection.toAddress != LOCALHOST_IP:
                if args.json:
                    jfmt['tcp'].append(connection.json())
                else:
                    print(connection.repr())

        if args.json:
            jfmt['udp'] = []
        else:
            print('UDP')

        for connection in udpOpenConnections:
            if connection.toAddress != LOCALHOST_IP:
                if args.json:
                    jfmt['udp'].append(connection.json())
                else:
                    print(connection.repr())

        if args.json:
            print(json.dumps(jfmt))

    else:
        jfmt = {}

        interfaces = getSystemInterfaces()
        interfaces = sorted(interfaces, key=lambda x: x.ifIndex)

        if (ifaceName := args.interface) is not None:
            found = False

            for interface in interfaces:
                if interface.name == ifaceName:
                    ok, jInfo = printIfaceInfo(interface, args)

                    if ok:
                        jfmt[interface.name] = jInfo

                    found = True
                    break

            if found:
                if args.json:
                    print(json.dumps(jfmt))

            else:
                print(f'Error: interface `{ifaceName}` not found')
                sys.exit(1)

            sys.exit(0)

        for interface in interfaces:
            ok, jInfo = printIfaceInfo(interface, args)

            if ok:
                if args.json:
                    jfmt[interface.name] = jInfo
                else:
                    print()

        if args.json:
            print(json.dumps(jfmt))