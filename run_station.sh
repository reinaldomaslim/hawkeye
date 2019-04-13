#!/bin/bash
echo "Hawkeye Server"
echo "project of reinaldomaslim"

#sleep wait for wifi to be up
# sleep 5
gnome-terminal --tab -e  "python station_node_1.py"

while true 
do
	#need to copy from server
	# rsync -avz --remove-source-files -e "ssh -i ~/Downloads/LightsailDefaultKey-ap-southeast-1.pem" ubuntu@3.0.67.37:/home/ubuntu/Documents/hawkeye/data/server/text/* ~/Documents/hawkeye/data/station/text
	rsync -avz -e "ssh -i ~/Downloads/LightsailDefaultKey-ap-southeast-1.pem" ubuntu@3.0.67.37:/home/ubuntu/Documents/hawkeye/data/server/backup/* ~/Documents/hawkeye/data/station/text
	rsync -avz -e "ssh -i ~/Downloads/LightsailDefaultKey-ap-southeast-1.pem" ubuntu@3.0.67.37:/home/ubuntu/Documents/hawkeye/data/server/android/*.geojson ~/Documents/hawkeye/data/station/android
	python station_node_2.py
	sleep 60
done