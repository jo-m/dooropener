# Setup on RasPi

This assumed you have a proxy/gateway server set up (e.g. on digitalocean) reachable on the domain gateway.eth.ec, running Ubuntu 16.04.

## WiFi Setup

Get `radius-service.ethz.ch.cer` from your OSX keychain.

sudo mkdir /etc/certs
sudo cp radius-service.ethz.ch.cer /etc/certs/

Add `ipv6` to `/etc/modules`.

`/etc/wpa_supplicant/wpa_supplicant.conf`:

    ctrl_interface=/var/run/wpa_supplicant
    network={
      ssid="eth"
      scan_ssid=1
      key_mgmt=WPA-EAP
      pairwise=CCMP TKIP
      group=CCMP TKIP
      eap=PEAP
      identity="<yourid>"
      password="<yourpass>"
      ca_cert="/etc/certs/radius-service.ethz.ch.cer"
      phase1="peapver=0"
      phase2="MSCHAPV2"
    }

`/etc/network/interfaces`:

    auto wlan0
    allow-hotplug wlan0
    iface wlan0 inet dhcp
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

Then, set up SSH (set a strong password for the pi user) and your ssh key on it.

## GPio Setup
Following <http://openmicros.org/index.php/articles/94-ciseco-product-documentation/raspberry-pi/217-getting-started-with-raspberry-pi-gpio-and-python>.

    sudo apt-get -y update
    sudo apt-get -y install python-dev
    sudo pip install rpio

    sudo rpio --setoutput 18:1; sudo rpio --setoutput 18:0

## Python and app (on RasPi)

    sudo apt-get update
    sudo apt-get install python3-pip libffi-dev autossh
    sudo adduser dooropener
    sudo passwd -l dooropener
    sudo su dooropener
    ssh-keygen
    cd
    pip3 install --user virtualenv
    git clone https://github.com/jo-m/dooropener.git dooropener
    cd dooropener
    ~/.local/bin/virtualenv -p python3 .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    crontab -e

    # add this line:
    @reboot cd /home/dooropener/dooropener/; ./dooropener.py

Add this to `/etc/network/if-up.d` on your pi:

    #!/usr/bin/env bash

    # ssh options:
    # -M: Monitoring port
    # -f: fork to background
    # -N: don't allocate a terminal
    # -q: quiet
    # -i: path to key file
    # -R: reverse tunnel remoteport:host:localport
    # -S: control socket location, or none

    export AUTOSSH_PORT=27554

    su -c "autossh -f -N -q -i /home/dooropener/.ssh/id_rsa -R 5050:localhost:5050 -S none -oControlMaster=no -oUserKnownHostsFile=/dev/null -oStrictHostKeyChecking=no dooropener@gateway.eth.ec" dooropener

Then add the following line to the sudoers file (command `visudo`) on your pi:

    dooropener ALL=(ALL) NOPASSWD: /usr/local/bin/rpio

## Proxy server

    sudo adduser dooropener
    sudo passwd -l dooropener
    sudo su dooropener
    cd
    mkdir .ssh
    nano .ssh/authorized_keys

Add the key like here:

    command="/bin/false",no-pty ssh-rsa AAAAB3Nz...GCBNc6P you@raspberrypi

Also, the proxy server `/etc/ssh/sshd_config` needs the `GatewayPorts yes` option set.
After a reboot, the app should be reachable at <http://gateway.eth.ec:5050/>.

## Slack setup
Add a new slack command here: <https://ethec.slack.com/services/new/slash-commands>.

* URL: <http://gateway.eth.ec:5050/dooropen/>
* Method: `POST`

Then, hash the token using `gen_hash.py` and add it to `config.txt` (copy the
sample config file `config.txt.sample`).

For logging, also add an incoming webhook here <https://ethec.slack.com/services/new/incoming-webhook>
and set its url into `config.txt` `slack_webhook`.

Thats it! You can now use `/opendoor` from Slack.
