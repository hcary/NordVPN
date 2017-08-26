
install:
	apt-get install strongswan strongswan-plugin-eap-mschapv2 strongswan-ikev2 libstrongswan-standard-plugins
	wget https://downloads.nordvpn.com/certificates/root.der -O /etc/ipsec.d/cacerts/NordVPN.der
	
	install -o root -m 0700 ipsec.secrets /etc/ipsec.secrets
	install -o root -m 0744 ipsec.conf /etc/ipsec.conf
	install -o root -m 0700 constraints.conf /etc/strongswan.d/charon/constraints.conf