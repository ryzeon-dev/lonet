#include <iostream>
#include <net/if.h>
#include <ifaddrs.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <vector>
#include <cstring>

using namespace std;

class NetIface {
public:
    NetIface(struct ifaddrs* iface) {
        this->name = string(iface->ifa_name);
        getIp(iface);
        getIndex();
    }

    void add(struct ifaddrs* iface) {
        getIp(iface);
    }

private:
    void getIp(struct ifaddrs* iface) {
        auto address = iface->ifa_addr;
        auto netmask = iface->ifa_netmask;

        if (address == nullptr)
            return;

        if (address->sa_family == AF_INET) {
            this->ipv4 = extractIp(address, INET_ADDRSTRLEN);
            this->netmask4 = extractIp(netmask, INET_ADDRSTRLEN);

        } else if (address->sa_family == AF_INET6) {
            this->ipv6 = extractIp(address, INET6_ADDRSTRLEN);
            this->netmask6 = extractIp(netmask, INET6_ADDRSTRLEN);

        } else {
            return;
        }
    }

    string extractIp(struct sockaddr* addr, socklen_t bufferSize) {
        char buffer[bufferSize] = {0, };

        inet_ntop(
            addr->sa_family,
            &((struct sockaddr_in*)addr)->sin_addr,
            buffer,
            bufferSize
        );

        return string(buffer);
    }

    void getIndex() {
        this->index = if_nametoindex(this->name.c_str());
    }

public:
    unsigned int index;
    string name;

    string ipv4;
    string netmask4;

    string ipv6;
    string netmask6;
};

vector<NetIface *> netIfaces;

extern "C" {
    void init() {
        struct ifaddrs *ifaddrIterator;
        auto res = getifaddrs(&ifaddrIterator);

        for (struct ifaddrs* iface = ifaddrIterator; iface; iface = iface->ifa_next) {
            bool found = false;

            for (auto netIface : netIfaces) {
                if (netIface->name == string(iface->ifa_name)) {
                    netIface->add(iface);

                    found = true;
                    break;
                }
            }

            if (found)
                continue;

            netIfaces.push_back(new NetIface(iface));
        }
    }

    NetIface* getIface(char* name) {
        for (auto iface : netIfaces) {
            if (iface->name == name) {
                return iface;
            }
        }
        return nullptr;
    }

    const char* netIface_getIPv4(NetIface* iface, char* buffer) {
        strcpy(buffer, iface->ipv4.c_str());
        return buffer;
    }

    const char* netIface_getIPv4Netmask(NetIface* iface, char* buffer) {
        strcpy(buffer, iface->netmask4.c_str());
        return buffer;
    }

    const char* netIface_getIPv6(NetIface* iface, char* buffer) {
        strcpy(buffer, iface->ipv6.c_str());
        return buffer;
    }

    const char* netIface_getIPv6Netmask(NetIface* iface, char* buffer) {
        strcpy(buffer, iface->netmask6.c_str());
        return buffer;
    }

    unsigned int netIface_getIfIndex(NetIface* iface) {
        return iface->index;
    }
}