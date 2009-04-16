from pinginventory import PingInventory
import sys
def take_inventory():
    ini_file = sys.argv[1]
    p = PingInventory(ini_file)

    i = p.take_inventory()
    print "Inventory ran for %s found %d hosts" % (i.endtime - i.starttime, i.numup)
