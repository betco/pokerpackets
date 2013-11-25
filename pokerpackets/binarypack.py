
from pokerpackets.packets import type2type_id, type_id2type
import pokerpackets.networkpackets # pylint: disable=W0611
import pokerpackets.clientpackets # pylint: disable=W0611

import simplejson
from struct import Struct

def pack(packet):
    """
    pack a packet

    packet: subclass of Packet

    returns: head + content of packet as binary data (string)
    """

    if '_binarypack_fast_pack' in packet.__class__.__dict__:
        # print 'fast pack', packet.info
        return packet._binarypack_fast_pack()

    buf = []
    _pack(packet, buf)
    return b''.join(buf)

def _pack(packet, buf):
    packet_type = packet.__class__
    type_id = type2type_id[packet_type]

    buf_pos = len(buf)

    buf.append(None)

    length = sum([_S_TYPE2PACK[s_type](getattr(packet, attr), buf) for attr, s_type in packet_type._binarypack_info])

    buf[buf_pos] = _S_PACKET_HEAD.pack(type_id, length)

    return _S_PACKET_HEAD.size + length

def unpack(data, offset=0):
    """
    unpack a binary packed packet

    data: head + content of packet as binary data (string)

    returns: packet
    """

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

def _pack_I(val, buf):
    buf.append(_S_I.pack(val))
    return _S_I.size

def _pack_Q(val, buf):
    buf.append(_S_Q.pack(val))
    return _S_Q.size

def _pack_B(val, buf):
    buf.append(_S_B.pack(val))
    return _S_B.size

def _pack_b(val, buf):
    buf.append(_S_B.pack(255 if val == -1 else val))
    return _S_B.size

def _pack_Bnone(val, buf):
    buf.append(_S_B.pack(255 if val == None else val))
    return _S_B.size

def _pack_bool(val, buf):
    buf.append(_S_B.pack(1 if val else 0))
    return _S_B.size

def _pack_cbool(val, buf):
    buf.append(_S_B.pack(1 if val == 'y' else 0))
    return _S_B.size

def _pack_H(val, buf):
    buf.append(_S_H.pack(val))
    return _S_H.size

def _pack_string(val, buf):
    val_len = len(val)
    buf.append(_S_H.pack(val_len))
    buf.append(val)
    return _S_H.size + val_len

def _pack_bstring(val, buf):
    if val == True: val = '_TRUE'
    elif val == False: val = '_FALSE'
    val_len = len(val)
    buf.append(_S_H.pack(val_len))
    buf.append(val)
    return _S_H.size + val_len

def _pack_j(val, buf):
    val = simplejson.dumps(val)
    val_len = len(val)
    buf.append(_S_H.pack(val_len))
    buf.append(val)
    return _S_H.size + val_len

def _pack_Bl(_list, buf, __cache={}): # pylint: disable=W0102
    list_len = len(_list)
    try:
        struct = __cache[list_len]
    except KeyError:
        struct = __cache[list_len] = Struct('!B'+str(list_len)+'B')
    buf.append(struct.pack(list_len, *_list))
    return struct.size

def _pack_Hl(_list, buf, __cache={}): # pylint: disable=W0102
    list_len = len(_list)
    try:
        struct = __cache[list_len]
    except KeyError:
        struct = __cache[list_len] = Struct('!B'+str(list_len)+'H')
    buf.append(struct.pack(list_len, *_list))
    return struct.size

def _pack_Il(_list, buf, __cache={}): # pylint: disable=W0102
    list_len = len(_list)
    try:
        struct = __cache[list_len]
    except KeyError:
        struct = __cache[list_len] = Struct('!B'+str(list_len)+'I')
    buf.append(struct.pack(list_len, *_list))
    return struct.size

def _pack_il(_list, buf, __cache={}): # pylint: disable=W0102
    list_len = len(_list)
    try:
        struct = __cache[list_len]
    except KeyError:
        struct = __cache[list_len] = Struct('!B'+str(list_len)+'i')
    buf.append(struct.pack(list_len, *_list))
    return struct.size

def _pack_pl(packets, buf):
    packets_len = len(packets)
    buf.append(_S_H.pack(packets_len))
    length = sum([_pack(packet, buf) for packet in packets])
    return _S_H.size + length

def _pack_money(val, buf):
    val_len = len(val)
    buf.append(_S_H.pack(val_len))
    for currency, (money, in_game, points) in val.iteritems():
        buf.append(_S_MONEY.pack(currency, money, in_game, points))
    return _S_H.size + _S_MONEY.size * val_len

def _pack_players(players, buf):
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

