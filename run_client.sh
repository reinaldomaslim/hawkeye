#!/bin/bash
echo "Hawkeye Client"
echo "project of reinaldomaslim"

#sleep wait for gps to be up
sleep 10

gnome-terminal --tab -e "python client_node_1.py"
gnome-terminal --tab -e "python client_node_2.py"