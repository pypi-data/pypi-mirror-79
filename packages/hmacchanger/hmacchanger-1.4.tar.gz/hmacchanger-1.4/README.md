![](https://photos.google.com/photo/AF1QipPXxg5MSyeL8pdxb1c9jML6-r2qEujcaeEBmrNa)

**MAC Address Changer**
=======================
The aim of this module is to build a MAC changer which is used to change the **MAC address** of the systems running **LINUX** operating systems with simple and easy commands. This is helpful to maintain privacy in this **Online World!**

------------------

**Requirements:**
> * net-tools
-------------------
**Installation:**
```terminal
sudo pip install hmacchanger
sudo apt install net-tools          //as mentioned in requirements
```

------------------
**Usage:**
For help just type 
```terminal
sudo hmacchanger --help
``` 
in linux terminal.

Specify **'-i'** or **'--interface'** for selecting the interface of which you want to change the MAC address.
Specify **'-m'** or **'--mac'** to give your desired MAC address as input.

**Syntax1: sudo hmacchanger -i <interface> -m <MAC_address>** // here <interface> = eth0,wlan0,etc. and <MAC_address> = Any MAC
> **eg. sudo hmacchanger -i wlan0 -m 00:11:22:33:44:55**

**Syntax2: sudo hmacchanger -i <interface>** // here <interface> = eth0,wlan0,etc.
> **eg. sudo hmacchanger -i wlan0** //random mac address will be auto generated.

**Syntax3: sudo hmacchanger -m <MAC_address>** // here <MAC_address> = Any MAC
> **eg. sudo hmacchanger -m 00:11:22:33:44:55** //Interface will be asked as input.

**Syntax4: sudo hmacchanger**
> **eg. sudo hmacchanger** //Interface will be asked as input and random mac address will be auto generated.


-----------------------
Author:
==========
Name:**Hariprasath.S.S**
Contact:**<hariprasath6112001@gmail.com>**
PyPi: **<https://pypi.org/user/hariprasath6112001/>**
Github: **<https://github.com/hairprasath6112001>**

------------------
**Report Bugs and Improvements**@ **<hariprasath6112001@gmail.com>**

--------------

