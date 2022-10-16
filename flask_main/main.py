# Author: Yee Chuen Teoh
# title: Main flask file
# description:

# Imports
from ctypes import sizeof
from flask import Flask, redirect, url_for, render_template, request
import pandas as pd
import plotly.express as px
import csv


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

# list for devices
device_ids = devices_df['device_id']
device_idslist = device_ids.values.tolist()


# 1. DONE: Creating endpoints (GET, POST) adding new devices, new rooms
# 2. DONE: Creating Flask Routes for endpoint

app = Flask(__name__)

# --- 5 main pages --- 
# homepage
# popup for creating new room
# roompage
# popup for creting new device
# devicepage 


@app.route("/", methods = ["POST","GET"])
@app.route("/<display_type>/<unit>/<time>", methods = ["POST","GET"])
def home(display_type="room", unit="kw", time="last-day"):
    
    if request.method == "POST":
        newroom = request.form["roomname"]
        newid = int(rooms_idlist[size-1])+1

        # TODO: create the new room in csv
        # create the csv writer
        with open('../Rooms.csv','a') as f:
            f.write(str(newid)+","+newroom)
            f.write("\n")
        # write a row to the csv file
        # close the file
        f.close()      

        return redirect(url_for("updateload"))

    else:
        time_interval = {
            "last-day": '2021-12-30',
            "last-week": '2021-12-25',
            "last-month": '2021-12-01',
            "last-year": '2021-01-01' 
        }
        oldest_time = time_interval[time]
        
        color = "room_name" if display_type == "room" else "device_type"
        
        line_chart = px.line(pd.merge(pd.merge(datalog_df[datalog_df.timestamp >= oldest_time], 
                                        devices_df, on='device_id', how='left'), rooms_df, on='room_id', 
                            how='left').groupby(['timestamp', 'device_type', 'room_name'])["device_kwh"].sum().reset_index(name='device_kwh'), 
                    x="timestamp", y="device_kwh", color=color)
        
        pie_chart = px.pie(pd.merge(pd.merge(datalog_df[datalog_df.timestamp >= oldest_time], 
                                        devices_df, on='device_id', how='left'), rooms_df, on='room_id', 
                            how='left').groupby([color])["device_kwh"].sum().reset_index(name='device_kwh'), values='device_kwh', names=color) 
        return render_template("index.html", pie_chart=pie_chart.to_html(full_html=False), line_chart=line_chart.to_html(full_html=False), display_type=display_type, unit=unit, time=time, size=size, room_id=rooms_idlist,room_list=roomslist)
    
@app.route("/load")
def updateload():
    global rooms_df
    global rooms
    global roomslist
    global rooms_ids
    global rooms_idlist
    global size
    rooms_df = pd.read_csv("../Rooms.csv")
    rooms = rooms_df['room_name']
    roomslist = rooms.values.tolist()
    rooms_ids = rooms_df['room_id']
    rooms_idlist = rooms_ids.values.tolist()
    size = len(roomslist)
    id=rooms_idlist[len(rooms_idlist)-1]

    return redirect(url_for("roompage", room_id=str(id)))

