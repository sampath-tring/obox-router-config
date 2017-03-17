import os
import re
import itertools
import argparse
import subprocess
from tabulate import tabulate
from commands import ip_block_command as ibc, ip_unblock_command as inc, \
mac_block_command as mbc, mac_unblock_command as muc, url_block_command as ubc, \
url_unblock_command as uuc, wifi_access_killer as wak, dhcp_enable_command as dec, \
dhcp_disable_command as ddc
from paths import WIFI_ACCESS_POINT as wap, DHCP_LEASE_FILE as dlf, \
DHCP_LEASE_FILE_PATH as dlfp, IP_ADDRESS_LOG_FILE as ip_log_file, \
MAC_ADDRESS_LOG_FILE as mac_log_file, \
URL_LOG_FILE as url_log_file
from termcolor import colored

#getting ipaddress, macaddress, url
parser = argparse.ArgumentParser()

parser.add_argument('-ip', '--ip', help="IP address", required=False)
parser.add_argument('-mac', '--mac', help="MAC address", required=False)
parser.add_argument('-url', '--url', help="URL", required=False)
parser.add_argument('-b', '--b', help="block", required=False, action='store_true')
parser.add_argument('-details', '--details', help="lisout existing device", required=False, action='store_true')
#dhcp
parser.add_argument('-dhcp', '--dhcp', help="dhcp", required=False, action='store_true')
parser.add_argument('-enable', '--enable', help="dhcp enable", required=False, action='store_true')
parser.add_argument('-disable', '--disable', help="dhcp disable", required=False, action='store_true')

parser.add_argument('-reset', '--reset', help="Factory reset", required=False, action='store_true')

arguments = parser.parse_args()

ip_address = arguments.ip
mac_address = arguments.mac
url = arguments.url
block = arguments.b
device_details = arguments.details
factory_reset = arguments.reset
#dhcp
dhcp = arguments.dhcp
dhcp_enable = arguments.enable
dhcp_disable = arguments.disable

def ip_address_blocker_and_unblocker(ip_address, block=None):
    if block:
        block_command = ibc % (ip_address)
        command_executer = os.system(block_command)
        save_command = "service iptables save"
        command_executer = os.system(save_command)
        #adding the ip to black list log file
        blacklist_log_file_creator(ip_address=ip_address)
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
        #adding the mac id to black list log file
        blacklist_log_file_creator(mac_address=mac_address)
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
        #adding url to black list log file
        blacklist_log_file_creator(url=url)
        print colored("url %s is blocked" % (url), 'red')
    else:
        unblock_command = "" % (url) 
        command_executer = os.system(unblock_command) 
        save_command = "service iptables save"
        command_executer = os.system(save_command)  
        print colored("url %s is unblocked" % (url), 'blue')

def blacklist_log_file_creator(ip_address=None, mac_address=None, url=None):
    if ip_address:
        file_opener = open(ip_log_file, "a")
        write = file_opener.write(ip_address+"\n")
        file_opener.close()
    elif mac_address:
        file_opener = open(mac_log_file, "a")
        write = file_opener.write(mac_address+"\n")
        file_opener.close()
    elif url:
        file_opener = open(url_log_file, "a")
        write = file_opener.write(url+"\n")
        file_opener.close()              

def blacklist_vanisher():
    ip_file_opener = open(ip_log_file, "r")
    for ip_address in ip_file_opener.readlines():
        ip_address_blocker_and_unblocker(ip_address=ip_address)
    ip_file_opener.close()

    mac_file_opener = open(mac_log_file, "r")
    for mac_address in mac_file_opener.readlines():
        mac_id_blocker_and_unblocker(mac_address=mac_address)
    mac_file_opener.close()    

    url_file_opener = open(url_log_file, "r")
    for url in url_file_opener.readlines():
        url_blocker_and_unblocker(url=url) 
    url_file_opener.close()       

def device_details():
    if os.path.exists(dlf):
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
        file_opener.close()
        # if "client-hostname" in line:
        #   hostname_list.append(line.replace("client-hostname ","").replace(";","").replace('"', ''))  
        listed_value = [list(values) for values in zip(ip_address_list,mac_address_list, binding_list)]
        listed_value_wo_duplicates = list(listed_value for listed_value,_ in itertools.groupby(listed_value))
        final_details_list = []
        for data in listed_value_wo_duplicates:
            final_details_list.append(data) if "   free" not in data[2] else ""
    
        print tabulate(final_details_list, headers = ['Ipaddress', 'Macaddress', 'Binding List']) 
    else:
        print "Dhcp lease file not found..."       

#reset    
def access_point_vanisher():
    command = wak
    os.system(command)
    for file in os.listdir(wap):
        file_path = os.path.join(wap, file)
        os.unlink(file_path)
        print colored("previously connected access point cleared", 'red')  

def connected_device_vanisher():
    for file in os.listdir(dlfp):
        if "dhcpd.leases" in file:
            file_path = os.path.join(dlfP, file)
            os.unlink(file_path)
            print colored("previously connected devices cleared", 'red')   

#dhcp
def dhcp_enabler_and_disabler(enable=None):
    if enable:
        os.system(dec)
        print colored("DHCP enabled", 'blue')
    else:
        os.system(ddc)    
        print colored("DHCP disabled", 'red')



if __name__ == "__main__":
    if ip_address:
        ip_address_blocker_and_unblocker(ip_address, block)
    elif mac_address:
        mac_id_blocker_and_unblocker(mac_address, block)
    if url:
        url_blocker_and_unblocker(url, block)        
    if device_details:
        device_details()
    if factory_reset:
        access_point_vanisher() 
        connected_device_vanisher()
        blacklist_vanisher()
    if dhcp:
        dhcp_enabler_and_disabler(dhcp_enable)
    
                
        


