from pinginventory import PingInventory
import sys
def take_inventory():
    ini_file = sys.argv[1]
    p = PingInventory(ini_file)

    i = p.take_inventory()
    print "Inventory ran for %s found %d hosts" % (i.endtime - i.starttime, i.numup)

def show_ip():
    ini_file = sys.argv[1]
    ip = sys.argv[2]

    p = PingInventory(ini_file)
    for time, state in p.get_ip_history(ip):
        print time.strftime("%x %X"), state
