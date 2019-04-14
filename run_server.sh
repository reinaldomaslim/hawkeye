#!/bin/bash
echo "Hawkeye Server"
echo "project of reinaldomaslim"

#sleep wait for wifi to be up

#python $HOME/Documents/hawkeye/server_node_1.py

while true 
do
	#need to copy from server
	python housekeeper.py
	#sleep for today
	sleep 24*3600
done