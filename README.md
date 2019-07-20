# network_device_backup

Basic program in Python to take backup of running configuration of network device.

1. Run "secure_credential.py" - This programme will ask your username and password to login into network devices. The programme will invoke "DataEncrypt" module to encrypt your password and store it in "Cred" named folder. Run this programme for first time before running the device backup file.

2. Run "device_backup.py" - This programme will create a "Backup" folder and create file in the name of device hostname (txt file) and push data in it. The config backup will be kept in a seperate folder named with date and time of running the script. It will invoke "DataDecrypt" module to use the password of the username in the devices to access. It will fetch input from two CSV files 

a) data.csv and b) command.csv.

a) data.csv - It contains device_type of Netmiko library, device hostname and username.

b) command.csv - It contain all the commands of related network device to fetch from the device, based on device_type.

The code is modular enough to take backup from most networking devices.

Finally it creates a report in txt file based on the result and put it in the same backup folder.

Enjoy!!!!
