import os, sys

#Loose-coupled interface with nartech_ws (no ROS Python dependency here)
#Ensure to run python3 /home/nartech/nartech_ws/src/nartech_ros/channels/grid.py first in the background

def rosgrid_perceive():
    global location
    with open("/home/nartech/nartech_ws/src/nartech_ros/channels/grid.txt","r") as f:
        w_h_newdata = f.read()
    data_valid = True
    width, height, agx, agy, data = (0,0,0,0,0)
    try:
        lines = w_h_newdata.split("\n")
        width = int(lines[0])
        height = int(lines[1])
        agx = int(lines[2])
        agy = int(lines[3])
        data = eval(lines[4])
        location = (agx, agy)
    except:
        data_valid = False
    return data_valid, width, height, agx, agy, data

def rosgrid_act(action):
    #flip up and down as the grids are inverted
    if action == "up":
        action = "down"
    elif action == "down":
        action = "up"
    #send command
    os.system("python3 ~/nartech_ws/src/nartech_ros/channels/move.py " + action)

#reversed mapping from M in grid.py
M = {100: 'o', 127: 'x', -126: 'T', -125: "u", -124: 'w'}

def rosgrid_toNACE(value):
    return M.get(value, ' ')
