#!/usr/bin/python3
import sshInfo
import validateIPv4
import connectivity

def main():
    ssh_Info = sshInfo.load_ssh_info()

    if ssh_Info:
        #going through the json file and print the router name, ip, and username
        for router_name, router_info in ssh_Info.items():
            ip = router_info['IP']
            print(f"Router: {router_name}, IP: {router_info['IP']}, Username: {router_info['Username']}")

            #check if the ip is valid or invalid
            if validateIPv4.validate_IPv4(ip):
                print(f"Valid IP")

                #check connectivity
                if connectivity.check_connectivity(ip):
                    print(f"{ip} is reachable")
                else:
                    print(f"{ip} is not reachable")
            else:
                print(f"Invalid IP")
    else:
        print("Failed to load SSH Info.")

if __name__ == "__main__":
    main()
