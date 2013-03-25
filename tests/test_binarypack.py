#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pokerpackets import binarypack, packets
import sys, unittest
from cStringIO import StringIO

# import networkpackets so they get tested as well
import pokerpackets.networkpackets


class BinaryPackTestCase(unittest.TestCase):

    # public functions

    def test_pack_unpack(self):
        "iterates over all packet types, packs and unpacks them and see if the result package equals the original packet"
        for type_id, packet_type in packets.type_id2type.iteritems():
            print packet_type
            packet = packet_type()
            packed = binarypack.pack(packet)
            assert binarypack.pack(packet) == packed
            assert binarypack.unpack(packed)[1] == packet

    # private functions

    def test__pack_I(self):
        assert binarypack._pack_I(StringIO(), 0).getvalue() == b"\x00\x00\x00\x00"
        assert binarypack._pack_I(StringIO(), 1).getvalue() == b"\x00\x00\x00\x01"
        assert binarypack._pack_I(StringIO(), 4294967295).getvalue() == b"\xFF\xFF\xFF\xFF"

    def test__pack_Q(self):
        assert binarypack._pack_Q(StringIO(), 0).getvalue() == b"\x00\x00\x00\x00\x00\x00\x00\x00"
        assert binarypack._pack_Q(StringIO(), 1).getvalue() == b"\x00\x00\x00\x00\x00\x00\x00\x01"
        assert binarypack._pack_Q(StringIO(), 18446744073709551615L).getvalue() == b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"

    def test__pack_B(self):
        assert binarypack._pack_B(StringIO(), 0).getvalue() == b"\x00"
        assert binarypack._pack_B(StringIO(), 1).getvalue() == b"\x01"
        assert binarypack._pack_B(StringIO(), 255).getvalue() == b"\xFF"

    def test__pack_b(self):
        assert binarypack._pack_b(StringIO(), 0).getvalue() == b"\x00"
        assert binarypack._pack_b(StringIO(), 10).getvalue() == b"\x0A"
        assert binarypack._pack_b(StringIO(), -1).getvalue() == b"\xFF"

    def test__pack_Bnone(self):
        assert binarypack._pack_Bnone(StringIO(), 0).getvalue() == b"\x00"
        assert binarypack._pack_Bnone(StringIO(), 10).getvalue() == b"\x0A"
        assert binarypack._pack_Bnone(StringIO(), None).getvalue() == b"\xFF"

    def test__pack_bool(self):
        assert binarypack._pack_bool(StringIO(), 5).getvalue() == b"\x01"
        assert binarypack._pack_bool(StringIO(), True).getvalue() == b"\x01"
        assert binarypack._pack_bool(StringIO(), False).getvalue() == b"\x00"

    def test__pack_cbool(self):
        assert binarypack._pack_cbool(StringIO(), 'y').getvalue() == b"\x01"
        assert binarypack._pack_cbool(StringIO(), 'n').getvalue() == b"\x00"
        assert binarypack._pack_cbool(StringIO(), 'test').getvalue() == b"\x00"

    def test__pack_H(self):
        assert binarypack._pack_H(StringIO(), 0).getvalue() == b"\x00\x00"
        assert binarypack._pack_H(StringIO(), 1).getvalue() == b"\x00\x01"
        assert binarypack._pack_H(StringIO(), 65535).getvalue() == b"\xFF\xFF"

    def test__pack_string(self):
        assert binarypack._pack_string(StringIO(), "").getvalue() == b"\x00\x00"
        assert binarypack._pack_string(StringIO(), "test").getvalue() == b"\x00\x04test"
        assert binarypack._pack_string(StringIO(), u"übel".encode("utf-8")).getvalue() == b"\x00\x05\xC3\xBCbel"

    def test__pack_bstring(self):
        assert binarypack._pack_bstring(StringIO(), "").getvalue() == b"\x00\x00"
        assert binarypack._pack_bstring(StringIO(), "test").getvalue() == b"\x00\x04test"
        assert binarypack._pack_bstring(StringIO(), True).getvalue() == b"\x00\x05_TRUE"
        assert binarypack._pack_bstring(StringIO(), False).getvalue() == b"\x00\x06_FALSE"

    def test__pack_j(self):
        assert binarypack._pack_j(StringIO(), None).getvalue() == b"\x00\x04null"
        assert binarypack._pack_j(StringIO(), {'test': 1}).getvalue() == b"\x00\x0B{\"test\": 1}"

    def test__pack_Bl(self):
        assert binarypack._pack_Bl(StringIO(), []).getvalue() == b"\x00"
        assert binarypack._pack_Bl(StringIO(), [1, 2, 3]).getvalue() == b"\x03\x01\x02\x03"

    def test__pack_Hl(self):
        assert binarypack._pack_Hl(StringIO(), []).getvalue() == b"\x00"
        assert binarypack._pack_Hl(StringIO(), [1, 2, 3]).getvalue() == b"\x03\x00\x01\x00\x02\x00\x03"

    def test__pack_Il(self):
        assert binarypack._pack_Il(StringIO(), []).getvalue() == b"\x00"
        assert binarypack._pack_Il(StringIO(), [1, 2, 3]).getvalue() == b"\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03"

    def test__pack_pl(self):
        assert binarypack._pack_pl(StringIO(), []).getvalue() == b"\x00\x00"
        assert binarypack._pack_pl(StringIO(), [packets.PacketLogin(), packets.PacketLogin()]).getvalue() == \
            b'\x00\x02\n\x00\x12\x00\x07unknown\x00\x07' \
            b'unknown\n\x00\x12\x00\x07unknown\x00\x07unknown'

    def test__pack_money(self):
        assert binarypack._pack_money(StringIO(), {}).getvalue() == b"\x00\x00"
        assert binarypack._pack_money(StringIO(), {1: (1, 2, 3)}).getvalue() == \
            b'\x00\x01\x00\x00\x00\x01\x00\x00' \
            b'\x00\x00\x00\x00\x00\x01\x00\x00' \
            b'\x00\x00\x00\x00\x00\x02\x00\x00' \
            b'\x00\x00\x00\x00\x00\x03'

    def test__pack_players(self):
        assert binarypack._pack_players(StringIO(), []).getvalue() == b"\x00\x00"
        assert binarypack._pack_players(StringIO(), [('name', 10, 0)]).getvalue() == b"\x00\x01\x00\x04name\x00\x00\x00\n\x00"

    def test__pack_c(self):
        assert binarypack._pack_c(StringIO(), []).getvalue() == b"\x00\x00\x00\x00"
        assert binarypack._pack_c(StringIO(), [10, 100]).getvalue() == b"\x00\x00\x03\xE8"

    def test__unpack_I(self):
        assert binarypack._unpack_I(b"\x00\x00\x00\x00", 0) == (4, 0)
        assert binarypack._unpack_I(b"\x00\x00\x00\x01", 0) == (4, 1)
        assert binarypack._unpack_I(b"\xFF\xFF\xFF\xFF", 0) == (4, 4294967295)

    def test__unpack_Q(self):
        assert binarypack._unpack_Q(b"\x00\x00\x00\x00\x00\x00\x00\x00", 0) == (8, 0)
        assert binarypack._unpack_Q(b"\x00\x00\x00\x00\x00\x00\x00\x01", 0) == (8, 1)
        assert binarypack._unpack_Q(b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF", 0) == (8, 18446744073709551615L)

    def test__unpack_B(self):
        assert binarypack._unpack_B(b"\x00", 0) == (1, 0)
        assert binarypack._unpack_B(b"\x01", 0) == (1, 1)
        assert binarypack._unpack_B(b"\xFF", 0) == (1, 255)

    def test__unpack_b(self):
        assert binarypack._unpack_b(b"\x00", 0) == (1, 0)
        assert binarypack._unpack_b(b"\x01", 0) == (1, 1)
        assert binarypack._unpack_b(b"\xFF", 0) == (1, -1)

    def test__unpack_Bnone(self):
        assert binarypack._unpack_Bnone(b"\x00", 0) == (1, 0)
        assert binarypack._unpack_Bnone(b"\x01", 0) == (1, 1)
        assert binarypack._unpack_Bnone(b"\xFF", 0) == (1, None)

    def test__unpack_bool(self):
        assert binarypack._unpack_bool(b"\x00", 0) == (1, False)
        assert binarypack._unpack_bool(b"\x01", 0) == (1, True)
        assert binarypack._unpack_bool(b"\xFF", 0) == (1, True)

    def test__unpack_cbool(self):
        assert binarypack._unpack_cbool(b"\x00", 0) == (1, 'n')
        assert binarypack._unpack_cbool(b"\x01", 0) == (1, 'y')
        assert binarypack._unpack_cbool(b"\x0F", 0) == (1, 'y')

    def test__unpack_H(self):
        assert binarypack._unpack_H(b"\x00\x00", 0) == (2, 0)
        assert binarypack._unpack_H(b"\x00\x01", 0) == (2, 1)
        assert binarypack._unpack_H(b"\xFF\xFF", 0) == (2, 65535)

    def test__unpack_string(self):
        assert binarypack._unpack_string(b"\x00\x00", 0) == (2, '')
        assert binarypack._unpack_string(b"\x00\x04test", 0) == (6, 'test')
        assert binarypack._unpack_string(b"\xFF\xFF" + "#"*65535, 0) == (65537, '#'*65535)

    def test__unpack_bstring(self):
        assert binarypack._unpack_bstring(b"\x00\x00", 0) == (2, '')
        assert binarypack._unpack_bstring(b"\x00\x04test", 0) == (6, 'test')
        assert binarypack._unpack_bstring(b"\x00\x05_TRUE", 0) == (7, True)
        assert binarypack._unpack_bstring(b"\x00\x06_FALSE", 0) == (8, False)
        assert binarypack._unpack_bstring(b"\xFF\xFF" + "#"*65535, 0) == (65537, '#'*65535)

    def test__unpack_json(self):
        assert binarypack._unpack_json(b"\x00\x04null", 0) == (6, None)
        assert binarypack._unpack_json(b"\x00\x0B{\"test\": 1}", 0) == (13, {'test': 1})

    def test__unpack_Bl(self):
        assert binarypack._unpack_Bl(b"\x00", 0) == (1, [])
        assert binarypack._unpack_Bl(b"\x03\x01\x02\x03", 0) == (4, [1, 2, 3])

    def test__unpack_Hl(self):
        assert binarypack._unpack_Hl(b"\x00", 0) == (1, [])
        assert binarypack._unpack_Hl(b"\x03\x00\x01\x00\x02\x00\x03", 0) == (7, [1, 2, 3])

    def test__unpack_Il(self):
        assert binarypack._unpack_Il(b"\x00", 0) == (1, [])
        assert binarypack._unpack_Il(b"\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03", 0) == (13, [1, 2, 3])

    def test__unpack_pl(self):
        assert binarypack._unpack_pl(b"\x00\x00", 0) == (2, [])
        assert binarypack._unpack_pl(
            b'\x00\x02\n\x00\x12\x00\x07unknown\x00\x07' \
            b'unknown\n\x00\x12\x00\x07unknown\x00\x07unknown'
        , 0) == (44, [packets.PacketLogin(), packets.PacketLogin()])

    def test__unpack_money(self):
        assert binarypack._unpack_money(b"\x00\x00", 0) == (2, {})
        assert binarypack._unpack_money(
            b'\x00\x01\x00\x00\x00\x01\x00\x00' \
            b'\x00\x00\x00\x00\x00\x01\x00\x00' \
            b'\x00\x00\x00\x00\x00\x02\x00\x00' \
            b'\x00\x00\x00\x00\x00\x03'
        , 0) == (30, {1: (1, 2, 3)})

    def test__unpack_players(self):
        assert binarypack._unpack_players(b'\x00\x00', 0) == (2, [])
        assert binarypack._unpack_players(b'\x00\x01\x00\x04name\x00\x00\x00\n\x00', 0) == (13, [('name', 10, 0)])

    def test__unpack_c(self):
        assert binarypack._unpack_c(b"\x00\x00\x00\x00", 0) == (4, [])
        assert binarypack._unpack_c(b"\x00\x00\x03\xE8", 0) == (4, [1, 1000])

if __name__ == '__main__':
    unittest.main()
