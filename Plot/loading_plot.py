import numpy as np
import matplotlib.pyplot as plt

#cases = ["Max RSSI-AP142", "MAx RSSI-AP204", "Baseline-AP142", "Baseline-AP204", "Proposal-AP142", "Proposal-AP204"]
cases = ["Max RSSI", "Baseline", "DAW", "Proposed"]

STAs = ["MAC1", "MAC2", "ASUS1", "ASUS2", "RAS1", "RAS2"]
groups = [[0, 0, 0, 0, 1, 0],
          [1, 0, 0, 0, 1, 0],
          [1, 1, 0, 0, 1, 0],
          [0, 0, 1, 0, 1, 0]]

effective_bitrate = [[76.329, 68.397, 29.630, 30.312, 28.912, 29.761],
                     [71.815, 60.465, 30.611, 30.629, 29.092, 29.752],
                     [69.469, 69.023, 32.002, 30.898, 29.420, 29.674], 
                     [72.372, 74.824, 29.843, 30.932, 29.480, 29.761]]

traffic_requirement = [5, 5, 10, 5, 3, 3]
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
