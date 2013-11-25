# -*- coding: utf-8 -*-

from pokerpackets import binarypack, packets

# import networkpackets so they get tested as well
import pokerpackets.networkpackets


# public functions

def test_pack_unpack():
    "iterates over all packet types, packs and unpacks them and see if the result package equals the original packet"

    def check_pack_unpack(packet_type):
        packet = packet_type()
        packed = binarypack.pack(packet)

        unpack_offset, unpack_packet = binarypack.unpack(packed)
        assert unpack_packet == packet
        assert unpack_offset > 0

    for type_id, packet_type in packets.type_id2type.iteritems():
        yield check_pack_unpack, packet_type

# private functions

def test__pack_I():
    buf = [] ; assert binarypack._pack_I(0, buf) == 4 ; assert "".join(buf) == b"\x00\x00\x00\x00"
    buf = [] ; assert binarypack._pack_I(1, buf) == 4 ; assert "".join(buf) == b"\x00\x00\x00\x01"
    buf = [] ; assert binarypack._pack_I(4294967295, buf) == 4 ; assert "".join(buf) == b"\xFF\xFF\xFF\xFF"

def test__pack_Q():
    buf = [] ; assert binarypack._pack_Q(0, buf) == 8 ; assert "".join(buf) == b"\x00\x00\x00\x00\x00\x00\x00\x00"
    buf = [] ; assert binarypack._pack_Q(1, buf) == 8 ; assert "".join(buf) == b"\x00\x00\x00\x00\x00\x00\x00\x01"
    buf = [] ; assert binarypack._pack_Q(18446744073709551615L, buf) == 8 ; assert "".join(buf) == b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF"

