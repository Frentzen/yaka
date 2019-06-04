import sys
import urllib2
import argparse
import re
import tempfile
from smb.SMBConnection import SMBConnection
import os
from pyfiglet import Figlet
from colorama import Fore, Back, Style
import string
from smb.SMBHandler import SMBHandler




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
group = parser.add_argument_group('pattern')
group.add_argument('-pattern', action='append', metavar="pattern", dest="collection", default=[], help="Pattern that will be search at name of files found")


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
ccregex = "([4-6]{1})([0-9]{3}-?)([0-9]{4}-?){2}([0-9]{4})"
pwdregex = "senha?(=|:| |: )[a-zA-Z0-9_]{4,}"

regexs = [pwdregex]

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

if options.hashes is not None:
    lmhash, nthash = options.hashes.split(':')
else:
    lmhash = ''
    nthash = ''


conn = SMBConnection(userID, password, server_name, server_name, use_ntlm_v2 = True, is_direct_tcp = True)
conn.connect(server_ip, 445)

resp = conn.listShares()
shares = []


for a in range(len(resp)):
    shares.append(resp[a].name)


files = []
directories = []


def walk_pathw(path):    
    
    for e in range(len(shares)):
        try:
            delta = []
            delta = conn.listPath(shares[e], path)
            for x in delta:
                if x.filename == '..' or x.filename == '.':
                    pass
            
                elif x.isDirectory > 0:
                    parentPath = path
                    if not parentPath.endswith('\\'):
                        parentPath += '\\'
                    walk_pathw(parentPath+x.filename)
                    directories.append(x.filename)
                
                elif x.isDirectory == 0:
                    parentPath = path
                    if not parentPath.endswith('\\'):
                        parentPath += '\\'
		    var1 = parentPath
		    var2 = re.sub(r'\\', '/', var1)
		    for patterns in pattern:
			if re.search(patterns, x.filename):
			    if Windows == True:
				fh = open(temp+'\\'+x.filename, 'wb')
				conn.retrieveFile(shares[e], parentPath+x.filename, fh)
				fh.close()
				print "[*] "+x.filename+" found with your pattern it is in your temp dir"
			    else:
				fh = open(temp+'/'+x.filename, 'wb')
				conn.retrieveFile(shares[e], parentPath+x.filename, fh)
				fh.close()
				print "[*] "+x.filename+" found with your pattern it is in your temp dir"
			else:
			    director = urllib2.build_opener(SMBHandler)
			    ft = director.open('smb://'+userID+':'+password+'@'+server_ip+'/'+shares[e]+var2+x.filename)
			    data = ft.read()
			    for reg in regexs:
			        if re.search(reg, data):
			    	    if Windows == True:
				        fh = open(temp+'\\'+x.filename, 'wb')
				        conn.retrieveFile(shares[e], parentPath+x.filename, fh)
				        fh.close()
				        print "[*] Data found in"+x.filename+" with the follow "+reg
			            else:
				        fh = open(temp+'/'+x.filename, 'wb')
				        conn.retrieveFile(shares[e], parentPath+x.filename, fh)
				        fh.close()
				        print "[*] Data found in"+x.filename+" with the follow "+reg
				
        except:
            pass


def walk_path(path):    
    
    for e in range(len(shares)):
        try:
            delta = []
            delta = conn.listPath(shares[e], path)
            for x in delta:
                if x.filename == '..' or x.filename == '.':
                    pass
            
                elif x.isDirectory > 0:
                    parentPath = path
                    if not parentPath.endswith('/'):
                        parentPath += '/'
                    walk_path(parentPath+x.filename)
                    directories.append(x.filename)
                
                elif x.isDirectory == 0:
                    parentPath = path
                    if not parentPath.endswith('/'):
                        parentPath += '/'
		    var1 = parentPath
		    for patterns in pattern:
			if re.search(patterns, x.filename):
			    if Windows == True:
				fh = open(temp+'\\'+x.filename, 'wb')
				conn.retrieveFile(shares[e], parentPath+x.filename, fh)
				fh.close()
				print "[*] "+x.filename+" found with your pattern it is in your temp dir"
			    else:
				fh = open(temp+'/'+x.filename, 'wb')
				conn.retrieveFile(shares[e], parentPath+x.filename, fh)
				fh.close()
				print "[*] "+x.filename+" found with your pattern it is in your temp dir"
			else:
			    director = urllib2.build_opener(SMBHandler)
			    ft = director.open('smb://'+userID+':'+password+'@'+server_ip+'/'+shares[e]+var2+x.filename)
			    data = ft.read()
			    for reg in regexs:
			        if re.search(reg, data):
			    	    if Windows == True:
				        fh = open(temp+'\\'+x.filename, 'wb')
				        conn.retrieveFile(shares[e], parentPath+x.filename, fh)
				        fh.close()
				        print "[*] Data found in"+x.filename+" with the follow "+reg
			            else:
				        fh = open(temp+'/'+x.filename, 'wb')
				        conn.retrieveFile(shares[e], parentPath+x.filename, fh)
				        fh.close()
				        print "[*] Data found in"+x.filename+" with the follow "+reg
				
        except:
            pass
    
print ""
banner = Figlet(font='epic')
print(banner.renderText("YAKA ---->>>"))

print "\033[1;37;41m --> Downloading files...\033[0;37;40m\n"

if os == 'Win':
    walk_pathw('\\')
elif os == 'Lin':
    walk_path('/')
'''
def grepfile():
    count = 0
    for c in files:
        for d in pattern:
            if re.search(d, c):
                print "\033[1;36;40m [*] \033[1;31;40m"+c+"\033[0;37;40m match with pattern\n"
                count += 1
            
    if not count > 0:
        print "\033[1;36;40m [*] \033[0;37;40m No file contains the desired pattern\n"  


def cred_card():
    for y in files:
        ft = open(temp+'/'+y)
        for line in ft:
            line = line.rstrip()
            w = re.match(ccregex, line)
            if w is not None:
                print "\033[1;36;40m [*] \033[1;31;40m"+w.group(0)+"\033[0;37;40m appears to be a credit card number\n"
    

def search_pwd():
    for t in files:
        fu = open(temp+'/'+t)
        for line in fu:
            line = line.rstrip()
            w = re.match(pwdregex, line)
            if w is not None:
                print "\033[1;36;40m [*] \033[1;31;40m"+w.group(0)+"\033[0;37;40m appears to be a password in "+t+"\n"


print "\033[1;37;41m --> Runing credit card number search...\033[0;37;40m\n"
#cred_card()
print "\033[1;37;41m --> Runing password search...\033[0;37;40m\n"
#search_pwd()
print "\033[1;37;41m --> Runing filename search...\033[0;37;40m\n"
#grepfile()
'''