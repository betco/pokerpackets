
from pokerpackets.packets import type2type_id, type_id2type
import pokerpackets.networkpackets # pylint: disable=W0611
import pokerpackets.clientpackets # pylint: disable=W0611

import simplejson
from struct import Struct

# pylint: disable=C0111

def pack(packet, buf):
    packet_type = packet.__class__
    type_id = type2type_id[packet_type]

    buf_pos = len(buf)

    buf.append(None)

    length = sum([_S_TYPE2PACK[s_type](getattr(packet, attr), buf) for attr, s_type in packet_type.binarypack_info])

    buf[buf_pos] = _S_PACKET_HEAD.pack(type_id, length)

    return _S_PACKET_HEAD.size + length

def unpack(data, offset=0):
    # parse packet head
    type_id, _length = _S_PACKET_HEAD.unpack_from(data, offset)

    # get packet class
    packet_type = type_id2type[type_id]

    packet = packet_type()
    offset += _S_PACKET_HEAD.size
    for attr, default, s_type in packet_type.info:
        if s_type == 'no net':
            continue
        offset, val = _S_TYPE2UNPACK[s_type](data, offset)
        if val != default:
            packet.__dict__[attr] = val

    return (offset, packet)

def pack_I(val, buf):
    buf.append(_S_I.pack(val))
    return _S_I.size

def pack_Q(val, buf):
    buf.append(_S_Q.pack(val))
    return _S_Q.size

def pack_B(val, buf):
    buf.append(_S_B.pack(val))
    return _S_B.size

def pack_b(val, buf):
    buf.append(_S_B.pack(255 if val == -1 else val))
    return _S_B.size

def pack_Bnone(val, buf):
    buf.append(_S_B.pack(255 if val == None else val))
    return _S_B.size

def pack_bool(val, buf):
    buf.append(_S_B.pack(1 if val else 0))
    return _S_B.size

def pack_cbool(val, buf):
    buf.append(_S_B.pack(1 if val == 'y' else 0))
    return _S_B.size

def pack_H(val, buf):
    buf.append(_S_H.pack(val))
    return _S_H.size

def pack_string(val, buf):
    val_len = len(val)
    buf.append(_S_H.pack(val_len))
    buf.append(val)
    return _S_H.size + val_len

def pack_bstring(val, buf):
    if val == True: val = '_TRUE'
    elif val == False: val = '_FALSE'
    val_len = len(val)
    buf.append(_S_H.pack(val_len))
    buf.append(val)
    return _S_H.size + val_len

def pack_j(val, buf):
    val = simplejson.dumps(val)
    val_len = len(val)
    buf.append(_S_H.pack(val_len))
    buf.append(val)
    return _S_H.size + val_len

def pack_Bl(_list, buf, __cache={}): # pylint: disable=W0102
    list_len = len(_list)
    try:
        struct = __cache[list_len]
    except KeyError:
        struct = __cache[list_len] = Struct('!B'+str(list_len)+'B')
    buf.append(struct.pack(list_len, *_list))
    return struct.size

def pack_Hl(_list, buf, __cache={}): # pylint: disable=W0102
    list_len = len(_list)
    try:
        struct = __cache[list_len]
    except KeyError:
        struct = __cache[list_len] = Struct('!B'+str(list_len)+'H')
    buf.append(struct.pack(list_len, *_list))
    return struct.size

def pack_Il(_list, buf, __cache={}): # pylint: disable=W0102
    list_len = len(_list)
    try:
        struct = __cache[list_len]
    except KeyError:
        struct = __cache[list_len] = Struct('!B'+str(list_len)+'I')
    buf.append(struct.pack(list_len, *_list))
    return struct.size

def pack_il(_list, buf, __cache={}): # pylint: disable=W0102
    list_len = len(_list)
    try:
        struct = __cache[list_len]
    except KeyError:
        struct = __cache[list_len] = Struct('!B'+str(list_len)+'i')
    buf.append(struct.pack(list_len, *_list))
    return struct.size

def pack_pl(packets, buf):
    packets_len = len(packets)
    buf.append(_S_H.pack(packets_len))
    length = sum([pack(packet, buf) for packet in packets])
    return _S_H.size + length

def pack_money(val, buf):
    val_len = len(val)
    buf.append(_S_H.pack(val_len))
    for currency, (money, in_game, points) in val.iteritems():
        buf.append(_S_MONEY.pack(currency, money, in_game, points))
    return _S_H.size + _S_MONEY.size * val_len

def pack_players(players, buf):
    players_len = len(players)
    buf.append(_S_H.pack(players_len))
    length = 0
    for name, chips, flags in players:
        name_len = len(name)
        buf.append(_S_H.pack(name_len))
        buf.append(name)
        buf.append(_S_IB.pack(chips, flags))
        length += _S_H.size + name_len + _S_IB.size

    return _S_H.size + length

def pack_c(chips, buf):
    amount = 0
    for i in xrange(len(chips) / 2):
        amount += chips[i * 2] * chips[i * 2 + 1]
    buf.append(_S_I.pack(amount))
    return _S_I.size

def unpack_I(data, offset):
    value, = _S_I.unpack_from(data, offset)
    return (offset + _S_I.size, value)

def unpack_Q(data, offset):
    value, = _S_Q.unpack_from(data, offset)
    return (offset + _S_Q.size, value)

def unpack_B(data, offset):
    value, = _S_B.unpack_from(data, offset)
    return (offset + _S_B.size, value)

def unpack_b(data, offset):
    value, = _S_B.unpack_from(data, offset)
    return (offset + _S_B.size, -1 if value == 255 else value)

