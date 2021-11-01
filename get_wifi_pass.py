
#    Import subprocess so to use cmd commands
import subprocess
#    Import the re module to recognize username and password from keypairs 
import re

#Following command shows ssid of all wifi points user has connected till now
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

# appending names of wifi names to a list called profile_names
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

# resultant list initialized as empty array
wifi_list = []

if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = {}
        
        # retrieving information about each wifi points
        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            # setting ssid field in dictionary as name
            wifi_profile["ssid"] = name


            # retrieving password for that name
            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info_pass)

            if password == None:
                wifi_profile["password"] = None
            else:
                # assigning password to password field
                wifi_profile["password"] = password[1]
            #    We append the ssid:password to wifi_list 
            wifi_list.append(wifi_profile) 

for x in range(len(wifi_list)):
    print(wifi_list[x]) 