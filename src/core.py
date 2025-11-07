import os

ROUTES = '/proc/net/route'
IFACES_DIR = '/sys/class/net/'
VIRTUAL_IFACES_DIR = '/sys/devices/virtual/net/'

TCP_ROUTES = '/proc/net/tcp'
UDP_ROUTES = '/proc/net/udp'

PROC = '/proc'

### UTILS ###

def _tryRead(path):
    try:
        with open(path, 'r') as file:
            return file.read().strip()
    except:
        return None

def checkBit(flags, bit):
    return (flags & bit) == bit

def removeBlank(list):
    while '' in list:
        list.remove('')
    return list

def reversedHexIpToIp(reversed):
    index = len(reversed)
    ipChunks = []

    for _ in range(4):
        ipChunks.append(str(int(reversed[index-2:index], 16)))
        index -= 2

    return '.'.join(ipChunks)

def reversedHexU16ToInt(reversed):
    return int(reversed[0:2], 16) | int(reversed[2:4], 16) << 8

def ipToU32(ip):
    chunks = ip.split('.')[::-1]
    u32 = 0

    for index, chunk in enumerate(chunks):
        u32 += int(chunk) << (8 * index)

    return u32

def maskToCidr(mask):
    u32Mask = ipToU32(mask)
    cidr = 0

    for i in range(32):
        if checkBit(u32Mask, 1 << i):
            cidr += 1

    return cidr

### INTERFACES ###

