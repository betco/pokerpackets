# -*- coding: utf-8 -*-

from pokerpackets import dictpack, packets

# import networkpackets so they get tested as well
import pokerpackets.networkpackets

from test_packets import generate_test_packets

def test_pack_unpack():
    def check_pack_unpack(packet, numeric_type):
        packed = dictpack.pack(packet, numeric_type)
        assert dictpack.pack(packet, numeric_type) == packed

        unpack_packet, unpack_numeric = dictpack.unpack(packed)
        assert unpack_packet == packet
        assert unpack_numeric == numeric_type

    for packet in generate_test_packets():
        yield check_pack_unpack, packet, True
        yield check_pack_unpack, packet, False

def test_unpack_errors():
    # test type not specified
    unpack_packet, unpack_numeric = dictpack.unpack({})
    assert isinstance(unpack_packet, packets.PacketError), 'unpack should return PacketError'
    assert unpack_numeric == False, 'unpack should return numeric type False'

    # test unknown string type
    unpack_packet, unpack_numeric = dictpack.unpack({'type': 'PacketPewPew'})
    assert isinstance(unpack_packet, packets.PacketError), 'unpack should return PacketError'
    assert unpack_numeric == False, 'unpack should return numeric type False'

    # test unknown numeric type
    unpack_packet, unpack_numeric = dictpack.unpack({'type': -1})
    assert isinstance(unpack_packet, packets.PacketError), 'unpack should return PacketError'
    assert unpack_numeric == True, 'unpack should return numeric type False'

def test_pack_errors():
    # test unknown packet
    class PacketUnknown(packets.Packet): pass

    packet = PacketUnknown()
    packed = dictpack.pack(PacketUnknown(), True)

    unpack_packet, unpack_numeric = dictpack.unpack(packed)
    assert isinstance(unpack_packet, packets.PacketError), 'unpack should return PacketError'
    assert unpack_numeric == True, 'unpack should return numeric type False'
