from flask import Flask, render_template, url_for, request
# from station_node_1 import make_html

app = Flask(__name__, template_folder="./data/server/html")

@app.route('/', methods=['GET', 'POST'])
def form():

    if request.method == 'POST':
        default_veh = 'dragon'
        default_date = '2019-04-30'

        vehicle = request.form.get('vehicle', default_veh)
        date = request.form.get('date', default_date).split('-')
        date = date[2]+'_'+date[1]+'_'+date[0]

        html_path = vehicle +'_'+date+'.html'
        # html_path = make_html(vehicle, date).split('/')[-1]
        print(html_path)
        
        return render_template(html_path)

    else:
        return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)