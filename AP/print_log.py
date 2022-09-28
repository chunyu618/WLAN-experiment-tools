import statistics
import sys
import matplotlib.pyplot as plt

colors = ['#ed6a5a', '#f0a202', '#58a4b0', 'lime', 'cyan', 'slategray', 'navy', 'slateblue']
sta_list = ['airtime', 'transmitted_bytes', 'transmitted_pkts', 'retransmitted_pkts', 'moving_avg_rate']
#sta_list = ['airtime', 'transmitted_pkts', 'retransmitted_pkts', 'moving_avg_rate']

addr_dict = {}

# Choose the station according the AP
addr_dict['MAC1'] = 'F0-18-98-66-D9-9F'
#addr_dict['MAC2'] = '3C-06-30-2B-1D-4C'
addr_dict['ASUS1'] = '4C-1D-96-04-14-F6'
addr_dict['ASUS2'] = '4C-1D-96-02-20-56'
#addr_dict['RAS1'] = 'DC-A6-32-F1-D1-B1'
#addr_dict['RAS2'] = 'DC-A6-32-F1-CF-B6'
numSTA = 3 # Number of the station
K = 'MAC1' # Any station name in the list

filename = sys.argv[1]
sta = {}
appear = {}
removed = []

def remove_by_index(arr, remove):
    rev = []
    for i in range(len(arr)):
        if i  not in remove:
            rev.append(arr[i])

    return rev        

def plot(sta, addr_dict, colors):
    x = range(len(sta[addr_dict[K]]['transmitted_pkts']) - 1)
    cnt = 0
    target = 'transmitted_pkts'

    for k in addr_dict:
        addr = addr_dict[k]
        #print(sta[addr]['transmitted_pkts'])
        print(addr, len(sta[addr][target]))
        if len(sta[addr][target]) - 1 == len(x):
            print("here")
            target_list = []
            for i in range(1, len(sta[addr][target])):
                target_list.append(sta[addr][target][i] - sta[addr][target][i - 1])
            plt.plot(x, target_list, label=addr, color=colors[cnt])
            cnt += 1

    ax = plt.gca()
    ax.set_ylim(0, 1e3)
    plt.show()

for addr in addr_dict.values():
    #print(addr)
    sta[addr] = {}
    appear[addr] = 0
    for k in sta_list:
        sta[addr][k] = []


with open(filename) as f:
    data = f.read().split("SSSSSSSSSSSSSSSSSSSSSSSSSS\n")
    numLVAP = []
    for s in data:
        lvaps = s.split("LLLLLLLLLLLLLLLLLLLLLLLLLL\n")
        flag = 0
        for l in lvaps:
            lines = l.split('\n')
            if len(lines) > 0:
                for i in range(len(lines)):
                    for k in addr_dict:
                        addr = addr_dict[k]
                        if 'DEBUG' in lines[i] and addr in lines[i] and 'support' not in lines[i]:
                            flag += 1
        if flag == numSTA:
            for l in lvaps:
                lines = l.split('\n')
                for i in range(len(lines)):
                    for addr in addr_dict.values():
                        if 'DEBUG' in lines[i] and addr in lines[i] and 'support' not in lines[i]:
                            offset = 1
                            for k in sta_list:
                                sta[addr][k].append(int(lines[i + offset].split()[-1]))
                                offset += 1
                            
                            appear[addr] += 1

#plot(sta, addr_dict, colors)
#exit(0)

idx_list = []
arr = sta[addr_dict[K]]['transmitted_pkts']
target1 = 'transmitted_pkts'
target2 = 'retransmitted_pkts'

for i in range(1, len(arr)):
    flag = 0
    for k in addr_dict:
        addr = addr_dict[k]
        if sta[addr][target1][i] - sta[addr][target1][i - 1] + sta[addr][target2][i] - sta[addr][target2][i - 1] > 50:
            flag += 1
    if flag == numSTA:
        idx_list.append(i)

    '''
    for s in sep_list:
        if len(s) > 100:
            print(s)
    '''

#print(idx_list)

start = []
end = []
start.append(idx_list[0])
for i in range(1, len(idx_list)):
    if idx_list[i] - idx_list[i - 1] > 10:
        end.append(idx_list[i - 1])
        start.append(idx_list[i])

end.append(idx_list[-1])
'''
for i in range(len(start)):
    print(start[i], end[i], end[i] - start[i])
'''
for k in addr_dict:
    addr = addr_dict[k]
    print("--------------------")
    #print(k, addr, appear[addr])
    avg_rate = []
    transmitted_pkts = []       
    transmitted_bytes = []       
    retransmitted_pkts = []
    retrans_rate = []
    airtime_used = []
    idx_len = []
    sum_rate = 0
    
    for i in range(len(start)):
        #print(idx)
        s = start[i]
        e = end[i]
        #print(s, e, e - s)
        if e - s >= 100:
            #s = e - 100
            rate_sum = 0
            for j in range(s, e + 1):
                rate_sum += sta[addr]['moving_avg_rate'][j];
            avg_rate.append(rate_sum / (e - s + 1))
          
            transmitted_pkts.append((sta[addr]['transmitted_pkts'][e] - sta[addr]['transmitted_pkts'][s]) / (e - s))
            retransmitted_pkts.append((sta[addr]['retransmitted_pkts'][e] - sta[addr]['retransmitted_pkts'][s]) / (e - s))
            transmitted_bytes.append((sta[addr]['transmitted_bytes'][e] - sta[addr]['transmitted_bytes'][s]) / (e - s))
            airtime_used.append((sta[addr]['airtime'][e] - sta[addr]['airtime'][s]) / (e - s))
            retrans_rate.append(retransmitted_pkts[-1] / (transmitted_pkts[-1] + retransmitted_pkts[-1]))
    
    avg_rate = remove_by_index(avg_rate, removed)
    transmitted_pkts = remove_by_index(transmitted_pkts, removed)
    retransmitted_pkts = remove_by_index(retransmitted_pkts, removed)
    transmitted_bytes = remove_by_index(transmitted_bytes, removed)
    airtime_used = remove_by_index(airtime_used, removed)
    retrans_rate = remove_by_index(retrans_rate, removed)
    
    if len(avg_rate) > 0:
        #print(avg_rate)
        #for i in idx_len:
        #    print(i)
        print("[%s] Number of record: %d" % (k, len(avg_rate)))
        print("[%s] Airtime: %f %f" % (k, statistics.mean(airtime_used), statistics.stdev(airtime_used)))
        print("[%s] Rate: %f %f" % (k, statistics.mean(avg_rate), statistics.stdev(avg_rate)))
        #print(airtime_used)
        print("[%s] Transmitted bytes: %f %f" % (k, statistics.mean(transmitted_bytes), statistics.stdev(transmitted_bytes)))
        print("[%s] Transmitted pkts: %f %f" % (k, statistics.mean(transmitted_pkts), statistics.stdev(transmitted_pkts)))
        print("[%s] Retransmitted pkts: %f %f" % (k, statistics.mean(retransmitted_pkts), statistics.stdev(retransmitted_pkts)))
        #print("Retransmitted pkts: ",  retransmitted_pkts)
        print("[%s] Retransmitted ratio: %f %f" % (k, statistics.mean(retrans_rate), statistics.stdev(retrans_rate)))

