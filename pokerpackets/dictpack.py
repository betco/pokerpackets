
from traceback import format_exc

from pokerpackets.packets import type2type_id, name2type, type_id2type, PacketError, type2name
import pokerpackets.networkpackets # pylint: disable=W0611
import pokerpackets.clientpackets # pylint: disable=W0611

from numbers import Integral

def pack(packet, numeric_type=True):
    "Pack a packet into a dictionary"
    try:
        packet_dict = {
            'type': type2type_id[packet.__class__] if numeric_type else type2name[packet.__class__]
        }
    except KeyError:
        return packet2dict(PacketError(
            message="Error converting packet to dict %s: %s" % (repr(packet), format_exc())
        ), numeric_type)

    for attr, _default, s_type in packet.__class__.info:
        if s_type is 'no net' or attr is 'type':
            continue

        elif s_type is 'pl':
            packet_dict[attr] = [packet2dict(p, numeric_type) for p in getattr(packet, attr)]

        elif s_type is 'money':
            money = getattr(packet, attr)
            packet_dict[attr] = dict([(k if isinstance(k, Integral) else 'X' + k, v) for k, v in money.items()])

        else:
            packet_dict[attr] = getattr(packet, attr)

    return packet_dict

def unpack(dict_packet):
    "Unpack a packet from a dictionary"
    try:
        packet_type_mixed = dict_packet.pop('type')
    except KeyError:
        return PacketError(message="packet type not set"), False

    numeric_type = isinstance(packet_type_mixed, Integral)

    try:
        packet_type = type_id2type[packet_type_mixed] if numeric_type else name2type[packet_type_mixed]
    except KeyError:
        return PacketError(message="Invalid packet type_id/name: " + repr(packet_type_mixed)), numeric_type

    # recurse for packetlists, check for format erros
    for attr, _default, s_type in packet_type.info:
        if attr not in dict_packet:
            continue

        elif s_type == 'pl' and attr in dict_packet:
            dict_packet[attr] = [dict2packet(d)[0] for d in dict_packet[attr]]

    try:
        return packet_type(**dict_packet), numeric_type
    except:
        return PacketError(
            message="Unable to instantiate %s(%s): %s" % (packet_type_mixed, dict_packet, format_exc()),
            other_type = type2type_id[packet_type] if numeric_type else type2name[packet_type]
        )

# compat old names
dict2packet = unpack # pylint: disable=C0103
packet2dict = pack # pylint: disable=C0103