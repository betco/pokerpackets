#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pokerpackets import packets, clientpackets
import sys, unittest


class PacketTestCase(unittest.TestCase):

    def test_all_packets(self):
        for name, Packet in packets.PacketFactory.iteritems():
            packet = Packet()

if __name__ == '__main__':
    unittest.main()