def unpack_Bnone(data, offset):
    value, = _S_B.unpack_from(data, offset)
    return (offset + _S_B.size, None if value == 255 else value)

def unpack_bool(data, offset):
    value, = _S_B.unpack_from(data, offset)
    return (offset + _S_B.size, value != 0)

def unpack_cbool(data, offset):
    value, = _S_B.unpack_from(data, offset)
    return (offset + _S_B.size, 'y' if value != 0 else 'n')

def unpack_H(data, offset):
    value, = _S_H.unpack_from(data, offset)
    return (offset + _S_H.size, value)

def unpack_string(data, offset):
    length, = _S_H.unpack_from(data, offset)
    return (offset + _S_H.size + length, data[offset + _S_H.size:offset + _S_H.size + length])

def unpack_bstring(data, offset):
    length, = _S_H.unpack_from(data, offset)
    value = data[offset + _S_H.size:offset + _S_H.size + length]
    if value == '_TRUE': value = True
    elif value == '_FALSE': value = False
    return (offset + _S_H.size + length, value)

def unpack_json(data, offset):
    length, = _S_H.unpack_from(data, offset)
    return(offset + _S_H.size + length, simplejson.loads(data[offset + _S_H.size:offset + _S_H.size + length]))

def unpack_Bl(data, offset, __cache={}): # pylint: disable=W0102
    list_len, = _S_B.unpack_from(data, offset)
    struct_format = '!%dB' % (list_len,)
    try:
        struct = __cache[list_len]
    except KeyError:
        __cache[list_len] = struct = Struct(struct_format)
    return(
        offset + _S_B.size + struct.size,
        list(struct.unpack_from(data, offset + _S_B.size)) if list_len else []
    )

def unpack_Hl(data, offset, __cache={}): # pylint: disable=W0102
    list_len, = _S_B.unpack_from(data, offset)
    struct_format = '!%dH' % (list_len,)
    try:
        struct = __cache[list_len]
    except KeyError:
        __cache[list_len] = struct = Struct(struct_format)
    return(
        offset + _S_B.size + struct.size,
        list(struct.unpack_from(data, offset + _S_B.size)) if list_len else []
    )

def unpack_Il(data, offset, __cache={}): # pylint: disable=W0102
    list_len, = _S_B.unpack_from(data, offset)
    struct_format = '!%dI' % (list_len,)
    try:
        struct = __cache[list_len]
    except KeyError:
        __cache[list_len] = struct = Struct(struct_format)
    return(
        offset + _S_B.size + struct.size,
        list(struct.unpack_from(data, offset + _S_B.size)) if list_len else []
    )

def unpack_il(data, offset, __cache={}): # pylint: disable=W0102
    list_len, = _S_B.unpack_from(data, offset)
    struct_format = '!%di' % (list_len,)
    try:
        struct = __cache[list_len]
    except KeyError:
        __cache[list_len] = struct = Struct(struct_format)
    return(
        offset + _S_B.size + struct.size,
        list(struct.unpack_from(data, offset + _S_B.size)) if list_len else []
    )

def unpack_pl(data, offset):
    length, = _S_H.unpack_from(data, offset)
    packets = []
    j = offset + _S_H.size
    for _ in xrange(length):
        j, packet = unpack(data, j)
        packets.append(packet)
    return (j, packets)

def unpack_money(data, offset):
    length, = _S_H.unpack_from(data, offset)
    money = {}
    for i in xrange(length):
        currency, amount, in_game, points = _S_MONEY.unpack_from(data, offset + _S_H.size + (_S_MONEY.size * i))
        money[currency] = (amount, in_game, points)
    return (offset + _S_H.size + (_S_MONEY.size * length), money)

def unpack_players(data, offset):
    length, = _S_H.unpack_from(data, offset)
    players = []
    j = offset + _S_H.size
    for _ in xrange(length):
        j, name = unpack_string(data, j)
        j, chips = unpack_I(data, j)
        j, flags = unpack_B(data, j)
        players.append((name, chips, flags))
    return (j, players)

def unpack_c(data, offset):
    amount, = _S_I.unpack_from(data, offset)
    return (offset + _S_I.size, [1, amount] if amount else [])

# compiled structs
_S_I = Struct('!I')
_S_H = Struct('!H')
_S_Q = Struct('!Q')
_S_B = Struct('!B')
_S_IB = Struct('!IB')
_S_PACKET_HEAD = Struct("!BH")
_S_MONEY = Struct('!IQQQ')

_S_TYPE2PACK = {
    'I': pack_I,
    'Q': pack_Q,
    'B': pack_B,
    'b': pack_b,
    'Bnone': pack_Bnone,
    'bool': pack_bool,
    'cbool': pack_cbool,
    'H': pack_H,
    's': pack_string,
    'bs': pack_bstring,
    'j': pack_j,
    'Bl': pack_Bl,
    'Hl': pack_Hl,
    'Il': pack_Il,
    'il': pack_il,
    'pl': pack_pl,
    'money': pack_money,
    'players': pack_players,
    'c': pack_c,
}

_S_TYPE2UNPACK = {
    'I': unpack_I,
    'Q': unpack_Q,
    'B': unpack_B,
    'b': unpack_b,
    'Bnone': unpack_Bnone,
    'bool': unpack_bool,
    'cbool': unpack_cbool,
    'H': unpack_H,
    's': unpack_string,
    'bs': unpack_bstring,
    'j': unpack_json,
    'Bl': unpack_Bl,
    'Hl': unpack_Hl,
    'Il': unpack_Il,
    'il': unpack_il,
    'pl': unpack_pl,
    'money': unpack_money,
    'players': unpack_players,
    'c': unpack_c,
}
