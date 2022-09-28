import numpy as np
import matplotlib.pyplot as plt

# Method
cases = ["Max RSSI", "Baseline", "DAW", "Proposed"]

# List of station
STAs = ["MAC1", "ASUS1", "ASUS2"]

# Association for every method, 0 for AP142 and 1 for AP204
groups = [[0, 0, 0],
          [1, 0, 0],
          [1, 0, 0],
          [0, 1, 0]]

# Bitrate of each station of each method
bitrateList = [[77.496, 38.970, 38.886], 
               [61.863, 38.917, 38.965], 
               [74.702, 38.990, 38.229], 
               [77.953, 38.932, 38.986]]

# Retransmission ratio of each station of each method
retransmissionRatioList = [[0.046804, 0.255770, 0.253963], 
                           [0.091486, 0.208858, 0.196812], 
                           [0.069507, 0.202221, 0.228708], 
                           [0.001265, 0.256359, 0.170255]]


# Effective bitrate of each station for every method
effective_bitrate = []

for i in range(len(bitrateList)):
    tmp = []
    for j in range(len(bitrateList[i])):
        tmp.append(bitrateList[i][j] / (1 + retransmissionRatioList[i][j])) 
    effective_bitrate.append(tmp)

# Traffic demand of each station 
traffic_requirement = [10, 10, 10]
loading = []

for i in range(len(effective_bitrate)):
    curr = []
    for j in range(len(effective_bitrate[i])):
        curr.append(round(traffic_requirement[j] / effective_bitrate[i][j], 3))
    loading.append(curr)

data = np.transpose(loading)
groups = np.transpose(groups)
colors = ['tab:red', 'skyblue', 'tab:green', 'rebeccapurple', 'tab:brown', 'slategray']
#colors = ['#ed6a5a', '#f0a202', '#58a4b0', 'lime', 'cyan', 'slategray', 'navy', 'slateblue']
data_142 = []
data_204 = []

for i in range(len(data)):
    curr_142 = []
    curr_204 = []
    for j in range(len(data[i])):
        curr_142.append((1 - groups[i][j]) * data[i][j])
        curr_204.append(groups[i][j] * data[i][j])

    data_142.append(curr_142)
    data_204.append(curr_204)

x = np.arange(len(data[0]))
accum_142 = np.zeros(len(data[0]))
accum_204 = np.zeros(len(data[0]))
bar_width = 0.3
shift = 0.2

# Plot bar
for i in range(0, len(data_142)):
    plt.bar(x - shift, data_142[i], width=bar_width, color=colors[i], bottom=accum_142, label=STAs[i], edgecolor='black', linewidth=0.5)
    for j in range(len(data_142[i])):
        if data_142[i][j] > 0:
            plt.text(x[j] - shift, accum_142[j] + data_142[i][j]/2 , data_142[i][j], ha = 'center', fontsize=8)
    accum_142 += data_142[i]
    
    plt.bar(x + shift, data_204[i], width=bar_width, color=colors[i], bottom=accum_204, edgecolor='black', linewidth=0.5)
    for j in range(len(data_204[i])):
        if data_204[i][j] > 0:
            plt.text(x[j] + shift, accum_204[j] + data_204[i][j]/2 , data_204[i][j], ha = 'center', fontsize=8)
    accum_204 += data_204[i]

print(accum_142)
print(data_142)
for i in range(len(accum_142)):
    plt.text(x[i] - shift, accum_142[i] + 0.01, "AP142:\n%.3f" % round(accum_142[i], 3), ha='center', fontsize=8)
    plt.text(x[i] + shift, accum_204[i] + 0.01, "AP204:\n%.3f" % round(accum_204[i], 3), ha='center', fontsize=8)

# Set Title, ticks, and labels
ax = plt.gca()
ax.set_ylim([0, 1])
#plt.title('Load Distribution', fontsize=15)
plt.xticks(x, cases, fontsize = 12)
#plt.yticks(fontsize=12)
#plt.xlabel("Metheds", fontsize=12)
plt.ylabel("Load", fontsize=12)
plt.legend(bbox_to_anchor=(1.05,1), loc='upper center', fontsize=8)

#plt.show()
png_filename = 'Loading-separately'
plt.savefig("./Figures/" + png_filename + ".png", dpi=600, bbox_inches='tight')
