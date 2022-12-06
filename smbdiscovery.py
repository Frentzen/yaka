import socket
import ipaddress
import threading
import time
import cidr
from queue import Queue


class SMBScanner:
    def __init__(self, network, thread):

        self.network = network
        self.threads = thread
        self.smbs = []
        self.queue = Queue()
        cidrs = cidr.CIDR(self.network)
        self.ips = cidrs.get_ips()
        for ip in self.ips:
            self.queue.put(ip)
        
    def scan_ip(self, ip_address):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip_address, 445))
            self.smbs.append(ip_address)
            
        except socket.error:
            
            pass
        finally:
            sock.close()
    
    def scan_worker(self):
        while True:
            ip = self.queue.get()
            self.scan_ip(ip)
            self.queue.task_done()
    
    def scan(self):       
        for _ in range(int(self.threads)):
            thread = threading.Thread(target=self.scan_worker)
            thread.daemon = True
            thread.start()

        self.queue.join()
        
        return self.smbs




        
