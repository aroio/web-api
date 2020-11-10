from typing import Optional
from pydantic import BaseModel
import socket


class LAN(BaseModel):
    dhcp: bool = True
    ipaddr: Optional[str] = None
    netmask: Optional[str] = None
    dnsserv: Optional[str] = None
    gateway: Optional[str] = None

    def valid_ipv4_addresses_or_none(self):
        """Returns if all addresses of LAN are IPv4 addresses, when dhcp is set to False."""
        if self.dhcp:
            return True

        for addr in [self.ipaddr, self.netmask, self.dnsserv, self.gateway]:
            try:
                socket.inet_aton(addr)
            except socket.error:
                return False
        return True


class WLAN(LAN):
    ssid: Optional[str] = None
    pwd: Optional[str] = None


class NetworkConfig(BaseModel):
    hostname: str = "Aroio"
    wifi: bool = False
    lan: LAN = LAN()
    wlan: WLAN = WLAN()
