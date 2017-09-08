#!/usr/bin/python

# Python library for handling NordVPN server statistics
# 
import sys
import json
import requests

    
class NordVPN:
    
    data        = {}
    
    flag        = {}
    country     = {}
    load        = {}
    domain      = {}
    ikev2       = {}
    openvpn_udp = {}
    openvpn_tcp = {}
    ip_address  = {}
    
    
    def __init__(self):

        self.apiURL          = 'http://api.nordvpn.com/server'
        self.openVPNFiles    = 'https://nordvpn.com/api/files'
        self.openVPNFilesURL = 'https://nordvpn.com/api/files/download'

    
    def get_servers(self):     

        print "Calling " + self.apiURL
        r = requests.get(self.apiURL)
        print r.status_code
        if r.status_code != 200:
            print "Error retrieving data from " + apiURL
            #sys.exit()
            return 'Error ' + r.status_code
 
        data = json.loads(r.text)
    
        
    
        lcount = len(data)
        for s in range(lcount):
            
            self.ip_address[ data[s]['id'] ]     = data[s]['ip_address']  
            self.flag[ data[s]['id'] ]           = data[s]['flag']
            self.country[ data[s]['id'] ]        = data[s]['country']
            self.load[ data[s]['id'] ]           = data[s]['load']
            self.domain[ data[s]['id'] ]         = data[s]['domain']
            self.ikev2[ data[s]['id'] ]          = data[s]['features']['ikev2']
            self.openvpn_udp[ data[s]['id'] ]    = data[s]['features']['openvpn_udp']
            self.openvpn_tcp[ data[s]['id'] ]    = data[s]['features']['openvpn_tcp']
            
            
            #catagories[ data[s]['id'] ][ data[s]['categories'] ][ data[s]['name'] ]
        return data   
            
    def get_api_files(self, localFile, remoteFile):
    
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
    
    def get_lowest_load(self):
        print "hello"
        # inside get_lowest_load
        
