#!/usr/bin/env python

from multiprocessing import Process
import threading
import time
import pexpect
import sys
import re
import os


#USERNAME_ARUBA = 'manager'
#PASSWORD_ARUBA = 'Password123'
USERNAME_ARUBA = 'operator'  
PASSWORD_ARUBA = 'Password123' 
USERNAME_HPE = 'operator'  
PASSWORD_HPE = 'Password123' 
#USERNAME_SS = 'manager'
#PASSWORD_SS = 'Password123'
USERNAME_SS = 'operator'  
PASSWORD_SS = 'Password123' 
#LOG_FILE = 'mylog.txt'
#OUTPUT_FILE = 'output_aruba.txt'
IP_APPARATI_ARUBA = 'apparati_aruba.txt'
IP_APPARATI_HPE = 'apparati_hpe.txt'
IP_APPARATI_SS = 'apparati_ss.txt'
ip_list = []
TIMEOUT = 480 #secondi per la attesa della risposta al comando (rx file di log)


#COMMAND_LIST_ARUBA = ['display current-configuration'] 
#COMMAND_LIST_ARUBA = ['show lldp info remote-device','show lldp info remote-device detail'] 
#COMMAND_LIST_ARUBA = ['#show system information','show system temperature','show system fan','show system power-consumption','show system power-supply']
#COMMAND_LIST_ARUBA = ['show spanning-tree'] 
#COMMAND_LIST_ARUBA = ['system-view','show system information','show system temperature','show system power-supply','exit'] 
COMMAND_LIST_ARUBA = ['show logging -r -d'] 
#COMMAND_LIST_ARUBA = ['clear logging'] #system-view only 
#COMMAND_LIST_ARUBA = ['show interface transceiver','show interface transceiver detail'] 
#COMMAND_LIST_ARUBA = ['#show interface brief | include Up','show interface trunk-utilization','#show interface port-utilization','#show interface status'] 
#COMMAND_LIST_ARUBA = ['#show mac-address','#show mac-address | include 001999-81d107','#show mac-address | include 001195-65dae8'] 
#COMMAND_LIST_ARUBA = ['#show mac-address | include 901b0e-bb4958','show mac-address | include 001999-81d107'] 
#COMMAND_LIST_ARUBA = ['show mac-address | e Trk1','#show mac-address | include 00d0b8-0ce9f3'] 
#COMMAND_LIST_ARUBA = ['show mac-address | e Trk1'] 

#COMMAND_LIST_HPE = ['#screen-length disable','display current-configuration'] 
#COMMAND_LIST_HPE = ['#screen-length disable','show arp'] 
#COMMAND_LIST_HPE = ['#show mac-address','show mac-address | e BAGG'] 
#COMMAND_LIST_HPE = ['#show interface bridge-aggregation brief','#display link-aggregation summary','#display link-aggregation member-port'] 
#COMMAND_LIST_HPE = ['show lldp neighbor-information'] 
#COMMAND_LIST_HPE = ['screen-length disable','#system-view','#display current-configuration','show system stable state','show power'] # Manager
COMMAND_LIST_HPE = ['show logbuffer reverse'] # screen-length disable and TIMEOUT in request
#COMMAND_LIST_HPE = ['screen-length disable','display current-configuration']
#COMMAND_LIST_HPE = ['screen-length disable','show system stable state','show power'] 
#COMMAND_LIST_HPE = ['show transceiver interface','show transceiver diagnosis interface','show transceiver alarm interface'] 
#COMMAND_LIST_HPE = ['show interface brief | include UP','show counters rate inbound interface','show counters rate outbound interface'] 
#COMMAND_LIST_HPE = ['show arp | include 192.168.1.100','show mac-address | include 0011-9565-dae8'] 
#COMMAND_LIST_HPE = ['show mac-address | e BAGG'] 

#COMMAND_LIST_SS = ['display current-configuration'] 
#COMMAND_LIST_SS = ['show lldp info remote-device','show lldp info remote-device detail'] 
COMMAND_LIST_SS = ['#show system information','show system temperature','show system fan','show system power-consumption','show system power-supply']
#COMMAND_LIST_SS = ['show spanning-tree'] 
#COMMAND_LIST_SS = ['system-view','show system information','show system temperature','show system power-supply','exit'] 
#COMMAND_LIST_SS = ['clear logging'] #system-view only 
#COMMAND_LIST_SS = ['show interface transceiver','show interface transceiver detail'] 
#COMMAND_LIST_SS = ['#show interface brief | include Up','show interface port-utilization','#show interface status','show interface trunk-utilization'] 
#COMMAND_LIST_SS = ['#show mac-address','#show mac-address | include 001999-81d107','#show mac-address | include 001195-65dae8'] 
#COMMAND_LIST_SS = ['#show mac-address | include 901b0e-bb4958','show mac-address | include 001999-81d107'] 
#COMMAND_LIST_SS = ['show mac-address | include d02788-c510d2','#show mac-address | include 00d0b8-0ce9f3'] 
#COMMAND_LIST_SS = ['show mac-address | e Trk1'] 
command = []


