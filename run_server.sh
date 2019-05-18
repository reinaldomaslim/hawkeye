#!/bin/bash
echo "Hawkeye Server"
echo "project of reinaldomaslim"

#sleep wait for wifi to be up

./launch_web.sh

while true 
do
	#need to copy from server
	python server_node_2.py
	#sleep for today
	sleep 60
done
