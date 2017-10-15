Welcome to NORD VPN for Linux
===========================

This is not an offial Nord VPN project, I wanted similar functionality on Linux as they provide on other platforms. They upgrade and add servers regularly so a method to manage and connect to the system with the lowest load was needed for Linux.

This Python script accepts a parameter of c for country and automatically downloads and connects you to the NordVPN system that has the lowest load.

It is currently a early BETA version that only covers the described functionality. 

My plan moving forward is to be able to list available countries, list server types such as peer-to-peer and double VPN and allow the user to choose a type. 

The script automatically downloads NordVPN configuration files to ~/nordvpn.configs, identified by the **openVpnFilesPath** variable in the configuration file and adds the path to your auth file to the configuation files for automatic VPN connection

Testing
-------
The project is currently being tested on Ubuntu 16.04 LTS