ansi_escape_8bit = re.compile(br'(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])')

os.chdir(os.path.abspath(os.path.dirname(__file__)))

#-------ARUBA_SWITCH---------
def connect_aruba(ip):
    prompt_exact = (r'(\<|\[)?(LT|lt|CE|HP)[a-zA-Z]{1}[0-9]?(-|_)[0-9]+(\(config\))?(#|\>|\])') #Complete Prompt (Manager user)
    #prompt_exact = (r'(\<|\[)?(LT|lt|CE)[a-zA-Z]{1}[0-9]?(-|_)[0-9]+(#|\>|\])') #not (config) Operator Prompt
    print('Apparato ARUBA %s' %ip)
    output_file = open(ip+".txt", 'wb')
    output_file.write(b'\r\n'+ip.encode('ascii')+b'\r\n\n')
    child=pexpect.spawn(str('telnet %s' % (ip)))
    #child.logfile = open(LOG_FILE,'ab')
    child.echo=False
#-----------------Login--------------------------------
    child.expect(['sername:','ogin:'])
    child.sendline(USERNAME_ARUBA)
    child.expect('assword:')
    child.sendline(PASSWORD_ARUBA)
    child.expect(prompt_exact)
    result = ansi_escape_8bit.sub(b'',child.after)
    #print(result)
    output_file.write(result)
    child.sendline('no page')
    child.expect(prompt_exact)
#--------------------command---------------------------
    for command in COMMAND_LIST_ARUBA:
        if (not command.startswith('#')):
            child.sendline(command)
            child.expect(prompt_exact,timeout=TIMEOUT)
            result=ansi_escape_8bit.sub(b'',child.before)         
            #print(result)
            output_file.write(result)
#-------------------Logout-----------------------------         
    child.sendline('logout')
    child.expect(r'\(y/n\)\?')
    child.sendline('yes')
    child.close()
    output_file.close()

#-------HPE_SWITCH---------
def connect_hpe(ip):
    prompt_exact = (r'(\<|\[)?(LT|lt|CE|HP)[a-zA-Z]{1}[0-9]?(-|_)[0-9]+(\(config\))?(#|\>|\])') #Complete Prompt (Manager user)
    #prompt_exact = (r'(\<|\[)?(LT|lt|CE)[a-zA-Z]{1}[0-9]?(-|_)[0-9]+(#|\>|\])')
    print('Apparato HPE %s' %ip)
    output_file = open(ip+".txt", 'wb')
    output_file.write(b'\r\n'+ip.encode('ascii')+b'\r\n\n')
    child=pexpect.spawn(str('telnet %s' % (ip)))
    #child.logfile = open(LOG_FILE,'ab')
    child.echo=False
#-----------------Login--------------------------------
    child.expect(['sername:','ogin:'])
    child.sendline(USERNAME_HPE)
    child.expect('assword:')
    child.sendline(PASSWORD_HPE)
    child.expect(prompt_exact)
    #result = ansi_escape_8bit.sub(b'',child.after)
    #print(result)
    #output_file.write(result)
    output_file.write(child.after)
    #if (USERNAME_HPE == 'manager'): # screen-length disable enabled in operator account
    #    child.sendline('screen-length disable') #only manager
    #    child.expect(prompt_exact)
    child.sendline('screen-length disable')
    child.expect(prompt_exact)
#--------------------command---------------------------
    for command in COMMAND_LIST_HPE:
        if (not command.startswith('#')):
            child.sendline(command)
            child.expect(prompt_exact,timeout=TIMEOUT)
            #result=ansi_escape_8bit.sub(b'',child.before)         
            #print(result)
            #output_file.write(result)
            output_file.write(child.before)
#-------------------Logout-----------------------------         
    child.sendline('exit')
    child.close()
    output_file.close()

#-------SWITCH_SS---------
def connect_ss(ip):
    prompt_exact = (r'(\<|\[)?(HPE1|HPE2|DOCUMENTALE|NUOVO_FUJITSU|EX_PENALE|EX_CIVILE|VERITAS|SICP|SIDIP)_[0-9]+(\(config\))?(#|\>|\])') # system-view (config)
    #prompt_exact = (r'(\<|\[)?(LT|lt|CE|HP)[a-zA-Z]{1}[0-9]?(-|_)[0-9]+(\(config\))?(#|\>|\])') #Complete Prompt (Manager user)
    #prompt_exact = (r'(\<|\[)?(LT|lt|CE)[a-zA-Z]{1}[0-9]?(-|_)[0-9]+(#|\>|\])') #not (config) Operator Prompt
    print('Apparato SS %s' %ip)
    output_file = open(ip+".txt", 'wb')
    output_file.write(b'\r\n'+ip.encode('ascii')+b'\r\n\n')
    child=pexpect.spawn(str('telnet %s' % (ip)))
    #child.logfile = open(LOG_FILE,'ab')
    child.echo=False
