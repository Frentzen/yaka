import ipaddress

class CIDR:
    def __init__(self, cidr):
        self.cidr = cidr
        self.ip_range = ipaddress.ip_network(self.cidr)
        self.ip_list = [str(ip) for ip in self.ip_range]

    def get_ips(self):
        return self.ip_list