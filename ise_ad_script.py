#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ise AD Script Console Script.

Copyright (c) 2019 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""



__author__ = "Charles Youssef"
__email__ = "cyoussef@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import paramiko
import time
import datetime
import socket
import sys
import smtplib
import getpass
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# update the variables in env_user file:
import env_user


ise_address = env_user.ise_address  
ise_username = env_user.ise_username 
ise_password = env_uesr.ise_password

probe_address = env_user.probe_address
probe_username = env_user.probe_username
probe_password = env_user.probe_password

sender_email = env_user.sender_email
# recipient_email is a list of comma-separated email addresses
recipient_email = env_user.recipient_email

smtp_server = "smtp.gmail.com"
smtp_server_port = 587

#############################################
#############################################


def restart_ise(ise_address, ise_username, ise_password, ise_port):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print(str(datetime.datetime.now()) + ": Trying to connect to ISE...")
        ssh.connect(ise_address, port=ise_port, username=ise_username, password=ise_password, look_for_keys=False, allow_agent=False)
    except socket.error:
        print(str(datetime.datetime.now()) + ": ISE is unreachable. "
                                                     "Please verify IP connectivity to ISE and rerun the script.")
        sys.exit()
    except paramiko.ssh_exception.AuthenticationException:
        print(str(datetime.datetime.now()) + ": Unable to login to ISE. Please verify ISE is reachable, "
                                             "verify proper username/password is set and rerun the script.")
        sys.exit()
    except paramiko.ssh_exception.NoValidConnectionsError:
        print(str(datetime.datetime.now()) + ": ISE is unreachable. Please "
                                             "verify IP connectivity to ISE and then rerun the script.")
        sys.exit()
    except paramiko.ssh_exception.SSHException:
        print(str(datetime.datetime.now()) + ": Unable to login to ISE. Please verify ISE is reachable, "
                                             "verify proper username/password is set and rerun the script.")
        sys.exit()
    print(str(datetime.datetime.now()) + ": Connected to ISE...")
    remote_conn = ssh.invoke_shell()
    remote_conn.send("\n")
    time.sleep(2)
    remote_conn.send("\n")
    time.sleep(2)
    print(str(datetime.datetime.now()) + ": Stopping ISE application...")
    remote_conn.send("application stop ise\n")
    time.sleep(300)
    print(str(datetime.datetime.now()) + ": ISE application has been stopped...")
    # output = remote_conn.recv(65535)
    remote_conn.send("application start ise\n")
    print(str(datetime.datetime.now()) + ": ISE application is being restarted; Please wait...")
    time.sleep(300)
    print(str(datetime.datetime.now()) + ": ISE application is being restarted; Please wait...")
    time.sleep(300)
    # output = remote_conn.recv(65535)
    print(str(datetime.datetime.now()) + ": ISE application has been restarted...")
    ssh.close()


def send_email(from_email, from_email_password, to_email, smtp_email_server_address, smtp_email_server_port):
    email_server = smtplib.SMTP(smtp_email_server_address, smtp_email_server_port)
    email_server.ehlo()
    email_server.starttls()
    email_server.ehlo()
    email_server.login(from_email, from_email_password)
    from_address = from_email
    to_address = to_email
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = ', '.join(to_address)
    msg['Subject'] = "Attention: ise application was restarted!"
    body = "ise application was stopped/started at " + str(datetime.datetime.now())
    msg.attach(MIMEText(body, 'plain'))
    email_text = msg.as_string()
    email_server.sendmail(from_address, to_address, email_text)
    print(str(datetime.datetime.now()) + ": A notification email was sent to " + ", ".join(str(i) for i in to_email))


def main():
	# Alternatively the variables can be input as below instead of importing the env_user variables.
    """
    ise_address = raw_input("Please enter your ise IP address: ")
    ise_username = raw_input("Please enter your username: ")
    ise_password = getpass.getpass(prompt="Please enter your password: ")
    probe_address = raw_input("Please enter your monitor probe IP address: ")
    probe_username = raw_input("Please enter your probe username: ")
    probe_password = getpass.getpass(prompt="Please enter your probe password: ")
    sender_email = raw_input("Please enter the sender email address: ")
    recipient_email = raw_input("Please enter the recipient email: ")
    """
    Email_password = getpass.getpass(prompt="Please enter the sender email password: ")
    while True:
        print(str(datetime.datetime.now()) + ": Starting the ise monitoring script using probe "
                                             "to " + probe_address + ".")
        failure_count = 0
        while failure_count < 3:
            try:
                probe = paramiko.SSHClient()
                probe.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                probe.connect(probe_address, port=22, username=probe_username, password=probe_password)
                time.sleep(30)
                probe.close()
                print(str(datetime.datetime.now()) + ": Monitoring probe is reachable. No actions needed.")
                failure_count = 0
            except socket.error:
                print(str(datetime.datetime.now()) + ": Monitor probe is unreachable. "
                                                     "Please verify IP connectivity to the probe and rerun the script.")
                sys.exit()
            except paramiko.ssh_exception.AuthenticationException:
                failure_count += 1
                print(str(datetime.datetime.now()) + ": Authentication failed " + str(failure_count) + " time(s).")
                time.sleep(60)
            except paramiko.ssh_exception.NoValidConnectionsError:
                print(str(datetime.datetime.now()) + ": Monitor probe is unreachable. Please "
                                                     "verify IP connectivity to the probe and then rerun the script.")
                sys.exit()
            except paramiko.ssh_exception.SSHException:
                print(str(datetime.datetime.now()) + ": Invalid credentials for the probe. Please "
                                                     "set proper username/password and rerun the script.")
                sys.exit()
        print(str(datetime.datetime.now()) + ": Authentication to probe "
                                             "unavailable. We will proceed with the ise restart to recover.")
        restart_ise(ise_address, ise_username, ise_password, 22)
        send_email(sender_email, Email_password, recipient_email, smtp_server, smtp_server_port)
        time.sleep(600)


if __name__ == '__main__':
    main()