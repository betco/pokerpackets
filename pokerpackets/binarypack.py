
from pokerpackets import log as packet_log
log = packet_log.get_child('binarypack')

from pokerpackets import packets

import simplejson
from struct import Struct

def pack(packet):
    """
    pack a packet

    packet: subclass of Packet

    returns: head + content of packet as binary data (string)
    """
    packet_type = packet.__class__
    type_id = packets.type2type_id[packet_type]

    data = []
    for attr, default, s_type in packet_type.info:
        if s_type == 'no net':
            continue
        try:
            data.append(_s_type2pack[s_type](packet.__dict__.get(attr, default)))
        except:
            log.error("failed to pack, s_type %s, attr %s, value %r", s_type, attr, packet.__dict__.get(attr))

    data = ''.join(data)
    return _s_packet_head.pack(type_id, len(data)) + data

def unpack(data, offset=0):
    """
    unpack a binary packed packet

    data: head + content of packet as binary data (string)

    returns: packet
    """

    # parse packet head
    type_id, length = _s_packet_head.unpack_from(data, offset)

    # get packet class
    packet_type = packets.type_id2type[type_id]

    packet = packet_type()
    offset += _s_packet_head.size
    for attr, default, s_type in packet_type.info:
        if s_type == 'no net':
            continue
        offset, val = _s_type2unpack[s_type](data, offset)
        if val != default:
            packet.__dict__[attr] = val

    return (offset, packet)

def _pack_b(val):
    return _s_B.pack(255 if val == -1 else val)

def _pack_Bnone(val):
    return _s_B.pack(255 if val == None else val)

def _pack_bool(val):
    return _s_B.pack(1 if val else 0)

def _pack_cbool(val):
    return _s_B.pack(1 if val == 'y' else 0)

def _pack_string(val):
    return _s_H.pack(len(val)) + val

def _pack_bstring(val):
    if val == True: val = '_TRUE'
    elif val == False: val = '_FALSE'
    return _s_H.pack(len(val)) + val

def _pack_j(val):
    val = simplejson.dumps(val)
    return _s_H.pack(len(val)) + val

def _pack_Bl(_list):
    struct_format = '!B%dB' % (len(_list),)
    try:
        struct = _struct_cache[struct_format]
    except KeyError:
        struct = Struct(struct_format)
        _struct_cache[struct_format] = struct
    return struct.pack(len(_list), *_list)

def _pack_Hl(_list):
    struct_format = '!B%dH' % (len(_list),)
    try:
        struct = _struct_cache[struct_format]
    except KeyError:
        struct = Struct(struct_format)
        _struct_cache[struct_format] = struct
    return struct.pack(len(_list), *_list)

def _pack_Il(_list):
    struct_format = '!B%dI' % (len(_list),)
    try:
        struct = _struct_cache[struct_format]
    except KeyError:
        struct = Struct(struct_format)
        _struct_cache[struct_format] = struct
    return struct.pack(len(_list), *_list)

def _pack_pl(packets):
    return _s_H.pack(len(packets)) + ''.join([pack(packet) for packet in packets])

def _pack_money(val):
    data = _s_H.pack(len(val))
    for currency, (money, in_game, points) in val.iteritems():
        data += _s_money.pack(currency, money, in_game, points)
    return data

def _pack_players(players):
    data = b""
    data += _s_H.pack(len(players))
    for name, chips, flags in players:
        data += _s_H.pack(len(name)) + name
        data += _s_IB.pack(chips, flags)
    return data

def _pack_c(chips):
    amount = 0
    for i in xrange(len(chips) / 2):
        amount += chips[i * 2] * chips[i * 2 + 1]
    return _s_I.pack(amount)

def _unpack_I(data, offset):
    value, = _s_I.unpack_from(data, offset)
    return (offset + _s_I.size, value)

def _unpack_Q(data, offset):
    value, = _s_Q.unpack_from(data, offset)
    return (offset + _s_Q.size, value)

def _unpack_B(data, offset):
    value, = _s_B.unpack_from(data, offset)
    return (offset + _s_B.size, value)

def _unpack_b(data, offset):
    value, = _s_B.unpack_from(data, offset)
    return (offset + _s_B.size, -1 if value == 255 else value)

def _unpack_Bnone(data, offset):
    value, = _s_B.unpack_from(data, offset)
    return (offset + _s_B.size, None if value == 255 else value)

def _unpack_bool(data, offset):
    value, = _s_B.unpack_from(data, offset)
    return (offset + _s_B.size, value != 0)

