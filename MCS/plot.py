import sys
import matplotlib.pyplot as plt
import numpy as np

dist = ['-35 ~ -40 dBm', '-60 dBm', '-75 dBm']
colors = ['#ed6a5a', '#f0a202', '#58a4b0', 'lime', 'cyan', 'slategray', 'navy', 'slateblue']
MAC_address = ['F0:18:98:66:D9:9F', 'F4:06:16:85:95:86']
bit_rate = {}
freq = float(sys.argv[2])
duration = float(sys.argv[1])
alpha = 0.8
deli = '--------------------'

for i in range(3, len(sys.argv)):
    filename = sys.argv[i]
    with open(filename, 'r') as f:
        data = f.read().split(deli)[0 : -1]
        #print(len(data))
        for m in MAC_address:
            k = m + '_' + filename
            bit_rate[k] = {}
            bit_rate[k]['RX'] = []
            bit_rate[k]['TX'] = []
        
        cnt = 0
        for res in data:
            #print(cnt)
            cnt += 1
            res_list = res.split()
            #print(res_list)
            for m in MAC_address:
                k = m + '_' + filename
                if m in res_list:
                    mac_ind = res_list.index(m)
                    rx_ind = res_list.index('RX:', mac_ind)
                    tx_ind = res_list.index('TX:', mac_ind)
                    #bit_rate[k]['RX'].append(float(res_list[rx_ind + 1]))
                    bit_rate[k]['TX'].append(float(res_list[tx_ind + 1]))
                else:
                    #bit_rate[k]['RX'].append(0.0)
                    bit_rate[k]['TX'].append(0.0)

                

for m in bit_rate.keys():
    print(len(bit_rate[m]['TX']))
    #print(bit_rate[m]['TX'])
x = np.linspace(0, duration, duration / freq)
cnt = 0
for MAC in bit_rate.keys():
    print(MAC)
    #if '9F' in MAC:
    #    continue
    #plt.plot(x, bit_rate[MAC]['RX'], label=MAC+'_RX', color=colors[cnt])
    #cnt += 1
    
    #label = 'Macbook' if '9F' in MAC else 'IPX'
    #label = dist[cnt]
    label = 'AP1' if '58' in MAC else 'AP2'

    #plt.plot(x, bit_rate[MAC]['TX'], label=MAC+'_TX', color=colors[cnt])
    plt.plot(x, bit_rate[MAC]['TX'], label=label, color=colors[cnt])
    cnt += 1

ax = plt.gca()
ax.set_ylim([0, 300])
title = input("Title: ")
plt.title(title)
plt.xlabel("Time (s)")
plt.ylabel("MCS (Mbps)")
plt.legend()

#pngfile = input("filename: ")
#plt.savefig('./0222/figures/' + pngfile + '.png', dpi=600)
plt.show()

