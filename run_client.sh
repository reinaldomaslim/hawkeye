#!/bin/bash
echo "Hawkeye Client"
echo "project of reinaldomaslim"

#sleep wait for gps to be up
sleep 1
gnome-terminal --tab --working-directory=$HOME/Documents/hawkeye/ -e "python client_node_1.py" \
               --tab --working-directory=$HOME/Documents/hawkeye -e "python client_node_2.py"
