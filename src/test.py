#!/usr/bin/python


from libnordvpn import NordVPN 
import string

#result = libnordvpn.get_servers()

x = NordVPN()
x.cflag = "US"

data = x.get_servers()

lcount = len(data)
for record in range(lcount):

    rid = data[record]['id']
    #if( str(data[record]['flag']) == 'US' ):

    #    print 'DOMAIN: ' + str(x.domain[rid])
        #print 'DOMAIN: ' + str(data[rid]['domain'])
        
        #print '         ID: ' + str(data[record]['id']) 
        #print '     Domain: ' + str(data[record]['domain'])   
        #print ' IP Address: ' + str(data[record]['ip_address'])
        #print '       Flag: ' + str(data[record]['flag'])
        #print '    Country: ' + str(data[record]['country'])
        #print '       Load: ' + str(data[record]['load'])
        #print '      IKEv2: ' + str(data[record]['features']['ikev2'])
        #print 'OpenVPN UDP: ' + str(data[record]['features']['openvpn_udp'])
        #print 'OpenVPN TCP: ' + str(data[record]['features']['openvpn_tcp'])
        
        #search_keywords
        
    #    print '------------------------------------------------------'

    #if( str(data[record]['flag']) == 'US' ):
    print "  Server ID: " + str(x.bestId)
    print "     Domain: " + str(data[x.bestArray]['domain'])
    print "       Load: " + str(data[record]['load']) + " Current min: " + str(x.curmin)
    print '------------------------------------------------------'
        #x.get_catagories(self, rid, data)   
    vpn_server = str(data[x.bestArray]['domain'])
    
fin = open("/home/hcary/.nordvpn/ipsec.conf", "r")
fout = open("/etc/ipsec.conf", "w")

lines = fin.readlines()
for line in lines:
    line = str(line)
    line = line.rstrip("\n")
    
    if line.find('right=SERVER') != -1:
        line = "  right=" + vpn_server
        
    print line
    fout.write(line + '\n') 
    

fout.close



   
    
    