# Aribox

- install python3 on the machine

## Install python
```python
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip
```

## Install project

install requirements

```shell
pip3 install -r requirements.txt
```

to install the project
```shell 
pip3 install -e .
```

## Install music software
```shell
sudo apt-get install vlc
```

## Install Music Player Demon
[MPD Docs](https://mpd.readthedocs.io/en/latest/user.html)

## Enable pi user to shutdown system with pwd
sudo visudo /etc/sudoers

Append to the file:
```shell
# Allow pi to shutdown without being pwd 
pi raspberrypi =NOPASSWD: /usr/bin/systectl poweroff,/usr/bin/systemctl halt,/usr/bin/systemctl reboot`
```
> To save and close in visudo `ctrl + o` + `ctrl + x`

Enabled commands: 
- `sudo systemctl poweroff`
- `sudo systemctl reboot`
- `sudo systemctl halt`
