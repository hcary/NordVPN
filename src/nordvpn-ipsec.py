#!/usr/bin/python

import sys
#import json
#import requests
#from pprint import pprint
from optparse import OptionParser
import ConfigParser
import os
import subprocess
import libnordvpn
from libnordvpn import NordVPN 
import string
import os
import time

ipsec_restart = "sudo ipsec restart"
ipsec_up = "sudo ipsec up NordVPN"
ipsec_down = "sudo ipsec down NordVPN"
ipsec_status = "sudo ipsec status"

HOMEDIR = os.getenv("HOME") + "/"
APPROOT = HOMEDIR + ".nordvpn/"
#VPNCONFIGS = os.getenv("HOME") + "/nordvpn.configs/"
config = ConfigParser.ConfigParser()
config.read(APPROOT + "nordvpn.conf")

# Set min_load to 100 so that any value less than that will replace it as the system loops through list
min_load        = 100
server_list     = {}
BestServer      = "none"

#authFile        = config.get('nordvpn', 'authFile')
#openVPNPid      = config.get('nordvpn', 'pid')
#DEF_PROTO       = config.get('nordvpn', config.get('nordvpn', 'DEF_PROTO'))
#VPNConfigs      = os.getenv("HOME") + "/" + config.get('nordvpn', 'openVpnFilesPath') + "/"
#high_limit      = int(config.get('nordvpn', 'limit'))

# defaults
dispall = False
startVpn = False
help_flag = False
startVpn = True

parser = OptionParser()
parser.add_option("-c", "--country", action="store", type="string", dest="country", default="")
parser.add_option("-l", "--load", action="store", type="int", dest="load")
parser.add_option("-a", "--all", action="store_true", dest="dispall", default=False)
parser.add_option("-s", "--start", action="store_true", dest="startVpn")
#parser.add_option("-h", "--help", action="store_true", dest="help_flag", default=False)

#print dispall
(opts, args) = parser.parse_args()
file_name =  os.path.basename(sys.argv[0])

def help_func():
    print
    print file_name [options]
    print 
    print "  -c --country  define country to act on"
    print "  -l --load"
    print "  -a --all "
    print "  -s --start     Activate VPN to the best server"
    print "  -h --help      This screen"
    
    exit

def run_cmd(cmd_str):
    
    cmd = cmd_str + ' 2>&1 | tee -a {}'.format( APPROOT + 'ipsec.log' )
    print "cmd: " + cmd
    os.system( cmd )

x = NordVPN()
x.cflag = "US"

data = x.get_servers()

lcount = len(data)
for record in range(lcount):

    rid = data[record]['id']
    #if( str(data[record]['flag']) == 'US' ):


    #if( str(data[record]['flag']) == 'US' ):
    #print "  Server ID: " + str(x.bestId)
    #print "     Domain: " + str(data[x.bestArray]['domain'])
    #print "       Load: " + str(data[record]['load']) + " Current min: " + str(x.curmin)
    #print '------------------------------------------------------'
        #x.get_catagories(self, rid, data)   
    vpn_server = str(data[x.bestArray]['domain'])



filein = APPROOT + "ipsec.conf"
fileout = "/etc/ipsec.conf"

f = open(filein,'r')
filedata = f.read()
f.close()

newdata = filedata.replace("right=SERVER","right=" + vpn_server)

f = open(fileout,'w')
f.write(newdata)
f.close()


print "*************************************************************"
print ""
print " Configuring IPSEC for: " + vpn_server
print "                  Load: " + str(x.curmin)
print ""
print "*************************************************************"


#run_cmd( ipsec_restart )
#run_cmd( ipsec_up )

#time.sleep(30)


   
    