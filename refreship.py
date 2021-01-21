#!/usr/bin/env python3

from urllib import request
from time import sleep, ctime
import requests
import signal
import sys

url='http://myexternalip.com/raw' # URL to retrieve external IP

max_request = 3 # Maximum number of requests
wait_time = 5 # Time between requests in seconds

# Base URL provided by Directnic (Do not share this link, using this link will change the IP address tied to this domain)
dnic_base_url ='https://directnic.com/dns/gateway/RANDOMNUMBERSANDLETTERS/?data='

def get_ip():
    try:
        response = requests.get(url)
        status = response.status_code
        ext_ip = response.text
    except IOError:
        print(f'{ctime()} - Error connecting to {url}')      
        sys.exit(0)

    return status, ext_ip

def sig_hand(sig, frame):
    """ Ensure a clean exit with CTRL+C """
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, sig_hand)
    for x in range (max_request):
        status, ext_ip = get_ip()
        if (status == 200):
            #print(ctime())
            print(f'{ctime()} - Request successful! - Your external IP: {ext_ip}')
            break
        else:
            print(f'{ctime()} - Request {x+1} unsuccessful! - HTTP Status Code: {status}')
            sleep(wait_time)
     
    # Concatenate Base URL with IP address
    dnic_full_url = (dnic_base_url + ext_ip)
    
    # Update DNS record
    try:
        response = requests.get(dnic_full_url)
        if response.status_code == 200:
            print(f'{ctime()} - Request successful! - Your DNS record was updated to {ext_ip}')
        else:
            print(f'{ctime()} - Request not successful! - HTTP Status Code: {response.status_code}')
    except IOError:
        print(f'{ctime()} - Error connecting to Directnic')
        sys.exit(0)
   
if __name__ == "__main__":
    main()