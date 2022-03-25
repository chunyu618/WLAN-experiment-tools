import sys
import matplotlib.pyplot as plt
import numpy as np
import argparse


dist = ['-35 ~ -40 dBm', '-60 dBm', '-75 dBm']
colors = ['#ed6a5a', '#f0a202', '#58a4b0', 'lime', 'cyan', 'slategray', 'navy', 'slateblue']

def main():
    parser = argparse.ArgumentParser("description='Plot MCS'")
    parser.add_argument('-t', '--time', help="Period of experiment", type=int, default=60)
    parser.add_argument('-f', '--freq', help="Frequency of requesting", type=float, default=0.5)
    parser.add_argument('-i', '--input', help="Input filename", type=str, required=True, nargs='+')
    parser.add_argument('-o', '--output', help="Output filename", type=str, required=False, default='')

    args = parser.parse_args()

    T = args.time
    freq = args.freq
    filename_list = args.input
    png_filename = args.output

    #print(filename_list)
    plot(filename_list, T, freq, png_filename)


def plot(filename_list, T, freq, png_filename=''):
    duration = T / freq
    bit_rate = {}
    deli = '--------------------'
    MAC_address = ['4C:1D:96:04:14:F6', '4C:1D:96:02:20:56']
    
    for filename in filename_list:
        with open(filename, 'r') as f:
            data = f.read().split(deli)[0 : -1]

            for m in MAC_address:
                k = m + '_' + filename
                bit_rate[k] = {}
                bit_rate[k]['RX'] = []
                bit_rate[k]['TX'] = []
            
            for res in data:
                res_list = res.split()

                for m in MAC_address:
                    k = m + '_' + filename
                    if m in res_list:
                        # Find the value after 'RX' and 'TX'
                        mac_ind = res_list.index(m)
                        rx_ind = res_list.index('RX:', mac_ind)
                        tx_ind = res_list.index('TX:', mac_ind)
                        bit_rate[k]['RX'].append(float(res_list[rx_ind + 1]))
                        bit_rate[k]['TX'].append(float(res_list[tx_ind + 1]))
                    else:
                        # If not find mac address, treat the value as 0
                        bit_rate[k]['RX'].append(0.0)
                        bit_rate[k]['TX'].append(0.0)

                    
    
    x = np.linspace(0, T, duration)
    # Plot TX and RX for every MAC address
    cnt = 0
    for MAC in bit_rate.keys():
        plt.plot(x, bit_rate[MAC]['TX'], label=MAC+'_TX', color=colors[cnt])
        plt.plot(x, bit_rate[MAC]['RX'], label=MAC+'RX', color=colors[cnt+1])
        cnt += 1
    

    ax = plt.gca()
    ax.set_ylim([0, 300])
    if png_filename != '':
        title = input("Title: ")
        plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("MCS (Mbps)")
    plt.legend()

    #pngfile = input("filename: ")
    if png_filename != '':
        plt.savefig('./figures/' + png_filename + '.png', dpi=600)
    plt.show()

if __name__ == '__main__':
    main()