def test__pack_B():
    buf = [] ; assert binarypack._pack_B(0, buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert binarypack._pack_B(1, buf) == 1 ; assert "".join(buf) == b"\x01"
    buf = [] ; assert binarypack._pack_B(255, buf) == 1 ; assert "".join(buf) == b"\xFF"

def test__pack_b():
    buf = [] ; assert binarypack._pack_b(0, buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert binarypack._pack_b(10, buf) == 1 ; assert "".join(buf) == b"\x0A"
    buf = [] ; assert binarypack._pack_b(-1, buf) == 1 ; assert "".join(buf) == b"\xFF"

def test__pack_Bnone():
    buf = [] ; assert binarypack._pack_Bnone(0, buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert binarypack._pack_Bnone(10, buf) == 1 ; assert "".join(buf) == b"\x0A"
    buf = [] ; assert binarypack._pack_Bnone(None, buf) == 1 ; assert "".join(buf) == b"\xFF"

def test__pack_bool():
    buf = [] ; assert binarypack._pack_bool(5, buf) == 1 ; assert "".join(buf) == b"\x01"
    buf = [] ; assert binarypack._pack_bool(True, buf) == 1 ; assert "".join(buf) == b"\x01"
    buf = [] ; assert binarypack._pack_bool(False, buf) == 1 ; assert "".join(buf) == b"\x00"

def test__pack_cbool():
    buf = [] ; assert binarypack._pack_cbool('y', buf) == 1 ; assert "".join(buf) == b"\x01"
    buf = [] ; assert binarypack._pack_cbool('n', buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert binarypack._pack_cbool('test', buf) == 1 ; assert "".join(buf) == b"\x00"

def test__pack_H():
    buf = [] ; assert binarypack._pack_H(0, buf) == 2 ; assert "".join(buf) == b"\x00\x00"
    buf = [] ; assert binarypack._pack_H(1, buf) == 2 ; assert "".join(buf) == b"\x00\x01"
    buf = [] ; assert binarypack._pack_H(65535, buf) == 2 ; assert "".join(buf) == b"\xFF\xFF"

def test__pack_string():
    buf = [] ; assert binarypack._pack_string("", buf) == 2 ; assert "".join(buf) == b"\x00\x00"
    buf = [] ; assert binarypack._pack_string("test", buf) == 6 ; assert "".join(buf) == b"\x00\x04test"
    buf = [] ; assert binarypack._pack_string(u"übel".encode("utf-8"), buf) == 7 ; assert "".join(buf) == b"\x00\x05\xC3\xBCbel"

def test__pack_bstring():
    buf = [] ; assert binarypack._pack_bstring("", buf) == 2 ; assert "".join(buf) == b"\x00\x00"
    buf = [] ; assert binarypack._pack_bstring("test", buf) == 6 ; assert "".join(buf) == b"\x00\x04test"
    buf = [] ; assert binarypack._pack_bstring(True, buf) == 7 ; assert "".join(buf) == b"\x00\x05_TRUE"
    buf = [] ; assert binarypack._pack_bstring(False, buf) == 8 ; assert "".join(buf) == b"\x00\x06_FALSE"

def test__pack_j():
    buf = [] ; assert binarypack._pack_j(None, buf) == 6 ; assert "".join(buf) == b"\x00\x04null"
    buf = [] ; assert binarypack._pack_j({'test': 1}, buf) == 13 ; assert "".join(buf) == b"\x00\x0B{\"test\": 1}"

def test__pack_Bl():
    buf = [] ; assert binarypack._pack_Bl([], buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert binarypack._pack_Bl([1, 2, 3], buf) == 4 ; assert "".join(buf) == b"\x03\x01\x02\x03"

def test__pack_Hl():
    buf = [] ; assert binarypack._pack_Hl([], buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert binarypack._pack_Hl([1, 2, 3], buf) == 7 ; assert "".join(buf) == b"\x03\x00\x01\x00\x02\x00\x03"

def test__pack_Il():
    buf = [] ; assert binarypack._pack_Il([], buf) == 1 ; assert "".join(buf) == b"\x00"
    buf = [] ; assert binarypack._pack_Il([1, 2, 3], buf) == 13 ; assert "".join(buf) == b"\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03"

def test__pack_pl():
    buf = [] ; assert binarypack._pack_pl([], buf) == 2 ; assert "".join(buf) == b"\x00\x00"
    buf = [] ; assert binarypack._pack_pl([packets.PacketLogin(), packets.PacketLogin()], buf) == 44 ; assert "".join(buf) == \
        b'\x00\x02\n\x00\x12\x00\x07unknown\x00\x07' \
        b'unknown\n\x00\x12\x00\x07unknown\x00\x07unknown'

def test__pack_money():
    buf = [] ; assert binarypack._pack_money({}, buf) == 2 ; assert "".join(buf) == b"\x00\x00"
    buf = [] ; assert binarypack._pack_money({1: (1, 2, 3)}, buf) == 30 ; assert "".join(buf) == \
        b'\x00\x01\x00\x00\x00\x01\x00\x00' \
        b'\x00\x00\x00\x00\x00\x01\x00\x00' \
        b'\x00\x00\x00\x00\x00\x02\x00\x00' \
        b'\x00\x00\x00\x00\x00\x03'

def test__pack_players():
    buf = [] ; assert binarypack._pack_players([], buf) == 2 ; assert "".join(buf) == b"\x00\x00"
    buf = [] ; assert binarypack._pack_players([('name', 10, 0)], buf) == 13 ; assert "".join(buf) == b"\x00\x01\x00\x04name\x00\x00\x00\n\x00"

def test__pack_c():
    buf = [] ; assert binarypack._pack_c([], buf) == 4 ; assert "".join(buf) == b"\x00\x00\x00\x00"
    buf = [] ; assert binarypack._pack_c([10, 100], buf) == 4 ; assert "".join(buf) == b"\x00\x00\x03\xE8"

def test__unpack_I():
    assert binarypack._unpack_I(b"\x00\x00\x00\x00", 0) == (4, 0)
    assert binarypack._unpack_I(b"\x00\x00\x00\x01", 0) == (4, 1)
    assert binarypack._unpack_I(b"\xFF\xFF\xFF\xFF", 0) == (4, 4294967295)

def test__unpack_Q():
    assert binarypack._unpack_Q(b"\x00\x00\x00\x00\x00\x00\x00\x00", 0) == (8, 0)
    assert binarypack._unpack_Q(b"\x00\x00\x00\x00\x00\x00\x00\x01", 0) == (8, 1)
    assert binarypack._unpack_Q(b"\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF", 0) == (8, 18446744073709551615L)

def test__unpack_B():
    assert binarypack._unpack_B(b"\x00", 0) == (1, 0)
    assert binarypack._unpack_B(b"\x01", 0) == (1, 1)
    assert binarypack._unpack_B(b"\xFF", 0) == (1, 255)

def test__unpack_b():
    assert binarypack._unpack_b(b"\x00", 0) == (1, 0)
    assert binarypack._unpack_b(b"\x01", 0) == (1, 1)
    assert binarypack._unpack_b(b"\xFF", 0) == (1, -1)

def test__unpack_Bnone():
    assert binarypack._unpack_Bnone(b"\x00", 0) == (1, 0)
    assert binarypack._unpack_Bnone(b"\x01", 0) == (1, 1)
    assert binarypack._unpack_Bnone(b"\xFF", 0) == (1, None)

def test__unpack_bool():
    assert binarypack._unpack_bool(b"\x00", 0) == (1, False)
    assert binarypack._unpack_bool(b"\x01", 0) == (1, True)
    assert binarypack._unpack_bool(b"\xFF", 0) == (1, True)

def test__unpack_cbool():
    assert binarypack._unpack_cbool(b"\x00", 0) == (1, 'n')
    assert binarypack._unpack_cbool(b"\x01", 0) == (1, 'y')
    assert binarypack._unpack_cbool(b"\x0F", 0) == (1, 'y')

def test__unpack_H():
    assert binarypack._unpack_H(b"\x00\x00", 0) == (2, 0)
    assert binarypack._unpack_H(b"\x00\x01", 0) == (2, 1)
    assert binarypack._unpack_H(b"\xFF\xFF", 0) == (2, 65535)

def test__unpack_string():
    assert binarypack._unpack_string(b"\x00\x00", 0) == (2, '')
    assert binarypack._unpack_string(b"\x00\x04test", 0) == (6, 'test')
    assert binarypack._unpack_string(b"\xFF\xFF" + "#"*65535, 0) == (65537, '#'*65535)

def test__unpack_bstring():
    assert binarypack._unpack_bstring(b"\x00\x00", 0) == (2, '')
    assert binarypack._unpack_bstring(b"\x00\x04test", 0) == (6, 'test')
    assert binarypack._unpack_bstring(b"\x00\x05_TRUE", 0) == (7, True)
    assert binarypack._unpack_bstring(b"\x00\x06_FALSE", 0) == (8, False)
    assert binarypack._unpack_bstring(b"\xFF\xFF" + "#"*65535, 0) == (65537, '#'*65535)

def test__unpack_json():
    assert binarypack._unpack_json(b"\x00\x04null", 0) == (6, None)
    assert binarypack._unpack_json(b"\x00\x0B{\"test\": 1}", 0) == (13, {'test': 1})

def test__unpack_Bl():
    assert binarypack._unpack_Bl(b"\x00", 0) == (1, [])
    assert binarypack._unpack_Bl(b"\x03\x01\x02\x03", 0) == (4, [1, 2, 3])

def test__unpack_Hl():
    assert binarypack._unpack_Hl(b"\x00", 0) == (1, [])
    assert binarypack._unpack_Hl(b"\x03\x00\x01\x00\x02\x00\x03", 0) == (7, [1, 2, 3])

def test__unpack_Il():
    assert binarypack._unpack_Il(b"\x00", 0) == (1, [])
    assert binarypack._unpack_Il(b"\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03", 0) == (13, [1, 2, 3])

def test__unpack_pl():
    assert binarypack._unpack_pl(b"\x00\x00", 0) == (2, [])
    assert binarypack._unpack_pl(
        b'\x00\x02\n\x00\x12\x00\x07unknown\x00\x07' \
        b'unknown\n\x00\x12\x00\x07unknown\x00\x07unknown'
    , 0) == (44, [packets.PacketLogin(), packets.PacketLogin()])

def test__unpack_money():
    assert binarypack._unpack_money(b"\x00\x00", 0) == (2, {})
    assert binarypack._unpack_money(
        b'\x00\x01\x00\x00\x00\x01\x00\x00' \
        b'\x00\x00\x00\x00\x00\x01\x00\x00' \
        b'\x00\x00\x00\x00\x00\x02\x00\x00' \
        b'\x00\x00\x00\x00\x00\x03'
    , 0) == (30, {1: (1, 2, 3)})

def test__unpack_players():
    assert binarypack._unpack_players(b'\x00\x00', 0) == (2, [])
    assert binarypack._unpack_players(b'\x00\x01\x00\x04name\x00\x00\x00\n\x00', 0) == (13, [('name', 10, 0)])

def test__unpack_c():
    assert binarypack._unpack_c(b"\x00\x00\x00\x00", 0) == (4, [])
    assert binarypack._unpack_c(b"\x00\x00\x03\xE8", 0) == (4, [1, 1000])
