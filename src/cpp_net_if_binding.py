import ctypes

sharedObjectPath = '/usr/local/share/lonet/libnet_if_binding.so'
libso = ctypes.CDLL(sharedObjectPath)

libso.init.argtypes = []
libso.init.restype = None

libso.getIface.argtypes = [ctypes.c_char_p]
libso.getIface.restype = ctypes.c_void_p

libso.getIPv4.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
libso.getIPv4.restype = ctypes.c_char_p

libso.getIPv4Netmask.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
libso.getIPv4Netmask.restype = ctypes.c_char_p

libso.getIPv6.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
libso.getIPv6.restype = ctypes.c_char_p

libso.getIPv6Netmask.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
libso.getIPv6Netmask.restype = ctypes.c_char_p

libso.getIfIndex.argtypes = [ctypes.c_void_p]
libso.getIfIndex.restype = ctypes.c_uint


class CppNetIface:
    def __init__(self, ifaceName):
        self.ifaceName = ifaceName

        self.ifacePtr = libso.getIface(ctypes.create_string_buffer(ifaceName.encode()))

        self.ipv4 = None
        self.netmask4 = None

        self.ipv6 = None
        self.netmask6 = None

        if self.ifacePtr is None:
            return

        self.ipv4 = libso.getIPv4(self.ifacePtr, ctypes.create_string_buffer(128)).decode()
        self.netmask4 = libso.getIPv4Netmask(self.ifacePtr, ctypes.create_string_buffer(128)).decode()

        self.ipv6 = libso.getIPv6(self.ifacePtr, ctypes.create_string_buffer(128)).decode()
        self.netmask6 = libso.getIPv6Netmask(self.ifacePtr, ctypes.create_string_buffer(128)).decode()

        self.ifIndex = libso.getIfIndex(self.ifacePtr)

    @staticmethod
    def new(ifaceName):
        instance = CppNetIface(ifaceName)

        if instance.ifacePtr is not None:
            return instance

    def __repr__(self):
        return f'CppNetIface ( name: {self.ifaceName} ; IPv4: {self.ipv4} [{self.netmask4}] ; IPv6: {self.ipv6} : [{self.netmask6}] )'

libso.init()