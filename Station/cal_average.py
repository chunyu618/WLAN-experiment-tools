import json
import sys
import matplotlib.pyplot as plt
import numpy as np
import argparse
import statistics



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
    parser.add_argument('-o', '--output', help="Output filename", type=str, required=False, default='')
    args = parser.parse_args()
    png_filename = args.output

    filename_list = args.input

    #print(filename_list)
    plot(filename_list, png_filename)


def plot(filename_list, png_filename=''):
    bit_rate = {}
    extension = ''

    for filename in filename_list:
        tag = filename.split('.')[0]
        bit_rate[tag] = []
        
        with open(filename) as f:
            data = json.load(f)
            for s in data['intervals']:
                bps = s['sum']['bits_per_second']
                bit_rate[tag].append(float(bps / 1e6))
    
    avg = []
    for m in bit_rate:
        #print("Length: ", len(bit_rate[m]))
        #print(bit_rate[m])
        avg.append(round(sum(bit_rate[m]) / len(bit_rate[m]), 2))

    # Average throughput
    for k in bit_rate:
        print("%s avg: " % (k), sum(bit_rate[k]) / len(bit_rate[k]))

    print(avg)
    print(statistics.mean(avg))
    print(statistics.stdev(avg))

if __name__ == '__main__':
    main()
