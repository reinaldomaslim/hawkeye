#!/bin/bash
echo "Hawkeye Server"
echo "project of reinaldomaslim"

#sleep wait for wifi to be up

gnome-terminal --tab -e  "python server_node_2.py"

while true 
do
	#need to copy from server
	python housekeeper.py
	#sleep for today
	sleep 86400
done