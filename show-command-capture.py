
#Install the prerequisite as follow
	#pip install json
	#pip install jsonrpclib
	#pip install pyeapi
	#pip install ssl
#==================================================================================
# coding: UTF-8
import os
import pyeapi
import ssl
import json
from jsonrpclib import Server
import getpass
import time
import datetime

ssl._create_default_https_context = ssl._create_unverified_context

#Edit the below list with the list of Switch's Management IP address from where the show command output is needed.
devices = ['1.1.1.1']

localtime = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M")

print "\nEnter your tacacs login credentials:-\n"
user_id = raw_input("Username:")
pass_wd = getpass.getpass("Password: ")

#Edit the below list with the list of show commands.
commands = [{"cmd": "enable", "input": pass_wd},"show version"] #add further commands at the end of the list

print "\nScript is capturing command output, please wait....\n"

for device in devices:
    switch = pyeapi.connect(transport='https',host=device,username=user_id,password=pass_wd,enablepwd=pass_wd)
    host_nm = switch.execute('show hostname')
    hostname = host_nm['result'][0]['hostname']
    target = "https://{}:{}@{}/command-api".format(user_id, pass_wd, device)
    output = Server(target)
    response = output.runCmds(1, commands, "text")
    i = 0
    while(i < len(response)-1):
        outfile = open(hostname+'_show-commands_output_'+localtime+'.txt', 'a')
        outfile.write("\nCOMMAND:- {} \n\n".format(commands[i+1]))
        outfile.write(response[i+1]["output"])
        outfile.write("\n**************************************************************************\n")
        outfile.close()
        i=i+1

print "\nScript is ended."
