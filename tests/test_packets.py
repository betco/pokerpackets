# -*- coding: utf-8 -*-

from pokerpackets import packets
import sys, unittest

def test_find():
    assert packets.find(lambda n: n == 2, [1, 2, 3]) == 2
    assert packets.find(lambda n: n == 0, [1, 2, 3]) == None

def test_init():
    packet = packets.Packet(test='test')
    assert packet.test == 'test'

def test_str():
    packet = packets.PacketPing(test='test')
    assert str(packet) == "PacketPing(5)"

def test_str_all():
    for type_id, Packet in packets.PacketFactory.iteritems():
        packet = Packet()
        str(packet)

def test_repr():
    packet = packets.PacketPing(test='test')
    assert repr(packet) == str(packet)

def test_eq():
    a, b = packets.PacketLogin(), packets.PacketLogin()
    assert a == b
    b.name = 'test'
    assert a != b
    b = packets.PacketList
    assert a != b

def test_infoDeclare():
    _dict = {}
    packets.Packet.infoDeclare(_dict, packets.Packet, packets.Packet, packets.Packet.__name__, -1)
    assert _dict['type2type_id'][packets.Packet] == -1
    assert _dict['type_id2type'][-1] == packets.Packet
    assert _dict['PacketNames'][-1] == 'Packet'
    assert _dict['PacketFactory'][-1] == packets.Packet
    assert _dict['PACKET_Packet'] == -1

def test_all_packets():
    for name, Packet in packets.PacketFactory.iteritems():
        packet = Packet()
