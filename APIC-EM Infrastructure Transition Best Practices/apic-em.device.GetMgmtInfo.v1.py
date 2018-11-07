# 
# script written for Python 2.7
# for mac run these commands prior to running the script
# "sudo easy_install pip"
# "sudo pip install requests"
#
# Note that I have not done anything in this script to 
# gracefully handle an invalid username or password
# or insufficient privileges on the APIC-EM server.
#

import getpass
import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth

print " "
print "    -----"
print "    This script returns the management info that APIC-EM"
print "    is using to access a particular network device."
print "    -----"
print " "

apicemIP = raw_input("    APIC-EM IP Address: ")
userID = raw_input("    APIC-EM Admin User ID: ")
userPW = getpass.getpass(prompt='    APIC-EM Admin Password: ') 
print " "
devIP = raw_input("    IP Address of the Device that you need the info for: ")

# The following disables the warning received due to the 
# APIC-EM self-signed certificate. Consider disabling for 
# security purposes. 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# print " "
# print "    -----"
# print "    If you have a self-signed certificate expect to see some errors."
# print "    However, this script will continue on certificate errors."
# print "    -----"
# print " "

apicemAuthTicketURL = 'https://'+apicemIP+'/api/v1/ticket'
apicemDevMgmtInfoURL = 'https://'+apicemIP+'/api/v1/network-device/management-info'
jsonHeaders = {'Content-Type': 'application/json'}

r_login = {
    "username" : userID,
    "password" : userPW
}

apicemAuthTicket = json.loads(requests.post(apicemAuthTicketURL, json.dumps(r_login), verify=False, auth=HTTPBasicAuth(userID, userPW), headers=jsonHeaders).text)['response']['serviceTicket']
authTicketHeaders = {'Content-Type': 'application/json', 'X-Auth-Token': apicemAuthTicket}

devMgmtInfo = json.loads(requests.get(apicemDevMgmtInfoURL, verify=False, headers=authTicketHeaders).text)['response']

devCount = len(devMgmtInfo['networkDeviceManagementInfo'])
loopCount = 0
ipNotFound = True

while loopCount <= devCount:
    if devMgmtInfo['networkDeviceManagementInfo'][loopCount]['managementIpAddress'] == devIP:
        print " "
        print "    -----"
        print "    Here is the Management Info for Device with IP: "+devIP
        print "    -----"
        print " "
        print "    CLI Transport: "+devMgmtInfo['networkDeviceManagementInfo'][loopCount]['credentials']['cli_transport']
        print "    CLI Login Username: "+devMgmtInfo['networkDeviceManagementInfo'][loopCount]['credentials']['cli_login_username']
        print "    CLI Login Password: "+devMgmtInfo['networkDeviceManagementInfo'][loopCount]['credentials']['cli_login_password']
        print "    CLI Enable Password: "+devMgmtInfo['networkDeviceManagementInfo'][loopCount]['credentials']['cli_enable_password']
        print "    SNMP Version: "+devMgmtInfo['networkDeviceManagementInfo'][loopCount]['credentials']['snmp_version']
        print "    SNMP RO Community String: "+devMgmtInfo['networkDeviceManagementInfo'][loopCount]['credentials']['snmp_read_cs']
        try: 
            devMgmtInfo['networkDeviceManagementInfo'][loopCount]['credentials']['snmp_write_cs']
        except KeyError:
            print "    SNMP RO Community String: NOT AVAILABLE"
        else:
            print "    SNMP RW Community String: "+devMgmtInfo['networkDeviceManagementInfo'][loopCount]['credentials']['snmp_write_cs']
        loopCount += 1
        ipNotFound = False
    else:
        loopCount += 1    
    try:
        devMgmtInfo['networkDeviceManagementInfo'][loopCount]['managementIpAddress'] == devIP
    except IndexError:
        if ipNotFound == True:
            break
        else:
            break
    else:
        continue

if ipNotFound == True:
    print " "
    print "    -----"
    print "    The Device Management IP Address that you entered was not found"
    print "    -----"
    print " "
else:
    print " "
    print "    -----"
    print "    We are done. You're welcome."
    print "    -----"
    print " "
