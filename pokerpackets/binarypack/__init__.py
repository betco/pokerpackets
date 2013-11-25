
import _binarypack

def pack(packet):
    """
    pack a packet

    packet: subclass of Packet

    returns: head + content of packet as binary data (string)
    """

    if 'binarypack_fast_pack' in packet.__class__.__dict__:
        # print 'fast pack', packet.info
        return packet.binarypack_fast_pack()

    buf = []
    _binarypack.pack(packet, buf)
    return b''.join(buf)

def unpack(data, offset=0):
    """
    unpack a binary packed packet

    data: head + content of packet as binary data (string)

    returns: packet
    """

    return _binarypack.unpack(data, offset)[1]

