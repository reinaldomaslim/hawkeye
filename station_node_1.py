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
import datetime
import math
import time
import random
from googlemaps import convert
from gmplot import gmplot
from math import sin, cos, sqrt, atan2, radians
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
dir_path = os.path.dirname(os.path.realpath(__file__))

####################### NODE 1 for station ###########################
##### this node performs gui, analytics, and generate html maps #####
#####################################################################

#### sleep to wait download new files and conversion
time.sleep(3)

##### INIT GMAPS #####

gmaps = googlemaps.Client(key=config.API_KEY)

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

def snap(path, time):
    snapped_path = []
    cnt = 100

    for i in range(int(len(path)/cnt)):
        #use gmaps service to snap to road, cannot accept nan
        snap_road_result = gmaps.snap_to_roads(path[i*cnt:(i+1)*cnt], interpolate = False)
        for k in snap_road_result:
            lat = k['location']['latitude']
            lon = k['location']['longitude']
            snapped_path.append([lat, lon])
    
    snap_road_result = gmaps.snap_to_roads(path[int(len(path)/cnt)*cnt:], interpolate = False)
    for k in snap_road_result:
        lat = k['location']['latitude']
        lon = k['location']['longitude']
        snapped_path.append([lat, lon])
    
    #randomly drop some time
    for i in range(len(time) - len(snapped_path)):
        ind = random.randint(0, len(time)-1)
        time.pop(ind)

    return snapped_path, time

def make_html(veh_id, date):
    #veh_id: e.g. '1', '2', '3'
    #date; e.g. '05_02_2019' 'dd_mm_yyyy'
    html_name = dir_path+'/data/station/html/'+veh_id+'_'+date+'.html'
    status_path = dir_path+'/data/station/html/'+veh_id+'_'+date+'.txt'
    currentDT = datetime.datetime.now()
    today_date = currentDT.strftime("%d_%m_%Y")

    if date != today_date and os.path.isfile(html_name):
        if os.path.isfile(status_path):
            f = open(status_path, 'r')
            status_text = f.readlines()[0]
            # status_label.setText(status_text)
            return html_name

    ftxts = glob.glob(dir_path+'/data/station/text/'+veh_id+'_'+date+'*.txt')
    ftxts.sort()

    raw_path = []
    snapped_path = []
    snapped_time = []

    for ftxt in ftxts:
        f = open(ftxt, 'r')
        lines = f.readlines()
        path = []
        time = []

        for line in lines:
            if len(line) == 0:
                continue

            msg = line.split(' ')
            try:
                lat = float(msg[0])
                lon = float(msg[1])
                clock = float(msg[2])
            except:
                continue

            if np.isnan(lat) or np.isnan(lon):
                continue
            if lat == 0 or lon == 0:
                continue

            raw_path.append([lat, lon])
            path.append([lat, lon])
            time.append(clock)

        if len(path) == 0:
            continue

        res_path, res_time = snap(path, time)
        snapped_path.extend(res_path)
        snapped_time.extend(res_time)

    if len(snapped_path) == 0:
        return

    snapped_path = np.asarray(snapped_path)
    raw_path = np.asarray(raw_path)

    #plot snapped path
    gmap = gmplot.GoogleMapPlotter(snapped_path[int(len(snapped_path)/2)][0], snapped_path[int(len(snapped_path)/2)][1], 15, config.API_KEY)

    #plot raw path, heavy 
    gmap.scatter(raw_path[:, 0], raw_path[:, 1], 'sienna', size=5, marker=False)
    # gmap.scatter(snapped_path[:, 0], snapped_path[:, 1], 'antiquewhite', size=5, marker=False)

    stop_cnt = 0
    total_dist = 0
    total_time = 0

    #color code: stop-fast | red-blue 
    for i in range(len(snapped_path)-1):
        dist = distance(snapped_path[i], snapped_path[i+1])
        total_dist += dist
        delta_time = max(snapped_time[i+1] - snapped_time[i], config.spc)
        speed = dist/delta_time
        
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
            gmap.scatter([snapped_path[i, 0]], [snapped_path[i, 1]], 'orange', size=5, marker=True)
            stop_cnt = 0

        if dist > 500 or delta_time > 500:   
            #separate ride
            gmap.scatter([snapped_path[i, 0]], [snapped_path[i, 1]], 'red', size=5, marker=True)
            
            time = str(int(snapped_time[i-1]/3600))+':'+str(int(snapped_time[i-1]/60%60))
            gmap.infowindow(time, snapped_path[i-1, 0], snapped_path[i-1, 1])

            time = str(int(snapped_time[i]/3600))+':'+str(int(snapped_time[i]/60%60))
            gmap.infowindow(time, snapped_path[i, 0], snapped_path[i, 1])

            continue
        else:
            total_time += delta_time

        gmap.plot(snapped_path[i:i+2, 0], snapped_path[i:i+2, 1], color, edge_width=10)

    #starting and current ending point

    time = 'start ' + str(int(snapped_time[0]/3600))+':'+str(int(snapped_time[0]/60%60))
    gmap.infowindow(time, snapped_path[0, 0], snapped_path[0, 1])

    time = 'end ' + str(int(snapped_time[-1]/3600))+':'+str(int(snapped_time[-1]/60%60))
    gmap.infowindow(time, snapped_path[-1, 0], snapped_path[-1, 1])

    res = gmaps.reverse_geocode((snapped_path[-1, 0], snapped_path[-1, 1]))
    last_position = res[0]['address_components'][0]['short_name']+' '+res[0]['address_components'][1]['short_name']
    
    hour = int(snapped_time[-1]/3600)
    minutes = int((snapped_time[-1]-hour*3600)/60)
    sec = int(snapped_time[-1]-hour*3600-minutes*60)
    status_text = ' || updated time: ' + str(hour)+':'+str(minutes)+':'+str(sec)+\
        ' || total distance: ' + str(round(float(total_dist)/1000, 2))+\
        ' km || elapsed time: ' + str(float(total_time)/60)+\
        ' min || average speed: ' + str(round(total_dist*3.6/total_time, 2))+\
        ' km/h || last position: ' + last_position+\
        ' ||'
        
    # gmap.infowindow("'hello'", snapped_path[-1, 0], snapped_path[-1, 1])
    # status_label.setText(status_text)

    f = open(status_path, 'w')
    f.write(status_text)
    f.close()

    if gmap is not None:
        #save plot as html
        gmap.draw(html_name)
        return html_name

    return 
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
        load_html(html_path)

        if app.focusWidget() is not None:    
            app.focusWidget().clearFocus()
    
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
        load_html(html_path)


    def selectionchange(self,i):
        global cur_vehicle, cur_date
        cur_date = str(self.cb.currentText())

        html_path = make_html(cur_vehicle, cur_date)
        load_html(html_path)

        if app.focusWidget() is not None:    
            app.focusWidget().clearFocus()
        
