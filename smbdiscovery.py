import socket
import ipaddress
import threading

class SMBScanner:
    def __init__(self, network):

        self.network = ipaddress.ip_network(network)

        #self.network_address = str(network.network_address)

    def get_ips(self):

        ips = []
        for addr in self.network.hosts():
            ips.append(str(addr))
        return ips

    def scan_ip(self, ip_address, smb_servers, sock):
        try:
            sock.settimeout(3)
            sock.connect((ip_address, 445))
            print(f'The {ip_address} has a SMB')
            smb_servers.append(ip_address)
            

        except socket.error:
            
            pass

    
    def scan(self):

        smb_servers = []
        current_ip = ipaddress.ip_address(socket.gethostbyname(socket.gethostname()))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ips = self.get_ips()
        threads = []
        for i in ips:
            self.scan_ip(i, smb_servers, sock)

        
        return smb_servers




        