#-----------------Login--------------------------------
    child.expect(['sername:','ogin:'])
    child.sendline(USERNAME_SS)
    child.expect('assword:')
    child.sendline(PASSWORD_SS)
    child.expect(prompt_exact)
    result = ansi_escape_8bit.sub(b'',child.after)
    #print(result)
    output_file.write(result)
    child.sendline('no page')
    child.expect(prompt_exact)
#--------------------command---------------------------
    for command in COMMAND_LIST_SS:
        if (not command.startswith('#')):
            child.sendline(command)
            child.expect(prompt_exact,timeout=TIMEOUT)
            result=ansi_escape_8bit.sub(b'',child.before)         
            #print(result)
            output_file.write(result)
#-------------------Logout-----------------------------         
    child.sendline('logout')
    child.expect(r'\(y/n\)\?')
    child.sendline('yes')
    child.close()
    output_file.close()


def main():

    #processes=[]
    threads = [] # Sospesi i thread in quanto sequenzializzano su grandi dati
    # apparati=open(IP_APPARATI_ARUBA,'r')
    # ip_list=apparati.read().splitlines()
    # apparati.close()

    with open(IP_APPARATI_ARUBA,'r') as apparati:
        ip_list=apparati.read().splitlines()

    while('' in ip_list): 
        ip_list.remove('') 

    for ip in ip_list:
        if (not ip.startswith('#')):
            #--------------In sequenza-----------------
            #connect_aruba(ip)
            #--------------con Processi----------------
            #p=Process(target=connect_aruba,args=(ip,))
            #p.start()
            #processes.append(p)
            #-------------con--Thread------------------
            t=threading.Thread(target=connect_aruba,args=(ip,)) # Sospesi i thread in quanto sequenzializzano su grandi dati
            t.start() # Sospesi i thread in quanto sequenzializzano su grandi dati
            threads.append(t) # Sospesi i thread in quanto sequenzializzano su grandi dati

    # apparati=open(IP_APPARATI_HPE,'r')
    # ip_list=apparati.read().splitlines()
    # apparati.close()

    with open(IP_APPARATI_HPE,'r') as apparati:
        ip_list=apparati.read().splitlines()

    while('' in ip_list): 
        ip_list.remove('') 

    for ip in ip_list:
        if (not ip.startswith('#')):
            #--------------In sequenza-----------------
            #connect_hpe(ip)
            #--------------con Processi----------------
            #p=Process(target=connect_hpe,args=(ip,))
            #p.start()
            #processes.append(p)
            #-------------con--Thread------------------
            t=threading.Thread(target=connect_hpe,args=(ip,)) # Sospesi i thread in quanto sequenzializzano su grandi dati
            t.start() # Sospesi i thread in quanto sequenzializzano su grandi dati
            threads.append(t) # Sospesi i thread in quanto sequenzializzano su grandi dati

    # apparati=open(IP_APPARATI_SS,'r')
    # ip_list=apparati.read().splitlines()
    # apparati.close()

    with open(IP_APPARATI_SS,'r') as apparati:
        ip_list=apparati.read().splitlines()

    while('' in ip_list): 
        ip_list.remove('') 

    for ip in ip_list:
        if (not ip.startswith('#')):
            #--------------In sequenza-----------------
            #connect_ss(ip)
            #--------------con Processi----------------
            #p=Process(target=connect_ss,args=(ip,))
            #p.start()
            #processes.append(p)
            #-------------con--Thread------------------
            t=threading.Thread(target=connect_ss,args=(ip,)) # Sospesi i thread in quanto sequenzializzano su grandi dati
            t.start() # Sospesi i thread in quanto sequenzializzano su grandi dati
            threads.append(t) # Sospesi i thread in quanto sequenzializzano su grandi dati

    #for process in processes:
    #    process.join()

    #for thread in threads: # Sospesi i thread in quanto sequenzializzano su grandi dati
    #    threads.join() # Sospesi i thread in quanto sequenzializzano su grandi dati

#    for ip in ip_list:
#        if (not ip.startswith('#')):
#            p.join()

if __name__ == '__main__':

    print('Starting connections')
    start=time.perf_counter()
    main()
    finish=time.perf_counter()
    print(f'Finishing connections in {round(finish-start,2)} second(s)')
