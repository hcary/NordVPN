#!/usr/bin/python


from libnordvpn import NordVPN 
import string
import os
import subprocess

ipsec_restart = "sudo /usr/sbin/ipsec restart"
ipsec_up = "sudo ipsec up NordVPN"
ipsec_up = "ipsec up NordVPN"
ipsec_down = "sudo ipsec down NordVPN"
ipsec_status = "sudo ipsec status"
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
#    print "  Server ID: " + str(x.bestId)
#    print "     Domain: " + str(data[x.bestArray]['domain'])
#    print "       Load: " + str(data[record]['load']) + " Current min: " + str(x.curmin)
#    print '------------------------------------------------------'
        #x.get_catagories(self, rid, data)   
    vpn_server = str(data[x.bestArray]['domain'])



filein = "/home/hcary/.nordvpn/ipsec.conf"
fileout = "/etc/ipsec.conf"

f = open(filein,'r')
filedata = f.read()
f.close()

newdata = filedata.replace("right=SERVER","right=" + vpn_server)

f = open(fileout,'w')
f.write(newdata)
f.close()


print "***************************************"
print " Starting IPSEC for " + vpn_server
#pid=os.fork()
#if pid==0: # new process

print "  " + ipsec_restart
os.system(ipsec_restart)
    #exit()

#pid=os.fork()
#if pid==0: # new process
#    print "  sudo ipsec up NordVPN"
#    os.system("sudo ipsec up NordVPN")
#    exit()  

#subprocess.Popen(["nohup", "sudo ipsec up NordVPN"],
#    stdout=open('/dev/null', 'w'),
#    stderr=open('logfile.log', 'a'),
#    preexec_fn=os.setpgrp
#    )
   
    