def onTimer():
    #refresh page for new files
    global cur_vehicle, cur_date
    html_path = make_html(cur_vehicle, cur_date)
    load_html(html_path)

def load_html(path):    
    try:
        browser.load(QUrl(path))
    except:
        browser.load(QUrl(config.not_found_path))

def keyHandler(e):
    global vehicle_box, date_box, app

    if e.key() == Qt.Key_Escape:
        print("boobye")
        sys.exit(app.exec_())
    elif e.key() == Qt.Key_Right:
        i = vehicle_list.index(vehicle_box.cb.currentText())
        ind = min(i+1, len(vehicle_list)-1)
        vehicle_box.cb.setCurrentIndex(ind)
    elif e.key() == Qt.Key_Left:
        i = vehicle_list.index(vehicle_box.cb.currentText())
        ind = max(i-1, 0)
        vehicle_box.cb.setCurrentIndex(ind)
    elif e.key() == Qt.Key_Up:
        i = date_list.index(date_box.cb.currentText())
        ind = max(i-1, 0)
        date_box.cb.setCurrentIndex(ind)
    elif e.key() == Qt.Key_Down:
        i = date_list.index(date_box.cb.currentText())
        ind = min(i+1, len(date_list)-1)
        date_box.cb.setCurrentIndex(ind)
    
##### MAIN #####

if __name__ == "__main__":
    print("station Node 1: GUI and Analytics") 
    
    ftxts = glob.glob(dir_path+'/data/station/text/*.txt')
    vehicle_list = []
    date_list = []
    reverse_date_list = []
    for ftxt in ftxts:
        name = ftxt.split('/')[-1].split('.')[0].split('_')
        vehicle = name[0]
        date = name[1]+'_'+name[2]+'_'+name[3]
        reverse_date = name[3]+'_'+name[2]+'_'+name[1]

        if vehicle not in vehicle_list:
            vehicle_list.append(vehicle)

        if date not in date_list:
            date_list.append(date)
            reverse_date_list.append(reverse_date)


    vehicle_list.sort()
    date_list = [x for _,x in sorted(zip(reverse_date_list, date_list), reverse=True)]

    cur_vehicle = vehicle_list[0]               
    cur_date = date_list[0]                      

    app = QApplication(['Hawkeye v1.0'])

    # create grid layout
    grid = QGridLayout()
    browser = QWebView()
        
    status_label = QLabel()
    status_label.setFixedHeight(20)
    status_label.setStyleSheet('color: white')

    #load available dates from vehicle folder
    vehicle_label = QLabel()
    vehicle_label.setText('Vehicle')
    vehicle_label.setFixedHeight(10)
    vehicle_label.setStyleSheet('color: limegreen')
    vehicle_box = VehicleBox(vehicle_list)
    vehicle_box.setFixedHeight(40)
    vehicle_box.setStyleSheet('color: black; background-color: white;')
    #load available dates from date folder
    date_label = QLabel()
    date_label.setText('Date')
    date_label.setFixedHeight(10)
    date_label.setStyleSheet('color: limegreen')
    date_box = DateBox(date_list)
    date_box.setFixedHeight(40)
    date_box.setStyleSheet('color: black; background-color: white;')

    grid.addWidget(vehicle_label, 1, 0)
    grid.addWidget(vehicle_box, 2, 0)
    grid.addWidget(date_label, 3, 0)
    grid.addWidget(date_box, 4, 0)
    grid.addWidget(status_label, 5, 0)
    grid.addWidget(browser, 6, 0)
    
    # main app window
    main_frame = QWidget()
    main_frame.setLayout(grid)
    main_frame.showMaximized()
    main_frame.setStyleSheet("color: white; background-color: black;")
    main_frame.keyPressEvent = keyHandler
    main_frame.setFocus()

    timer = QTimer(grid)
    timer.timeout.connect(onTimer)
    timer.setInterval(config.rpf_min*60*1000) #in ms, every rpf minutes
    timer.start() 

    # close app when user closes window
    sys.exit(app.exec_())
