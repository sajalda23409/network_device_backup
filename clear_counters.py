# Backup the running configuration of network devices

from netmiko import ConnectHandler

from netmiko.ssh_exception import SSHException

from netmiko.ssh_exception import NetMikoTimeoutException

from netmiko.ssh_exception import AuthenticationException

import os

import csv

import sys

from datetime import datetime

# User defined Class

from DataDecrypt import DecryptProcess

try:

    print("\nProgrammer: Debanjan Banerjee")

    print("\nClearing counters program")
    
    my_tmp_lst = []

    my_username_password_lst = []

    # Creating a variable with current date and time

    mytime = datetime.now().strftime("Date-" + "%d" + "-" + "%b" + "-" + "%Y" + " " + "Time-" + "%H" + "." + "%M" + "." + "%S")

    # Checking Credential folder and associated files in it exist or not

    myactualpath = os.getcwd()

    my_cred_path = myactualpath + "\\Cred"

    if os.path.exists(my_cred_path) == False:

        print("There is no credential to login to network device. Run 'secure_credential' app first. Then fire this app.\n")

        sys.exit()

    elif len(os.listdir(my_cred_path)) == 0:

        print(
            "There is no credential to login to network device. Run 'secure_credential' app first. Then fire this app.\n")

        sys.exit()

    # Going back to original path

    os.chdir(myactualpath)

    # Access the device details from the 'data.csv' file in a list

    with open('data.csv', 'r') as my_data:

        my_input = list(csv.reader(my_data))

    my_data.close()

    # Moving to Cred folder

    os.chdir(my_cred_path)

    # Listing out all username folders in my_cred_folder list

    my_cred_folder = os.listdir(my_cred_path)

    # Retrieving all usernames from my_input list

    for i in range(1, len(my_input)):

        my_tmp_lst.append(my_input[i][2])

    # Creating an unique list of usernames using set()

    my_username_lst = list(set(my_tmp_lst))

    # Flushing out my_tmp_lst list

    my_tmp_lst.clear()

    # Creating a final unique list of username and its corresponding decrypted password

    for i in range(len(my_username_lst)):

        for j in range(len(my_cred_folder)):

            if(my_username_lst[i]==my_cred_folder[j]):

                os.chdir(my_cred_path + "\\" + my_cred_folder[j])

                with open('key.key', 'rb') as key_file:

                    getkey = key_file.read()

                key_file.close()

                with open(my_cred_folder[j] + ".txt", 'rb') as my_pass_file:

                    get_enc_pass = my_pass_file.read()

                my_pass_file.close()

                # Start Decryption process

                start_decrypt = DecryptProcess(getkey, get_enc_pass)

                my_decrypt_pass = start_decrypt.decrypt()

                # Here is the final list of username and password that to be used in login to network device

                my_username_password_lst.append([my_username_lst[i], my_decrypt_pass])
    
    # fullpath = mybackuppath + "/" + mytime

    # Flushing out the temporary my_username_lst list

    my_username_lst.clear()

    os.chdir(myactualpath)


    # Starting login to network device and fetching configuration process

    for i in range(1, len(my_input)):

        # Adding the device_type value in j variable

        j = my_input[i][0]

        # Adding the username value in u variable

        u = my_input[i][2]

        # Fetching the corresponding password from username & starting the backup process

        for ii in range(len(my_username_password_lst)):

            if (u==my_username_password_lst[ii][0]):

                # Adding the corresponding password value in p variable

                # Ensured that u & p combination is always unique

                p = my_username_password_lst[ii][1]

                # Getting into Backup folder to push configurations

                # os.chdir(fullpath)

                try:
        
                    # Accessing the network device and fetching configuration

                    # Noting down the start time to track

                    start_time = datetime.now()

                    print("\nAccessing...", my_input[i][1],)

                    # Login to the device

                    connect_to_device = ConnectHandler(device_type=j, host=my_input[i][1], username=u, password=p, secret=p)

                    # Getting into enable/privilege mode

                    connect_to_device.enable()

                    # Sending 'clear counters' to all devices one by one
 
                    connect_to_device.send_command_timing("clear counters")

                    # Closing the connection

                    connect_to_device.disconnect()

                    # Noting down the end time to track

                    end_time = datetime.now()
        
                except (AuthenticationException):
        
                    print("Unable to authenticate to the network device. Please check and try again:", my_input[i][1])

                except (NetMikoTimeoutException):
        
                    print("Network timeout. Check the network and configuration:", my_input[i][1])

                except (SSHException):
        
                    print("Unable to SSH the network device. Check the network and configuration:", my_input[i][1])

                except (EOFError):
        
                    print("End of attemptimg the network device:", my_input[i][1])

                except:
        
                    print("Something wrong to the network device or network itself. Check and try again.", my_input[i][1])

    os.chdir(myactualpath)

    print("\nDone. Please check in Backup folder. Thank you.")

except (ValueError, OverflowError, NameError, EnvironmentError, TypeError) as e:

    print("Something wrong happened. Please correct the error:",e)

except:

    print("Something wrong happened. Try again.")

finally:

    # Flushing out all lists

    my_username_password_lst.clear()

    my_tmp_lst.clear()

    my_username_lst.clear()

    my_cred_folder.clear()

    print("\n...END OF THE PROGRAM...")
