import paramiko, time, sys
import argparse
import pathlib

#T = int(sys.argv[2])
#freq = float(sys.argv[3])
#duration = T / freq
#hostname = sys.argv[4]

def main():
    parser = argparse.ArgumentParser("description='Monitor MCS'")
    parser.add_argument('-t', '--time', help="Period of experiment", type=int, default=60)
    parser.add_argument('-f', '--freq', help="Frequency of requesting", type=float, default=0.5)
    parser.add_argument('-o', '--output', help="Output filename", type=str, required=True)
    parser.add_argument('-i', '--ip', help="IP os hostname to query", type=str, default='192.168.1.1')
    args = parser.parse_args()

    T = args.time
    freq = args.freq
    duration = T / freq
    hostname = args.ip
    filename = args.output

    print("[LOG] Monitoring for %d seconds..." % (T))
    monitor(duration, freq, hostname, filename)

def monitor(duration, freq, hostname, filename):
    username = 'root'
    password = 'root'
    port = 22
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password, allow_agent=False,look_for_keys=False)

    t = 0
    with open(filename, 'w') as f:
        results = []
        while(t < duration):
            stdin, stdout, stderr = client.exec_command('iwinfo wlan1 assoclist')
            
            data = stdout.read().decode("utf8")
            
            #f.write(data)
            results.append(data)
            '''
            for line in data:
                if 'ago' in line:
                    print(line.split()[0])
                if 'RX' in line or 'TX' in line:
                    print(line.split()[1])
            '''
            t += 1
            time.sleep(freq)
        for r in results:
            f.write(r)
            f.write('--------------------\n')
            
if __name__ == '__main__':
    main()
