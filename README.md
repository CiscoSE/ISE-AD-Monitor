# ISE AD Script

*ISE AD Script*

---

**ToDo's:**

- [ ] Consider writing your README first.  Doing so helps you clarify your intent, focuses your project, and it is much more fun to write documentation at the beginning of a project than at the end of one, see:
    - [Readme Driven Development](http://tom.preston-werner.com/2010/08/23/readme-driven-development.html)
    - [GitHub Guides: Mastering Markdown](https://guides.github.com/features/mastering-markdown/)
- [ ] Ensure you put the [license and copyright header](./HEADER) at the top of all your source code files.
- [ ] Be mindful of the third-party materials you use and ensure you follow Cisco's policies for creating and sharing Cisco Sample Code.

---

## Motivation

Due to a software defect in Cisco ISE, the connectivity between ISE and Active Directory can randomly go down, and the only workaround to restore this connectivity is to restart the ISE application from the ISE CLI. Based on a customer request, this script was developed to automatically apply the workaround when the issue happens, a temporary workaround to be used until the issue is permanently fixed in software.


## Show Me!

What visual, if shown, clearly articulates the impact of what you have created?  In as concise a visualization as possible (code sample, CLI output, animated GIF, or screenshot) show what your project makes possible.

## Features

Include a succinct summary of the features/capabilities of your project.

- The script monitors the success of authentication to a monitoring probe which uses ISEs for AAA (Authentication) services.
- In case 3 authentication attempts fail due to unresponsiveness, the ISE application is stopped and then restarted. 
- An email notification is also sent to the specified recipient list.


## Technologies & Frameworks Used

This is Cisco Sample Code!  What Cisco and third-party technologies are you working with?  Are you using a coding framework or software stack?  A simple list will set the context for your project.

**Cisco Products & Services:**

- Product
- Service

**Third-Party Products & Services:**

- Product
- Service

**Tools & Frameworks:**

- Framework 1
- Automation Tool 2

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

$ python ISE_AD_Script_v2.py
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

Provide a step-by-step series of examples and explanations for how to install your project and its dependencies.

## Authors & Maintainers

Smart people responsible for the creation and maintenance of this project:

- Charles Youssef <cyoussef@cisco.com>

## Credits

Give proper credit.  Inspired by another project or article?  Was your work made easier by a tutorial?  Include links to the people, projects, and resources that were influential in the creation of this project.

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).
