import socket
import ipaddress
import threading
import time
import cidr



class SMBScanner:
    def __init__(self, network):

        self.network = network
        self.smbs = []
        


    def scan_ip(self, ip_address, sock):
        try:

            sock.settimeout(1)
            sock.connect((ip_address, 445))
            print(f'The {ip_address} has a SMB')
            
            self.smbs.append(ip_address)
            
        except socket.error:
            
            pass
        finally:
            sock.close()

    
    def scan(self):

        threads = []
        current_ip = ipaddress.ip_address(socket.gethostbyname(socket.gethostname()))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cidrs = cidr.CIDR(self.network)
        ips = cidrs.get_ips()
        
        for i in ips:
            thread = threading.Thread(target=self.scan_ip, args=(i, sock))
            thread.start()
            threads.append(thread)

        for t in threads:
            t.join()


        
        return self.smbs




        
