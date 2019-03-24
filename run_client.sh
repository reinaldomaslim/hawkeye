#!/bin/bash
echo "Hawkeye Client"
echo "project of reinaldomaslim"

#sleep wait for gps to be up
sleep 1
gnome-terminal --tab --working-directory=$HOME/Documents/hawkeye/ -e "python client_node_1.py"

while true 
do
	#need to copy from server
	rsync -avz -e "ssh -i ~/Documents/hawkeye/LightsailDefaultKey-ap-southeast-1.pem" $HOME/Documents/hawkeye/data/client/* ubuntu@3.0.67.37:/home/ubuntu/Documents/hawkeye/data/server/text/ 
	rsync -avz --remove-source-files -e "ssh -i ~/Documents/hawkeye/LightsailDefaultKey-ap-southeast-1.pem" $HOME/Documents/hawkeye/data/client/* ubuntu@3.0.67.37:/home/ubuntu/Documents/hawkeye/data/server/backup/

	sleep 600
done

#gnome-terminal --tab --working-directory=$HOME/Documents/hawkeye/ -e "python client_node_1.py" \
#               --tab --working-directory=$HOME/Documents/hawkeye -e "python client_node_2.py"
