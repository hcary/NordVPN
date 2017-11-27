Welcome to NORD VPN IKEv2 for Linux
===========================
This is not an offial Nord VPN project, I wanted similar functionality on Linux as they provide on other platforms. They upgrade and add servers regularly so a method to manage and connect to the system with the lowest load was needed for Linux.

This Python script accepts a parameter of c for country and automatically downloads and connects you to the NordVPN system that has the lowest load.

It is currently a early BETA version that only covers the described functionality. 

Execution
---------
/usr/local/bin/nordvpn.sh **executes** /usr/local/bin/nordvpn.py 
/usr/local/bin/nordvpn.py **writes startup instructions to** /usr/local/bin/nord.sh
/usr/local/bin/nordvpn.sh **executes** /usr/local/bin/nord.sh to establish tunnel

Feature Road Map
----------------

My plan moving forward is to be able to list available countries, list server types such as peer-to-peer and double VPN and allow the user to choose a type. 

The script automatically downloads NordVPN configuration files to ~/nordvpn.configs, identified by the **openVpnFilesPath** variable in the configuration file and adds the path to your auth file to the configuation files for automatic VPN connection

Testing
-------
The project is currently being tested on Ubuntu 16.04 LTS

Install
-------
**sudo ./setup-ike.sh** 
[sudo] password for hcary: 

This script comes without warrenty and is meant to aid you in setting up your NordVPN client configurations and scripts
By running this script you agree than any damages or issues that arise are the reponsibility of the user.

The script will create the files in /home/**USERNAME**/.nordvpn. You will need to enter y before it will replace the configuration files, you can also choose to manually put these files in place manually...

This script will execute apt-get using sudo to install the prerequisites to run IKEv2 mode NordVPN

Updating /etc/strongswan.d/charon/constraints.conf load from yes to no
Enter your NordVPN username, followed by [ENTER]:
**my_user_name**
Enter your NordVPN password, followed by [ENTER]:
**my_passwd**                                                                                                                                                                         
Creating /home/**USERNAME**/.nordvpn/ipsec.secrets...                                                                                                                                    
Creating /home/**USERNAME**/.nordvpn/ipsec.conf...                                                                                                                                       
Downloading NordVPN root Certificate...                                                                                                                                           
--2017-11-02 11:34:18--  https://downloads.nordvpn.com/certificates/root.der                                                                                                      
Resolving downloads.nordvpn.com (downloads.nordvpn.com)... 104.20.16.34, 104.20.17.34                                                                                             
Connecting to downloads.nordvpn.com (downloads.nordvpn.com)|104.20.16.34|:443... connected.                                                                                       
HTTP request sent, awaiting response... 200 OK                                                                                                                                    
Length: 1294 (1.3K) [application/x-x509-ca-cert]                                                                                                                                  
Saving to: ‘/home/**USERNAME**/.nordvpn/NordVPN.der’                                                                                                                                     

/home/hcary/.nordvpn/NordVPN.der             100%[============================================================================================>]   1.26K  --.-KB/s    in 0s       

2017-11-02 11:34:19 (12.5 MB/s) - ‘/home/**USERNAME**/.nordvpn/NordVPN.der’ saved [1294/1294]                                                                                            

All of the files created by the this install script are located in /home/**USERNAME**/.nordvpn                                                                                           

**You can press y to have the script put the files in place for you or do it manual [y/N]:**


Running
-------
sudo ~/.nordvpn-ike up -c US

The default is to use UDP but can be changed to TCP by chaning the **DEF_PROTO**value in the configuration file. 

