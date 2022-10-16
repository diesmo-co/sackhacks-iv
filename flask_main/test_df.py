# testing zone
'''
graph in devices
select all power of a specific device (example. kWh of device 1 in all rooms)
select all duration of a specific device (example. duration of device 1 in all rooms)

graph in rooms
select all power of a specific room (example. kWh of all device in room 1)
select all duration of a specific room (example. duration of all device in room 1)

graph in homepage
select all power by different room
select all duration by different room
select all power by different device type
select all duration by different device type
'''

import pandas as pd

rooms_df = pd.read_csv("Rooms.csv")
devices_df = pd.read_csv("Devices.csv")
datalog_df = pd.read_csv("DataLog.csv")

print(devices_df)

print("----------------------- basic ---------------------------")
# below do join operation like SQL
# df_test join both table on key "device_id"
df_test = datalog_df.merge(devices_df, on='device_id')
print(df_test)

print("----------------------- basic ---------------------------")
# show devices
# df_test2 only have devices in room_id == 1
df_test2 = devices_df.query("(room_id == 1)")
print(df_test2)

print("----------------------- basic ---------------------------")
# devices is df with only device_name
devices = df_test2['device_name']
print(devices)

print("----------------- TRY BY CATEGORY 1-----------------")
# df here only contain power/duration information on specific device
df_test3 = datalog_df.merge(devices_df, on='device_id')
df_test4 = df_test3.query("(device_id == 1)")
print(df_test4)

print("----------------- TRY BY CATEGORY 2-----------------")
# df here only contain power/duration information on all device on a specific room
df_test2 = devices_df.query("(room_id == 1)")
df_test5 = datalog_df.merge(df_test2, on='device_id')
print(df_test5)

print("----------------- TRY BY CATEGORY 3-----------------")
# df here only contain power/duration information on all device on a specific room
df_test6 = datalog_df.merge(devices_df, on='device_id')
df_test7 = df_test6.merge(rooms_df, on='room_id')
print(df_test7)


print("----------------- get room name in list -----------------")
rooms = rooms_df['room_name']
roomslist = rooms.values.tolist()
print(roomslist)


print("----------------- get device name in list in specific room -----------------")


rooms_ids = rooms_df['room_id']
rooms_idlist = rooms_ids.values.tolist()
choose_room = str(rooms_idlist[0])
choosen_room = "room_id == "+choose_room
devices_in_room = devices_df.query(choosen_room)

print(devices_df)

lights_in_room = devices_df.query('device_type == "lights"')
lightsdevices = lights_in_room['device_name']
lightdeviceslist = lightsdevices.values.tolist()
print(lightdeviceslist)

    # all device in device_type temperature  
temperature_in_room = devices_df.query('device_type == "temperature"')
temperaturedevices = temperature_in_room['device_name']
temperaturedeviceslist = temperaturedevices.values.tolist()
print(temperaturedeviceslist)
    
    # all device in device_type appliances  
appliances_in_room = devices_df.query('device_type == "appliances"')
appliancesdevices = appliances_in_room['device_name']
appliancesdeviceslist = appliancesdevices.values.tolist()
print(appliancesdeviceslist)
    
    # all device in device_type security  
security_in_room = devices_df.query('device_type == "security"')
securitydevices = security_in_room['device_name']
securitydeviceslist = securitydevices.values.tolist()
print(securitydeviceslist)


devices = devices_in_room['device_name']
deviceslist = devices.values.tolist()
print(devices)