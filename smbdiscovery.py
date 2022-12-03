import socket
import ipaddress
import threading

class SMBScanner:
    def __init__(self, network):

        network = ipaddress.ip_network(network)

        self.network_address = str(network.network_address)

    def scan(self):

        smb_servers = []
        current_ip = ipaddress.ip_address(socket.gethostbyname(socket.gethostname()))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        for i in range(1, 255):
            ip_address = self.network_address + str(i)
            if ip_address == current_ip:
                continue
            thread = threading.Thread(target=self.scan_ip, args=(ip_address, smb_servers, sock))
            thread.start()
            thread.join()
            sock.close()
            return smb_servers

    def scan_ip(self, ip_address, smb_servers, sock):
        try:
            sock.connect((ip_address, 445))
            sock.sendall(b"\x00\x00\x00\x2f\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x18\x01\x28\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xfe\x00\x08\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
            response = sock.recv(1024)

            if response[8:10] == b"\x72\x00":
                smb_servers.append(ip_address)

        except socket.error:
            pass


        
