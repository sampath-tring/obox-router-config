import os

MAC_ADDRESS_LIST = []

IP_ADDRESS_LIST = []

URL_LIST = []

def ip_address_blocker_and_unblocker(ip_address, block=None):
    if block:
        block_command = "iptables -A INPUT -s %s -j DROP" % (ip_address)
        command_executer = os.system(block_command)
        save_command = "service iptables save"
        command_executer = os.system(save_command)
    else:
        unblock_command = "iptables -D INPUT -s %s -j DROP" % (ip_address)
        command_executer = os.system(command)
        save_command = "service iptables save"
        command_executer = os.system(save_command)        

def mac_id_blocker_and_unblocker(mac_address, block=None):
    if block:
        block_command = "iptables -A INPUT -m mac --mac-source %s -j DROP" % (mac_address)
        command_executer = os.system(block_command)
        save_command = "service iptables save"
        command_executer = os.system(save_command)
    else:
        unblock_command = "iptables -I INPUT -m mac --mac-source %s -j ACCEPT" % (mac_address) 
        command_executer = os.system(unblock_command) 
        save_command = "service iptables save"
        command_executer = os.system(save_command)

def url_blocker_and_unblocker(url, block=None):
    if block:
        block_command = "iptables -t nat -I INPUT --sport 443 -m string \
                 --string %s --algo bm -j REJECT" % (url)
        command_executer = os.system(block_command)
        save_command = "service iptables save"
        command_executer = os.system(save_command)
    else:
        unblock_command = "" % (url) 
        command_executer = os.system(unblock_command) 
        save_command = "service iptables save"
        command_executer = os.system(save_command)   



