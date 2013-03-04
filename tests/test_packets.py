#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pokerpackets import packets
import sys, unittest


class ModuleTestCase(unittest.TestCase):

    def test_find(self):
        assert packets.find(lambda n: n == 2, [1, 2, 3]) == 2
        assert packets.find(lambda n: n == 0, [1, 2, 3]) == None

class PacketTestCase(unittest.TestCase):

    def test_init(self):
        packet = packets.Packet(test='test')
        assert packet.test == 'test'

    def test_str(self):
        packet = packets.PacketPing(test='test')
        assert str(packet) == "PacketPing(5)"

    def test_str_all(self):
        for type_id, Packet in packets.PacketFactory.iteritems():
            packet = Packet()
            str(packet)

    def test_repr(self):
        packet = packets.PacketPing(test='test')
        assert repr(packet) == str(packet)

    def test_eq(self):
        a, b = packets.PacketLogin(), packets.PacketLogin()
        assert a == b
        b.name = 'test'
        assert a != b
        b = packets.PacketList
        assert a != b

    def test_infoDeclare(self):
        _dict = {}
        packets.Packet.infoDeclare(_dict, packets.Packet, packets.Packet, packets.Packet.__name__, -1)
        assert _dict['type2type_id'][packets.Packet] == -1
        assert _dict['type_id2type'][-1] == packets.Packet
        assert _dict['PacketNames'][-1] == 'Packet'
        assert _dict['PacketFactory'][-1] == packets.Packet
        assert _dict['PACKET_Packet'] == -1

    def test_all_packets(self):
        for name, Packet in packets.PacketFactory.iteritems():
            packet = Packet()

if __name__ == '__main__':
    unittest.main()
