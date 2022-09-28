#!/bin/bash

host=MAC1 # Hostname
port=8888 # port number
filename="$host-$3.json" # iperf output filename, json format

# First make sure the file doesn't exist, otherwise the output file will be appended.
rm -rf $filename 

# Sometime deleting file lasts a while, so wait 2 second here to make sure the file is deleted
sleep $2 


# Run iPerf3 client. use `iperf3 -h` to see the options
iperf3 -c 192.168.1.147 -p $port -t 300 -u -R -b $1 --json --logfile $filename

# Wait 1 second for iperf3 finishing 
sleep 1

# To see the average throughput
python3 print_result.py -i $filename
