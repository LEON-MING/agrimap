from flask import Flask, render_template, request
from map import *

application = Flask(__name__)

@application.route('/')
def home():
    return render_template("home.html",
                            rainfall=get_rainfall_map(1999),
                            temp=get_temp_map(1999))

@application.route('/data')
def rainfall():
    year = request.args.get('year')
    print(year)
    return { "rainfall" : get_rainfall_map(int(year)),
             "temp" : get_temp_map(int(year)),
             "year" : year }

if __name__ == "__main__":
    application.run()
