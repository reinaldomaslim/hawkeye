#! /usr/bin/python

###################
##### HAWKEYE #####
###################
import os
import glob
import numpy as np 

import subprocess
from station_node_1 import make_html
from station_node_2 import convert_to_text

dir_path = os.path.dirname(os.path.realpath(__file__))

####################### NODE 2 for server ###########################
##### this node performs gui, analytics, and generate html maps #####
#####################################################################


#run through all existing texts and check if html file has been created
#for today's text, keep updating html if new textfile exist (via created time)

##### MAIN #####

if __name__ == "__main__":
    print("server Node 2: Create HTMLS template") 
    
    subprocess.call(['./launch_web.sh'])
        
    while True:
        convert_to_text()

        new_html = False
        ftxts = glob.glob('./data/station/text/*.txt')
        
        for ftxt in ftxts:
            txt = ftxt.split('/')[-1].split('_')
            veh = txt[0]
            date = txt[1]+'_'+txt[2]+'_'+txt[3]

            html_path = './data/station/html/'+veh+'_'+date+'.html'
            print(html_path)

            if not os.path.isfile(html_path):
                print('file doesnt exist')
                make_html(veh, date)
                new_html = True
            else:
                html_time = os.path.getmtime(html_path)
                ftxt_time = os.path.getmtime(ftxt)
                if ftxt_time > html_time:
                    make_html(veh, date)
                    new_html = True
        
            if new_html:
                #relaunch when new file is created
                subprocess.call(['./launch_web.sh'])
        
        time.sleep(60*5)