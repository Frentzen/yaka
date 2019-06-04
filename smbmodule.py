import urllib2
import re
from smb.SMBConnection import SMBConnection
from smb.SMBHandler import SMBHandler

class SMBModule:

    def __init__(self, userID, password, server_name, server_ip, domain):
        self.userID = userID
        self.password = password
        self.server_name = server_name
        self.server_ip = server_ip
        self.domain = domain
        
    
    def connlist(self):
        obj = SMBConnection(self.userID, self.password, self.server_name, self.server_name, use_ntlm_v2 = True, is_direct_tcp = True)
        obj.connect(self.server_ip, 445)
        resp = obj.listShares()
        shares = []
        for share in range(len(resp)):
            shares.append(resp[share].name)
        return obj, shares


def walk_pathw(userID, password, server_ip, shared, conn, path, patterns, Windows, temp, regexs):
    for count in range(len(shared)):
        try:
            delta = []
            delta = conn.listPath(shared[count], path)
            for x in delta:
                if x.filename == '..' or x.filename == '.':
                    pass
                elif x.isDirectory > 0:
                    parentPath = path
                    if not parentPath.endswith('\\'):
                        parentPath += '\\'
                    walk_pathw(userID, password, server_ip, shared, conn, parentPath+x.filename, patterns, Windows, temp, regexs)
                elif x.isDirectory == 0:
                    parentPath = path
                    if not parentPath.endswith('\\'):
                        parentPath += '\\'
                    var1 = parentPath
                    var2 = re.sub(r'\\', '/', var1)
                    for pattern in patterns:
                        if re.search(pattern, x.filename):
                            if Windows == True:
                                fh = open(temp+'\\'+x.filename, 'wb')
                                conn.retrieveFile(shared[count], parentPath+x.filename, fh)
                                fh.close()
                                print "[*] "+x.filename+" found with your pattern it is in your temp dir"
                            else:
                                fh = open(temp+'/'+x.filename, 'wb')
                                conn.retrieveFile(shared[count], parentPath+x.filename, fh)
                                fh.close()
                                print "[*] "+x.filename+" found with your pattern it is in your temp dir"
                        else:
                            director = urllib2.build_opener(SMBHandler)
                            ft = director.open('smb://'+userID+':'+password+'@'+server_ip+'/'+shared[count]+var2+x.filename)
                            data = ft.read()
                            for reg in regexs:
                                if re.search(reg, data):
                                    if Windows == True:
                                        fh = open(temp+'\\'+x.filename, 'wb')
                                        conn.retrieveFile(shared[count], parentPath+x.filename, fh)
                                        fh.close()
                                        print "[*] Data found in "+x.filename+" with the follow regex: "+reg+"\n"
                                    else:
                                        fh = open(temp+'/'+x.filename, 'wb')
                                        conn.retrieveFile(shared[count], parentPath+x.filename, fh)
                                        fh.close()
                                        print "[*] Data found in "+x.filename+" with the follow regex: "+reg+"\n"
        except:
            pass

def walk_pathl(userID, password, server_ip, shared, conn, path, patterns, Windows, temp, regexs):
    for count in range(len(shared)):
        try:
            delta = []
            delta = conn.listPath(shared[count], path)
            for x in delta:
                if x.filename == '..' or x.filename == '.':
                    pass
                elif x.isDirectory > 0:
                    parentPath = path
                    if not parentPath.endswith('/'):
                        parentPath += '/'
                    walk_pathl(userID, password, server_ip, shared, conn, parentPath+x.filename, patterns, Windows, temp, regexs)
                elif x.isDirectory == 0:
                    parentPath = path
                    if not parentPath.endswith('/'):
                        parentPath += '/'
                    var1 = parentPath
                    for pattern in patterns:
                        if re.search(pattern, x.filename):
                            if Windows == True:
                                fh = open(temp+'\\'+x.filename, 'wb')
                                conn.retrieveFile(shared[count], parentPath+x.filename, fh)
                                fh.close()
                                print "[*] "+x.filename+" found with your pattern it is in your temp dir"
                            else:
                                fh = open(temp+'/'+x.filename, 'wb')
                                conn.retrieveFile(shared[count], parentPath+x.filename, fh)
                                fh.close()
                                print "[*] "+x.filename+" found with your pattern it is in your temp dir"
                        else:
                            director = urllib2.build_opener(SMBHandler)
                            ft = director.open('smb://'+userID+':'+password+'@'+server_ip+'/'+shared[count]+var1+x.filename)
                            data = ft.read()
                            for reg in regexs:
                                if re.search(reg, data):
                                    if Windows == True:
                                        fh = open(temp+'\\'+x.filename, 'wb')
                                        conn.retrieveFile(shared[count], parentPath+x.filename, fh)
                                        fh.close()
                                        print "[*] Data found in "+x.filename+" with the follow regex: "+reg+"\n"
                                    else:
                                        fh = open(temp+'/'+x.filename, 'wb')
                                        conn.retrieveFile(shared[count], parentPath+x.filename, fh)
                                        fh.close()
                                        print "[*] Data found in "+x.filename+" with the follow regex: "+reg+"\n"
        except:
            pass
