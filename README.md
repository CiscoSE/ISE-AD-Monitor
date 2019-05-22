# ISE AD Script

## Motivation

Due to a software defect in Cisco ISE, the connectivity between ISE and Active Directory can randomly go down, and the only workaround to restore this connectivity is to restart the ISE application from the ISE CLI. Based on a customer request, this script was developed to automatically apply the workaround when the issue happens, a temporary workaround to be used until the issue is permanently fixed in software.

## Features

- The script monitors the success of authentication to a monitoring probe which uses ISEs for AAA (Authentication) services.
- In case 3 authentication attempts fail due to unresponsiveness, the ISE application is stopped and then restarted. 
- An email notification is also sent to the specified recipient list.


**Cisco Products & Services:**

- Cisco ISE 

**Third-Party Products & Services:**

- Microsoft Active Directory


## Usage

- Machine on which to run the script:
Python 2.7 is installed along with packages:
Paramiko, smtplib, getpass

- Verify IP reachability to ISE and monitoring probe management interfaces

- Update the ISE and monitoring probe static fields manually inside the script (at specified section via comments):
ISE Address, username, password
Probe Address, username, password
Sender and recipient emails and SMTP server

- It is recommended to log the terminal session in which the script is running. All events are tagged with timestamps.

- Script will exit when the probe is unreachable
- A failure is considered only when the probe is reachable but authentication via ISE is failing
- When the probe re-authenticates successfully after a failure (failure_count < 3), the failure count is reset and subsequently 3 consecutive failures would be needed to trigger the ISE reset
- Script will exit when ISE is unreachable and when authentication is failing to ISE

Sample run:

$ python ISE_AD_Script.py
Please enter the sender email password:
2018-11-19 11:48:22.376207: Starting the ISE monitoring script using probe to 10.0.0.161.
2018-11-19 11:48:31.042594: Authentication failed 1 time(s).
2018-11-19 11:49:42.418197: Authentication failed 2 time(s).
2018-11-19 11:50:50.299453: Authentication failed 3 time(s).
2018-11-19 11:51:50.300386: Authentication to probe unavailable. We will proceed with the ISE restart to recover.
2018-11-19 11:51:51.000314: Trying to connect to ISE...
2018-11-19 11:51:54.413905: Unable to login to ISE. Please verify ISE is reachable, verify proper username/password is set and rerun the script.
$


## Installation


## Authors & Maintainers

- Charles Youssef <cyoussef@cisco.com>

## Credits

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](./LICENSE).
