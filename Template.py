#!/usr/bin/env python3
import binascii
import hashlib
import json
import time
import sys
import asyncio
import aiohttp
import requests

def md5_checksum(data):# This function calculates the checksum
    return hashlib.md5(data.encode()).hexdigest()

def find_port(md5): #Complete this function to get your unique port from the server
    url = "http://100.26.120.158:5000/port"
    payload = {
        "ID": md5
    }
    response = requests.post(url, json=payload).json()
    return response['Port']
def find_limits(md5,port,first_number=0.0,second_number=0.0,verbose=False):#Complete this function to find the first and second rate limits for your own account
    url = f"http://100.26.120.158:{port}/compute"
    first_limit=0
    second_limit=0
    print(first_number,second_number,port)
    payload = {
        "ID": md5,
        "N1": first_number,
        "N2": second_number
    }
    Test = True
    while Test:
        try:
            response = requests.post(url, json=payload, timeout=5).json()
            print(response)
            if response["Answer"] == "Error":
                Test = False
                print("False")
            elif(type(response["Answer"]) == int):
                second_limit += 1
                print(first_limit)
            else:
                second_limit += 1
                first_limit += 1
            time.sleep(1/60)
        except requests.exceptions.Timeout:
            print("The request timed out.")
            Test = False

    print(response)

    return first_limit,second_limit
def main():
    verbose = False
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <Last 4 digits of Cougar ID> <first_number> <second_number> <-v(Verbose Option)>")
        sys.exit(1)
    md5=md5_checksum(sys.argv[1])
    first_number=float(sys.argv[2])
    second_number=float(sys.argv[3])
    port=find_port(md5)
    print(f"MD5: {md5}",f"Port: {port}",sep=",")
    if len(sys.argv) >4:
        verbose=True
    first_limit,second_limit=find_limits(md5,port,first_number,second_number,verbose)
    print(f"MD5: {md5}",f"Port: {port}",f"First Limit: {first_limit}",f"Second Limit: {second_limit}",sep=",")
    print(verbose)

if __name__ == "__main__":
    main()
