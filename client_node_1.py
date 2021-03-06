#! /usr/bin/python

###################
##### HAWKEYE #####
###################

import os
from gps import *
from time import *
import time
import threading
import datetime
import config
import math
import subprocess

##### NODE 1 for CLIENT #####
# this node reads gps, and constantly write to txt file #

##### INIT GPS #####
gpsd = None #seting the global variable

class GpsPoller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        global gpsd #bring it in scope
        gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
        self.current_value = None
        self.running = True #setting the thread running to true

    def run(self):
        global gpsd
        while gpsp.running:
          #this will continue to loop and grab EACH set of gpsd info to clear the buffer
          gpsd.next() 

##### MAIN #####

if __name__ == '__main__':
    print("Client Node 1: Read GPS and store data")  

    gpsp = GpsPoller() # create the thread
    try:    
        gpsp.start()
                
        veh_id = config.veh_id
        spc = config.spc #how many sec per capture, every 5 seconds
        rpf = int(config.rpf_min*60/spc) # how many readings per file, every 15 minutes
        cnt = 0
        start = True
        while True:
            currentDT = datetime.datetime.now()       
            date = currentDT.strftime("%d_%m_%Y")
            duration = str(currentDT).split(' ')[-1].split(':')            
            current_time = int(float(duration[0])*3600+float(duration[1])*60+float(duration[2]))

            if cnt%rpf == 0:
               time.sleep(1)   
				                     
               subprocess.call(['./client_send_msg.sh'])
               if start:
                   start = False
               else:
                   f.close()
               #vehicleID + date + time
               file_name = './data/client/'+veh_id+'_'+date+'_'+str(current_time)+'.txt'
               print(file_name)
               f = open(file_name, 'w')               
               cnt = 0
            else:
               f = open(file_name, 'a', 0)

            print('--------------------')      					
            #It may take a second or two to get good data
            #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
            text = str(gpsd.fix.latitude)+' '+str(gpsd.fix.longitude)+' '+str(current_time)+'\n' 		    
            
            f.write(text)	
            print(text)

            cnt += 1
            time.sleep(spc) #set to whatever
            gpsd.next() 	       

    except: #when you press ctrl+c
        print("\nKilling Thread...")
        f.close()
        gpsp.running = False
        gpsp.join() # wait for the thread to finish what it's doing

    print("Done.\nExiting.")
