#! /usr/bin/python

###################
##### HAWKEYE #####
###################
import os
import json
import glob

##### MAIN #####

if __name__ == "__main__":
    print("station Node 2: convert geojson files to txt") 

    files = glob.glob('./data/station/android/*.geojson')
    for file in files:
        f = open(file)
        profile = file.split('/')[-1].split('_')[0]
        day = file.split('/')[-1].split('_')[1][:2]
        month = file.split('/')[-1].split('_')[1][2:4]
        year = file.split('/')[-1].split('_')[1][4:]

        clock = str(int(file.split('/')[-1].split('_')[-1].split('.')[0])*3600)
        text_path = './data/station/text/' + profile +'_'+ day +'_'+ month +'_'+ year +'_'+clock+'.txt'
        
        if os.path.isfile(text_path):
            continue

        print(text_path)
        res = open(text_path, 'w')

        data = json.load(f)
        for feature in data['features']:
            accuracy = feature['properties']['accuracy']
            provider = feature['properties']['provider']

            if provider == 'network':
                continue
            print(provider, accuracy)


            time = feature['properties']['time']
            h = int(time.split('T')[-1].split(':')[0])
            m = int(time.split('T')[-1].split(':')[1])
            s = float(time.split('T')[-1].split(':')[-1][:6])
            clock = 3600*h+60*m+int(s)
            lon = feature['geometry']['coordinates'][0]
            lat = feature['geometry']['coordinates'][1]
            print(lat, lon, clock)

            text = str(lat) +' '+ str(lon)+' '+str(clock)+'\n'
            # break
            res.write(text)

        res.close()

        