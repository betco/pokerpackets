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
from struct import pack, unpack, calcsize
from copy import deepcopy

from pokerpackets import log as packets_log
log = packets_log.get_child('packets')

PacketFactory = {}
PacketNames = {}

PACKET_NONE = 0
PacketNames[PACKET_NONE] = "NONE"

def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item): return item

def packets2maps(packets, packet_type_numeric=True):
    return (packet2map(packet,packet_type_numeric) for packet in packets)
    
def packet2map(packet, packet_type_numeric=True):
    attributes = packet.__dict__.copy()
    
    for attr_name in attributes.keys():
        if attr_name[0] == '_':
            del attributes[attr_name]
            
    if isinstance(packet, PacketList):
        attributes['packets'] = list(packets2maps(attributes['packets'], packet_type_numeric))
    
    if 'length' in attributes:
        del attributes['length']
        
    msg = getattr(packet,'message', None)
    if msg is not None:
        attributes['message'] = msg
        
    #
    # FIXME the followiong statement is NOT true (anymore?)
    # It is forbidden to set a map key to a numeric (native
    # numeric or string made of digits). Taint the map entries
    # that are numeric and hope the client will figure it out.
    dict_keys = [
        k for (k,v) in attributes.iteritems()
        if isinstance(v, dict) and find(lambda el: not isinstance(el,str), v.keys()) is not None
    ]
    for key in dict_keys:
        new_dict = attributes[key].copy()
        for (subkey,subvalues) in new_dict.iteritems():
            if not isinstance(subkey,str):
                del new_dict[subkey]
                subkey_new = str(subkey)
                if subkey_new.isdigit():
                    subkey_new = 'X'+ subkey_new
                new_dict[subkey_new] = subvalues
        attributes[key] = new_dict
                    
    attributes['type'] = packet.__class__.__name__ \
        if not packet_type_numeric \
        else packet.type            
        
    return attributes


import simplejson
class JSON:
    """
    JSON implementation used for packet en/decoding
    """
    encoder = simplejson.JSONEncoder(ensure_ascii=False,separators=(',', ':'))
    decoder = simplejson.JSONDecoder()
    
    def encode(self,obj):
        """encode an object, returning a utf8 encoded string (not a unicode string!)"""
        return self.encoder.encode(obj).encode('utf-8')
    def decode(self,string):
        return self.decoder.decode(string)
        
