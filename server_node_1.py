#! /usr/bin/python

###################
##### HAWKEYE #####
###################

import os
import socket             
import config
from shutil import copyfile


dir_path = os.path.dirname(os.path.realpath(__file__))

##### NODE 1 for SERVER #####
# this node listens to clients and receive txt data #

##### MAIN #####

if __name__ == '__main__':
    print('Server Node 1: Listens to clients and receive data')

    s = socket.socket()             # Create a socket object
    host = socket.gethostname()     # Get local machine name
    port = config.port              # Reserve a port for your service.
    
    s.bind(('0.0.0.0', port))              # Bind to the port

    s.listen(30)                    # Now wait for client connection, queue up to 30 channels

    while True:
        try:
            c, addr = s.accept()    # Establish connection with client.
            print('Got connection from', addr)
            l = c.recv(1024)
            print(l)
            fpath = dir_path+'/data/server/text/'+l
            f = open(fpath,'w')

            while True:
                l = c.recv(1024)
                if not l:
                    break
                f.write(l)
                    
            f.close()
            c.close()                # Close the connection 
            copyfile(fpath, dir_path+'/data/server/backup/'+l)
            print("Done Receiving")
        except:
            print('Exiting Server')
            break

    s.close()