class NetworkInterface:
    def __init__(self, path):
        self.sysFsPath = path
        self.type = ''

        self.name = None
        self.nameAssignment = None
        self.mac = None
        self.mtu = None
        self.state = None
        self.physicalLink = None
        self.devId = None
        self.devPort = None
        self.physPortId = None
        self.physPortName = None
        self.speed = None
        self.duplex = None
        self.flags = None
        self.alias = None

        self.ip = None
        self.network = None
        self.mask = None
        self.cidr = None

        self.__inspectSysFs()

    def __inspectSysFs(self):
        realPath = os.path.realpath(self.sysFsPath)

        if 'virtual' in realPath.lower():
            self.type = 'virtual'

        else:
            self.type = 'physical'

        self.name = self.sysFsPath.split('/')[-1]

        nameAssignment = _tryRead(os.path.join(self.sysFsPath, 'name_assign_type'))
        if nameAssignment == '1':
            self.nameAssignment = 'kernel (unpredictable)'

        elif nameAssignment == '2':
            self.nameAssignment = 'kernel (predictable)'

        elif nameAssignment == '3':
            self.nameAssignment = 'userspace'

        elif nameAssignment == '4':
            self.nameAssignment = 'renamed'

        self.mac = _tryRead(os.path.join(self.sysFsPath, 'address'))
        self.mtu = _tryRead(os.path.join(self.sysFsPath, 'mtu'))

        self.state = _tryRead(os.path.join(self.sysFsPath, 'operstate'))
        self.physicalLink = _tryRead(os.path.join(self.sysFsPath, 'carrier'))

        if self.physicalLink:
            if self.physicalLink == '0':
                self.physicalLink = 'disconnected'

            elif self.physicalLink == '1':
                self.physicalLink = 'connected'

            else:
                self.physicalLink = 'unknown'

        self.devId = _tryRead(os.path.join(self.sysFsPath, 'dev_id'))
        self.devPort = _tryRead(os.path.join(self.sysFsPath, 'dev_port'))

        self.physPortId = _tryRead(os.path.join(self.sysFsPath, 'phys_port_id'))
        self.physPortName = _tryRead(os.path.join(self.sysFsPath, 'phys_port_name'))

        self.speed = _tryRead(os.path.join(self.sysFsPath, 'speed'))

        if self.speed is not None:
            if not self.speed.isnumeric():
                self.speed = 'unknown'
            else:
                self.speed += ' Mbps'

        self.duplex = _tryRead(os.path.join(self.sysFsPath, 'duplex'))

        self.flags = _tryRead(os.path.join(self.sysFsPath, 'flags'))
        if self.flags is not None:
            try:
                self.flags = int(self.flags, 16)
            except:
                self.flags = 'unknown'

        self.alias = _tryRead(os.path.join(self.sysFsPath, 'ifalias'))

        iflink = _tryRead(os.path.join(self.sysFsPath, 'iflink'))
        ifindex = _tryRead(os.path.join(self.sysFsPath, 'ifindex'))

        if iflink != ifindex:
            if self.type == 'physical':
                self.type = 'unknown'

    def decodeFlags(self):
        if not isinstance(self.flags, int):
            return ''

        strFlags = []

        if checkBit(self.flags, 1 << 0):
            strFlags.append('up')

        if checkBit(self.flags, 1 << 1):
            strFlags.append('broadcast')

        if checkBit(self.flags, 1 << 2):
            strFlags.append('debug')

        if checkBit(self.flags, 1 << 3):
            strFlags.append('lookpack')

        if checkBit(self.flags, 1 << 4):
            strFlags.append('point to point')

        if checkBit(self.flags, 1 << 5):
            strFlags.append('no trailers')

        if checkBit(self.flags, 1 << 6):
            strFlags.append('running')

        if checkBit(self.flags, 1 << 7):
            strFlags.append('no arp')

        if checkBit(self.flags, 1 << 8):
            strFlags.append('promisc')

        if checkBit(self.flags, 1 << 9):
            strFlags.append('all multi')

        if checkBit(self.flags, 1 << 10):
            strFlags.append('master')

        if checkBit(self.flags, 1 << 11):
            strFlags.append('slave')

        if checkBit(self.flags, 1 << 12):
            strFlags.append('multicast')

        if checkBit(self.flags, 1 << 13):
            strFlags.append('portsel')

        if checkBit(self.flags, 1 << 14):
            strFlags.append('automedia')

        if checkBit(self.flags, 1 << 15):
            strFlags.append('dynamic')

        if checkBit(self.flags, 1 << 16):
            strFlags.append('lower up')

        if checkBit(self.flags, 1 << 17):
            strFlags.append('dormant')

        if checkBit(self.flags, 1 << 18):
            strFlags.append('echo')

        return ', '.join(strFlags)

    def __repr__(self):
        return f'NetworkInterface( {self.name} [{self.mac}] ; type: {self.type} ; state: {self.state} ; speed: {self.speed} ; mtu: {self.mtu} ; flags: {self.decodeFlags()} )'

    def completeIpConfiguration(self):
        if self.mac == '00:00:00:00:00:00':
            self.ip = '127.0.0.1'
            self.mask = '0.0.0.0'

        if self.mask:
            self.cidr = maskToCidr(self.mask)

    def pretty(self):
        self.completeIpConfiguration()

        repr = f'{self.name} : {self.type} interface'

        if self.alias:
            repr += f'\n  alias: {self.alias}'

        if self.mac:
            repr += f'\n  mac: {self.mac}'

        if self.ip:
            repr += f'\n  ip: {self.ip}'

        if self.network:
            repr += f'\n  network: {self.network}'

        if self.mask:
            repr += f'\n  mask: {self.mask}'

        if self.mtu:
            repr += f'\n  mtu: {self.mtu}'

        if self.speed:
            repr += f'\n  speed: {self.speed}'

        if self.state:
            repr += f'\n  state: {self.state}'

        if self.duplex:
            repr += f'\n  duplex: {self.duplex}'

        if self.flags:
            repr += f'\n  flags: {self.decodeFlags()}'

        return repr

    def concise(self):
        self.completeIpConfiguration()

        fmt = f'{self.name} : {self.type} interface'
        if self.mac:
            fmt += f'\n  mac: {self.mac}'

        if self.ip:
            fmt += f'\n  ip: {self.ip}'

            if self.cidr is not None:
                fmt += f'/{self.cidr}'

        if self.state:
            fmt += f'\n  state: {self.state}'

        if self.speed:
            fmt += f'\n  speed: {self.speed}'

        return fmt

    def verbose(self):
        self.completeIpConfiguration()

        repr = f'{self.name} : {self.type} interface'

        if self.nameAssignment:
            repr += f'\n  name assignment: {self.nameAssignment}'

        if self.alias:
            repr += f'\n  alias: {self.alias}'

        if self.mac:
            repr += f'\n  mac: {self.mac}'

        if self.ip:
            repr += f'\n  ip: {self.ip}'

        if self.network:
            repr += f'\n  network: {self.network}'

        if self.mask:
            repr += f'\n  mask: {self.mask}'

        if self.mtu:
            repr += f'\n  mtu: {self.mtu}'

        if self.speed:
            repr += f'\n  speed: {self.speed}'

        if self.state:
            repr += f'\n  state: {self.state}'

        if self.physicalLink:
            repr += f'\n  physical link: {self.physicalLink}'

        if self.devId:
            repr += f'\n  device id: {self.devId}'

        if self.devPort:
            repr += f'\n  device port: {self.devPort}'

        if self.physPortId:
            repr += f'\n  physical port id: {self.physPortId}'

        if self.physPortName:
            repr += f'\n  physical port name: {self.physPortName}'

        if self.duplex:
            repr += f'\n  duplex: {self.duplex}'

        if self.flags:
            repr += f'\n  flags: {self.decodeFlags()}'

        return repr

