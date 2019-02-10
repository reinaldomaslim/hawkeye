#!/bin/bash
echo "Hawkeye Server"
echo "project of reinaldomaslim"

#sleep wait for wifi to be up
sleep 5

gnome-terminal --tab -e "python ~/Documents/hawkeye/server_node_1.py"
gnome-terminal --tab -e "python ~/Documents/hawkeye/server_node_2.py"