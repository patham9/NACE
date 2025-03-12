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

def rosgrid_act(action, plan = None, max_planlen = None):
    actionname = action.__name__
    oldlen = len(plan)
    if not max_planlen is None:
        plan = plan[:max_planlen]
    newlen = len(plan)
    if plan and len(plan) > 1 and "atomicaction" not in sys.argv:
        truncateplan = plan #plan[:-1] if newlen == oldlen else plan
        actionname = ",".join([a.__name__ for a in truncateplan]) #plan[:-1] if the last action should be omitted
    #send command
    #start_time = time.time()
    os.system("python3 ~/nartech_ws/src/nartech_ros/optional/move.py " + actionname)
    #elapsed_time = time.time() - start_time
    #remaining_time = max(0, 5 - elapsed_time)
    #stime.sleep(remaining_time)

#reversed mapping from M in grid.py
M = { 100: 'o',  #obstacle
      127: 'x',  #agent
     -126: 'T',  #table
     -125: "u",  #cup
     -124: 'w',  #human
     -120: 'T' } #chair

def rosgrid_toNACE(value):
    return M.get(value, ' ')
