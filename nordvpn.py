#!/usr/bin/python

import sys
import json
import requests
from pprint import pprint
from optparse import OptionParser
import ConfigParser
import os
import subprocess

HOMEDIR = os.getenv("HOME") + "/"
APPROOT = HOMEDIR + ".nordvpn/"
#VPNCONFIGS = os.getenv("HOME") + "/nordvpn.configs/"
config = ConfigParser.ConfigParser()
config.read(APPROOT + "nordvpn.conf")

min_load = 100
server_list = {}
apiURL = config.get('nordvpn', 'apiURL')
authFile = config.get('nordvpn', 'authFile')
openVPNFiles = config.get('nordvpn', 'openVPNFiles')
openVPNFilesURL = config.get('nordvpn', 'openVPNFilesURL')
DEF_PROTO  = config.get('nordvpn', config.get('nordvpn', 'DEF_PROTO'))
VPNConfigs = os.getenv("HOME") + "/" + config.get('nordvpn', 'openVpnFilesPath') + "/"
high_limit = int(config.get('nordvpn', 'limit'))

# defaults
dispall = False

parser = OptionParser()
parser.add_option("-c", "--country", action="store", type="string", dest="country", default="")
parser.add_option("-l", "--load", action="store", type="int", dest="load")
parser.add_option("-a", "--all", action="store_true", dest="dispall", default=False)
#print dispall


(opts, args) = parser.parse_args()

def get_api_files(localFile, remoteFile):

    # Download OpenVPN files

    vpnFileUrl = openVPNFilesURL + "/" + remoteFile

    print "Downloading " + vpnFileUrl + " -> " + localFile
    apif = requests.get(vpnFileUrl)

    with open(localFile, "wb") as code:
        code.write(apif.content)

    update_vpn_config(localFile)


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

# Main routine start
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
            
                if not (os.path.exists(loc_file)):
                    #print loc_file + " Going to download..."
                    get_api_files(loc_file, rem_file)
                
        elif len(str(opts.country)) == 0:
            print "Inside Else...\n"
            print str(data[s]['domain']) + " - " + str(data[s]['load'])
    
#print candidate + ' ' + str(min_load) + " - " + loc_file
print "***********************************************************************************"
print
print "      Country: " + countryFlag
print "Connecting to: " + loc_file
print " Current Load: " + str(min_load)
print
print "***********************************************************************************"

openvpn_cmd = ['sudo', 'openvpn', loc_file]
prog = subprocess.Popen(openvpn_cmd)

