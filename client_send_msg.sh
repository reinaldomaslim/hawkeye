#!/bin/bash
#need to copy to server
rsync -avz -e "ssh -i ~/Documents/hawkeye/LightsailDefaultKey-ap-southeast-1.pem" $HOME/Documents/hawkeye/data/client/* ubuntu@3.0.67.37:/home/ubuntu/Documents/hawkeye/data/server/backup/
#--remove-source-files 
