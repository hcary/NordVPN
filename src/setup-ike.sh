#!/bin/bash

#declare -a packages=("strongswan-ikev2" "strongswan" "strongswan-plugin-eap-mschapv2" "libstrongswan-standard-plugins" "python-requests")
packages="strongswan-ikev2 strongswan strongswan-plugin-eap-mschapv2 libstrongswan-standard-plugins python-requests"
NORD_CONF_DIR=$HOME/.nordvpn
pylibpath=`python -c "import sys; print('\n'.join(sys.path))" | sed -r "/^\r?$/d" | head -1`

echo ""
echo "This script comes without warrenty and is meant to aid you in setting up your NordVPN client configurations and scripts"
echo "By running this script you agree than any damages or issues that arise are the reponsibility of the user."
echo ""
echo "The script will create the files in $NORD_CONF_DIR. You will need to enter y before it will replace the configuration files, you can also choose to manually put these files in place manually..."
echo ""
echo "This script will execute apt-get using sudo to install the prerequisites to run IKEv2/IPSEC mode NordVPN"
echo ""

CONSTRNT_FILE_TMP=$NORD_CONF_DIR"/constraints.conf"
SECRETS_TMP=$NORD_CONF_DIR"/ipsec.secrets"
IPSECCNF_TMP=$NORD_CONF_DIR"/ipsec.conf"
NORD_CRT_TMP=$NORD_CONF_DIR"/NordVPN.der"

CONSTRNT_FILE="/etc/strongswan.d/charon/constraints.conf"
SECRETS="/etc/ipsec.secrets"
IPSECCNF="/etc/ipsec.conf"
NORD_CRT="/etc/ipsec.d/cacerts/NordVPN.der"

if [ "$1" == "clean" ];
then
    rm -f $CONSTRNT_FILE_TMP $SECRETS_TMP $IPSECCNF_TMP $NORD_CRT_TMP $CONSTRNT_FILE_TMP.bak
    exit
fi



#sudo apt install strongswan strongswan-plugin-eap-mschapv2 strongswan-ikev2 libstrongswan-standard-plugins
echo ""

if [ ! -d $NORD_CONF_DIR ];
then
    
    mkdir $NORD_CONF_DIR
    chmod 700 $NORD_CONF_DIR
fi

   
echo "Updating $CONSTRNT_FILE load from yes to no"
cp $CONSTRNT_FILE $CONSTRNT_FILE_TMP
sed -i.bak s/load\ =\ yes/load\ =\ no/g $CONSTRNT_FILE_TMP   


echo "Enter your NordVPN username, followed by [ENTER]:"
read username

echo "Enter your NordVPN password, followed by [ENTER]:"
read password

#echo "${username} : EAP \"${password}\""
#username="my_username.$$"
#password="my_password.$$"

echo "Creating $SECRETS_TMP..."
cat > $SECRETS_TMP<<EOF
# This file holds shared secrets or RSA private keys for authentication."
# RSA private key for this host, authenticating it to any other host"

# which knows the public part.

${username} : EAP "${password}"

EOF

if [ -f /etc/ipsec.conf ];
then
    cp /etc/ipsec.conf /etc/ipsec.conf.bak
fi

echo "Creating $IPSECCNF_TMP..."
cat > $IPSECCNF_TMP<<EOF
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

cp nordvpn-ike.conf ~/.nordvpn
#sudo wget https://downloads.nordvpn.com/certificates/root.der -O /etc/ipsec.d/cacerts/NordVPN.der
echo "Downloading NordVPN root Certificate..."
wget https://downloads.nordvpn.com/certificates/root.der -O $NORD_CRT_TMP

echo All of the files created by the this install script are located in $NORD_CONF_DIR
echo
echo "You can press y to have the script put the files in place for you or do it manual [y/N]:"

read yn

if [ "$yn" == "y" ];
then

    echo "Checking Dependencies... "
    ## now loop through the above array
    sudo apt-get install $packages
#    for pkg in "${packages[@]}"
#    do
#        if [ $(dpkg-query -W -f='${Status}' $pkg 2>/dev/null | grep -c "ok installed") -eq 0 ];
#            then
#                sudo apt-get install $pkg
#        else
#                echo "  $pkg Installed..."
#        fi
#    done


    sudo cp $CONSTRNT_FILE_TMP $CONSTRNT_FILE
    sudo cp $SECRETS_TMP $SECRETS
    sudo cp $IPSECCNF_TMP $IPSECCNF
    sudo cp $NORD_CRT_TMP $NORD_CRT

fi

cat << EOF
************************************************************************************************************
Change SERVER to prefered NordVPN server in $IPSECCNF

Restart ipsec in order to reload all configuration files.

sudo ipsec restart​

If you've made any typos in /etc/ipsec.conf file you'll be notified when service will be trying to start.

After it's done, you can connect by launching this command:

sudo ipsec up NordVPN​

This command should show the output "connection NordVPN has been established successfully".

To disconnect, simply type sudo ipsec down NordVPN.
************************************************************************************************************

EOF
