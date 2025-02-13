#!/usr/bin/python3

def validate_IPv4(ip):
    try:
        octets = ip.split('.')
        #check if there are 4 octets
        if len(octets) != 4:
            return False
        
        #storing each octet inside to convert to integer
        int_octets = []

        #check if no letters, special characters, or empty values
        for octet in octets:
            if not octet.isdigit() or octet.strip() == "":
                return False
        
            #check each octet for its number is in range of 0 - 255
            num = int(octet)
            if num < 0 or num > 255:
                return False

            #store the num value into the integer list
            int_octets.append(num)
        
        #check for loopback
        if 127 == int_octets[0]:
            return False
        
        #check for link-local
        if int_octets[0] == 169 and int_octets[1] == 254:
            return False

        #check for Reserved or experimental or broadcast or multicast
        if int_octets[0] >= 224:
            return False

        #if everything is good
        return True
    
    except ValueError:
        return False