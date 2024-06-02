import matplotlib.pyplot as plt
import os.path
import sys
import numpy as np

_challenge = "0"
for arg in sys.argv:
    if arg.startswith("world="):
        _challenge = str(int(arg.split("world=")[1])) #ensures also it is int

syslists = []
scoresAll = {}
for index in range(1,101):
    F = f"run_world{_challenge}_{index}.run"
    if not os.path.exists(F):
        break
    with open(F) as f:
        lines = f.read().split("\n")
    syslist = []
    for line in lines:
        if " " in line:
            idx = int(line.split(" ")[0])
            if idx not in scoresAll:
                scoresAll[idx] = []
            value = float(line.split(" ")[1])
            scoresAll[idx].append(value)
            syslist.append(value)
    syslists.append(syslist)

scores = []
for key in scoresAll:
    #if key > 5:
    #    continue
    V = 0
    for v in scoresAll[key]:
        V += v
    V /= len(scoresAll[key])
    scores.append(V)

worldstr = "MiniGrid-DoorKey-8x8-v0"
if "10" == _challenge:
    worldstr = "MiniGrid-Empty-8x8-v0"
if "11" == _challenge:
    worldstr = "BabyAI-GoToRedBallNoDists-v0"
if "12" == _challenge:
    worldstr = "MiniGrid-DistShift2-v0"
if "13" == _challenge:
    worldstr = "MiniGrid-LavaGapS7-v0"
if "14" == _challenge:
    worldstr = "MiniGrid-SimpleCrossingS11N5-v0"
if "15" == _challenge:
    worldstr = "MiniGrid-LavaCrossingS11N5-v0"
if "16" == _challenge:
    worldstr = "MiniGrid-Unlock-v0"
if "17" == _challenge:
    worldstr = "MiniGrid-DoorKey-8x8-v0"
if "18" == _challenge:
    worldstr = "MiniGrid-UnlockPickup-v0"
if "19" == _challenge:
    worldstr = "MiniGrid-BlockedUnlockPickup-v0"

# Plotting the average with standard deviation shading
plt.plot(scores, color="green", label="NARS Avg.")
if len(syslists) > 1:
    plt.fill_between(
        range(len(scores)),
        scores - np.std(syslists, axis=0),
        scores + np.std(syslists, axis=0),
        color="green",
        alpha=0.1,
    )


# Adding title and labels
plt.title(f'Avg. reward over episodes ({worldstr})')
plt.xlabel('Episode')
plt.ylabel('Avg. reward')

# Display the plot
plt.grid(True)
plt.show()
