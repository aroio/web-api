import socket

class Validator:

    @staticmethod
    def ipv4(address: str) -> bool:
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
