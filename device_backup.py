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

    print("\nNetwork Device Configuration Backup program")
    
    my_tmp_lst = []

    my_username_password_lst = []

    report_collector = {}
    
    # Creating a variable with current date and time

    mytime = datetime.now().strftime("Date-" + "%d" + "-" + "%b" + "-" + "%Y" + " " + "Time-" + "%H" + "." + "%M" + "." + "%S")

    # Creating a standard report file name

    my_report = "Report-" + mytime + ".txt"

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

    mybackuppath = myactualpath + "\\Backup"

    # Checking if "Backup" dir exists or not, if not, create the directory

    if os.path.exists(mybackuppath) == False:

        os.mkdir(mybackuppath)

    # Create the folder with current date and time where the backup will be pushed

    fullpath = mybackuppath + "/" + mytime

    os.mkdir(fullpath)

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

    # Flushing out the temporary my_username_lst list

    my_username_lst.clear()

    # Moving to actual path to access the command.csv file

    os.chdir(myactualpath)

    # Access the list of commands from 'command.csv' file in a list

    with open('command.csv', 'r') as cmd:

        my_command = list(csv.reader(cmd))

    cmd.close()
    
    # Report creation
    
    os.chdir(fullpath)

    my_report_file = open(my_report, 'w')
        
    my_report_file.write("Report of network device backup on "+mytime+"\n")
    
    my_report_file.write("*****************************************************************************\n")
    
    my_report_file.close()
    
    # Moving to actual path

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

                os.chdir(fullpath)

                try:
        
                    # Accessing the network device and fetching configuration

                    # Noting down the start time to track

                    start_time = datetime.now()

                    print("\nAccessing...", my_input[i][1])

                    # Login to the device

                    connect_to_device = ConnectHandler(device_type=j, host=my_input[i][1], username=u, password=p, timeout=5*60)

                    # Getting into enable/privilege mode

                    connect_to_device.enable()

                    # Creating config file with hostname/IP address of the network device

                    store_my_cmd_output = open(my_input[i][1] + ".txt", 'a')
        
                    # Pushing list of commands one by one to fetch output from network device

                    for k in range(1, len(my_command)):
        
                        if (my_command[k][0] == j):

                            # Writing the command in file

                            store_my_cmd_output.write("\n\nCommand-"+my_command[k][1]+"\n\n")
        
                            store_my_cmd_output.write(connect_to_device.send_command_timing(my_command[k][1]))
        
                    store_my_cmd_output.close()

                    # Closing the connection

                    connect_to_device.disconnect()

                    # Noting down the end time to track

                    end_time = datetime.now()
                    
                    # Update the report dictionary
                
                    report_collector.update({my_input[i][1]: "Success"})
                
                except (AuthenticationException) as auth_error:

                    report_collector.update({my_input[i][1]: str(auth_error)})

                    print("Unable to authenticate to the network device. Please check and try again:", my_input[i][1])

                except (NetMikoTimeoutException) as time_out_error:

                    report_collector.update({my_input[i][1]: str(time_out_error)})

                    print("Network timeout. Check the network and configuration:", my_input[i][1])

                except (SSHException) as ssh_exp_error:

                    report_collector.update({my_input[i][1]: str(ssh_exp_error)})

                    print("Unable to SSH the network device. Check the network and configuration:", my_input[i][1])

                except (EOFError) as eof_err:

                    report_collector.update({my_input[i][1]: str(eof_err)})
        
                    print("End of attemptimg the network device:", my_input[i][1])

                except:

                    report_collector.update({my_input[i][1]: "Something wrong to the network device or network itself. Check and try again"})
        
                    print("Something wrong to the network device or network itself. Check and try again.", my_input[i][1])

    os.chdir(myactualpath)
    
    print("Done. Please check in Backup folder. Thank you.")

except (ValueError, OverflowError, NameError, EnvironmentError, TypeError) as general_error:

    report_collector.update({"Not a network problem": str(general_error)})

    print("Something wrong happened. Please correct the error:", general_error)

except:

    report_collector.update({"Weired problem": "Something wrong happened. Try again"})

    print("Something wrong happened. Try again.")

finally:

    # Updating the report file with gathered data

    os.chdir(fullpath)

    update_report_file= open(my_report, 'a')
    
    update_report_file.write(str(report_collector))
    
    update_report_file.close()

    os.chdir(myactualpath)

    # Flushing out all lists & dictionaries

    my_username_password_lst.clear()

    my_tmp_lst.clear()

    my_username_lst.clear()

    my_cred_folder.clear()

    report_collector.clear()

    print("...END OF THE PROGRAM...")
