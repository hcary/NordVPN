#!/usr/bin/python


from libnordvpn import NordVPN 

#result = libnordvpn.get_servers()

x = NordVPN()
data = x.get_servers()

lcount = len(data)
for record in range(lcount):

    rid = data[record]['id']
    if( str(data[record]['flag']) == 'US' ):

        print 'DOMAIN: ' + str(x.domain[rid])
    
        print '         ID: ' + str(data[record]['id']) 
        print '     Domain: ' + str(data[record]['domain'])   
        print ' IP Address: ' + str(data[record]['ip_address'])
        print '       Flag: ' + str(data[record]['flag'])
        print '    Country: ' + str(data[record]['country'])
        print '       Load: ' + str(data[record]['load'])
        print '      IKEv2: ' + str(data[record]['features']['ikev2'])
        print 'OpenVPN UDP: ' + str(data[record]['features']['openvpn_udp'])
        print 'OpenVPN TCP: ' + str(data[record]['features']['openvpn_tcp'])
        print '------------------------------------------------------'
    
    
    