def _pack_c(chips, buf):
    amount = 0
    for i in xrange(len(chips) / 2):
        amount += chips[i * 2] * chips[i * 2 + 1]
    buf.append(_S_I.pack(amount))
    return _S_I.size

def _unpack_I(data, offset):
    value, = _S_I.unpack_from(data, offset)
    return (offset + _S_I.size, value)

def _unpack_Q(data, offset):
    value, = _S_Q.unpack_from(data, offset)
    return (offset + _S_Q.size, value)

def _unpack_B(data, offset):
    value, = _S_B.unpack_from(data, offset)
    return (offset + _S_B.size, value)

def _unpack_b(data, offset):
    value, = _S_B.unpack_from(data, offset)
    return (offset + _S_B.size, -1 if value == 255 else value)

def _unpack_Bnone(data, offset):
    value, = _S_B.unpack_from(data, offset)
    return (offset + _S_B.size, None if value == 255 else value)

def _unpack_bool(data, offset):
    value, = _S_B.unpack_from(data, offset)
    return (offset + _S_B.size, value != 0)

def _unpack_cbool(data, offset):
    value, = _S_B.unpack_from(data, offset)
    return (offset + _S_B.size, 'y' if value != 0 else 'n')

def _unpack_H(data, offset):
    value, = _S_H.unpack_from(data, offset)
    return (offset + _S_H.size, value)

def _unpack_string(data, offset):
    length, = _S_H.unpack_from(data, offset)
    return (offset + _S_H.size + length, data[offset + _S_H.size:offset + _S_H.size + length])

def _unpack_bstring(data, offset):
    length, = _S_H.unpack_from(data, offset)
    value = data[offset + _S_H.size:offset + _S_H.size + length]
    if value == '_TRUE': value = True
    elif value == '_FALSE': value = False
    return (offset + _S_H.size + length, value)

def _unpack_json(data, offset):
    length, = _S_H.unpack_from(data, offset)
    return(offset + _S_H.size + length, simplejson.loads(data[offset + _S_H.size:offset + _S_H.size + length]))

def _unpack_Bl(data, offset, __cache={}): # pylint: disable=W0102
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

def _unpack_Hl(data, offset, __cache={}): # pylint: disable=W0102
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

def _unpack_Il(data, offset, __cache={}): # pylint: disable=W0102
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

def _unpack_il(data, offset, __cache={}): # pylint: disable=W0102
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

def _unpack_pl(data, offset):
    length, = _S_H.unpack_from(data, offset)
    packets = []
    j = offset + _S_H.size
    for _ in xrange(length):
        j, packet = unpack(data, j)
        packets.append(packet)
    return (j, packets)

def _unpack_money(data, offset):
    length, = _S_H.unpack_from(data, offset)
    money = {}
    for i in xrange(length):
        currency, amount, in_game, points = _S_MONEY.unpack_from(data, offset + _S_H.size + (_S_MONEY.size * i))
        money[currency] = (amount, in_game, points)
    return (offset + _S_H.size + (_S_MONEY.size * length), money)

def _unpack_players(data, offset):
    length, = _S_H.unpack_from(data, offset)
    players = []
    j = offset + _S_H.size
    for _ in xrange(length):
        j, name = _unpack_string(data, j)
        j, chips = _unpack_I(data, j)
        j, flags = _unpack_B(data, j)
        players.append((name, chips, flags))
    return (j, players)

def _unpack_c(data, offset):
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
    'I': _pack_I,
    'Q': _pack_Q,
    'B': _pack_B,
    'b': _pack_b,
    'Bnone': _pack_Bnone,
    'bool': _pack_bool,
    'cbool': _pack_cbool,
    'H': _pack_H,
    's': _pack_string,
    'bs': _pack_bstring,
    'j': _pack_j,
    'Bl': _pack_Bl,
    'Hl': _pack_Hl,
    'Il': _pack_Il,
    'il': _pack_il,
    'pl': _pack_pl,
    'money': _pack_money,
    'players': _pack_players,
    'c': _pack_c,
}

_S_TYPE2UNPACK = {
    'I': _unpack_I,
    'Q': _unpack_Q,
    'B': _unpack_B,
    'b': _unpack_b,
    'Bnone': _unpack_Bnone,
    'bool': _unpack_bool,
    'cbool': _unpack_cbool,
    'H': _unpack_H,
    's': _unpack_string,
    'bs': _unpack_bstring,
    'j': _unpack_json,
    'Bl': _unpack_Bl,
    'Hl': _unpack_Hl,
    'Il': _unpack_Il,
    'il': _unpack_il,
    'pl': _unpack_pl,
    'money': _unpack_money,
    'players': _unpack_players,
    'c': _unpack_c,
}

__all__ = ['pack', 'unpack']
