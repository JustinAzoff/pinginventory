from unittest import TestCase

from pinginventory import PingInventory, model

class InventoryTest(TestCase):
    def setUp(self):
        self.p = PingInventory("test.ini")
        model.metadata.drop_all()
        model.metadata.create_all()

    def test_inventory_simple(self):
        def fake_scan():
            return ['1.2.3.4','5.6.7.8']

        i = self.p.take_inventory(fake_scan)
        assert i.numup == 2
        r = self.p.get_latest_up_nodes()
        assert r == ['1.2.3.4','5.6.7.8']

    def test_inventory_ip_history(self):
        def fake_scan_a():
            return ['1.2.3.4','5.6.7.8','9.10.11.12']
        def fake_scan_b():
            return ['1.2.3.4','9.10.11.12']

        i1 = self.p.take_inventory(fake_scan_a)
        i2 = self.p.take_inventory(fake_scan_b)
        i3 = self.p.take_inventory(fake_scan_a)
        i4 = self.p.take_inventory(fake_scan_a)

        hist = self.p.get_ip_history('5.6.7.8')
        assert len(hist) == 4

        hist = list(self.p.get_ip_history_short('5.6.7.8'))
        assert len(hist) == 3

        assert hist[0][0] == i1.starttime
        assert hist[1][0] == i2.starttime
        assert hist[2][0] == i3.starttime

        assert hist[1][1] == False
