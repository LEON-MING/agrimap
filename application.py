from flask import Flask, render_template, request
from map import *

application = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html", rainfall=get_rainfall_map(1999))

@app.route('/rainfall')
def rainfall():
    year = request.args.get('year')
    print(year)
    return get_rainfall_map(int(year));
