
import re
from traceback import format_exc

from pokerpackets.packets import type2type_id, name2type, type_id2type, PacketError

def dict2packet(dict_packet):
    numeric_type = type(dict_packet['type']) == int
    try:
        packet_type = type_id2type[dict_packet['type']] if type(dict_packet['type']) == int else name2type[dict_packet['type']]
        del dict_packet['type']
    except KeyError:
        return PacketError(message = "Invalid packet type_id/name: " + repr(dict_packet.get('type'))), numeric_type

    # recurse for packetlists
    for attr, default, s_type in packet_type.info:
        if s_type == 'pl' and attr in dict_packet:
            dict_packet[attr] = [dict2packet(d)[0] for d in dict_packet[attr]]

    try:
        return packet_type(**dict_packet), numeric_type
    except:
        return PacketError(
            message = "Unable to istantiate %s(%s): %s" % (dict_packet.get('type'), dict_packet, format_exc()),
            other_type = type2type_id.get(packet_type, 3)
        ), numeric_type

def packet2dict(packet, numeric_type=True):
    packet_type = packet.__class__
    type_id = type2type_id.get(packet_type)

    if type_id == None:
        #TODO error handling
        return

    result = {
        'type': type_id if numeric_type else packet_type.__name__
    }

    for attr, default, s_type in packet_type.info:
        if s_type == 'no net':
            continue
        elif s_type == 'pl':
            result[attr] = [packet2dict(p, numeric_type) for p in getattr(packet, attr)]

        # FIXME get rid of the X+int crap
        elif s_type == 'money':
            money = getattr(packet, attr)
            result[attr] = {}
            for k, v in money.iteritems():
                result[attr]['X%d' % (k,) if type(k) == int else k] = v
        else:
            result[attr] = getattr(packet, attr)

    return result
