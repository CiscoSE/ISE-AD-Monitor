#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ISE AD Script Console Script

Due to instability in the AD connector between Cisco ISE and Microsoft Active Directory, triggered by highly tweaked and hardened AD configuration and change activities causing the AD nodes to flap, the connectivity between ISE and Active Directory can go down and stay down even after the specific failed AD node comes back up. The other AD servers are not used even though they stayed up. When this occurs, the only workaround to restore the ISE connectivity to AD servers is to restart the ISE application from the ISE CLI.

This script was developed to automatically apply the workaround when the issue happens, a temporary workaround to be used until the issue is permanently fixed in software.

"""

import paramiko
import time
import datetime
import socket
import sys
import smtplib
import getpass
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

try:
    import env_user
except (SyntaxError, ModuleNotFoundError):
    print("Invalid input in env_file. Please complete the required fields in the proper format.")
    sys.exit(1)

__author__ = "Charles Youssef"
__email__ = "cyoussef@cisco.com"
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2018 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

try:
    ise_address = env_user.ise_address
    ise_username = env_user.ise_username
    ise_password = env_uesr.ise_password

    probe_address = env_user.probe_address
    probe_username = env_user.probe_username
    probe_password = env_user.probe_password

    sender_email = env_user.sender_email
    # recipient_email is a list of comma-separated email addresses
    recipient_email = env_user.recipient_email
    smtp_server = env_user.smtp_server
    smtp_server_port = env_user.smtp_server_port
except (NameError, KeyError):
    print("Invalid input in env_user file. Please complete the required fields in the proper format.")
    sys.exit(1)


def restart_ise(ise_address, ise_username, ise_password, ise_port):
    """This function is for restarting ISE server with the specified arguments
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        print("%s: Trying to connect to ISE..." % str(datetime.datetime.now()))
        ssh.connect(ise_address, port=ise_port, username=ise_username, password=ise_password, look_for_keys=False, allow_agent=False)
    except socket.error:
        print("%s: ISE is unreachable. Please verify IP connectivity to ISE and rerun the script."
        % str(datetime.datetime.now()))
        sys.exit(1)
    except paramiko.ssh_exception.AuthenticationException:
        print("%s: Unable to login to ISE. Please verify ISE is reachable, verify proper " \
            "username/password is set and rerun the script." % str(datetime.datetime.now()))
        sys.exit(1)
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("%s: ISE is unreachable. Please verify IP connectivity to ISE and then rerun the script."
                % str(datetime.datetime.now()))
        sys.exit(1)
    except paramiko.ssh_exception.SSHException:
        print("%s: Unable to login to ISE. Please verify ISE is reachable, verify proper " \
            "username/password is set and rerun the script." % str(datetime.datetime.now()))
        sys.exit(1)
    print("%s: Connected to ISE..." % str(datetime.datetime.now()))
    # sleep timers are set based on lab testing response times:
    remote_conn = ssh.invoke_shell()
    remote_conn.send("\n")
    time.sleep(2)
    remote_conn.send("\n")
    time.sleep(2)
    print("%s: Stopping ISE application..." % str(datetime.datetime.now()))
    remote_conn.send("application stop ise\n")
    time.sleep(300)
    print("%s: ISE application has been stopped..." % str(datetime.datetime.now()))
    remote_conn.send("application start ise\n")
    print("%s: ISE application is being restarted; Please wait..." % str(datetime.datetime.now()))
    time.sleep(300)
    print("%s: ISE application is being restarted; Please wait..." % str(datetime.datetime.now()))
    time.sleep(300)
    print("%s: ISE application has been restarted..." % str(datetime.datetime.now()))
    ssh.close()

def send_email(from_email, from_email_password, to_email, smtp_email_server_address, smtp_email_server_port):
    """Function to send an email
    """
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
    print("%s: A notification email was sent to " + ", ".join(str(i) for i in to_email) %
        str(datetime.datetime.now()))


def main():

    Email_password = getpass.getpass(prompt="Please enter the sender email password: ")
    while True:
        print("%s: Starting the ise monitoring script using probe to %s." % (
            str(datetime.datetime.now()), probe_address))

        failure_count = 0
        while failure_count < 3:
            try:
                probe = paramiko.SSHClient()
                probe.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                probe.connect(probe_address, port=22, username=probe_username, password=probe_password)
                time.sleep(30)
                probe.close()
                print("%s: Monitoring probe is reachable. No actions needed." % str(datetime.datetime.now()))
                failure_count = 0
            except socket.error:
                print("%s: Monitor probe is unreachable. Please verify IP connectivity to the probe" \
                    " and rerun the script." str(datetime.datetime.now()))
                sys.exit(1)
            except paramiko.ssh_exception.AuthenticationException:
                failure_count += 1
                print("%s: Authentication failed %s time(s)." % (str(datetime.datetime.now())),
                    str(failure_count))
                time.sleep(60)
            except paramiko.ssh_exception.NoValidConnectionsError:
                print("%s: Monitor probe is unreachable. Please verify IP connectivity to the probe" \
                    " and then rerun the script." % str(datetime.datetime.now()))
                sys.exit(1)
            except paramiko.ssh_exception.SSHException:
                print("%s: Invalid credentials for the probe. Please set proper username/password " \
                    "and rerun the script." % str(datetime.datetime.now()))
                sys.exit(1)
        print("%s: Authentication to probe unavailable. We will proceed " \
            "with the ise restart to recover." % str(datetime.datetime.now()))
        restart_ise(ise_address, ise_username, ise_password, 22)
        send_email(sender_email, Email_password, recipient_email, smtp_server, smtp_server_port)
        time.sleep(600)

if __name__ == '__main__':
main()
