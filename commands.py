ip_block_command = "iptables -A INPUT -s %s -j DROP"
ip_unblock_command = "iptables -D INPUT -s %s -j DROP"

mac_block_command = "iptables -A INPUT -m mac --mac-source %s -j DROP"
mac_unblock_command = "iptables -I INPUT -m mac --mac-source %s -j ACCEPT"

url_block_command = "iptables -A INPUT -s" + "%s" + "-j DROP"
url_unblock_command = "iptables -D INPUT -s" + "%s" + "-j DROP"