class Packet:
    """
     Packet base class
    """
    
    JSON = JSON()

    type = PACKET_NONE
    length = -1
    format = "!BH"
    format_size = calcsize(format)

    format_list_length = "!B"

    def infoInit(self, **kwargs):
        for (field, default, format) in self.info:
            if field == 'type':
                self.type = self.type # type is now in __dict__, for serialization
            if field not in self.__dict__:
                if field in kwargs:
                    self.__dict__[field] = \
                        kwargs[field].encode('utf-8') \
                        if format == 'u' and type(kwargs[field]) == unicode \
                        else kwargs[field]
                elif type(default) in (str,int,long,float):
                    self.__dict__[field] = default
                else:
                    self.__dict__[field] = deepcopy(default)
        self.length = self.infoCalcsize()
        return None
            
    def packJson(self):
        return Packet.JSON.encode(packet2map(self))
    
    def pack(self):
        return pack(Packet.format, self.type, self.calcsize())

    def infoPack(self):
        blocks = []
        self.length = self.infoCalcsize()
        for (field, _default, format) in self.info:
            if format != 'no net':
                packer = self.format_info[format]['pack']
                blocks.append(packer(self.__dict__[field]))
        return "".join(blocks)
            
    def unpack(self, block):
        (self.type,self.length) = unpack(Packet.format, block[:Packet.format_size])
        return block[Packet.format_size:]

    def infoUnpack(self, block):
        for (field, _default, format) in self.info:
            if format != 'no net':
                unpacker = self.format_info[format]['unpack']
                ( block, self.__dict__[field] ) = unpacker(block)
        return block

    @staticmethod
    def infoUnpackerb(block):
        value = unpack('B', block[0])[0]
        if value == 255: value = -1
        return ( block[1:], value )
    
    @staticmethod
    def infoPackerb(data):
        if data == -1: data = 255
        return pack('B', data)
    
    @staticmethod
    def infoUnpackerBnone(block):
        value = unpack('B', block[0])[0]
        if value == 255: value = None
        return ( block[1:], value )
    
    @staticmethod
    def infoPackerBnone(data):
        if data == None: data = 255
        return pack('B', data)
    
    @staticmethod
    def infoUnpackerBool(block):
        value = unpack('B', block[0])[0]
        if value != 0: value = True
        else: value = False
        return ( block[1:], value )
    
    @staticmethod
    def infoPackerBool(data):
        if data: data = 1
        else: data = 0
        return pack('B', data)
    
    @staticmethod
    def infoUnpackerCBool(block):
        value = unpack('B', block[0])[0]
        if value != 0: value = 'y'
        else: value = 'n'
        return ( block[1:], value )
    
    @staticmethod
    def infoPackerCBool(data):
        if data == 'y': data = 1
        else: data = 0
        return pack('B', data)
    
    def calcsize(self):
        return Packet.format_size

    def infoCalcsize(self):
        size = 0
        for (field, _default, format) in self.info:
            if format != 'no net':
                calcsize = self.format_info[format]['calcsize']
                size += calcsize(self.__dict__[field])
        return size

    @staticmethod
    def packlist(l, format):
        block = pack(Packet.format_list_length, len(l))
        for value in l:
            block += pack(format, value)
        return block

    @staticmethod
    def unpacklist(block, format):
        (length,) = unpack(Packet.format_list_length, block[:calcsize(Packet.format_list_length)])
        format_size = calcsize(format)
        block = block[calcsize(Packet.format_list_length):]
        l = []
        for _i in xrange(length):
            l.append(unpack(format, block[:format_size])[0])
            block = block[format_size:]
        return (block, l)

    @staticmethod
    def calcsizelist(l, format):
        return calcsize(Packet.format_list_length) + len(l) * calcsize(format)

    @staticmethod
    def packstring(string):
        return pack("!H", len(string)) + string

    @staticmethod
    def unpackstring(block):
        offset = calcsize("!H")
        (length,) = unpack("!H", block[:offset])
        string = block[offset:offset + length]
        return (block[offset + length:], string)

    @staticmethod
    def calcsizestring(string):
        return calcsize("!H") + len(string)

    @staticmethod
    def packbstring(obj):
        if obj == True: string = '_TRUE'
        elif obj == False: string = '_FALSE'
        else: string = obj
        return pack("!H", len(string)) + string

    @staticmethod
    def unpackbstring(block):
        offset = calcsize("!H")
        (length,) = unpack("!H", block[:offset])
        obj = block[offset:offset + length]
        if obj == '_TRUE': string = True
        elif obj == '_FALSE': string = False
        else: string = obj
        return (block[offset + length:], string)

    @staticmethod
    def calcsizebstring(obj):
        if obj == True: string = '_TRUE'
        elif obj == False: string = '_FALSE'
        else: string = obj
        return calcsize("!H") + len(string)

    @staticmethod
    def packjson(obj):
        return Packet.packstring(Packet.JSON.encode(obj))

    @staticmethod
    def unpackjson(block):
        ( block, string ) = Packet.unpackstring(block)
        obj = Packet.JSON.decode(string)
        return ( block, obj)

    @staticmethod
    def calcsizejson(obj):
        return len(Packet.packjson(obj))

    @staticmethod
    def packpackets(packets):
        block = pack('!H', len(packets))
        for packet in packets:
            block += packet.pack()
        return block

    @staticmethod
    def unpackpackets(block):
        (length,) = unpack('!H', block[0:2])
        block = block[2:]
        t = Packet()
        count = 0
        packets = []
        while len(block) > 0 and count < length:
            t.unpack(block)
            if t.type not in PacketFactory:
                log.warn("unknown packet type %d (knwon types are %s)", t.type, PacketNames)
                return None
            packet = PacketFactory[t.type]()
            block = packet.unpack(block)
            count += 1
            packets.append(packet)
        if count != length:
            log.warn("expected a list of %d packets but found %d", length, count)
            return None
        return ( block, packets )

    @staticmethod
    def calcsizepackets(packets):
        return 2 + sum([ packet.calcsize() for packet in packets ])
    
    @staticmethod
    def packmoney(obj):
        block = pack('!H', len(obj))
        for (currency, money) in obj.iteritems():
            fields = (currency,) + money
            block += pack('!IQQQ', *fields)
        return block

    @staticmethod
    def unpackmoney(block):
        (length,) = unpack('!H', block[:calcsize('!H')])
        block = block[calcsize('!H'):]
        fmt = '!IQQQ'
        format_size = calcsize(fmt)
        obj = {}
        for _i in xrange(length):
            fields = unpack(fmt, block[:format_size])
            obj[fields[0]] = fields[1:]
            block = block[format_size:]
        return (block, obj)

    @staticmethod
    def calcsizemoney(obj):
        return calcsize('!H') + len(obj) * calcsize('!IQQQ')
    
    @staticmethod
    def packplayers(obj):
        block = pack('!H', len(obj))
        for (name, chips, flags) in obj:
            block += Packet.packstring(name)
            block += pack('!IB', chips, flags)
        return block

    @staticmethod
    def unpackplayers(block):
        (length,) = unpack('!H', block[:calcsize('!H')])
        block = block[calcsize('!H'):]
        format = '!IB'
        format_size = calcsize(format)
        obj = []
        for _i in xrange(length):
            (block, name) = Packet.unpackstring(block)
            (chips, flags) = unpack(format, block[:format_size])
            obj.append((name, chips, flags))
            block = block[format_size:]
        return (block, obj)

    @staticmethod
    def calcsizeplayers(obj):
        size = calcsize('!H')
        for (name, _chips, _flags) in obj:
            size += Packet.calcsizestring(name) + calcsize('!IB')
        return size
    
    def __str__(self):
        return "type = %s(%d)" % ( PacketNames[self.type], self.type )

    def infoStr(self):
        strings = [ PacketNames[self.type] + " " ]
        for (field, _default, format) in self.info:
            strings.append("%s = %s" % (field, self.__dict__[field]))
        return " ".join(strings)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return isinstance(other, Packet) and self.type == other.type

    @staticmethod
    def infoDeclare(dictionary, type, base_type, name, index):
        dictionary['PacketNames'][index] = name
        dictionary['PacketFactory'][index] = type
        dictionary['PACKET_' + name] = index
        type.type = index
        type.__init__ = Packet.infoInit
        type.pack = Packet.infoPack
        type.unpack = Packet.infoUnpack
        type.calcsize = Packet.infoCalcsize
        type.__str__ = Packet.infoStr

