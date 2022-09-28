import json
import sys
import matplotlib.pyplot as plt
import numpy as np
import argparse
import statistics

# This file is used to print out single iperf result (json format)
# Usage:
# python3 print_result -i yourfile.json


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
    print_result(filename_list, png_filename)


def print_result(filename_list, png_filename=''):
    bit_rate = []
    
    # This file is able to preocess multiple json file at one time
    for filename in filename_list:
        # open file and parse it as json format
        with open(filename) as f:
            data = json.load(f)
            for s in data['intervals']:
                bps = s['sum']['bits_per_second']
                bit_rate.append(float(bps / 1e6))

    # Calculate average throughput
    avg = round(sum(bit_rate) / len(bit_rate), 2)
    
    print(avg, "Mbps")
        
if __name__ == '__main__':
    main()
