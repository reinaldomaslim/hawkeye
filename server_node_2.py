#! /usr/bin/python

###################
##### HAWKEYE #####
###################

import os
import numpy as np 
import googlemaps
import glob
import sys
import config
from googlemaps import convert
from gmplot import gmplot
from math import sin, cos, sqrt, atan2, radians
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
dir_path = os.path.dirname(os.path.realpath(__file__))


####################### NODE 2 for SERVER ###########################
##### this node performs gui, analytics, and generate html maps #####
#####################################################################

##### INIT GMAPS #####

API_KEY = config.API_KEY     #setup key
gmaps = googlemaps.Client(key=API_KEY)

def distance(pt1, pt2):
    # approximate radius of earth in m
    R = 6373000
    #must be in rads not degrees
    lat1 = radians(pt1[0])
    lon1 = radians(pt1[1])
    lat2 = radians(pt2[0])
    lon2 = radians(pt2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

def make_html(veh_id, date):
    #veh_id: e.g. '1', '2', '3'
    #date; e.g. '05_02_2019' 'dd_mm_yyyy'
    if veh_id == 'all':
        for j in range(1, len(vehicle_list)):
            veh = vehicle_list[j]
            ftxts = glob.glob(dir_path+'/data/server/text/'+veh+'_'+date+'*.txt')
            ftxts.sort()

            snapped_path = []
            raw_path = []
            time = []
            
            for ftxt in ftxts:
                f = open(ftxt, 'r')
                lines = f.readlines()
                path = []

                for line in lines:
                    if len(line) == 0:
                        continue

                    msg = line.split(' ')
                    lat = float(msg[0])
                    lon = float(msg[1])
                    clock = float(msg[2])

                    #sanity checks
                    if np.isnan(lat) or np.isnan(lon):
                        continue
                    if lat == 0 or lon == 0:
                        continue

                    raw_path.append([lat, lon])
                    path.append([lat, lon])
                    time.append(clock)
                
                if len(path) == 0:
                    continue

                #use gmaps service to snap to road, cannot accept nan
                snap_road_result = gmaps.snap_to_roads(path, interpolate = False)
                for k in snap_road_result:
                    lat = k['location']['latitude']
                    lon = k['location']['longitude']
                    snapped_path.append([lat, lon])
            
            snapped_path = np.asarray(snapped_path)
            raw_path = np.asarray(raw_path)

            #plot snapped path
            if j == 1:
                gmap = gmplot.GoogleMapPlotter(snapped_path[int(len(snapped_path)/2)][0], snapped_path[int(len(snapped_path)/2)][1], 15, API_KEY)
            
            #plot raw path
            gmap.scatter(raw_path[:, 0], raw_path[:, 1], 'sienna', size=5, marker=False)
            gmap.scatter(snapped_path[:, 0], snapped_path[:, 1], 'antiquewhite', size=5, marker=False)

            stop_cnt = 0

            #color code: stop-fast | red-blue 
            for i in range(len(snapped_path)-1):
                dist = distance(snapped_path[i], snapped_path[i+1])
                speed = dist/(time[i+1] - time[i])
                if speed < 1:
                    #essentially stop
                    stop_cnt += 1
                else:
                    #> 50 kmph
                    stop_cnt = 0

                if stop_cnt > 1*60/config.spc: #we wait 5 minutes
                    #stopped for too long, put a flag
                    gmap.scatter([snapped_path[i, 0]], [snapped_path[i, 1]], 'red', size=5, marker=True)
                    stop_cnt = 0

                gmap.plot(snapped_path[i:i+2, 0], snapped_path[i:i+2, 1], config.colors[j%len(config.colors)], edge_width=10)

    else:
        ftxts = glob.glob(dir_path+'/data/server/text/'+veh_id+'_'+date+'*.txt')
        ftxts.sort()

        snapped_path = []
        raw_path = []
        time = []
        
        for ftxt in ftxts:
            f = open(ftxt, 'r')
            lines = f.readlines()
            path = []

            for line in lines:
                if len(line) == 0:
                    continue

                msg = line.split(' ')
                lat = float(msg[0])
                lon = float(msg[1])
                clock = float(msg[2])

                #sanity checks
                if np.isnan(lat) or np.isnan(lon):
                    continue
                if lat == 0 or lon == 0:
                    continue

                raw_path.append([lat, lon])
                path.append([lat, lon])
                time.append(clock)
            
            if len(path) == 0:
                continue

            #use gmaps service to snap to road, cannot accept nan
            snap_road_result = gmaps.snap_to_roads(path, interpolate = False)
            for k in snap_road_result:
                lat = k['location']['latitude']
                lon = k['location']['longitude']
                snapped_path.append([lat, lon])
        

        snapped_path = np.asarray(snapped_path)
        raw_path = np.asarray(raw_path)

        #plot snapped path
        gmap = gmplot.GoogleMapPlotter(snapped_path[int(len(snapped_path)/2)][0], snapped_path[int(len(snapped_path)/2)][1], 15, API_KEY)
        #plot raw path
        gmap.scatter(raw_path[:, 0], raw_path[:, 1], 'sienna', size=5, marker=False)
        gmap.scatter(snapped_path[:, 0], snapped_path[:, 1], 'antiquewhite', size=5, marker=False)

        stop_cnt = 0

        #color code: stop-fast | red-blue 
        for i in range(len(snapped_path)-1):
            dist = distance(snapped_path[i], snapped_path[i+1])
            speed = dist/(time[i+1] - time[i])
            if speed < 1:
                #essentially stop
                color = 'red'
                stop_cnt += 1
            elif speed < 10/3.6:
                #below 10 kmph
                color = 'maroon'
                stop_cnt = 0
            elif speed < 25/3.6:
                #below 25 kmph
                color = 'darkorange'
                stop_cnt = 0
            elif speed < 50/3.6:
                #below 50 kmph
                color = 'seagreen'
                stop_cnt = 0
            else:
                #> 50 kmph
                color = 'royalblue'
                stop_cnt = 0

            if stop_cnt > 1*60/config.spc: #we wait 5 minutes
                #stopped for too long, put a flag
                gmap.scatter([snapped_path[i, 0]], [snapped_path[i, 1]], 'red', size=5, marker=True)
                stop_cnt = 0

            gmap.plot(snapped_path[i:i+2, 0], snapped_path[i:i+2, 1], color, edge_width=10)


    #save plot as html
    html_name = dir_path+'/data/server/html/'+veh_id+'_'+date+'.html'
    gmap.draw(html_name)
    
    return html_name

##### INIT WIDGETS #####

class VehicleBox(QWidget):
    def __init__(self, items):
        super(VehicleBox, self).__init__()

        layout = QHBoxLayout()
        self.cb = QComboBox()
        self.cb.addItems(items)
        self.cb.currentIndexChanged.connect(self.selectionchange)

        layout.addWidget(self.cb)
        self.setLayout(layout)

    def selectionchange(self,i):
        global cur_vehicle, cur_date
        cur_vehicle = str(self.cb.currentText())

        html_path = make_html(cur_vehicle, cur_date)
        browser.load(QUrl(html_path))

class DateBox(QWidget):
    def __init__(self, items):
        super(DateBox, self).__init__()

        layout = QHBoxLayout()
        self.cb = QComboBox()
        self.cb.addItems(items)
        self.cb.currentIndexChanged.connect(self.selectionchange)

        layout.addWidget(self.cb)
        self.setLayout(layout)

        html_path = make_html(cur_vehicle, cur_date)
        browser.load(QUrl(html_path))

    def selectionchange(self,i):
        global cur_vehicle, cur_date
        cur_date = str(self.cb.currentText())

        html_path = make_html(cur_vehicle, cur_date)
        browser.load(QUrl(html_path))

def onTimer():
    print('refresh')
    global cur_vehicle, cur_date
    html_path = make_html(cur_vehicle, cur_date)
    browser.load(QUrl(html_path))


##### MAIN #####

if __name__ == "__main__":
    print("Server Node 2: GUI and Analytics") 

    ftxts = glob.glob(dir_path+'/data/server/text/*.txt')
    vehicle_list = []
    date_list = []

    for ftxt in ftxts:
        name = ftxt.split('/')[-1].split('.')[0].split('_')
        vehicle = name [0]
        date = name[1]+'_'+name[2]+'_'+name[3]

        if vehicle not in vehicle_list:
            vehicle_list.append(vehicle)

        if date not in date_list:
            date_list.append(date)

    vehicle_list.sort()
    vehicle_list.insert(0, 'all')
    date_list.sort(reverse=True)

    cur_vehicle = vehicle_list[0]               
    cur_date = date_list[0]                      

    app = QApplication(['Hawkeye v1.0'])

    # create grid layout
    grid = QGridLayout()
    browser = QWebView()
    # url_input = UrlInput(browser)

    #load available dates from vehicle folder
    vehicle_label = QLabel()
    vehicle_label.setText('Vehicle')
    vehicle_label.setFixedHeight(10)
    vehicle_label.setStyleSheet('color: yellow')
    vehicle_box = VehicleBox(vehicle_list)
    vehicle_box.setFixedHeight(40)
    vehicle_box.setStyleSheet('color: black; background-color: white;')
    #load available dates from date folder
    date_label = QLabel()
    date_label.setText('Date')
    date_label.setFixedHeight(10)
    date_label.setStyleSheet('color: yellow')
    date_box = DateBox(date_list)
    date_box.setFixedHeight(40)
    date_box.setStyleSheet('color: black; background-color: white;')
    grid.addWidget(vehicle_label, 1, 0)
    grid.addWidget(vehicle_box, 2, 0)
    grid.addWidget(date_label, 3, 0)
    grid.addWidget(date_box, 4, 0)
    grid.addWidget(browser, 5, 0)
    
    # main app window
    main_frame = QWidget()
    main_frame.setLayout(grid)
    main_frame.showMaximized()
    main_frame.setStyleSheet("color: white; background-color: black;")

    timer = QTimer(grid)
    timer.timeout.connect(onTimer)
    timer.setInterval(config.rpf_min*60*1000) #in ms, every rpf minutes
    timer.start() 
    
    # close app when user closes window
    sys.exit(app.exec_())
