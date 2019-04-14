#!/bin/bash
echo "Hawkeye Client"
echo "project of reinaldomaslim"

#check for internet, so time is correct
sleep 2

sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket
sudo killall gpsd
sudo gpsd  /dev/ttyUSB0 -F  /var/run/gpsd.sock

#sleep wait for gps to be up
echo "wait for gps"
sleep 2
gnome-terminal --tab --working-directory=$HOME/Documents/hawkeye/ -e "python client_node_1.py"\
               --tab -e "cgps"

while true 
do
	#need to copy from server
	python housekeeper.py
	sleep 24*3600
done