#!/bin/bash
echo "Hawkeye Client"
echo "project of reinaldomaslim"

sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sudo killall gpsd
sudo gpsd  /dev/ttyUSB0 -F  /var/run/gpsd.sock

#sleep wait for gps to be up
sleep 1
gnome-terminal --tab --working-directory=$HOME/Documents/hawkeye/ -e "python client_node_1.py"

#gnome-terminal --tab --working-directory=$HOME/Documents/hawkeye/ -e "python client_node_1.py" \
#               --tab --working-directory=$HOME/Documents/hawkeye -e "python client_node_2.py"
