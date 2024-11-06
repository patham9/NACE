import os, time

#loose-coupling interface with nartech_ws
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
    os.system("python3 ~/nartech_ws/src/nartech_ros/channels/move.py " + action)
    time.sleep(10)

M = {100: 'o', 127: 'x'}
def rosgrid_toNACE(value):
    return M.get(value, ' ')
