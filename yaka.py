# -*- coding: utf-8 -*-
import sys
import argparse
import re
import tempfile
import os
from pyfiglet import Figlet
import smbmodule


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
temp = tempfile.gettempdir()

Windows = False


temp = tempfile.gettempdir()
if re.search("[Cc]:", temp):
    Windows = True

if Windows == True:
    if os.path.exists(temp+'\\'+'storage'):
        temp += '\\storage'
    else:
        os.system("mkdir "+temp+"\\storage")

else:
    if os.path.exists(temp+'/'+'storage'):
        temp += '/storage'
    else:
        os.system("mkdir "+ temp+'/storage')
        temp += '/storage'

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

userID = options.U
password = options.P
server_name = options.N
server_ip = options.target
domain = options.D
hashes = options.hashes
pattern = options.collection
os = options.O
#ccregex = "([4-6]{1})([0-9]{3}-?)([0-9]{4}-?){2}([0-9]{4})"
#pwdregex = "senha?(=|:| |: )[a-zA-Z0-9_]{4,}"
regexs = options.collection2

if server_name is None:
    server_name = ''

if domain is None:
    domain = ''

if password is None and userID != None and hashes is None:
    from getpass import getpass
    password = getpass("Password: ")
elif password is not None and userID is None:
    parser.print_help()
    print ""
    print "\033[1;34;40m[*]\033[1;31;40m Please enter a valid username or left both field blank\n"
elif userID is None and password is None:
    password = ''
    userID = ''

if options.hashes is not None:
    lmhash, nthash = options.hashes.split(':')
else:
    lmhash = ''
    nthash = ''

print ""
print banner

if options.smb == True:
    print "\033[1;37;41m --> Scanning files...\033[0;37;40m\n"
    p1 = smbmodule.SMBModule(userID, password, server_name, server_ip, domain)
    conn, shares = p1.connlist()
    
    for ftx in shares:
	    print "[*] Share "+ftx+" is avaliable"
    
    if os == 'Win':
        smbmodule.smbtunner(userID, password, server_ip, shares, conn, '\\', pattern, Windows, temp, regexs, os)
    elif os == 'Lin':
        smbmodule.smbtunner(userID, password, server_ip, shares, conn, '/', pattern, Windows, temp, regexs, os)
    else:
        print "[*] Choice between Lin or Win options"
        parser.print_help
        sys.exit(1)
else:
    print "\033[1;37;41m --> Please select a valid module\033[0;37;40m\n"
    parser.print_help()
    sys.exit(1)


