#!/usr/bin/python

import sys
import json
import requests
from pprint import pprint
from optparse import OptionParser
import ConfigParser
import os
import subprocess
import libnordvpn

RESTART = "sudo ipsec restart"
TUN_UP = "sudo ipsec up NordVPN"
TUN_DOWN = "sudo ipsec down NordVPN"

HOMEDIR = os.getenv("HOME") + "/"
APPROOT = HOMEDIR + ".nordvpn/"
#VPNCONFIGS = os.getenv("HOME") + "/nordvpn.configs/"
config = ConfigParser.ConfigParser()
config.read(APPROOT + "nordvpn.conf")

# Set min_load to 100 so that any value less than that will replace it as the system loops through list
min_load        = 100
server_list     = {}
BestServer      = "none"

authFile        = config.get('nordvpn', 'authFile')
openVPNPid      = config.get('nordvpn', 'pid')
DEF_PROTO       = config.get('nordvpn', config.get('nordvpn', 'DEF_PROTO'))
VPNConfigs      = os.getenv("HOME") + "/" + config.get('nordvpn', 'openVpnFilesPath') + "/"
high_limit      = int(config.get('nordvpn', 'limit'))

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
    
def get_api_files(localFile, remoteFile):

    global BestServer
    # Download OpenVPN files
    if (os.path.exists(loc_file)):
        BestServer = localFile
        return
    
    vpnFileUrl = openVPNFilesURL + "/" + remoteFile

    print "Downloading " + vpnFileUrl + " -> " + localFile
    apif = requests.get(vpnFileUrl)
    
    #if isinstance('{"status":404}', apif.content):
    if '{"status":404}' in apif.content:
       print "Error: status: 404"
       #os.remove(localFile)
    else:
        with open(localFile, "wb") as code:
            code.write(apif.content)

        update_vpn_config(localFile)
        BestServer = localFile
        
def update_vpn_config(localFile):

    os.rename( localFile, localFile+"~" )
    destination= open( localFile, "w" )
    source= open( localFile+"~", "r" )
    for line in source:
        if "auth-user-pass" in line:
            line = line.replace("\n", " ")
            destination.write( line + " " + authFile )
        else:
           destination.write( line )

    os.remove(localFile+"~")   
    
def gen_remote_filename(fqdn):
    return fqdn + "." + DEF_PROTO

def gen_local_filename(fqdn):
    return fqdn + "." + DEF_PROTO + ".ovpn"

def gen_local_path(fqdn):
    return VPNConfigs + gen_local_filename(fqdn) 

def set_path(str):
    if str[0] != "/":
        return HOMEDIR + str

def start_vpn(loc_file):
    print "***********************************************************************************"
    print
    print "      Country: " + countryFlag
    print "Connecting to: " + loc_file
    print " Current Load: " + str(min_load)
    print
    print "***********************************************************************************"
    
    pid=os.fork()
    if pid==0: # new process
        print "sudo openvpn  --config " + loc_file + " &"
        os.system("sudo openvpn  --config " + loc_file + " &")
        exit()
    
####################################################################
# Main routine start

if ( help_flag ):
    help_func()
    
authFile = set_path(authFile)
#print authFile   
#
# Main function
print "Calling " + apiURL
r = requests.get(apiURL)
print r.status_code
if r.status_code != 200:
    print "Error retrieving data from " + apiURL
    sys.exit()

data = json.loads(r.text)

if not (opts.country is None):
    countryFlag = opts.country.upper()

lcount = len(data)

for s in range(lcount):
    if data[s]['load'] < high_limit or dispall == True:
        if len(str(countryFlag)) > 1 and countryFlag == str(data[s]['flag']):
            
            #print str(data[s]['domain']) + " - " + str(data[s]['load'])
            server_list[str(data[s]['domain'])] = [data[s]['load']]
            
            if data[s]['load'] < min_load:
                min_load = data[s]['load']
                candidate = data[s]['domain']

                loc_file = gen_local_path(data[s]['domain'])
                rem_file = gen_remote_filename(data[s]['domain'])
            
                #if not (os.path.exists(loc_file)):
            #   print loc_file + " Going to download..."
                get_api_files(loc_file, rem_file)
            
        elif len(str(opts.country)) == 0:
            print "Inside Else...\n"
            print str(data[s]['domain']) + " - " + str(data[s]['load'])


if startVpn == True:
    start_vpn(BestServer)


