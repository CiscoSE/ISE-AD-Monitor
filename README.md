# ISE AD Script

## Motivation

Due to instability in the AD connector between Cisco ISE and Microsoft Active Directory, triggered by highly tweaked and hardened AD configuration and change activities causing the AD nodes to flap, the connectivity between ISE and Active Directory can go down and stay down even after the specific failed AD node comes back up. The other AD servers are not used even though they stayed up.
When this occurs, the only workaround to restore the ISE connectivity to AD servers is to restart the ISE application from the ISE CLI. 

This script was developed to automatically apply the workaround when the issue happens, a temporary workaround to be used until the issue is permanently fixed in software.

## Features

- The script monitors the success of authentication to a monitoring probe which uses ISE for AAA (Authentication) services.
- In case 3 authentication attempts fail due to unresponsiveness, the script performs the workaround of restarting the ISE application. 
- An email notification is also sent to a specified recipient list.


**Cisco Products & Services:**

- Cisco Identity Services Engine (ISE)

**Third-Party Products & Services:**

- Microsoft Active Directory Server

## Usage

1. Update the variables with the required information in the environment variables file (env_user.py).

2. Verify IP reachability between ISE server and the machine where the script is to run, and between ISE server and the AAA client where authentication is to be monitored.

3. Verify that the username & password used in the authentication checks is valid and can successfully authenticate.

4. Run the script by:
$ python ise_ad_script.py

Notes:
- Script will exit when the probe is unreachable
- A failure is considered only when the probe is reachable but authentication via ISE is failing
- When the probe re-authenticates successfully after a failure (failure_count < 3), the failure count is reset and subsequently 3 consecutive failures would be needed to trigger the ISE reset
- Script will exit when ISE is unreachable and when authentication is failing to ISE

For sample runs of the script, please check the screenshots folder.


## Installation & Prerequisites:

It is recommended to install the Python dependencies in a new virtual environment based on Python 2.7 or above. For information on setting up a virtual environment please check: http://docs.python-guide.org/en/latest/dev/virtualenvs/

Python package prerequisites in "requirements.txt" file which is located in the root directory of this distribution. To install them: 
$ pip install -r requirements.txt


## Authors & Maintainers

- Charles Youssef <cyoussef@cisco.com>

## Credits

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](./LICENSE).
