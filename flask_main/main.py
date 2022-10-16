# Author: Yee Chuen Teoh
# title: Main flask file
# description:

# Imports
from flask import Flask, redirect, url_for, render_template, request
import pandas as pd
import plotly.express as px


# dataframes for csv files
rooms_df = pd.read_csv("../Rooms.csv")
devices_df = pd.read_csv("../Devices.csv")
datalog_df = pd.read_csv("../DataLog.csv")


# list of room names and is
# indexes in both list refers to the same room
rooms = rooms_df['room_name']
roomslist = rooms.values.tolist()
rooms_ids = rooms_df['room_id']
rooms_idlist = rooms_ids.values.tolist()
size = len(roomslist)


# 1. DONE: Creating endpoints (GET, POST) adding new devices, new rooms
# 2. DONE: Creating Flask Routes for endpoint

app = Flask(__name__)

# --- 5 main pages --- 
# homepage
# popup for creating new room
# roompage
# popup for creting new device
# devicepage 


size = len(roomslist)
@app.route("/")
@app.route("/<display_type>/<unit>/<time>")
def home(display_type="room", unit="kw", time="last-year"):
    
    # Assumes that the latest record is 2021-12-31, which is true for our dataset
    time_interval = {
        "last-day": '2021-12-30',
        "last-week": '2021-12-25',
        "last-month": '2021-12-01',
        "last-year": '2021-01-01' 
    }
    oldest_time = time_interval[time]
    
    color = "room_name" if display_type == "room" else "device_type"
    
    fig = px.line(pd.merge(pd.merge(datalog_df[datalog_df.timestamp >= oldest_time], 
                                    devices_df, on='device_id', how='left'), rooms_df, on='room_id', 
                           how='left').groupby(['timestamp', 'device_type', 'room_name'])["device_kwh"].sum().reset_index(name='device_kwh'), 
                  x="timestamp", y="device_kwh", color=color)
    return render_template("index.html", fig=fig.to_html(full_html=False), display_type=display_type, unit=unit, time=time, size=size, room_id=rooms_idlist,room_list=roomslist)


# # below need to get some parameter to know which room to go
@app.route("/room/<room_id>/")
def roompage(room_id):
    # TODO: check the html page name
    # TODO: check the header variable name
    # TODO: potentially pass the graph information& list of devices
    room_name = roomslist[int(room_id)-1]

    # get all devices from this room
    choosen_room = "room_id == "+(room_id)
    devices_in_room = devices_df.query(choosen_room)

    # TODO: names of device type changes based on Yiheng's csv
    # all device in device_type lights  
    lights_in_room = devices_in_room.query('device_type == "lights"')
    lightsdevices = lights_in_room['device_name']
    lightdeviceslist = lightsdevices.values.tolist()

    # all device in device_type temperature  
    temperature_in_room = devices_in_room.query('device_type == "temperature"')
    temperaturedevices = temperature_in_room['device_name']
    temperaturedeviceslist = temperaturedevices.values.tolist()
    
    # all device in device_type appliances  
    appliances_in_room = devices_in_room.query('device_type == "appliances"')
    appliancesdevices = appliances_in_room['device_name']
    appliancesdeviceslist = appliancesdevices.values.tolist()
    
    # all device in device_type security  
    security_in_room = devices_in_room.query('device_type == "security"')
    securitydevices = security_in_room['device_name']
    securitydeviceslist = securitydevices.values.tolist()

    # filter the dataframe to get all the devices
    # df_devices = rooms_df.filter()

    
    # filter the dataframe devices unit categories
    '''df_statistics = rooms_df.filter()'''

    return render_template("room.html", Rooms=room_name, light_list=lightdeviceslist, temperature_list=temperaturedeviceslist, appliance_list=appliancesdeviceslist, security_list=securitydeviceslist, room_list=roomslist)

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
        return redirect(url_for("device.html", device_name = device_name))
    else:
        # TODO: check the html page name
        # TODO ? : pass a list of available room for the dropdown options
        return render_template("newdevice.html")


@app.route("/d=<device_name>")
def devicepage(device_name):
    # TODO: check the html page name
    # TODO: check the header variable name
    # TODO ? : potentially pass the graph & list of devices information

    return render_template("device.html", device_name=device_name)


if __name__ == "__main__":
    app.run(debug = True)
