import os
import argparse
import subprocess

MAC_ADDRESS_LIST = []

IP_ADDRESS_LIST = []

URL_LIST = []

#getting ipaddress, macaddress, url
parser = argparse.ArgumentParser()

parser.add_argument('-ip', '--ip', help="IP address", required=False)
parser.add_argument('-mac', '--mac', help="MAC address", required=False)
parser.add_argument('-url', '--url', help="URL", required=False)
parser.add_argument('-b', '--b', help="block", required=False, action='store_true')
parser.add_argument('-details', '--details', help="lisout existing device", required=False, action='store_true')
arguments = parser.parse_args()

ip_address = arguments.ip
mac_address = arguments.mac
url = arguments.url
block =arguments.b
device_details = arguments.details

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

def device_details_listouter():
    command = "arp"
    command_executer = subprocess.call(command)         


if __name__ == "__main__":
    if ip_address:
        ip_address_blocker_and_unblocker(ip_address, block)
    elif mac_address:
        mac_id_blocker_and_unblocker(mac_address, block)
    if url:
        url_blocker_and_unblocker(url, block)        
    if device_details:
        device_details_listouter()


