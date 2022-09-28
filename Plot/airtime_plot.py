import numpy as np
import matplotlib.pyplot as plt

# Method
cases = ["Max RSSI", "Baseline", "DAW", "Proposed"]

# List of station
STAs = ["MAC1", "MAC2", "ASUS1", "ASUS2", "RAS1", "RAS2"]

# Association for every method, 0 for AP142 and 1 for AP204
groups = [[0, 0, 0, 0, 1, 0],
          [1, 0, 0, 0, 1, 0],
          [1, 1, 0, 0, 1, 0],
          [0, 0, 1, 0, 1, 0]]

# Airtime per 500ms of each station for every method
airtime = [[56.169, 61.207, 75.575, 75.594, 96.227, 75.681],
           [59.538, 72.948, 107.003, 107.028, 94.002, 84.104],
           [75.016, 74.400, 159.762, 127.960, 89.227, 85.540], 
           [62.602, 58.997, 236.262, 123.736, 87.480, 84.732]]

data = np.transpose(airtime) * 2
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
            plt.text(x[j] - shift, accum_142[j] + data_142[i][j]//2 , round(data_142[i][j]), ha = 'center', fontsize=8)
    accum_142 += data_142[i]
    
    plt.bar(x + shift, data_204[i], width=bar_width, color=colors[i], bottom=accum_204, edgecolor='black', linewidth=0.5)
    for j in range(len(data_204[i])):
        if data_204[i][j] > 0:
            plt.text(x[j] + shift, accum_204[j] + data_204[i][j]//2 , round(data_204[i][j]), ha = 'center', fontsize=8)
    accum_204 += data_204[i]

print(accum_142)
print(data_142)
for i in range(len(accum_142)):
    plt.text(x[i] - shift, accum_142[i] + 10, "AP142:\n%d" % round(accum_142[i]), ha='center', fontsize=8)
    plt.text(x[i] + shift, accum_204[i] + 10, "AP204:\n%d" % round(accum_204[i]), ha='center', fontsize=8)

# Set Title, ticks, and labels
ax = plt.gca()
ax.set_ylim([0, 850])
#plt.title('Average Airtime Usage per Second of 2 APs', fontsize=15)
plt.xticks(x, cases, fontsize = 12)
#plt.yticks(fontsize=15)
#plt.xlabel("Metheds", fontsize=12)
plt.ylabel("Airtime (ms)", fontsize=12)
plt.legend(bbox_to_anchor=(1.05,1), loc='upper center', fontsize=8)

#plt.show()
png_filename = 'Airtime-separately'
plt.savefig("./Figures/" + png_filename + ".png", dpi=600, bbox_inches='tight')
