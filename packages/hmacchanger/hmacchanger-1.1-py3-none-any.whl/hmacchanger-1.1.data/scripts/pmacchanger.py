import subprocess
import re
import optparse
import random

def randchoice():
    return (random.choice(["a","b","c","d","e","f"]))

def randchoice1():
    return (random.choice(["0","1","2","3","4","5","6","7","8","9"]))

def randmac():
    a = str(randchoice()+randchoice1()+":"+randchoice()+randchoice1()+":"+randchoice()+randchoice1()+":"+randchoice()+randchoice1()+":"+randchoice()+randchoice1()+":"+randchoice()+randchoice1())
    return a

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change the MAC")
    parser.add_option("-m", "--mac", dest="new_MAC", help="MAC address to change")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("Please specify an interface/use --help for more info")
    elif not options.new_MAC:
        options.new_MAC = randmac()
    return options

class MACLINUX:
    def change_MAC(self, interface, new_MAC):
        print("***Changing MAC Address for " + interface + "*** to " + new_MAC)
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", new_MAC])
        subprocess.call(["ifconfig", interface, "up"])

    def get_current_MAC(self, interface):
        ifconfig_result = subprocess.check_output(["ifconfig", interface])
        MAC_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
        if MAC_address_search_result:
            return MAC_address_search_result.group(0)
        else:
            print("Could not fine MAC address.")

options = get_arguments()

m = MACLINUX()
current_MAC = m.get_current_MAC(options.interface)
print("\nCurrent MAC = " + str(current_MAC))
m.change_MAC(options.interface, options.new_MAC)
current_MAC = m.get_current_MAC(options.interface)
if current_MAC == options.new_MAC:
    print("MAC address was successfully changed")
    print("New MAC = " + current_MAC)
else:
    print("MAC address did not get changed")
print("Do you want to print 'ifconfig " + options.interface + "'(y/n): ", end='')
ch = input()
if ch == "y":
    print("\n")
    print(subprocess.call(["ifconfig", options.interface]))
    print("\n")
else:
    print("\n\tGoooooooooooood Byeeeeeee\n")
