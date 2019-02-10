#! /usr/bin/python

###################
##### HAWKEYE #####
###################

import os
import socket
import glob
import time
import datetime
import config
dir_path = os.path.dirname(os.path.realpath(__file__))

##### NODE 2 for CLIENT #####
# this node checks and sends txt files #
# check new, if written > 30 s ago, send file to server, move file to old
# check old, if written > 1 month ago, erase file

##### INIT SOCKET #####

host_ip = config.host_ip
port = config.port

def send_file(file_name):
    s = socket.socket()
    while True:        
        try:    
            s.connect((host_ip, port))
            break
        except:
            time.sleep(1)		
            print('Waiting for connection...')

    s.send(file_name.split('/')[-1])	
    time.sleep(0.1)
	
    f = open(file_name, 'r')

    lines = f.readlines()
    for line in lines:
        print('Sending...')
        s.send(line)
        time.sleep(0.1)

    f.close()
    #s.shutdown(socket.SHUT_WR)
    s.close()

##### MAIN #####

def is_older(current_date, txt_date):
	#return the difference
	#change to days wrt 2019
	current_days = float(current_date[0])+31*float(current_date[1])+365*(float(current_date[2])-2019)
	txt_days = float(txt_date[0])+31*float(txt_date[1])+365*(float(txt_date[2])-2019)

	diff = int(current_days - txt_days)
	return diff

if __name__ == '__main__':
    print("Client Node 2: Send to server and bookeeping")  

    while True:
        currentDT = datetime.datetime.now()
        current_date = currentDT.strftime("%d_%m_%Y").split('_')
        duration = str(currentDT).split(' ')[-1].split(':')            
        current_time = int(float(duration[0])*3600+float(duration[1])*60+float(duration[2]))

        #check new folder
        ftxts = glob.glob(dir_path+'/data/client/new/*.txt')
        sent = []
        print(ftxts)
        for ftxt in ftxts:
            print(ftxt)
            name = ftxt.split('/')[-1].split('.')[0]
            txt_date = name.split('_')[1:4]
            txt_time = int(name.split('_')[-1])			
			
            print(current_time, txt_time, is_older(current_date, txt_date))
            if is_older(current_date, txt_date) > 0:
                #send file
                send_file(ftxt)
                sent.append(ftxt)
            if is_older(current_date, txt_date) == 0 and (current_time - txt_time) > 60*20:
                #send file
                send_file(ftxt)
                sent.append(ftxt)
        
        for ftxt in sent:                
            #move file to old
            name = ftxt.split('/')[-1].split('.')[0]
            destination = dir_path+'/data/client/old/'+name+'.txt'
            os.rename(ftxt, destination)
		
        #check old folder
        ftxts = glob.glob(dir_path+'/data/client/old/*.txt')
        for ftxt in ftxts:
            name = ftxt.split('/')[-1].split('.')[0]
            txt_date = name.split('_')[1:4]

            if is_older(current_date, txt_date) > 31:
	            os.remove(ftxt)
        
        time.sleep(60)

