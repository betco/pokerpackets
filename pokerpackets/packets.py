#
# Copyright (C) 2006, 2007, 2008, 2009 Loic Dachary <loic@dachary.org>
# Copyright (C) 2004, 2005, 2006 Mekensleep <licensing@mekensleep.com>
#                                24 rue vieille du temple, 75004 Paris
#
# This software's license gives you freedom; you can copy, convey,
# propagate, redistribute and/or modify this program under the terms of
# the GNU Affero General Public License (AGPL) as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version of the AGPL published by the FSF.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program in a file in the toplevel directory called
# "AGPLv3".  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#  Loic Dachary <loic@dachary.org>
#  Henry Precheur <henry@precheur.org> (2004)
#

import re
from struct import Struct

from pokerpackets import log as packets_log
log = packets_log.get_child('packets')

name2type = {}
type2type_id = {}
type_id2type = {}

PACKET_NONE = 0

def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): return item


import simplejson
class JSON:
    """
    JSON implementation used for packet en/decoding
    """
    encoder = simplejson.JSONEncoder(ensure_ascii=False, separators=(',', ':'))
    decoder = simplejson.JSONDecoder()

    def encode(self, obj):
        """encode an object, returning a utf8 encoded string (not a unicode string!)"""
        return self.encoder.encode(obj).encode('utf-8')

    def decode(self, string):
        return self.decoder.decode(string)
        
class Packet:
    """
     Packet base class
    """
    
    JSON = JSON()

    type = PACKET_NONE
    info = ()

    def __init__(self, **kw):
        if kw:
            self.__dict__ = kw
            
    def __str__(self):
        string = "%s(%d)" % (self.__class__.__name__, self.__class__.type)
        for attr, _d, _t in self.__class__.info:
            string += " %s: %s" % (attr, repr(getattr(self, attr)))
        return string

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return \
            self.__class__ is other.__class__ and \
            not any(getattr(self, attr) != getattr(other, attr) for attr, _default, _s_info in self.__class__.info)

    @staticmethod
    def infoDeclare(dictionary, packet_type, base_type, name, index):
        # setup dictionary
        if 'type2type_id' not in dictionary: dictionary['type2type_id'] = {}
        if 'type_id2type' not in dictionary: dictionary['type_id2type'] = {}
        if 'name2type' not in dictionary: dictionary['name2type'] = {}
        if 'PacketFactory' not in dictionary: dictionary['PacketFactory'] = {PACKET_NONE: Packet}
        if 'PacketNames' not in dictionary: dictionary['PacketNames'] = {PACKET_NONE: "NONE"}

        # setup _type
        packet_type.type = index
        for attr, default, _s_type in packet_type.info:
            setattr(packet_type, attr, default)

        # binpack info
        packet_type._binarypack_info = [(attr, s_type) for attr, _default, s_type in packet_type.info if s_type != 'no net']

        # fast pack
        struct_format = '!BH'
        attr_names = []
        for attr, default, s_type in packet_type.info:

            # skip 'no net' attributes
            if s_type == 'no net':
                continue

            # break if type is not fixed length and no other evaluation is needed
            if s_type not in ('B', 'H', 'I', 'Q'):
                break

            # 
            struct_format += s_type
            attr_names.append(attr)

        else:
            if attr_names:
                fast_struct = Struct(struct_format)
                fast_struct_size = fast_struct.size - 3 # 3 is the size of the packet head
                packet_type._binarypack_fast_pack = lambda p: fast_struct.pack(
                    index,
                    fast_struct_size,
                    *[getattr(p, attr) for attr in attr_names]
                )

        # insert type into dictionary
        dictionary['type2type_id'][packet_type] = index
        dictionary['type_id2type'][index] = packet_type
        dictionary['name2type'][packet_type.__name__] = packet_type
        dictionary['PacketNames'][index] = name
        dictionary['PacketFactory'][index] = packet_type
        dictionary['PACKET_' + name] = index

class PacketString(Packet):
    """
    Packet containing a single string
    """

    info = Packet.info + (
        ('string', '', 's'),
    )
                           
Packet.infoDeclare(globals(), PacketString, Packet, "STRING", 1) # 1 #


class PacketInt(Packet):
    """
    Packet containing an unsigned integer value
    """

    info = Packet.info + (
        ('value', 0, 'I'),
    )
    
Packet.infoDeclare(globals(), PacketInt, Packet, "INT", 2) # 2 #


class PacketError(Packet, Exception):
    """
    Packet describing an error
    """
    
    def __init__(self, **kw):
        Packet.__init__(self, **kw)
        Exception.__init__(self)

    info = Packet.info + (
       ('message', 'no message', 's'),
       ('code', 0, 'I' ),
       ('other_type', 3, 'B'),
    )
    