Packet.info = (
    ('type', PACKET_NONE, 'B'),
    ('length', -1, 'H'),
    )
    
Packet.format_info = {
    #
    # Not transfered over the network.
    #
    'no net': None,
    #
    # Unsigned integer, int, 4 bytes, network order (big endian).
    # Example: 1 <=> \x00\x00\x00\x01
    #
    'I': {'pack': lambda data: pack('!I', data),
          'unpack': lambda block: ( block[4:], int(unpack('!I', block[:4])[0]) ),
          'calcsize': lambda data: 4,
          },
    #
    # Unsigned long long, long, 8 bytes, network order (big endian).
    # Example: 1 <=> \x00\x00\x00\x00\x00\x00\x00\x01
    #
    'Q': {'pack': lambda data: pack('!Q', data),
          'unpack': lambda block: ( block[8:], int(unpack('!Q', block[:8])[0]) ),
          'calcsize': lambda data: 8,
          },
    #
    # Unsigned integer, char, 1 byte
    # Example: 1 <=> \x01
    #
    'B': {'pack': lambda data: pack('B', data),
          'unpack': lambda block: ( block[1:], unpack('B', block[0])[0] ),
          'calcsize': lambda data: 1,
          },
    #
    # Integer range [-1..254], char, 1 byte
    # -1 is 255
    # Example: 1 <=> \x01, -1 <=> \xff, 254 <=> \xfe
    #
    'b': {'pack': Packet.infoPackerb,
          'unpack': Packet.infoUnpackerb,
          'calcsize': lambda data: 1,
          },
    #
    # Integer range [0..254, None], char, 1 byte
    # None is 255
    # Example: 1 <=> \x01, None <=> \xff, 254 <=> \xfe
    #
    'Bnone': {'pack': Packet.infoPackerBnone,
              'unpack': Packet.infoUnpackerBnone,
              'calcsize': lambda data: 1,
          },
    #
    # Integer range [0,1], char, 1 byte
    # True is 1, False is 0
    # Example: True <=> \x01, False <=> \x00
    #
    'bool': {'pack': Packet.infoPackerBool,
             'unpack': Packet.infoUnpackerBool,
             'calcsize': lambda data: 1,
          },
    #
    # Integer range ['n','y'], char, 1 byte
    # 'y' is 1, 'n' is 0
    # Example: 'y' <=> \x01, 'n' <=> \x00
    #
    'cbool': {'pack': Packet.infoPackerCBool,
              'unpack': Packet.infoUnpackerCBool,
              'calcsize': lambda data: 1,
              },
    #
    # Unsigned integer, short, 2 bytes, network order (big endian).
    # Example: 1 <=> \x00\x01
    #
    'H': {'pack': lambda data: pack('!H', data),
          'unpack': lambda block: ( block[2:], unpack('!H', block[:2])[0] ),
          'calcsize': lambda data: 2,
          },
    #
    # Character string, length as a 2 bytes integer, network order (big endian)
    #   followed by the content of the string.
    # Example: "abc" <=> \x00\x03abc
    #          "a" <=> \x00\x01a
    #          "" <=> \x00\x00
    #
    's': {'pack': Packet.packstring,
          'unpack': Packet.unpackstring,
          'calcsize': Packet.calcsizestring,
          },

    #
    # utf-8 encoded string, length as a 2 bytes integer, network order (big endian)
    #  followed by the content of the string. Is used to encode unicode to utf8 in infoInit
    #
    'u': {'pack': Packet.packstring,
          'unpack': Packet.unpackstring,
          'calcsize': Packet.calcsizestring,
         },
    #
    # Character string or boolean, length as a 2 bytes integer, network order (big endian)
    #   followed by the content of the string.
    # Example: "abc" <=> \x00\x03abc
    #          "" <=> \x00\x00
    #          True <=> \x00\x04TRUE
    #
    'bs': {'pack': Packet.packbstring,
          'unpack': Packet.unpackbstring,
          'calcsize': Packet.calcsizebstring,
          },
    #
    # JSon.org encoded string, length as a 2 bytes integer, network order (big endian)
    #   followed by the content of the string.
    # Example: "{'a':1}" <=> \x00\x07{'a':1}
    #
    'j': {'pack': Packet.packjson,
          'unpack': Packet.unpackjson,
          'calcsize': Packet.calcsizejson,
          },
    #
    # List of integer, length of the list as a 1 byte unsigned integer in the range [0-255]
    # Each integer is a 1 byte unsigned value in the range [0-255]
    # Example: [] <=> \x00
    #          [5] <=> \x01\x05
    #          [5, 255] <=> \x02\x05\xff
    #
    'Bl': {'pack': lambda data: Packet.packlist(data, 'B'),
           'unpack': lambda block: Packet.unpacklist(block, 'B'),
           'calcsize': lambda data: Packet.calcsizelist(data, 'B'),
           },
    #
    # List of integer, length of the list as a 1 byte unsigned integer in the range [0-255]
    # Each integer is a 2 bytes unsigned value in network order (big endian)
    # Example: [] <=> \x00
    #          [5] <=> \x01\x00\x05
    #          [5, 255] <=> \x02\x00\x05\x00\xff
    #
    'Hl': {'pack': lambda data: Packet.packlist(data, '!H'),
           'unpack': lambda block: Packet.unpacklist(block, '!H'),
           'calcsize': lambda data: Packet.calcsizelist(data, '!H'),
           },
    #
    # List of integer, length of the list as a 1 byte unsigned integer in the range [0-255]
    # Each integer is a 4 bytes unsigned value in network order (big endian)
    # Example: [] <=> \x00
    #          [5] <=> \x01\x00\x00\x00\x05
    #          [5, 255] <=> \x02\x00\x00\x00\x05\x00\x00\x00\xff
    #
    'Il': {'pack': lambda data: Packet.packlist(data, '!I'),
           'unpack': lambda block: Packet.unpacklist(block, '!I'),
           'calcsize': lambda data: Packet.calcsizelist(data, '!I'),
           },

    #
    # List of packets, length of the list as a short unsigned integer in the range [0-65535]
    # Each packet is a derived from Packet
    # Example: [] <=> \x00\x00
    #          [PacketPing()] <=> \x00\x01\x05\x00\x03
    #          [PacketPing(), PacketPing()] <=> \x00\x02\x05\x00\x03\x05\x00\x03
    #
    'pl': {'pack': Packet.packpackets,
           'unpack': Packet.unpackpackets,
           'calcsize': Packet.calcsizepackets,
           },
    
    #
    # List of user money status, length of the list as a 2 byte unsigned integer in the range [0-65535]
    # Each money status is a list of 4 unsigned integers
    #  currency
    #  bankroll
    #  in_game
    #  points
    # Example: {} <=> \x00
    #          {5: (2, 3, 4)} <=> \x01\x05\x02\x03\x04
    #          {5: (2, 3, 4), 10: (1, 1, 1)} <=> \x02\x05\x02\x03\x04\x0a\x01\x01\x01
    #
    'money': {
              'pack': Packet.packmoney,
              'unpack': Packet.unpackmoney,
              'calcsize': Packet.calcsizemoney
              },
    
    #
    # List of players, length of the list as a 4 byte unsigned integer in the range [0-65535]
    # Each player is a list of 3 elements
    #  name (string)
    #  money (4 byte unsigned integer)
    #  flags (2 byte unsigned integer)
    # Example: [] <=> \x00\x00
    #          [('player',1000,0)] <=> \x00\x01\x00\x06player\x00\x00\x03\xe8\x00
    #
    'players': {
                'pack': Packet.packplayers,
                'unpack': Packet.unpackplayers,
                'calcsize':Packet.calcsizeplayers
                }
    }

