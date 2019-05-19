import glob
import os
from flask import Flask, render_template, url_for, request
#from shutil import copyfile


###############################################
#get vehicle names from 
ftxts = glob.glob('./data/station/html/*.html')
vehicle_list = set()
for ftxt in ftxts:
    name = ftxt.split('/')[-1].split('.')[0].split('_')
    vehicle = name[0]
    vehicle_list.add(vehicle)

vehicle_list = list(vehicle_list)


template_folder = './data/station/html'

#copyfile('./form.html', template_folder+'/form.html')


###############################################
app = Flask(__name__, template_folder=template_folder)

@app.route('/', methods=['GET', 'POST'])
def form():

    if request.method == 'POST':
        default_veh = vehicle_list[0]
        default_date = '2019-04-30'

        vehicle = request.form.get('vehicle', default_veh)
        
        date = request.form.get('date', default_date).split('-')
        date = date[2]+'_'+date[1]+'_'+date[0]

        html_path = vehicle +'_'+date+'.html'
        
        if os.path.isfile(template_folder+'/'+html_path):
            return render_template(html_path)
        else:
            return render_template("form.html", vehicle_list = vehicle_list)


    else:
        return render_template("form.html", vehicle_list = vehicle_list)


###############################################
if __name__ == "__main__":
    app.run(debug=True)
