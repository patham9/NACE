run_name = "soccer_run"
files = []
for i in range(1,10+1):
    files.append(run_name + str(i) + ".txt")

syslists = []
for name in files:
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
    syslists += [scores]

import ast
import numpy as np
import matplotlib.pyplot as plt

total = 0
syslistsavg = [0 for i in range(len(syslists[0]))]
for syslist in syslists:
    for i,x in enumerate(syslist):
        syslistsavg[i] += x
    total+=1

for i,x in enumerate(syslistsavg):
    syslistsavg[i] /= total

syslistsavg = np.array(syslistsavg)

# to check if syslists is a 2D array where all inner lists are of same length
try:
    arr = np.array(syslists)
    print(arr.shape) # should output (m, 300) where m is number of lists in syslists
except ValueError as e:
    print(f"syslists is not a 2D list with inner lists of equal length. Error: {e}")

# Plotting the average with standard deviation shading
plt.plot(syslistsavg, color="green", label="NACE Avg.")
plt.fill_between(
    range(len(syslistsavg)),
    syslistsavg - np.std(syslists, axis=0),
    syslistsavg + np.std(syslists, axis=0),
    color="green",
    alpha=0.1,
)

# Adding labels and a legend
plt.xlabel('Time')
plt.ylabel('Scores')
plt.legend()

# Display the plot
plt.show()