PacketFactory[PACKET_NONE] = Packet

########################################

class PacketString(Packet):
    """
    Packet containing a single string
    """

    info = Packet.info + (
        ( 'string', '', 's' ),
        )
                           
Packet.infoDeclare(globals(), PacketString, Packet, "STRING", 1) # 1 #
########################################

class PacketInt(Packet):
    """
    Packet containing an unsigned integer value
    """

    info = Packet.info + (
        ( 'value', 0, 'I' ),
        )
    
Packet.infoDeclare(globals(), PacketInt, Packet, "INT", 2) # 2 #
########################################

class PacketError(Packet, Exception):
    """
    Packet describing an error
    """
    

    info = Packet.info + (
       ('message', 'no message', 's'),
       ('code', 0, 'I' ),
       ('other_type', 3, 'B'),
       )
    

Packet.infoDeclare(globals(), PacketError, Packet, "ERROR", 3) # 3 #

def packetErrorInit(obj, **kwargs):
    Packet.infoInit(obj, **kwargs)
    Exception.__init__(obj)
PacketError.__init__ = packetErrorInit
########################################

class PacketAck(Packet):
    ""

Packet.infoDeclare(globals(), PacketAck, Packet, "ACK", 4) # 4 #

########################################

class PacketPing(Packet):
    ""

