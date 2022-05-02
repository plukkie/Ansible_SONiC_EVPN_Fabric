#!/usr/bin/env python3

import paramiko
import time
import getpass
import os
#from host_seedfile import network_devices
#from host_config_file import host_conf

inventoryfile = 'hosts'
hoststr = 'ansible_host='
UN = 'admin'
PW = 'admin123'
commandlist = [ "sonic-cli", "write erase", "y", "reboot" ]
 
#UN = input("Username : ")
#PW = getpass.getpass("Password : ")


def create_host_list (inventoryfile):
    
    """
    This function searches for ansible hosts in the ansible invnentory file
    This file defaults to 'hosts'
    The Ip addresses of the hosts are returned in a list
    If no hosts found, quit and do nothing.
    """

    hostlist = []

    with open(inventoryfile) as f:
        datafile = f.readlines()

    for line in datafile:
        index = line.find(hoststr)
        if index != -1: #Found ansible host line
            sliced = line[index+len(hoststr):].split() #Strip all leading chars till host ip-address and breakup on spaces
            hostlist.append(sliced[0]) #Add IP address to list

    hosts = len(hostlist)    
    print()

    if hosts == 0:
        print('No hosts found in inventory file. No action taken.\n')
        quit()
    else:
        print('Found ' + str(hosts) + ' hosts in ansible inventory. Will execute on following list:')
        print(hostlist,'\n')
        time.sleep(1)

    return hostlist


def execute_commands (hosts, commands):

    """
    This function logs into the hosts with ssh and executes the list with cli commands
    """

    for ip in hosts:
        print('Accessing ' + ip + ':\n')
        
        try:
            twrssh = paramiko.SSHClient()
            twrssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            twrssh.connect(ip, port=22, username=UN, password=PW)
            remote = twrssh.invoke_shell()
        
            for cmd in commands:
                print('Send command: ' + cmd)
                remote.send(cmd + '\r')
                time.sleep(1)
                #buf = remote.recv(65000)
                #print (buf)
                #f = open('sshlogfile0001.txt', 'ab')
                #f.write(buf)
                #f.close()

            print('\n- OK -- Host should reboot with default config, but retains Mgt IP ' + ip)
            print('----------------------------------------------------------------------------------\n')

            twrssh.close()

        except:
            print('Error accessing host ' + ip + ' !')
            print('----------------------------------------------------------------------------------\n')


def yes_or_no(question):
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        try:
            if reply[0] == 'y':
                return True
            if reply[0] == 'n':
                return False
        except:
            pass


## ==================
## Start main program
## ==================

print()
result = yes_or_no ('Are you sure you want to delete startup-configs and reboot hosts from ansible iventory?')
if (result == False):
    print()
    quit()

iplist = create_host_list(inventoryfile) #Create list with ip addresses of all hosts
execute_commands (iplist, commandlist)   #Login to hosts and execute commands

print('All Done.\n')

