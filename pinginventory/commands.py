from pinginventory import PingInventory
import sys

def setup(p):
    p.create_tables()

def take_inventory(p):
    i = p.take_inventory()
    print "Inventory ran for %s found %d hosts" % (i.endtime - i.starttime, i.numup)

def show_ip(p, ip):
    for time, state in p.get_ip_history(ip):
        print time.strftime("%x %X"), state

def list(p):
    for i in p.list():
        print "%4d %s %s" % (i.id, i.starttime.strftime("%x %X"), i.numup)

def show(p, idx=None):
    if not idx:
        i = p.latest()
    else:
        i = p.get(idx)
    for n in i.nodes:
        print n.ip

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage %s file.ini command [args]\n" % sys.argv[0])
        sys.stderr.write("Commands:\n"
                         "  take_inventory\n"
                         "  list\n"
                         "  show [inventory_id]\n"
                         "  show_ip ip\n")

        sys.exit(1)
    ini_file = sys.argv[1]
    command = sys.argv[2]
    args = sys.argv[3:]

    p = PingInventory(ini_file)
    func = globals()[command]
    func(p, *args)
