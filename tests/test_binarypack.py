# -*- coding: utf-8 -*-

from pokerpackets import binarypack, packets
from pokerpackets.binarypack import _binarypack

from test_packets import generate_test_packets

# import networkpackets so they get tested as well
import pokerpackets.networkpackets

# public functions

def test_pack_unpack():
    def check_pack_unpack(packet):
        assert packet.type != -1 
        packed = binarypack.pack(packet)
        assert binarypack.unpack(packed) == packet

    for packet in generate_test_packets():
        yield check_pack_unpack, packet

# private functions

def test_pack_I():
    buf = [] ; assert _binarypack.pack_I(0, buf) == 4 ; assert "".join(buf) == b"\x00\x00\x00\x00"
    buf = [] ; assert _binarypack.pack_I(1, buf) == 4 ; assert "".join(buf) == b"\x00\x00\x00\x01"
    buf = [] ; assert _binarypack.pack_I(4294967295, buf) == 4 ; assert "".join(buf) == b"\xFF\xFF\xFF\xFF"

def test_pack_Q():
    buf = [] ; assert _binarypack.pack_Q(0, buf) == 8 ; assert "".join(buf) == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    buf = [] ; assert _binarypack.pack_Q(1, buf) == 8 ; assert "".join(buf) == b"\x00\x00\x00\x00\x00\x00\x00\x01"
    buf = [] ; assert _binarypack.pack_Q(18446744073709551615L, buf) == 8 ; assert "".join(buf) == b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"