Packet.infoDeclare(globals(), PacketError, Packet, "ERROR", 3) # 3 #


class PacketAck(Packet):
    ""

Packet.infoDeclare(globals(), PacketAck, Packet, "ACK", 4) # 4 #


class PacketPing(Packet):
    ""

Packet.infoDeclare(globals(), PacketPing, Packet, "PING", 5) # 5 #


class PacketSerial(Packet):
    """\
Semantics: the serial number of the authenticated user
           associated to the client after a PacketLogin
           was sent. This packet is sent to the client
           after the PacketAuthOk acknowledging the success
           of the authentication.

Direction: server => client

serial: the unique number associated to the user.
    """

    info = Packet.info + (
        ('serial', 0, 'I'),
    )
    
Packet.infoDeclare(globals(), PacketSerial, Packet, "SERIAL", 6) # 6 #


class PacketQuit(Packet):
    """
    Client tells the server it will leave
    """
    
Packet.infoDeclare(globals(), PacketQuit, Packet, "QUIT", 7) # 7  #


class PacketAuthOk(Packet):
    """\
Semantics: authentication request succeeded.

Direction: server => client
    """

Packet.infoDeclare(globals(), PacketAuthOk, Packet, "AUTH_OK", 8) # 8 #


class PacketAuthRefused(PacketError):
    """\
Semantics: authentication request was refused by the server.

Direction: server => client

message: human readable reason for the authentication failure
code: machine readable code matching the human readable message
      the list of which can be found in the PacketPokerSetAccount
      packet definition
other_type: the type of the packet that triggered the authentication
            error, i.e. :class:`PACKET_LOGIN <pokerpackets.packets.PacketLogin>`
    """

Packet.infoDeclare(globals(), PacketAuthRefused, Packet, "AUTH_REFUSED", 9) # 9 #


class PacketLogin(Packet):
    """\
Semantics: authentify user "name" with "password".

Direction: server <= client

If the user/password combination is valid, the
PacketAuthOk packet will be sent back to the client,
immediately followed by the PacketSerial packet that
holds the serial number of the user.

If the user/password combination is invalid, the
PacketAuthRefused packet will be sent back to the client.
If the user is already logged in, a PacketError is sent
with code set to PacketLogin.LOGGED.

name: valid user name as a string
password: matching password string
    """

    LOGGED = 1
    
    info = Packet.info + (
        ('name', 'unknown', 's'),
        ('password', 'unknown', 's'),
    )
    
Packet.infoDeclare(globals(), PacketLogin, Packet, "LOGIN", 10) # 10 #


class PacketAuth(Packet):
    """\
Semantics: authentify user with "auth" token.

Direction: server <= client

If the auth string is valid, the
PacketAuthOk packet will be sent back to the client,
immediately followed by the PacketSerial packet that
holds the serial number of the user.

If the auth string is invalid, the
PacketAuthRefused packet will be sent back to the client.
If the user is already logged in, a PacketError is sent
with code set to PacketAuth.LOGGED.

auth: valid user auth hash as a string
    """
    LOGGED = 1
    info = Packet.info + (
        ('auth', 'unknown', 's'),
    )
    
Packet.infoDeclare(globals(), PacketAuth, Packet, "AUTH", 25) # 25 #


class PacketAuthRequest(Packet):
    """
    Packet to ask authentification from the client
    """
    
Packet.infoDeclare(globals(), PacketAuthRequest, Packet, "AUTH_REQUEST", 11) # 11  #


class PacketList(Packet):
    """
    Packet containing a list of packets
    """
    info = Packet.info + (
        ('packets', [], 'pl'),
    )
    
Packet.infoDeclare(globals(), PacketList, Packet, "LIST", 12) # 12 #


class PacketLogout(Packet):
    """
    Login out
    """
    NOT_LOGGED_IN = 1
    
Packet.infoDeclare(globals(), PacketLogout, Packet, "LOGOUT", 13) # 13 #


class PacketBootstrap(Packet):
    ""

Packet.infoDeclare(globals(), PacketBootstrap, Packet, "BOOTSTRAP", 14) # 14  #


class PacketProtocolError(PacketError):
    """
    Client protocol version does not match server protocol version.
    """

Packet.infoDeclare(globals(), PacketProtocolError, Packet, "PROTOCOL_ERROR", 15) # 15 #


class PacketMessage(PacketString):
    """
    server => client
    Informative messages
    """

Packet.infoDeclare(globals(), PacketMessage, Packet, "MESSAGE", 16) # 16 #

_TYPES = range(0,39)

### !!!!!! NO SERIAL >= 50 !!!!!! ####

#
# only export things starting with Packet or PACKET_
__all__ = [n for n in locals().keys() if re.match('Packet|PACKET_', n)] + ['type2type_id', 'type_id2type', 'name2type']
