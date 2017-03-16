import os
import argparse
import subprocess
from commands import ip_block_command as ibc, ip_unblock_command as inc, mac_block_command as mbc, mac_unblock_command as muc, url_block_command as ubc, url_unblock_command as uuc
from paths import WIFI_ACCESS_POINT as wap
from termcolor import colored

#getting ipaddress, macaddress, url
parser = argparse.ArgumentParser()



parser.add_argument('-ip', '--ip', help="IP address", required=False)
parser.add_argument('-mac', '--mac', help="MAC address", required=False)
parser.add_argument('-url', '--url', help="URL", required=False)
parser.add_argument('-b', '--b', help="block", required=False, action='store_true')
parser.add_argument('-details', '--details', help="lisout existing device", required=False, action='store_true')
parser.add_argument('-reset', '--reset', help="Factory reset", required=False, action='store_true')

arguments = parser.parse_args()

ip_address = arguments.ip
mac_address = arguments.mac
url = arguments.url
block = arguments.b
device_details = arguments.details
factory_reset = arguments.reset

def ip_address_blocker_and_unblocker(ip_address, block=None):
    if block:
        block_command = ibc % (ip_address)
        command_executer = os.system(block_command)
        save_command = "service iptables save"
        command_executer = os.system(save_command)
        print colored("Device %s is blocked" % (ip_address), 'red')
    else:
        unblock_command = "iptables -D INPUT -s %s -j DROP" % (ip_address)
        command_executer = os.system(unblock_command)
        save_command = "service iptables save"
        command_executer = os.system(save_command)   
        print colored("Device %s is unblocked" % (ip_address), 'blue')     

def mac_id_blocker_and_unblocker(mac_address, block=None):
    if block:
        block_command =  mbc % (mac_address)
        command_executer = os.system(block_command)
        save_command = "service iptables save"
        command_executer = os.system(save_command)
        print colored("Device %s is blocked" % (mac_address), 'red')
    else:
        unblock_command =  muc % (mac_address) 
        command_executer = os.system(unblock_command) 
        save_command = "service iptables save"
        command_executer = os.system(save_command)
        print colored("Device %s is unblocked" % (mac_address), 'blue')

def url_blocker_and_unblocker(url, block=None):
    if block:
        block_command = "iptables -t nat -I INPUT --sport 443 -m string \
                 --string %s --algo bm -j REJECT" % (url)
        command_executer = os.system(block_command)
        save_command = "service iptables save"
        command_executer = os.system(save_command)
        print colored("url %s is blocked" % (url), 'red')
    else:
        unblock_command = "" % (url) 
        command_executer = os.system(unblock_command) 
        save_command = "service iptables save"
        command_executer = os.system(save_command)  
        print colored("url %s is unblocked" % (url), 'blue')

def device_details_listouter():
    command = "arp"
    command_executer = subprocess.call(command)      

def access_point_vanisher():
    for file in os.listdir(wap):
        file_path = os.path.join(wap, file)
        os.unlink(file_path)
        print colored("access point %s has been removed" % (file), 'red')       




if __name__ == "__main__":
    if ip_address:
        ip_address_blocker_and_unblocker(ip_address, block)
    elif mac_address:
        mac_id_blocker_and_unblocker(mac_address, block)
    if url:
        url_blocker_and_unblocker(url, block)        
    if device_details:
        device_details_listouter()
    if factory_reset:
        access_point_vanisher()    


