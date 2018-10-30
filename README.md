# Deploy and update a TeamSpeak server

## About
This playbook installs or updates a TeamSpeak server
Simply provide the download link to the TeamSpeak server files and the playbook will automatically set everything up.
---

### TeamSpeak 3 Server
#### Dependencies
The target machine should be setup for ansible:
- MariaDB server (external or on the same machine)
- A user for the TeamSpeak server that has rights on a database of the MariaDB server
- Python needs to be installed
- A user should be able to execute sudo commands without being asked for password confirmation
..* You can make sure your target machine meets these requirements by running the following bash script: [Prepare host for ansible](https://github.com/siw36/bash-prepare-workstation)
- All TeamSpeak related dependencies will be installed during the play

#### How to use
1. Customize your ansible host file:
- add a group named `teamspeak3`
- add th desired hosts (ip/hostname) to the `teamspeak3` group inside your host file
2. Customize the configuration files in the repository
- MariaDB connection details in: `files/ts3db_mariadb.ini`
- TeamSpeak server configuration file in: `files/ts3server.ini`
- Version check configuration file in: `version_check/config.ini`

Exec the teamspeak3.yml playbook to install or update a TeamSpeak 3 server.

#### What is going on
- The TeamSpeak server files will be downloaded from the link you provide at the start of the play
- A new system user called `teamspeak` will be crated (without a login shell)
- The server files will be extracted and copied to the `teamspeak` users home directory
- Permissions will be set
- A systemd script will be copied to the host and a service for the TeamSpeak server will be set up
- The configuration files you customized will be copied to the target host
- Firewall rules will be set up
- Icons from the repository directory `files/icons` will be copied to the target host (useful if you are reinstalling a new server with an existing MariaDB database)
- The teamspeak server gets started
- A python script will be copied to the target host
- A cronjob will be scheduled for everyday at 4:36AM to run the python script
> This python script will parse the `https://teamspeak.com/en/downloads/#server` website and will extract the latest stable version of TeamSpeak3 Server. It will send an email to the specified address in the `config.ini` file if your server is not running the latest version of TeamSpeak3.
---



## Supported Linux systems
- CentOS 7.5

*Note: This script may work for other Linux derivatives. Only the above are tested.*
