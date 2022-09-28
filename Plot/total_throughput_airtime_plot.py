import numpy as np
import matplotlib.pyplot as plt

# Method
cases = ["Max RSSI", "Baseline", "DAW", "Proposed"]

# Throughput of each method
throughput = [20.85, 23.39, 27.534, 30.357]

# Airtime usage of each method
airtime = [688.452 + 192.454, 742.166 + 307.08, 746.524 + 477.286, 660.134 + 647.484]

x = np.arange(len(throughput))
bar_width = 0.3
shift = 0.2

fig, ax1 = plt.subplots()
# Plot throughput at (0, 0)
bar1 = ax1.bar(x - shift, throughput, width=bar_width, color='lightgray', edgecolor='black', linewidth=0.5, label='Throughput')
for i in range(len(x)):
    plt.text(x[i] - shift, throughput[i] + 0.3, round(throughput[i], 2), ha='center', fontsize=8)

ax2 = ax1.twinx()
bar2 = ax2.bar(x + shift, airtime, width=bar_width, color='dimgray', edgecolor='black', linewidth=0.5, label="Airtime Usage")
for i in range(len(x)):
    plt.text(x[i] + shift, airtime[i] + 10, round(airtime[i]), ha='center', fontsize=8)

# Set Title, ticks, and labels
ax1.set_ylim([0, 35])
ax1.set_ylabel("Throughput (Mbps)", fontsize=12)
ax2.set_ylabel("Airtime Usage (ms)", fontsize=12)
ax2.set_ylim([1, 1400])
ax1.set_xticks(x)
ax1.set_xticklabels(cases, fontsize=12)
#plt.legend(bbox_to_anchor=(1.02,1), loc='upper center', fontsize=8)
fig.legend()

#plt.show()
png_filename = 'Throughput-airtime-total'
plt.savefig("./Figures/" + png_filename + ".png", dpi=600, bbox_inches='tight')
