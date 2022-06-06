#!./venv/bin/python

import subprocess
from requests import adapters
import json
import urllib
import socket
import netifaces

# get local info
hostname = socket.gethostname()
hostIP = socket.gethostbyname(hostname)
gws = netifaces.gateways()
gateway = gws['default'][netifaces.AF_INET][0]

def speedtest():
    print(f'CHECKING INTERNET SPEED\n')
    subprocess.run([f'speedtest-cli'], shell=True, stdout=True, universal_newlines=True,
                   check=True)


def checkinternet():
    print(f'TRACING 1ST GATEWAY HOP\n')
    results = subprocess.run([f'traceroute -w 2 -f 2 -m 2 -I -d google.com'], shell=True, stdout=True,
                             universal_newlines=True,
                             check=True)
    if results.returncode == 0:
        print(f'\nINTERNET CONNECTION IS UP\n')
        speedtest()
    else:
        print(f'\nCHECK INTERNET ACCESS\n')

print(f'\nLocal Machine: {hostname}\nIP: {hostIP}\nDefault GW: {gateway}\n')

hosts = [hostname, gateway]  # list of host addresses

print(f'PINGING........\n')
for host in hosts:
    try:
        results = subprocess.run([f'ping -c 1 {host}'], shell=True, capture_output=True, universal_newlines=True,
                                 check=True)
        print(f'Success from host {host}\n')
        if host == 'google.com' and results.returncode == 0:
            speedtest()
    except subprocess.CalledProcessError as err:
        print(f'Error from host {host}\n')
        print(f'{err}\n')
        print(f'Try again on host {host} \n')
        results2 = subprocess.run([f'ping -c 1 {host}'], shell=True, capture_output=True, universal_newlines=True)
        if results2.returncode != 0:
            print(f'Error again from host {host}\n')

        else:
            print(f'Success from host {host}\n')
            continue

checkinternet()

url = 'http://ipinfo.io/json'
adapters.DEFAULT_RETRIES = 5
response = urllib.request.urlopen(url)
data = json.load(response)

IP = data['ip']
org = data['org']
city = data['city']
country = data['country']
region = data['region']
gps = data['loc']

print('\nPUBLIC IP DETAILS\n ')
print(f'Public IP : {IP} \nRegion : {region} \nCountry : {country} \nCity : {city} \nGPS : {gps} \nOrg : {org}')

# ifconfig | grep "inet " | grep -v 127.0.0.1|grep broadcast|awk '{print $2}'

