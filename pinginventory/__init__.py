import ConfigParser
import datetime


import model
import nmapping
class PingInventory:

    def __init__(self, inifile):
        c = ConfigParser.ConfigParser()
        c.read(inifile)
        uri = c.get("db","uri")
        model.init_model(model.sa.create_engine(uri))
        self.networks = c.get("scan", "networks").split(";")

    def list(self):
        return model.Inventory.list()

    def latest(self):
        return model.Inventory.latest()

    def get(self, inventory_id):
        return model.Inventory.get(inventory_id)

    def get_latest_up_nodes(self):
        """Return all the nodes listed as being up"""
        i = model.Inventory.latest()
        return [n.ip for n in i.nodes]

    def get_ip_history(self, ip):
        return model.get_ip_history(ip)

    def get_ip_history_short(self, ip):
        last = None
        for time, state in model.get_ip_history(ip):
            if state != last:
                yield time, state
            last = state
            

    def do_ping_scan(self):
        return nmapping.ping(self.networks,use_sudo=True)

    def take_inventory(self, scanner=None):
        if scanner is None:
            scanner = self.do_ping_scan

        i = model.Inventory()
        i.starttime = datetime.datetime.now()
        model.Session.add(i)

        num = 0
        for ip in scanner():
            n=model.Node()
            n.ip = ip
            n.inventory = i
            model.Session.add(n)
            num +=1

        i.numup = num
        i.endtime = datetime.datetime.now()

        model.Session.add(i)
        model.Session.flush()
        model.Session.commit()
        return i
