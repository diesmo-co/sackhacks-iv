# Author: Yee Chuen Teoh
# title: Main flask file
# description:

# Imports
from flask import Flask, redirect, url_for, render_template, request
import panda as pd

df1 = pd.read_csv

# TODO:
# 1. DONE: Creating endpoints (GET, POST) adding new devices, new rooms
# 2. DONE: Creating Flask Routes for endpoint

app = Flask(__name__)

# --- 5 main pages --- 
# homepage
# popup for creating new room
# roompage
# popup for creting new device
# devicepage 

@app.route("/")
def home():
    # TODO: check the html page name
    return render_template("homepage.html")

# roompage pop up for creating new room
@app.route("/newroom", methods=["POST","GET"])
def newroom():
    if request.method == "POST":
        # new room name get the parameter using post
        # TODO: check the variable name for the form
        room_name = request.form["room_name"]
        # new room id to be added to csv
        # room_id
        # TODO: go to csv, max(room_id)+1 will be new id

        # TODO:pass the room_name to the roompage
        return redirect(url_for("roompage", room_name = room_name))
    else:
        # TODO: check the html page name
        return render_template("newroom.html")

# below need to get some parameter to know which room to go
@app.route("/<room_name>")
def roompage(room_name):
    # TODO: check the html page name
    # TODO: check the header variable name
    # TODO ? : potentially pass the graph information& list of devices

    return render_template("roompage.html", room_name = room_name)

# devicepage pop up for creating new device
@app.route("/newdevice", methods=["POST","GET"])
def newdevice():
    if request.method == "POST":
        # new device name get the parameter using post
        # TODO: check the variable name for the form
        device_name = request.form["device_name"]

        # TODO: check the variable name for the form
        room_id = request.form["room_id"]

        # TODO: check the variable name for the form
        device_type = request.form["device_type"]

        # TODO: check the variable name for the form
        device_kWh = request.form["device_kWh"]
        

        # new device id to be added to csv
        # device_id
        # TODO: go to csv, max(device_id)+1 will be new id

        # TODO:pass the room_name to the roompage
        return redirect(url_for("devicepage.html", device_name = device_name))
    else:
        # TODO: check the html page name
        # TODO ? : pass a list of available room for the dropdown options
        return render_template("home.html")


@app.route("/<device_name>")
def devicepage(device_name):
    # TODO: check the html page name
    # TODO: check the header variable name
    # TODO ? : potentially pass the graph & list of devices information
    return render_template("devicepage.html", device_name=device_name)

if __name__ == "__main__":
    app.run(debug = True)
