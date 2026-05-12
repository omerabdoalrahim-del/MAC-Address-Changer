import optparse
import subprocess
import random
import time
import os
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="Network_Interface", help="this options is for network interface")
    parser.add_option("-m", "--mac", dest="new_mac", help="this options is for new MAC address")
    parser.add_option("-r", "--random", action="store_true", dest="random_mac", help="generate a random MAC address")
    parser.add_option("-t", "--time", dest="change_time", help="this options is for time to change MAC address in seconds (required with -r)")
    parser.add_option("-c", "--current", action="store_true", dest="show_current", help="show the current MAC address")
    parser.add_option("-V", "--version", action="store_true", dest="show_version", help="Print version and exit")
    (options, arguments) = parser.parse_args()

    if options.show_version:
        print("Version 1.0")
        exit(0)

    if not options.Network_Interface:
        parser.error("[-] please add Network_Interface type -h for help")

    if options.show_current:
        show_current_mac(options.Network_Interface)
        exit(0)

    if options.random_mac and options.new_mac:
        parser.error("[-] you can't use -r and -m options together")

    if options.random_mac and not options.change_time:
        options.change_time = 10  # default time to change MAC address if not specified
    elif not options.random_mac and options.change_time:
        parser.error("[-] you can't use -t option without -r option")

    return options

def show_current_mac(Network_Interface):
    print("Current MAC address:")
    current_mac = subprocess.check_output(["ip", "link", "show", Network_Interface])
    current_mac = current_mac.decode("utf-8").split("link/ether ")[1].split(" brd")[0]
    print(current_mac)

def change_mac(Network_Interface, new_mac):
    print("[+] Changing MAC address for " + Network_Interface + " to " + new_mac)
    subprocess.call(["ip", "link", "set", Network_Interface, "down"])
    time.sleep(1)  # Add a delay to ensure the interface is fully down

    # Check if the MAC address is already in use
    output = subprocess.check_output(["ip", "neigh", "show", "dev", Network_Interface])
    if new_mac in output.decode("utf-8"):
        print("[-] Error: MAC address " + new_mac + " is already in use by another device")
        return False

    # Check current MAC address
    current_mac = subprocess.check_output(["ip", "link", "show", Network_Interface])
    current_mac = current_mac.decode("utf-8").split("link/ether ")[1].split(" brd")[0]

    # Change MAC address
    try:
        subprocess.call(["ip", "link", "set", Network_Interface, "address", new_mac])
        subprocess.call(["ip", "link", "set", Network_Interface, "up"])
    except:
        print("RTNETLINK answers: Cannot assign requested address")
        return False

    # Check if MAC address has been changed successfully
    new_current_mac = subprocess.check_output(["ip", "link", "show", Network_Interface])
    new_current_mac = new_current_mac.decode("utf-8").split("link/ether ")[1].split(" brd")[0]

    if new_current_mac == new_mac:
        return True
    else:
        return False

def main():
    options = get_arguments()
    if options.random_mac:
        while True:
            new_mac = "%02x:%02x:%02x:%02x:%02x:%02x" % (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            if change_mac(options.Network_Interface, new_mac):
                print("[+] MAC has been changed successfully")
                time.sleep(int(options.change_time))
            else:
                time.sleep(5)  # default time to try the next MAC address if the current one fails
    else:
        if change_mac(options.Network_Interface, options.new_mac):
            print("[+] MAC has been changed successfully")

if __name__ == "__main__":
    if os.geteuid()!= 0:
        print("[-] Please run this script with root privileges.")
    else:
        main()