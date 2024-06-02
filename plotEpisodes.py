import matplotlib.pyplot as plt
import os.path
import sys

worldn = 0
for arg in sys.argv:
    if arg.startswith("world="):
        worldn = int(arg.split("world=")[1])

lines = []
scoresAll = {}
for index in range(1,101):
    F = f"run_world{worldn}_{index}.run"
    if not os.path.exists(F):
        break
    with open(F) as f:
        lines = f.read().split("\n")
    for line in lines:
        if " " in line:
            idx = int(line.split(" ")[0])
            if idx not in scoresAll:
                scoresAll[idx] = []
            scoresAll[idx].append(float(line.split(" ")[1]))

scores = []
for key in scoresAll:
    #if key > 5:
    #    continue
    V = 0
    for v in scoresAll[key]:
        V += v
    V /= len(scoresAll[key])
    scores.append(V)


# Define the list of values
L = scores

# Plot the list of values
plt.plot(L, marker='o')

# Adding title and labels
plt.title('Avg. reward over episodes (MiniGrid-UnlockPickup-v0)')
plt.xlabel('Episode')
plt.ylabel('Avg. reward')

# Display the plot
plt.grid(True)
plt.show()
