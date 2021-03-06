ip_block_command = "iptables -A INPUT -s %s -j DROP"
ip_unblock_command = "iptables -D INPUT -s %s -j DROP"

mac_block_command = "iptables -A INPUT -m mac --mac-source %s -j DROP"
mac_unblock_command = "iptables -I INPUT -m mac --mac-source %s -j ACCEPT"

url_block_command = "iptables -A INPUT -s" + "%s" + "-j DROP"
url_unblock_command = "iptables -D INPUT -s" + "%s" + "-j DROP"

wifi_access_killer = "sudo pkill -9 hostapd"

#dhcp
dhcp_enable_command = "sudo service isc-dhcp-server start"
dhcp_disable_command = "sudo service isc-dhcp-server stop"