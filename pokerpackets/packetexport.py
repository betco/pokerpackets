from pokerpackets.packets import type_id2type, PacketNames
import pokerpackets.networkpackets
import pokerpackets.clientpackets

def packetToExport(ptype):
    packet = type_id2type[ptype]
    pname = PacketNames[ptype]
    return {
        'name': pname,
        'fields': packet.info
    }

def exportPackets():
    return [(type_id, packetToExport(type_id)) for type_id in type_id2type.iterkeys()]


if __name__ == '__main__':
    import json
    encoder = json.JSONEncoder(separators=(',', ':'))
    exp = exportPackets()
    print '{%s}' % ',\n'.join('"%d": %s' % (p[0], encoder.encode(p[1])) for p in exp)