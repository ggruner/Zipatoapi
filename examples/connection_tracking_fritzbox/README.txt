This is a possibility to track hardware devices (online / offline) at home on my.zipato.com.
This version only works with a FRITZ!Box Router.
Please consider below the "Known Issues" Topic!!!

### Tested Hardware:
- Raspberry Pi 2 (Raspbian JESSIE)
- FRITZ!Box 7490

### Prerequisite:

You have to install some python packages

# Debian based systems
apt-get	install python-yaml python-requests python-pycurl python-json

# RHEL / CENTOS based systems
yum install python-yaml python-requests python-pycurl python-json

### Files:
All the below files have to be in the same directory.

- connection_tracking.py
Put your login credentials on line 29,30

- connection_tracking.yaml
Put the mac address(UPPERCASE) and a name in yaml syntax
to track this device. The Name is important, because I use this to
create a virtual Endpoint Sensor with this Name.
EXAMPLE:
- mac: 80:AF:23:D2:3F:12
  name: Ben
- mac: 8F:AA:33:D2:3D:1D
  name: Tina

- fritzconnection.py, fritzhosts.py, known_hosts.yaml
This both python scripts are coming from the fritzconnection package.
I've rewritten the fritzhosts.py script, that it will create a file "known_hosts.yaml"
and put all the output of the known devices from your AVM Fritzbox in this file.
You can run the script as follow:
python fritzhosts.py -p "YOUR_FRITZBOX_PASSWORD"

- Zipatoapi.py
A python library based on the Zipato API.
Project URL: https://github.com/ggruner/Zipatoapi

### ToDo's:
You can create a Cronjob that both Scripts are running every Minute to update the state
0-59 * * * * python /path/script/fritzhosts.py -p "YOUR_FRITZBOX_PASSWORD" && python /path/sript/connection_tracking.py

Or run it manually:
python /path/script/fritzhosts.py -p "YOUR_FRITZBOX_PASSWORD" && /path/script/connection_tracking.py

### Known Issues
- After the virtual Endpoints Sensors were craeted by the script, you have to sync your zipabox!!! After the sync is finished, then the status will be updated on the sensors
- Please consider that the mac Address should be UPPERCASE in the connection_tracking.yaml file.
