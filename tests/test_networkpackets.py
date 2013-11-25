# -*- coding: utf-8 -*-

from pokerpackets import packets, networkpackets

def test_all_packets():
    for name, Packet in packets.PacketFactory.iteritems():
        packet = Packet()
