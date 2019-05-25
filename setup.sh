#!/bin/bash

sudo apt-get install gpsd gpsd-clients
sudo apt-get install gnome-terminal
sudo apt-get install python-qt4
sudo apt-get install python-pip
pip install googlemaps
pip install gmplot
pip install flask
scp ./update_gmplot/gmplot.py ~/.local/lib/python2.7/site-packages/gmplot/

#### set autorun via .bashrc, 
#remove login by adding /usr/share/lightdm/lightdm.conf.d/60-lightdm-gtk-greeter.conf file. 
#greeter-session=lightdm-gtk-greeter 
#autologin-user=srackham 
#go to settings and enable autologin