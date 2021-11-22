# Aribox

## Prerequisites

### Python

```python
sudo apt-get update
sudo apt-get install python3 python3-venv python3-pip
sudo apt-get install python3-gpiozero
sudo apt-get install python-alsaaudio
```

### VLC

```shell
sudo apt-get install vlc
```

### VLC

```shell
sudo apt-get install vlc
```

## Install project

```shell
pip3 install -r requirements.txt
```

to install the project
```shell 
pip3 install -e .
```

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
