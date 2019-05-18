#! /usr/bin/python

###################
##### HAWKEYE #####
###################
import os
import glob
import numpy as np 
import json
import subprocess
import config
from station_node_1 import make_html
from shutil import copyfile

dir_path = os.path.dirname(os.path.realpath(__file__))

####################### NODE 2 for server ###########################
##### this node performs gui, analytics, and generate html maps #####
#####################################################################

def convert_to_text():
    files = glob.glob('./data/server/android/*.geojson')
    for file in files:
        f = open(file)
        profile = file.split('/')[-1].split('_')[0]
        day = file.split('/')[-1].split('_')[1][:2]
        month = file.split('/')[-1].split('_')[1][2:4]
        year = file.split('/')[-1].split('_')[1][4:]

        clock = str(int(file.split('/')[-1].split('_')[-1].split('.')[0])*3600)
        text_path = './data/station/text/' + profile +'_'+ day +'_'+ month +'_'+ year +'_'+clock+'.txt'
        
        if os.path.isfile(text_path):
            json_time = os.path.getmtime(file)
            txt_time = os.path.getmtime(text_path)
            if json_time<txt_time:
                continue
            else:
                os.remove(text_path)
       
        res = open(text_path, 'w')
        print('make text '+text_path)
        data = json.load(f)
        for feature in data['features']:
            accuracy = feature['properties']['accuracy']
            provider = feature['properties']['provider']

            if provider == 'network':
                continue

            time = feature['properties']['time']
            h = int(time.split('T')[-1].split(':')[0]) + config.timezone
            m = int(time.split('T')[-1].split(':')[1])
            s = float(time.split('T')[-1].split(':')[-1][:6])
            clock = 3600*h+60*m+int(s)
            lon = feature['geometry']['coordinates'][0]
            lat = feature['geometry']['coordinates'][1]

            text = str(lat) +' '+ str(lon)+' '+str(clock)+'\n'
            res.write(text)

        res.close()

    files = glob.glob('./data/server/backup/*.txt')
    for file in files:
        dst = file.replace('backup', 'text').replace('server', 'station')
        if not os.path.isfile(dst):
            copyfile(file, dst)

#run through all existing texts and check if html file has been created
#for today's text, keep updating html if new textfile exist (via created time)

def upload_to_cloud(html_path):
    
    command = ['gsutil cp ' + html_path + ' gs://staging.neon-bank-181705.appspot.com/']
    subprocess.call(command, shell = True)

##### MAIN #####

if __name__ == "__main__":
    print("server Node 2: Create HTMLS template") 
    
    # subprocess.call(['./launch_web.sh'])
         
    convert_to_text()

    ftxts = glob.glob('./data/station/text/*.txt')
    ftxts.sort()
    
    new_htmls = []
    for ftxt in ftxts:
        txt = ftxt.split('/')[-1].split('_')
        veh = txt[0]
        date = txt[1]+'_'+txt[2]+'_'+txt[3]

        html_path = './data/station/html/'+veh+'_'+date+'.html'
    
        if not os.path.isfile(html_path):
            print(html_path + ' doesnt exist')
            make_html(veh, date)
            new_htmls.append(html_path)
        else:
            html_time = os.path.getmtime(html_path)
            ftxt_time = os.path.getmtime(ftxt)
            #print(ftxt_time, html_time)      
            if ftxt_time > html_time:
                print('updated html '+ html_path)
                os.remove(html_path)
                make_html(veh, date)
                new_htmls.append(html_path)

    for html_path in set(new_htmls):
        upload_to_cloud(html_path)
