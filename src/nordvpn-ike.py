#!/usr/bin/python

# MIT License

# Copyright (c) [2017] [Harvey Cary]

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
from optparse import OptionParser
import ConfigParser
from libnordvpn import NordVPN

HOMEDIR = os.getenv("HOME") + "/"
APPROOT = HOMEDIR + ".nordvpn/"
config = ConfigParser.ConfigParser()
config.read(APPROOT + "nordvpn-ike.conf")

# Set min_load to 100 so that any value less than that will replace it as the system loops through list
min_load        = 100
server_list     = {}
BestServer      = "none"

# defaults
dispall = False
startVpn = False
help_flag = False
startVpn = True

def_country = config.get('nordvpn', 'DEF_COUNTRY')

parser = OptionParser("usage: %prog [options] ",
                          version="%prog 1.0")

parser.add_option("-c", "--country",
                action="store",
                type="string",
                dest="str_country",
                default=config.get('nordvpn', 'DEF_COUNTRY'),
                help="2 digit country identifier")

parser.add_option("-m", "--mode",
                action="store",
                type="string",
                dest="str_mode",
                default=config.get('nordvpn', 'DEF_MODE'),
                help="Mode to run in ink or openvpn")

parser.add_option("-l", "--load",
                action="store",
                type="int",
                dest="load")

parser.add_option("-a", "--all",
                  action="store_true",
                  dest="dispall",
                  default=False)




(options, args) = parser.parse_args()

file_name =  os.path.basename(sys.argv[0])



def help_func():
    print
    print file_name [options]
    print 
    print "  -c --country  define country to act on"
    print "  -l --load"
    print "  -h --help      This screen"
    
    exit

def run_cmd(cmd_str):
    
    cmd = cmd_str + ' 2>&1 | tee -a {}'.format( APPROOT + 'ipsec.log' )
    print "cmd: " + cmd
    os.system( cmd )

x = NordVPN()
x.cflag = options.str_country.upper()

data = x.get_servers()

lcount = len(data)
for record in range(lcount):

    rid = data[record]['id']
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


   
    