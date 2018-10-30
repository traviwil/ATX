# 
# script written for Python 2.7
# for mac run these commands prior to running the script
# "sudo easy_install pip"
# "sudo pip install requests"
#
# Note that I have not done anything in this script to 
# gracefully handle an invalid username or password
# or insufficient privileges on the DNA Center server.
#

import getpass
import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth

print " "
print "    -----"
print "    This script returns the management info that DNA Center"
print "    is using to access a particular network device."
print "    -----"
print " "

dnacIP = raw_input("DNA Center IP Address: ")
userID = raw_input("DNA Center Admin User ID: ")
userPW = getpass.getpass(prompt='DNA Center Admin Password: ') 
print " "
devIP = raw_input("IP Address of the Device that you need the info for: ")

# The following disables the warning received due to the 
# DNAC self-signed certificate. Consider disabling for 
# security purposes. 

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# print " "
# print "    -----"
# print "    If you have a self-signed certificate expect to see some errors."
# print "    However, this script will continue on certificate errors."
# print "    -----"
# print " "

dnacAuthTokenURL = 'https://'+dnacIP+'/api/system/v1/auth/token'
dnacDevMgmtInfoURL = 'https://'+dnacIP+'/api/v1/network-device/management-info'
jsonHeaders = {'Content-Type': 'application/json'}

dnacAuthToken = json.loads(requests.post(dnacAuthTokenURL, verify=False, auth=HTTPBasicAuth(userID, userPW), headers=jsonHeaders).text)['Token']
authTokenHeaders = {'Content-Type': 'application/json', 'X-Auth-Token': dnacAuthToken}

devMgmtInfo = json.loads(requests.get(dnacDevMgmtInfoURL, verify=False, headers=authTokenHeaders).text)['response']

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
        print json.dumps(devMgmtInfo['networkDeviceManagementInfo'][loopCount]['credentials'], sort_keys=True, indent=4, separators=(',', ': '))
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
