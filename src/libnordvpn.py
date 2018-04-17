#!/usr/bin/python

# Python library for handling NordVPN server statistics
#
import os
import sys
import json
import requests
import zipfile
    
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
    
    curmin      = 100
    bestId      = ''
    bestArray   = ''
    
    
    def __init__(self):

        self.apiURL             = 'http://api.nordvpn.com/server'
        self.openVPNFiles       = 'https://nordvpn.com/api/files'
        self.openVPNFilesURL    = 'https://nordvpn.com/api/files/download'
        #self.data               = {}
        self.curmin             = 100
        self.bestId             = ''
        self.cflag              = None
        
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
            
            
            if self.cflag is not None:
                if str(data[s]['flag']) != self.cflag:
                    continue
            
            if data[s]['load'] < self.curmin:
                self.curmin = data[s]['load']
                self.bestId = data[s]['id']
                self.bestArray = s
                
                #print "Current min: " + str(self.curmin)
                #print "  Server ID: " + str(self.bestId)
                
                                      
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
    

        
    def get_catagories(self, rid, data):
        
        print rid
        lcount = len(data[rid]['categories'])
        
        for s in range(lcount):
            print 'Catagories: ' + str(data[s]['categories']['name'])
            
        
        
        
    def get_api_files(self, local_path, server_ovpn):
                      #local_file, remote_file):
    
        # Download OpenVPN files
        local_file = local_path + "/" + server_ovpn
        if (os.path.exists(local_file)):
            BestServer = local_file
            return
        
        vpnFileUrl = self.openVPNFilesURL + "/" + server_ovpn
    
        print "Downloading " + vpnFileUrl + " -> " + local_file
        apif = requests.get(vpnFileUrl)
        
        #if isinstance('{"status":404}', apif.content):
        if '{"status":404}' in apif.content:
           print "Error: status: 404"
           #os.remove(local_file)
        else:
            with open(local_file, "wb") as code:
                code.write(apif.content)
    
            update_vpn_config(local_file)
            BestServer = local_file
    
    def get_ovpn_zip(self, ovpn_configs, url_ovpn_configs, ovpn_file):

        local_file = ovpn_configs + "/" + ovpn_file
        uri = url_ovpn_configs + ovpn_file
        
        print "Downloading " + uri + " -> " + local_file
        apif = requests.get(uri)

        #if isinstance('{"status":404}', apif.content):
        if '{"status":404}' in apif.content:
           print "Error: status: 404"
           #os.remove(local_file)
        else:
            with open(local_file, "wb") as code:
                code.write(apif.content)
        
        with zipfile.ZipFile(local_file, "r") as zip_ref:
            zip_ref.extractall(ovpn_configs)
        
        #os.chown(ovpn_configs, os.getlogin(), os.getlogin())
        
    def get_lowest_load(self):
        print "hello"
        # inside get_lowest_load
        
