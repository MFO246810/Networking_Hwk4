#!/usr/bin/env python3
import binascii
import hashlib
import json
import time
import sys
import asyncio
import aiohttp

def md5_checksum(data):# This function calculates the checksum
    return hashlib.md5(data.encode()).hexdigest()

async def find_port(md5): #Complete this function to get your unique port from the server
    url = "http://100.26.120.158:5000/port"
    port = 0
    payload = {"ID": md5}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            data = await response.json()
            port = data["Port"]

    return port

async def find_limits(md5,port,first_number=0.0,second_number=0.0,verbose=False):#Complete this function to find the first and second rate limits for your own account
    global results
    results = []
    url = f"http://100.26.120.158:{port}/compute"
    first_limit=0
    second_limit=0
    payload = { "ID": md5, "N1": first_number, "N2": second_number}

    status = None
    limit = 1
    async with aiohttp.ClientSession() as session:
        while status != "Error":
        
            tasks = [asyncio.create_task(Handle_Posts(session, url, payload)) for _ in range(limit)]

            for task in asyncio.as_completed(tasks):
                result = await task
                print("Response:", result) 
                if(type(result) == int):
                    if(first_limit == 0):
                        first_limit = limit
                        print("first_limit:", first_limit)
                elif(type(result) == str):
                    second_limit = limit
                    status = "Error"
                    print("second_limit:", second_limit)
            limit = limit + 1 
            print("Current Limit: ", limit) 
            await asyncio.sleep(1)          
    return first_limit,second_limit

async def Handle_Posts(session, url, payload):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as resp:
            try:
                result = await resp.json()
                return result['Answer']
            except KeyError:
                return "Error"
            except aiohttp.ContentTypeError:
                text = await resp.text()
                if resp.status == 503:
                    return "Error" 
                return f"Non-JSON response: {text[:50]}"


async def main():
    verbose = False
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <Last 4 digits of Cougar ID> <first_number> <second_number> <-v(Verbose Option)>")
        sys.exit(1)
    md5=md5_checksum(sys.argv[1])
    first_number=float(sys.argv[2])
    second_number=float(sys.argv[3])
    port= await find_port(md5)
    print(f"MD5: {md5}",f"Port: {port}",sep=",")
    if len(sys.argv) >4:
        verbose=True
    first_limit,second_limit= await find_limits(md5,port,first_number,second_number,verbose)
    print(f"MD5: {md5}",f"Port: {port}",f"First Limit: {first_limit}",f"Second Limit: {second_limit}",sep=",")
    print(verbose)

if __name__ == "__main__":
    asyncio.run(main())
