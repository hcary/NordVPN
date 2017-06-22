Welcome to NORD VPN for Linux
===========================
This Python script accepts a parameter of c for country and automatically downloads and connects you to the NordVPN system that has the lowest load.

It is currently a early BETA version that only covers the described functionality. 

My plan moving forward is to be able to list available countries, list server types such as peer-to-peer and double VPN and allow the user to choose a type. 

The script automatically downloads NordVPN configuration files to ~/nordvpn.configs, identified by the **openVpnFilesPath** variable in the configuration file and adds the path to your auth file to the configuation files for automatic VPN connection

Testing
-------
The project is currently being tested on Ubuntu 16.04 LTS

Running
-------
mkdir ~/.nordvpn
mkdir ~/nordvpn.configs
Create a auth file that contains your NordVPN username on the first list and password on the second line

Copy nordvpn.conf to ~/.nordvpn
Edit ~/.nordvpn/nordvpn.conf
Change **authFile** to point to you auth file

The default is to use UDP but can be changed to TCP by chaning the **DEF_PROTO**value in the configuration file. 

