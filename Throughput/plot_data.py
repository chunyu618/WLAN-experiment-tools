import json
import sys
import matplotlib.pyplot as plt
import numpy as np
import argparse



colors = ['#ed6a5a', '#f0a202', '#58a4b0', 'lime', 'cyan', 'slategray', 'navy', 'slateblue']
dist = ['-35 ~ -40 dBm', '-60 dBm', '-75 dBm']

def my_sum(vec):
    rev = 0
    for i in vec:
        rev += i;
    return rev    

def main():
    parser = argparse.ArgumentParser("description='Plot Throughput'")
    parser.add_argument('-i', '--input', help="Input filename", type=str, required=True, nargs='+')
    args = parser.parse_args()

    filename_list = args.input

    #print(filename_list)
    plot(filename_list)


def plot(filename_list):
    bit_rate = {}
    extension = ''
    title = input("Title: ")

    for filename in filename_list:
        if 'json' in filename:
            extension = 'json'
        else:
            extension = 'txt'

        tag = filename.split('.')[0]
        bit_rate[tag] = []
        
        with open(filename) as f:
            # json file
            if extension == 'json':
                data = json.load(f)
                for s in data['intervals']:
                    bps = s['sum']['bits_per_second']
                    bit_rate[tag].append(float(bps / 1e6))
            # txt file
            elif extension == 'txt':
                data = f.readlines()
                for line in data:
                    d = line.split()
                    if len(d) < 6 or d[0] == 'IPerf':
                        continue
                    bps = float(d[5])
                    bit_rate[tag].append(bps)
    
    # Average throughput
    for k in bit_rate:
        print("Avg: ", sum(bit_rate[k]) / len(bit_rate[k]))
            
    x = range(len(bit_rate[tag]))
    cnt = 0
    for tag in bit_rate:
        plt.plot(x, bit_rate[tag], label=tag, color=colors[cnt])
        cnt += 1    

    ax = plt.gca()
    ax.set_ylim([0, 100])

    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Throughput (Mbps)")
    plt.legend()
    #plt.arrow(100, 80, 0, -20, width = 1, head_width = 5, length_includes_head=True)
    #plt.axvline(x=100, ymin = 0, ymax = y_max_100/100, color='red', linestyle='--')
    #tag = input("Figure name: ")
    #plt.savefig("./figures/" + tag + ".png", dpi=600)
    plt.show()


if __name__ == '__main__':
    main()
