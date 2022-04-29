import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter, NullFormatter
import seaborn as sns
sns.set()

normal = [0,24,51,95]
mtcp = [3, 75, 78, 79]
connections = ["Base","1","10","25"]

fig, ax = plt.subplots()
x_pos = [i for i,_ in enumerate(connections)]
normal=np.array(normal)
mtcp=np.array(mtcp)
x_pos=np.array(x_pos)
width = 0.35
plt.plot(x_pos, normal, color='black', marker="*", ls ="--", zorder=10, label="Linux Stack")
plt.plot(x_pos+width, mtcp, color='black', marker="^", ls="--", zorder=10, label="mTCP")
plt.bar(x_pos, normal,width,color='cornflowerblue', label = "Linux Stack")
plt.bar(x_pos+width, mtcp,width ,color='coral', label="mTCP")
plt.xlabel("Number of Connections")
plt.ylabel("CPU Usage(%)")
ax.set_ylim([0,100])
plt.setp(ax.patches, linewidth=0)
ax.xaxis.grid(False)
plt.legend(loc = 0)
plt.xticks(x_pos + width/2, connections)
plt.savefig("cpu.png")
plt.close()


