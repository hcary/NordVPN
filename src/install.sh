#!/bin/bash

#CONSTRNT_FILE="/etc/strongswan.d/charon/constraints.conf"
#SECRETS="/etc/ipsec.secrets​"
#IPSECCNF="/etc/ipsec.conf"

CONSTRNT_FILE="constraints.conf"
SECRETS="ipsec.secrets​"
IPSECCNF="ipsec.conf"

# 
#sudo apt install strongswan strongswan-plugin-eap-mschapv2 strongswan-ikev2 libstrongswan-standard-plugins

echo "Chaning $CONSTRNT_FILE load from yes to no and creating backup file $CONSTRNT_FILE.bak"
sed -i.bak s/load\ =\ yes/load\ =\ no/g $CONSTRNT_FILE

echo "Enter your NordVPN username, followed by [ENTER]:"
read username

echo "Enter your NordVPN password, followed by [ENTER]:"
read password

#echo "${username} : EAP \"${password}\""
username="my_username.$$"
password="my_password.$$"
echo $HOME

cat > $SECRETS<<EOF
# This file holds shared secrets or RSA private keys for authentication."
# RSA private key for this host, authenticating it to any other host"

# which knows the public part.

${username} : EAP "${password}"

EOF

if [ -f /etc/ipsec.conf ];
then
    cp /etc/ipsec.conf /etc/ipsec.conf.bak
fi

cat > $IPSECCNF<<EOF
conn NordVPN
  keyexchange=ikev2
  dpdaction=clear
  dpddelay=300s
  eap_identity="${username}"
  leftauth=eap-mschapv2
  left=%defaultroute
  leftsourceip=%config
  right=SERVER
  rightauth=pubkey
  rightsubnet=0.0.0.0/0
  rightid=%any
  type=tunnel
  auto=add

EOF

#sudo wget https://downloads.nordvpn.com/certificates/root.der -O /etc/ipsec.d/cacerts/NordVPN.der
wget https://downloads.nordvpn.com/certificates/root.der -O NordVPN.der