Packet.infoDeclare(globals(), PacketPing, Packet, "PING", 5) # 5 #
########################################

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
########################################

class PacketQuit(Packet):
    """
    Client tells the server it will leave
    """
    
Packet.infoDeclare(globals(), PacketQuit, Packet, "QUIT", 7) # 7  #
########################################

class PacketAuthOk(Packet):
    """\
Semantics: authentication request succeeded.

Direction: server => client
    """

Packet.infoDeclare(globals(), PacketAuthOk, Packet, "AUTH_OK", 8) # 8 #
########################################

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
########################################

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
########################################

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
########################################

class PacketAuthRequest(Packet):
    """
    Packet to ask authentification from the client
    """
    
Packet.infoDeclare(globals(), PacketAuthRequest, Packet, "AUTH_REQUEST", 11) # 11  #
########################################

class PacketList(Packet):
    """
    Packet containing a list of packets
    """
    info = Packet.info + (
        ('packets', [], 'pl'),
        )
    
Packet.infoDeclare(globals(), PacketList, Packet, "LIST", 12) # 12 #
########################################

class PacketLogout(Packet):
    """
    Login out
    """
    NOT_LOGGED_IN = 1
    
Packet.infoDeclare(globals(), PacketLogout, Packet, "LOGOUT", 13) # 13 #
########################################

class PacketBootstrap(Packet):
    ""

Packet.infoDeclare(globals(), PacketBootstrap, Packet, "BOOTSTRAP", 14) # 14  #
########################################

class PacketProtocolError(PacketError):
    """
    Client protocol version does not match server protocol version.
    """

Packet.infoDeclare(globals(), PacketProtocolError, Packet, "PROTOCOL_ERROR", 15) # 15 #
########################################

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
import re
__all__ = [n for n in locals().keys() if re.match('Packet|PACKET_',n)]
