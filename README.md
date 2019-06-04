# YAKA ---->>>

# Author: Frentzen

# Intro

Yaka is a tool of post-exploitation that search for files that contains sensitive information. Its atuation be in server of file sharing and mail service in local network and public web pages. Its name is based in arrow of Youndu, character of Guardians of Galaxy.

# Usage
```
usage: yaka.py [-h] [-U username] [-P passowrd] [-D domain] [-N hostname]
               [-hashes LMHASH:NTHASH] [-dc-ip ip-address]
               [-target ip-address] [-port [destination port]] [-O Lin or Win]
               [-pattern pattern]

YAKA is a tool for search of files

optional arguments:
  -h, --help            show this help message and exit

authentication:
  -U username           Username for connection in SMB share
  -P passowrd           Password for conncetion in SMB share
  -D domain             Domain for connection in SMB share
  -N hostname           Name of machine for connection in SMB share
  -hashes LMHASH:NTHASH
                        NTLM hashes, format is LMHASH:NTHASH

connection:
  -dc-ip ip-address     IP Address of the domain controller. If omitted it
                        will use the domain part (FQDN) specified in the
                        target parameter
  -target ip-address    IP Address of the target machine. If omitted it will
                        use whatever was specified as target. This is useful
                        when target is the NetBIOS name and you cannot resolve
                        it
  -port [destination port]
                        Destination port to connect to SMB Server
  -O Lin or Win         OS to choise

pattern:
  -pattern pattern      Pattern that will be search at name of files found
```
```
python yaka.py -U <username> -P <password> -N <server_hostname> -target <ip-address> -O <Lin|Win> -pattern <senha.txt>
```
# Requirements
```
pip install pysmb pyfiglet
```