# below need to get some parameter to know which room to go
@app.route("/room/<room_id>/", methods = ["POST","GET"])
@app.route("/room/<room_id>/<time>", methods = ["POST","GET"])
def roompage(room_id, time="last-day"):
    if request.method == "POST":
        newdevice_id = int(device_idslist[len(device_idslist)-1])+1
        newdevice_name = request.form["devicename"]
        newdevice_roomid = request.form["roomid"]
        newdevice_roomid = int(request.form["roomid"])
        newdevice_type = request.form["device_type"]
        newdevice_power = request.form["devicepower"]

        # TODO: create the new room in csv
        # create the csv writer
        with open('../Devices.csv','a') as f:
            f.write(str(newdevice_id)+","+newdevice_name+","+str(newdevice_roomid)+","+newdevice_type+","+newdevice_power)
            f.write("\n")
        # write a row to the csv file
        # close the file
        f.close()   

        
        global devices_df
        devices_df = pd.read_csv("../Devices.csv")
        # TODO: IMPLEMENT THE PARAMETER PASSING
        return redirect(url_for("devicepage", device_id=str(newdevice_id)))

    else:
        room_name = roomslist[int(room_id)-1]

        # get all devices from this room
        choosen_room = "room_id == "+(room_id)
        devices_in_room = devices_df.query(choosen_room)
        
        time_interval = {
            "last-day": '2021-12-30',
            "last-week": '2021-12-25',
            "last-month": '2021-12-01',
            "last-year": '2021-01-01' 
        }
        oldest_time = time_interval[time]
        line_chart = px.line(pd.merge(pd.merge(datalog_df[datalog_df.timestamp >= oldest_time], 
                                        devices_in_room, on='device_id', how='left'), rooms_df, on='room_id', 
                            how='left').groupby(['timestamp', 'device_type', 'room_name'])["device_kwh"].sum().reset_index(name='device_kwh'), 
                    x="timestamp", y="device_kwh", color='device_type')
         

        # all device in device_type lights  
        lights_in_room = devices_in_room.query('device_type == "lights"')
        lightsdevices = lights_in_room['device_name']
        lightsdevices_id = lights_in_room['device_id']
        lightdeviceslist_id = lightsdevices_id.values.tolist()
        lightdeviceslist = lightsdevices.values.tolist()

        # all device in device_type temperature  
        temperature_in_room = devices_in_room.query('device_type == "temperature"')
        temperaturedevices = temperature_in_room['device_name']
        temperaturedevices_id = temperature_in_room['device_id']
        temperaturedeviceslist_id = temperaturedevices_id.values.tolist()
        temperaturedeviceslist = temperaturedevices.values.tolist()
        
        # all device in device_type appliances  
        appliances_in_room = devices_in_room.query('device_type == "appliances"')
        appliancesdevices = appliances_in_room['device_name']
        appliancesdevices_id = appliances_in_room['device_id']
        appliancesdeviceslist_id = appliancesdevices_id.values.tolist()
        appliancesdeviceslist = appliancesdevices.values.tolist()
        
        # all device in device_type security  
        security_in_room = devices_in_room.query('device_type == "security"')
        securitydevices = security_in_room['device_name']
        securitydevices_id = security_in_room['device_id']
        securitydeviceslist_id = securitydevices_id.values.tolist()
        securitydeviceslist = securitydevices.values.tolist()

        lightsize = len(lightdeviceslist)
        tempsize = len(temperaturedeviceslist)
        appsize = len(appliancesdeviceslist)
        sersize = len(securitydeviceslist)

        return render_template("room.html", line_chart=line_chart.to_html(full_html=False), room_list=roomslist, roomsize=size,
        light_list=lightdeviceslist, light_id=lightdeviceslist_id, lsize=lightsize,
        temperature_list=temperaturedeviceslist, temp_id=temperaturedeviceslist_id, tsize=tempsize,
        appliance_list=appliancesdeviceslist, app_id=appliancesdeviceslist_id, asize=appsize,
        security_list=securitydeviceslist, ser_id=securitydeviceslist_id, ssize=sersize,
        room_ids=rooms_idlist, room_id=room_id, time=time)

@app.route("/d=<device_id>", methods = ["POST","GET"])
def devicepage(device_id):
    if request.method == "POST":
        global devices_df
        newdevice_name = request.form["device_name"]
        newdevice_room = request.form["roomid"]
        newdevice_type = request.form["device_type"]
        newdevice_power = request.form["device_power"]
        
        idx = int(device_id)
        # updating the column value/data
        #if newdevice_name:
        devices_df.loc[idx, 'device_name'] = newdevice_name
        #if newdevice_room:
        devices_df.loc[idx, 'room_id'] = newdevice_room
        #if newdevice_type:
        devices_df.loc[idx, 'device_type'] = newdevice_type
        #if newdevice_power:
        devices_df.loc[idx, 'device_kwh'] = newdevice_power
        # writing into the file
        devices_df.to_csv("../Devices.csv", index=False)
        
        devices_df = pd.read_csv("../Devices.csv")

        return render_template("device.html", device_id=device_id, roomsize=int(size), room_name=roomslist, room_id=rooms_idlist)
        
    else:
        return render_template("device.html", device_id=device_id, roomsize=int(size), room_name=roomslist, room_id=rooms_idlist)


if __name__ == "__main__":
    app.run(debug = True)