def _unpack_cbool(data, offset):
    value, = _s_B.unpack_from(data, offset)
    return (offset + _s_B.size, 'y' if value != 0 else 'n')

def _unpack_H(data, offset):
    value, = _s_H.unpack_from(data, offset)
    return (offset + _s_H.size, value)

def _unpack_string(data, offset):
    length, = _s_H.unpack_from(data, offset)
    return (offset + _s_H.size + length, data[offset + _s_H.size:offset + _s_H.size + length])

def _unpack_bstring(data, offset):
    length, = _s_H.unpack_from(data, offset)
    value = data[offset + _s_H.size:offset + _s_H.size + length]
    if value == '_TRUE': value = True
    elif value == '_FALSE': value = False
    return (offset + _s_H.size + length, value)

def _unpack_json(data, offset):
    length, = _s_H.unpack_from(data, offset)
    return(offset + _s_H.size + length, simplejson.loads(data[offset + _s_H.size:offset + _s_H.size + length]))

def _unpack_Bl(data, offset):
    length, = _s_B.unpack_from(data, offset)
    struct_format = '!%dB' % (length,)
    try:
        struct = _struct_cache[struct_format]
    except KeyError:
        struct = Struct(struct_format)
        _struct_cache[struct_format] = struct
    return(
        offset + _s_B.size + struct.size,
        list(struct.unpack_from(data, offset + _s_B.size)) if length else []
    )

def _unpack_Hl(data, offset):
    length, = _s_B.unpack_from(data, offset)
    struct_format = '!%dH' % (length,)
    try:
        struct = _struct_cache[struct_format]
    except KeyError:
        struct = Struct(struct_format)
        _struct_cache[struct_format] = struct
    return(
        offset + _s_B.size + struct.size,
        list(struct.unpack_from(data, offset + _s_B.size)) if length else []
    )

def _unpack_Il(data, offset):
    length, = _s_B.unpack_from(data, offset)
    struct_format = '!%dI' % (length,)
    try:
        struct = _struct_cache[struct_format]
    except KeyError:
        struct = Struct(struct_format)
        _struct_cache[struct_format] = struct
    return(
        offset + _s_B.size + struct.size,
        list(struct.unpack_from(data, offset + _s_B.size)) if length else []
    )

def _unpack_pl(data, offset):
    length, = _s_H.unpack_from(data, offset)
    packets = []
    j = offset + _s_H.size
    for i in xrange(length):
        j, packet = unpack(data, j)
        packets.append(packet)
    return (j, packets)

def _unpack_money(data, offset):
    length, = _s_H.unpack_from(data, offset)
    money = {}
    for i in xrange(length):
        currency, amount, in_game, points = _s_money.unpack_from(data, offset + _s_H.size + (_s_money.size * i))
        money[currency] = (amount, in_game, points)
    return (offset + _s_H.size + (_s_money.size * length), money)

def _unpack_players(data, offset):
    length, = _s_H.unpack_from(data, offset)
    players = []
    j = offset + _s_H.size
    for i in xrange(length):
        j, name = _unpack_string(data, j)
        j, chips = _unpack_I(data, j)
        j, flags = _unpack_B(data, j)
        players.append((name, chips, flags))
    return (j, players)

def _unpack_c(data, offset):
    amount, = _s_I.unpack_from(data, offset)
    return (offset + _s_I.size, [1, amount] if amount else [])

# compiled structs
_s_I = Struct('!I')
_s_H = Struct('!H')
_s_Q = Struct('!Q')
_s_B = Struct('!B')
_s_IB = Struct('!IB')
_s_packet_head = Struct("!BH")
_s_money = Struct('!IQQQ')

_struct_cache = {}

_s_type2pack = {
    'I': _s_I.pack,
    'Q': _s_Q.pack,
    'B': _s_B.pack,
    'b': _pack_b,
    'Bnone': _pack_Bnone,
    'bool': _pack_bool,
    'cbool': _pack_cbool,
    'H': _s_H.pack,
    's': _pack_string,
    'bs': _pack_bstring,
    'j': _pack_j,
    'Bl': _pack_Bl,
    'Hl': _pack_Hl,
    'Il': _pack_Il,
    'pl': _pack_pl,
    'money': _pack_money,
    'players': _pack_players,
    'c': _pack_c,
}

_s_type2unpack = {
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
    'pl': _unpack_pl,
    'money': _unpack_money,
    'players': _unpack_players,
    'c': _unpack_c,
}

__all__ = ['pack', 'unpack']
