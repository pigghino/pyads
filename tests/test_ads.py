import pyads
from pyads import AmsAddr
from pyads.utils import platform_is_linux
import unittest


class AdsTest(unittest.TestCase):

    def test_AmsAddr(self):
        netid = '5.33.160.54.1.1'
        port = 851

        adr = AmsAddr()
        self.assertEqual(adr.netid, '0.0.0.0.0.0')
        self.assertEqual(adr.port, 0)

        adr = AmsAddr(netid, port)
        self.assertEqual(adr.netid, netid)
        self.assertEqual(adr.port, port)

        # check if ams addr struct has been changed
        ams_addr_numbers = [x for x in adr._ams_addr.netId.b]
        netid_numbers = [int(x) for x in netid.split('.')]
        self.assertEqual(len(ams_addr_numbers), len(netid_numbers))
        for i in range(len(ams_addr_numbers)):
            self.assertEqual(ams_addr_numbers[i], netid_numbers[i])
        self.assertEqual(adr.port, adr._ams_addr.port)

    def test_set_local_address(self):

        # Skip test on Windows as set_local_address is not supported for Windows
        if platform_is_linux():
            pyads.open_port()
            org_adr = pyads.get_local_address()
            org_netid = org_adr.netid

            # Set netid to specific value
            pyads.set_local_address('0.0.0.0.1.5')
            netid = pyads.get_local_address().netid
            self.assertEqual(netid, '0.0.0.0.1.5')

            # Change netid by String
            pyads.set_local_address('0.0.0.0.1.6')
            netid = pyads.get_local_address().netid
            self.assertEqual(netid, '0.0.0.0.1.6')

            # Change netid by Struct
            pyads.set_local_address(org_adr.netIdStruct())
            netid = pyads.get_local_address().netid
            self.assertEqual(netid, org_netid)

            # Check inadequate netid
            with self.assertRaises(ValueError):
                pyads.set_local_address('1.2.3.a')

            # Check wrong netid datatype
            with self.assertRaises(AssertionError):
                pyads.set_local_address(123)


if __name__ == '__main__':
    unittest.main()
