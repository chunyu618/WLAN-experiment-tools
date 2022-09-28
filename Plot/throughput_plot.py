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

# Throughput of every station for every method
throughput = [[4.988, 4.756, 2.729, 2.788, 2.977, 2.612], 
              [4.993, 4.159, 4.194, 4.142, 2.982, 2.929], 
              [4.96, 4.945, 6.673, 4.992, 2.983, 2.981],
              [4.987, 4.936, 9.518, 4.978, 2.984, 2.954]]

throughput = np.transpose(throughput)
groups = np.transpose(groups)
colors = ['tab:red', 'skyblue', 'tab:green', 'rebeccapurple', 'tab:brown', 'slategray']
#colors = ['#ed6a5a', '#f0a202', '#58a4b0', 'lime', 'cyan', 'slategray', 'navy', 'slateblue']
throughput_142 = []
throughput_204 = []

for i in range(len(throughput)):
    curr_142 = []
    curr_204 = []
    for j in range(len(throughput[i])):
        curr_142.append((1 - groups[i][j]) * throughput[i][j])
        curr_204.append(groups[i][j] * throughput[i][j])

    throughput_142.append(curr_142)
    throughput_204.append(curr_204)

x = np.arange(len(throughput[0]))
accum_142 = np.zeros(len(throughput[0]))
accum_204 = np.zeros(len(throughput[0]))
bar_width = 0.3
shift = 0.2


# Plot bar
for i in range(0, len(throughput_142)):
    plt.bar(x - shift, throughput_142[i], width=bar_width, color=colors[i], bottom=accum_142, label=STAs[i], edgecolor='black', linewidth=0.5)
    for j in range(len(throughput_142[i])):
        if throughput_142[i][j] > 0:
            plt.text(x[j] - shift, accum_142[j] + throughput_142[i][j]/2 , round(throughput_142[i][j], 2), ha = 'center', fontsize=8)
    accum_142 += throughput_142[i]
    
    plt.bar(x + shift, throughput_204[i], width=bar_width, color=colors[i], bottom=accum_204, edgecolor='black', linewidth=0.5)
    for j in range(len(throughput_204[i])):
        if throughput_204[i][j] > 0:
            plt.text(x[j] + shift, accum_204[j] + throughput_204[i][j]/2 , round(throughput_204[i][j], 2), ha = 'center', fontsize=8)
    accum_204 += throughput_204[i]

print(accum_142)
print(throughput_142)
for i in range(len(accum_142)):
    plt.text(x[i] - shift, accum_142[i] + 0.2, "AP142:\n%.2f" % round(accum_142[i], 2), ha='center', fontsize=8)
    plt.text(x[i] + shift, accum_204[i] + 0.2, "AP204:\n%.2f" % round(accum_204[i], 2), ha='center', fontsize=8)

# Set Title, ticks, and labels
ax = plt.gca()
ax.set_ylim([0, 21])
#plt.title('Average Throughput of 2 APs', fontsize=15)
plt.xticks(x, cases, fontsize = 12)
#plt.yticks(fontsize=12)
#plt.xlabel("Metheds", fontsize=12)
plt.ylabel("Throughput (Mbps)", fontsize=12)
plt.legend(bbox_to_anchor=(1.05,1), loc='upper center', fontsize=8)

#plt.show()
png_filename = 'Throughput-separately'
plt.savefig("./Figures/" + png_filename + ".png", dpi=600, bbox_inches='tight')