def test_pack_B():
    buf = [] ; assert _binarypack.pack_B(0, buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert _binarypack.pack_B(1, buf) == 1 ; assert "".join(buf) == b"\x01"
    buf = [] ; assert _binarypack.pack_B(255, buf) == 1 ; assert "".join(buf) == b"\xFF"

def test_pack_b():
    buf = [] ; assert _binarypack.pack_b(0, buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert _binarypack.pack_b(10, buf) == 1 ; assert "".join(buf) == b"\x0A"
    buf = [] ; assert _binarypack.pack_b(-1, buf) == 1 ; assert "".join(buf) == b"\xFF"

def test_pack_Bnone():
    buf = [] ; assert _binarypack.pack_Bnone(0, buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert _binarypack.pack_Bnone(10, buf) == 1 ; assert "".join(buf) == b"\x0A"
    buf = [] ; assert _binarypack.pack_Bnone(None, buf) == 1 ; assert "".join(buf) == b"\xFF"

def test_pack_bool():
    buf = [] ; assert _binarypack.pack_bool(5, buf) == 1 ; assert "".join(buf) == b"\x01"
    buf = [] ; assert _binarypack.pack_bool(True, buf) == 1 ; assert "".join(buf) == b"\x01"
    buf = [] ; assert _binarypack.pack_bool(False, buf) == 1 ; assert "".join(buf) == b"\x00"

def test_pack_cbool():
    buf = [] ; assert _binarypack.pack_cbool('y', buf) == 1 ; assert "".join(buf) == b"\x01"
    buf = [] ; assert _binarypack.pack_cbool('n', buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert _binarypack.pack_cbool('test', buf) == 1 ; assert "".join(buf) == b"\x00"

def test_pack_H():
    buf = [] ; assert _binarypack.pack_H(0, buf) == 2 ; assert "".join(buf) == b"\x00\x00"
    buf = [] ; assert _binarypack.pack_H(1, buf) == 2 ; assert "".join(buf) == b"\x00\x01"
    buf = [] ; assert _binarypack.pack_H(65535, buf) == 2 ; assert "".join(buf) == b"\xFF\xFF"

def test_pack_string():
    buf = [] ; assert _binarypack.pack_string("", buf) == 2 ; assert "".join(buf) == b"\x00\x00"
    buf = [] ; assert _binarypack.pack_string("test", buf) == 6 ; assert "".join(buf) == b"\x00\x04test"
    buf = [] ; assert _binarypack.pack_string(u"übel".encode("utf-8"), buf) == 7 ; assert "".join(buf) == b"\x00\x05\xC3\xBCbel"

def test_pack_bstring():
    buf = [] ; assert _binarypack.pack_bstring("", buf) == 2 ; assert "".join(buf) == b"\x00\x00"
    buf = [] ; assert _binarypack.pack_bstring("test", buf) == 6 ; assert "".join(buf) == b"\x00\x04test"
    buf = [] ; assert _binarypack.pack_bstring(True, buf) == 7 ; assert "".join(buf) == b"\x00\x05_TRUE"
    buf = [] ; assert _binarypack.pack_bstring(False, buf) == 8 ; assert "".join(buf) == b"\x00\x06_FALSE"

def test_pack_j():
    buf = [] ; assert _binarypack.pack_j(None, buf) == 6 ; assert "".join(buf) == b"\x00\x04null"
    buf = [] ; assert _binarypack.pack_j({'test': 1}, buf) == 13 ; assert "".join(buf) == b"\x00\x0B{\"test\": 1}"

def test_pack_Bl():
    buf = [] ; assert _binarypack.pack_Bl([], buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert _binarypack.pack_Bl([1, 2, 3], buf) == 4 ; assert "".join(buf) == b"\x03\x01\x02\x03"

def test_pack_Hl():
    buf = [] ; assert _binarypack.pack_Hl([], buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert _binarypack.pack_Hl([1, 2, 3], buf) == 7 ; assert "".join(buf) == b"\x03\x00\x01\x00\x02\x00\x03"

def test_pack_Il():
    buf = [] ; assert _binarypack.pack_Il([], buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert _binarypack.pack_Il([1, 2, 3], buf) == 13 ; assert "".join(buf) == b"\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03"

def test_pack_pl():
    buf = [] ; assert _binarypack.pack_pl([], buf) == 2 ; assert "".join(buf) == b"\x00\x00"
    buf = [] ; assert _binarypack.pack_pl([packets.PacketLogin(), packets.PacketLogin()], buf) == 44 ; assert "".join(buf) == \
        b'\x00\x02\n\x00\x12\x00\x07unknown\x00\x07' \
        b'unknown\n\x00\x12\x00\x07unknown\x00\x07unknown'

def test_pack_money():
    buf = [] ; assert _binarypack.pack_money({}, buf) == 2 ; assert "".join(buf) == b"\x00\x00"
    buf = [] ; assert _binarypack.pack_money({1: (1, 2, 3)}, buf) == 30 ; assert "".join(buf) == \
        b'\x00\x01\x00\x00\x00\x01\x00\x00' \
        b'\x00\x00\x00\x00\x00\x01\x00\x00' \
        b'\x00\x00\x00\x00\x00\x02\x00\x00' \
        b'\x00\x00\x00\x00\x00\x03'

def test_pack_players():
    buf = [] ; assert _binarypack.pack_players([], buf) == 2 ; assert "".join(buf) == b"\x00\x00"
    buf = [] ; assert _binarypack.pack_players([('name', 10, 0)], buf) == 13 ; assert "".join(buf) == b"\x00\x01\x00\x04name\x00\x00\x00\n\x00"

def test_pack_c():
    buf = [] ; assert _binarypack.pack_c([], buf) == 4 ; assert "".join(buf) == b"\x00\x00\x00\x00"
    buf = [] ; assert _binarypack.pack_c([10, 100], buf) == 4 ; assert "".join(buf) == b"\x00\x00\x03\xE8"

def test_unpack_I():
    assert _binarypack.unpack_I(b"\x00\x00\x00\x00", 0) == (4, 0)
    assert _binarypack.unpack_I(b"\x00\x00\x00\x01", 0) == (4, 1)
    assert _binarypack.unpack_I(b"\xFF\xFF\xFF\xFF", 0) == (4, 4294967295)

def test_unpack_Q():
    assert _binarypack.unpack_Q(b"\x00\x00\x00\x00\x00\x00\x00\x00", 0) == (8, 0)
    assert _binarypack.unpack_Q(b"\x00\x00\x00\x00\x00\x00\x00\x01", 0) == (8, 1)
    assert _binarypack.unpack_Q(b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF", 0) == (8, 18446744073709551615L)

def test_unpack_B():
    assert _binarypack.unpack_B(b"\x00", 0) == (1, 0)
    assert _binarypack.unpack_B(b"\x01", 0) == (1, 1)
    assert _binarypack.unpack_B(b"\xFF", 0) == (1, 255)

def test_unpack_b():
    assert _binarypack.unpack_b(b"\x00", 0) == (1, 0)
    assert _binarypack.unpack_b(b"\x01", 0) == (1, 1)
    assert _binarypack.unpack_b(b"\xFF", 0) == (1, -1)

def test_unpack_Bnone():
    assert _binarypack.unpack_Bnone(b"\x00", 0) == (1, 0)
    assert _binarypack.unpack_Bnone(b"\x01", 0) == (1, 1)
    assert _binarypack.unpack_Bnone(b"\xFF", 0) == (1, None)

def test_unpack_bool():
    assert _binarypack.unpack_bool(b"\x00", 0) == (1, False)
    assert _binarypack.unpack_bool(b"\x01", 0) == (1, True)
    assert _binarypack.unpack_bool(b"\xFF", 0) == (1, True)

def test_unpack_cbool():
    assert _binarypack.unpack_cbool(b"\x00", 0) == (1, 'n')
    assert _binarypack.unpack_cbool(b"\x01", 0) == (1, 'y')
    assert _binarypack.unpack_cbool(b"\x0F", 0) == (1, 'y')

def test_unpack_H():
    assert _binarypack.unpack_H(b"\x00\x00", 0) == (2, 0)
    assert _binarypack.unpack_H(b"\x00\x01", 0) == (2, 1)
    assert _binarypack.unpack_H(b"\xFF\xFF", 0) == (2, 65535)

def test_unpack_string():
    assert _binarypack.unpack_string(b"\x00\x00", 0) == (2, '')
    assert _binarypack.unpack_string(b"\x00\x04test", 0) == (6, 'test')
    assert _binarypack.unpack_string(b"\xFF\xFF" + "#"*65535, 0) == (65537, '#'*65535)

def test_unpack_bstring():
    assert _binarypack.unpack_bstring(b"\x00\x00", 0) == (2, '')
    assert _binarypack.unpack_bstring(b"\x00\x04test", 0) == (6, 'test')
    assert _binarypack.unpack_bstring(b"\x00\x05_TRUE", 0) == (7, True)
    assert _binarypack.unpack_bstring(b"\x00\x06_FALSE", 0) == (8, False)
    assert _binarypack.unpack_bstring(b"\xFF\xFF" + "#"*65535, 0) == (65537, '#'*65535)

def test_unpack_json():
    assert _binarypack.unpack_json(b"\x00\x04null", 0) == (6, None)
    assert _binarypack.unpack_json(b"\x00\x0B{\"test\": 1}", 0) == (13, {'test': 1})

def test_unpack_Bl():
    assert _binarypack.unpack_Bl(b"\x00", 0) == (1, [])
    assert _binarypack.unpack_Bl(b"\x03\x01\x02\x03", 0) == (4, [1, 2, 3])

def test_unpack_Hl():
    assert _binarypack.unpack_Hl(b"\x00", 0) == (1, [])
    assert _binarypack.unpack_Hl(b"\x03\x00\x01\x00\x02\x00\x03", 0) == (7, [1, 2, 3])

def test_unpack_Il():
    assert _binarypack.unpack_Il(b"\x00", 0) == (1, [])
    assert _binarypack.unpack_Il(b"\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03", 0) == (13, [1, 2, 3])

def test_unpack_pl():
    assert _binarypack.unpack_pl(b"\x00\x00", 0) == (2, [])
    assert _binarypack.unpack_pl(
        b'\x00\x02\n\x00\x12\x00\x07unknown\x00\x07' \
        b'unknown\n\x00\x12\x00\x07unknown\x00\x07unknown'
    , 0) == (44, [packets.PacketLogin(), packets.PacketLogin()])

def test_unpack_money():
    assert _binarypack.unpack_money(b"\x00\x00", 0) == (2, {})
    assert _binarypack.unpack_money(
        b'\x00\x01\x00\x00\x00\x01\x00\x00' \
        b'\x00\x00\x00\x00\x00\x01\x00\x00' \
        b'\x00\x00\x00\x00\x00\x02\x00\x00' \
        b'\x00\x00\x00\x00\x00\x03'
    , 0) == (30, {1: (1, 2, 3)})

def test_unpack_players():
    assert _binarypack.unpack_players(b'\x00\x00', 0) == (2, [])
    assert _binarypack.unpack_players(b'\x00\x01\x00\x04name\x00\x00\x00\n\x00', 0) == (13, [('name', 10, 0)])

def test_unpack_c():
    assert _binarypack.unpack_c(b"\x00\x00\x00\x00", 0) == (4, [])
    assert _binarypack.unpack_c(b"\x00\x00\x03\xE8", 0) == (4, [1, 1000])