def getSystemInterfaces():
    try:
        entries = os.listdir(IFACES_DIR)

    except:
        return []

    ifaces = []

    for entry in entries:
        entryPath = os.path.join(IFACES_DIR, entry)

        if not os.path.isdir(entryPath):
            continue

        ifaces.append(NetworkInterface(entryPath))

    return ifaces

def networkToInterface(ifaces):
    netRoutes = _tryRead(ROUTES)

    if not netRoutes:
        return ifaces

    for line in netRoutes.split('\n')[1:]:
        chunks = removeBlank(line.split('\t'))

        ifaceName = chunks[0]
        network = chunks[1]
        mask = chunks[7]

        if not network.replace('0', ''):
            continue

        network = reversedHexIpToIp(network)
        mask = reversedHexIpToIp(mask)

        for iface in ifaces:
            if iface.name == ifaceName:
                iface.network = network
                iface.mask = mask
                break

    fibTrie = _tryRead('/proc/net/fib_trie')
    if not fibTrie:
        return ifaces

    localFibTrie = fibTrie.split('Local:')[1].strip()
    for chunk in localFibTrie.split('+--'):
        chunkLines = chunk.split('\n')
        if len(chunkLines) == 1:
            continue

        address = chunkLines[1].replace('|--', '').strip()
        if not address:
            continue

        u32Address = ipToU32(address)

        for iface in ifaces:
            if iface.network is None or iface.mask is None or iface.ip is not None:
                continue

            u32Network = ipToU32(iface.network)
            u32Mask = ipToU32(iface.mask)

            u32BaseAddress = u32Network & u32Mask
            u32BroadcastAddress = u32BaseAddress | ((~u32Mask) & 0xFFFFFFFF)

            if u32BaseAddress < u32Address < u32BroadcastAddress:
                iface.ip = address
                break

    return ifaces

### PORTS ###

def processesInodes():
    try:
        processes = os.listdir(PROC)

    except:
        return {}

    inodes = {
        # inode : (pid, name)
    }

    for process in processes:
        if not process.isnumeric():
            continue
        processPath = os.path.join(PROC, process)

        pid = process
        status = _tryRead(os.path.join(processPath, 'status'))
        name = None

        if status:
            name = status.split('Name:')[1].split('\n')[0].strip()

        try:
            fds = os.listdir(os.path.join(processPath, 'fd'))

        except:
            continue

        for fd in fds:
            linkPath = os.path.join(processPath, 'fd', fd)
            linkContent = os.path.realpath(linkPath)

            if 'socket:' not in linkContent:
                continue

            inode = linkContent.split('socket:')[1][1:-1]

            inodes[inode] = (pid, name)

    return inodes

def mapOpenPorts(file):
    openPorts = _tryRead(file)

    if not openPorts:
        return {}

    ports = {
        # inode : (address, port)
    }

    mapped = {
        # address : set(ports)
    }

    for line in openPorts.split('\n')[1:]:
        chunks = removeBlank(line.strip().split(' '))

        if chunks[3] not in  ('0A', '07'):
            continue

        source = chunks[1]
        address, port = source.split(':')

        address = reversedHexIpToIp(address)
        port = int(port, 16)

        if address not in mapped:
            mapped[address] = set()
        mapped[address].add(port)
        # port = reversedHexU16ToInt(port)

        inode = chunks[9]
        ports[inode] = (address, port)

    return ports, mapped