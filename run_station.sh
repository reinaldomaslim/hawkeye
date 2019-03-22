#!/bin/bash
echo "Hawkeye Server"
echo "project of reinaldomaslim"

#sleep wait for wifi to be up
# sleep 5


gnome-terminal --tab -e  "python station_node_1.py"

while true 
do
	#need to copy from server
	rsync -avz --remove-source-files -e "ssh -i ~/Downloads/LightsailDefaultKey-ap-southeast-1.pem" ubuntu@3.0.67.37:/home/ubuntu/Documents/hawkeye/data/server/text/* ~/Documents/hawkeye/data/station/text
	sleep 60
done