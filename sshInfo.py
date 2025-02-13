#!/usr/bin/python3
import json

#read json file
def load_ssh_info(file_path="sshInfo.json"):
    try:
        with open(file_path, "r") as file:
            ssh_info = json.load(file)
            return ssh_info
    
    #checking if file exist
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return None
    
    #checking if file not formatted correctly
    except json.JSONDecodeError:
        print(f"Error: {file_path} is not properly formatted.")
        return None
    
    #checking if do not have the permission to open file
    except PermissionError:
        print(f"Error: NO permission to read {file_path}")
        return None
