# -*- coding: utf-8 -*-
import sys
import argparse
import smbdiscovery
from termcolor import colored



banner = '''

                                                    ▄██   ▄      ▄████████    ▄█   ▄█▄    ▄████████ 
                                                    ███   ██▄   ███    ███   ███ ▄███▀   ███    ███ 
                                                    ███▄▄▄███   ███    ███   ███▐██▀     ███    ███ 
                                                    ▀▀▀▀▀▀███   ███    ███  ▄█████▀      ███    ███ 
                                                    ▄██   ███ ▀███████████ ▀▀█████▄    ▀███████████ 
                                                    ███   ███   ███    ███   ███▐██▄     ███    ███ 
                                                    ███   ███   ███    ███   ███ ▀███▄   ███    ███ 
                                                    ▀█████▀    ███    █▀    ███   ▀█▀   ███    █▀  
                                                                            ▀                      

'''


parser = argparse.ArgumentParser(add_help = True, description = "YAKA is a tool for search of files")




group = parser.add_argument_group('authentication')

group.add_argument('-U', action="store", metavar="username", help='Username for connection in SMB share')
group.add_argument('-P', action="store", metavar="passowrd", help='Password for conncetion in SMB share')
group.add_argument('-D', action="store", metavar="domain", help='Domain for connection in SMB share')
group.add_argument('-N', action="store", metavar="hostname", help='Name of machone for connection in SMB share')
group.add_argument('-hashes', action="store", metavar = "LMHASH:NTHASH", help='NTLM hashes, format is LMHASH:NTHASH')
group = parser.add_argument_group('connection')
group.add_argument('-dc-ip', action='store', metavar="ip-address", help='IP Address of the domain controller. If omitted it will use the domain part (FQDN) specified in the target parameter')
group.add_argument('-target', action='store', metavar="ip-address", help='IP Address of the target machine. If omitted it will use whatever was specified as target. This is useful when target is the NetBIOS name and you cannot resolve it')
group.add_argument('--network', action='store', metavar="ip-address", help='IP range of the network. If omitted it will use whatever was specified as target. This is useful when target is the NetBIOS name and you cannot resolve it')
group.add_argument('--threads', action='store', metavar="threads", help='Theads to run simutaneously')
group.add_argument('-port', choices=['139', '445'], nargs='?', default='445', metavar="destination port", help="Destination port to connect to SMB Server")
group.add_argument('-O', action="store", metavar = "Lin or Win", help="OS to choise")
group = parser.add_argument_group('modules')
group.add_argument('-smb', action="store_true", help="Enable SMBModule")
group = parser.add_argument_group('pattern')
group.add_argument('-pattern', action='append', metavar="pattern", dest="collection", default=[], help="Pattern that will be search at name of files found")
group.add_argument('-regex', action='append', metavar="regex", dest="collection2", default=[], help="Regex that will be search at content of files")


if len(sys.argv) ==1:
    parser.print_help()
    sys.exit(1)
    
options = parser.parse_args()


scanner = smbdiscovery.SMBScanner(options.network, options.threads)
smb_servers = scanner.scan()
print(smb_servers)



