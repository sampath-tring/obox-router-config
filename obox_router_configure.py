import os
import re
import itertools
import argparse
import subprocess
from commands import ip_block_command as ibc, ip_unblock_command as inc, \
mac_block_command as mbc, mac_unblock_command as muc, url_block_command as ubc, \
url_unblock_command as uuc
from paths import WIFI_ACCESS_POINT as wap, DHCP_LEASE_FILE as dlf
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

def device_details():
    file_opener = open(dlf, "rb")
    file_reader = file_opener.readlines()
    ip_address_list = []
    mac_address_list = []
    binding_list = []
    hostname_list = []
    for line in file_reader:
        if "lease " in line and "#" not in line:
            ip_address_list.append(line.replace("lease ", "").replace("{","").replace("\n", ""))
        if "hardware ethernet" in line:
            mac_address_list.append(line.replace("hardware ethernet ", "").replace(";", "").replace("\n", ""))
        if "binding state" in line and "next" not in line and "rewind" not in line:
            binding_list.append(line.replace("binding state", "").replace(";", "").replace("\n", ""))
        # if "client-hostname" in line:
        #   hostname_list.append(line.replace("client-hostname ","").replace(";","").replace('"', ''))  
    listed_value = [list(values) for values in zip(ip_address_list,mac_address_list, binding_list)]
    listed_value_wo_duplicates = list(listed_value for listed_value,_ in itertools.groupby(listed_value))
    final_details_list = []
    for data in listed_value_wo_duplicates:
        final_details_list.append(data) if "   free" not in data[2] else ""
    
    print tabulate(final_details_list, headers = ['Ipaddress', 'Macaddress', 'Binding List'])    
    
def access_point_vanisher():
    for file in os.listdir(wap):
        file_path = os.path.join(wap, file)
        os.unlink(file_path)
        print colored("access point %s has been removed" % (file), 'red')  

def vpn_vanisher():
    for file in os.listdir(vpn):
        file_path = os.path.join(vpn, file)
        os.unlink(file_path)
        print colored("vpn %s has been removed") % (file), 'red')     

def black_list_remover():




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
        vpn_vanisher()   


