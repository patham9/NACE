import matplotlib.pyplot as plt
import os.path
import sys
import numpy as np

_challenge = "0"
for arg in sys.argv:
    if arg.startswith("world="):
        _challenge = str(int(arg.split("world=")[1])) #ensures also it is int

rewardValuesOfIndex = dict([])
lenValuesOfIndex = dict([])
def AppendToDict(D, K, V):
    if K not in D:
        D[K] = []
    D[K].append(V)

indices = []
rewardlists = []
lenlists = []
rewardAll = {}
lenAll = {}
for index in range(1,101):
    F = f"run_world{_challenge}_{index}.run"
    if not os.path.exists(F):
        break
    with open(F) as f:
        lines = f.read().split("\n")
    rewardlist = []
    lenlist = []
    for line in lines:
        if " " in line:
            idx = int(line.split(" ")[1].split("=")[1])
            if idx not in rewardAll:
                rewardAll[idx] = []
                lenAll[idx] = []
            if idx not in indices:
                indices.append(idx)
            rewardvalue = float(line.split(" ")[3].split("=")[1])
            if "noclip" not in sys.argv:
                rewardvalue = max(0.0, rewardvalue)
            lenvalue = float(line.split(" ")[2].split("=")[1])
            rewardAll[idx].append(rewardvalue)
            rewardlist.append(rewardvalue)
            AppendToDict(rewardValuesOfIndex, idx, rewardvalue)
            lenAll[idx].append(lenvalue)
            lenlist.append(lenvalue)
            AppendToDict(lenValuesOfIndex, idx, lenvalue)
    rewardlists.append(rewardlist)
    lenlists.append(lenlist)

rewardsAvgOfIndex = dict([])
lensAvgOfIndex = dict([])
rewards = []
lens = []
for key in rewardAll:
    #if key > 5:
    #    continue
    V = 0
    for v in rewardAll[key]:
        V += v
    V /= len(rewardAll[key])
    rewardsAvgOfIndex[key] = V
    rewards.append(V)
    V = 0
    for v in lenAll[key]:
        V += v
    V /= len(lenAll[key])
    lensAvgOfIndex[key] = V
    lens.append(V)

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
if "30" == _challenge:
    worldstr = "MiniGrid-Empty-6x6-v0"
if "31" == _challenge:
    worldstr = "MiniGrid-Empty-8x8-v0"
if "32" == _challenge:
    worldstr = "MiniGrid-Empty-16x16-v0"
if "33" == _challenge:
    worldstr = "MiniGrid-Empty-Random-5x5-v0"
if "34" == _challenge:
    worldstr = "MiniGrid-Empty-Random-6x6-v0"
if "35" == _challenge:
    worldstr = "MiniGrid-FourRooms-v0"
if "36" == _challenge:
    worldstr = "MiniGrid-MultiRoom-N6-v0"

def genplot(rewards, rewardlists, name):
    # Plotting the average with standard deviation shading
    plt.xlim(1,5)
    plt.plot([0]+rewards, color="green", label="NARS Avg.")
    if len(rewardlists) > 1:
        plt.fill_between(
            range(1,1+len(rewards)),
            rewards - np.std(rewardlists, axis=0),
            rewards + np.std(rewardlists, axis=0),
            color="green",
            alpha=0.1,
        )
    # Adding title and labels
    plt.title(f'Avg. {name} over timesteps ({worldstr})')
    plt.xlabel('Timesteps/100')
    plt.ylabel(f'Avg. {name}')
    # Display the plot
    plt.grid(True)
    plt.show()

if "noplot" not in sys.argv:
    genplot(rewards, rewardlists, "reward")
    genplot(lens, lenlists, "episode length")

if "nocsv" not in sys.argv:
    with open(f"{worldstr}_NACE.csv", "w") as f:
        f.write("Timesteps,Mean Episode Reward,Standard Deviation of Episode Reward,Mean Episode Length,Standard Deviation of Episode Length\n")
        #if "boilerplate" in sys.argv: #no need
        #    f.write(f"{0}, {0}, {0}, {500}, {0}\n")
        #    f.write(f"{1}, {0}, {0}, {500}, {0}\n")
        timestepslast = 0
        for timesteps in indices:
            timestepslast = timesteps
            f.write(f"{timesteps}, {rewardsAvgOfIndex[timesteps]}, {np.std(rewardValuesOfIndex[timesteps])}, {lensAvgOfIndex[timesteps]}, {np.std(lenValuesOfIndex[timesteps])}\n")
        if "boilerplate" in sys.argv:
            timestepslastlast = 10000000 
            #f.write(f"{timestepslastlast}, {rewardsAvgOfIndex[timestepslast]}, {np.std(rewardValuesOfIndex[timestepslast])}, {lensAvgOfIndex[timestepslast]}, {np.std(lenValuesOfIndex[timestepslast])}\n")
            for timestepslastlast in range(timestepslast, 10000000, 100):
                f.write(f"{timestepslastlast}, {rewardsAvgOfIndex[timestepslast]}, {np.std(rewardValuesOfIndex[timestepslast])}, {lensAvgOfIndex[timestepslast]}, {np.std(lenValuesOfIndex[timestepslast])}\n")
                
