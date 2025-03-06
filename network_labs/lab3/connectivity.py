#!/usr/bin/python3
import os

def check_connectivity(ip):
    #ping the destination ip three times
    response = os.system(f"ping -c 3 {ip}")

    #ping will return 0 if the target host responds, non-zero if does not
    return response == 0