run_names = ["shock_run", "shock_rand"]
files = dict([])
for run_name in run_names:
    for i in range(1,10+1):
        if run_name not in files:
            files[run_name] = []
        files[run_name].append(run_name + str(i) + ".txt")

syslists = dict([])
for run_name in run_names:
    for name in files[run_name]:
        with open(name) as f:
            content = f.read()
        t=0
        scores = []
        for line in content.split("\n"):
            if "World t=" in line:
                t=line.split("World t=")[1].split(" ")[0]
            if line.startswith("score="):
                score = line.split("score=")[1].split(",")[0]
                scores.append(int(score))
        print(score, scores)
        if run_name not in syslists:
            syslists[run_name] = []
        syslists[run_name] += [scores]

import ast
import numpy as np
import matplotlib.pyplot as plt

total = dict([])
syslistsavg = dict([])
for run_name in run_names:
    total[run_name] = 0
    syslistsavg[run_name] = [0 for i in range(len(syslists[run_name][0]))]
    for syslist in syslists[run_name]:
        for i,x in enumerate(syslist):
            syslistsavg[run_name][i] += x
        total[run_name]+=1
    for i,x in enumerate(syslistsavg[run_name]):
        syslistsavg[run_name][i] /= total[run_name]
    syslistsavg[run_name] = np.array(syslistsavg[run_name])

# to check if syslists is a 2D array where all inner lists are of same length
try:
    for run_name in run_names:
        arr = np.array(syslists[run_name])
        print(arr.shape) # should output (m, 300) where m is number of lists in syslists
except ValueError as e:
    print(f"syslists is not a 2D list with inner lists of equal length. Error: {e}")

# Plotting the average with standard deviation shading
for i, run_name in enumerate(run_names):
    colors=["green", "red"]
    names = ["NACE Avg.", "Random Avg."]
    plt.plot(syslistsavg[run_name], color=colors[i], label=names[i])
    plt.fill_between(
        range(len(syslistsavg[run_name])),
        syslistsavg[run_name] - np.std(syslists[run_name], axis=0),
        syslistsavg[run_name] + np.std(syslists[run_name], axis=0),
        color=colors[i],
        alpha=0.1,
    )

# Adding labels and a legend
plt.xlabel('Time')
plt.ylabel('Scores')
plt.legend()

# Display the plot
plt.show()
