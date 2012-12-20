#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, 2008, 2009 Loic Dachary <loic@dachary.org>
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

import unittest, sys
from os import path

TESTS_PATH = path.dirname(path.realpath(__file__))
sys.path.insert(0, path.join(TESTS_PATH, ".."))

from struct import pack

import testpackets

from pokerpackets import packets

class PacketsTestCase(testpackets.PacketsTestBase):
    
    def setUp(self):
        self._origInfo = {
            'PacketFactory': packets.PacketFactory,
            'PacketNames': packets.PacketNames
        }
        packets.PacketFactory = {}
        packets.PacketNames = {}
        self.d = {'PacketFactory': {}, 'PacketNames': {}}
        
    def tearDown(self):
        packets.PacketFactory = self._origInfo['PacketFactory']
        packets.PacketNames = self._origInfo['PacketNames']
        
    def updatePacketDicts(self):
        packets.PacketFactory.update(self.d['PacketFactory'])
        packets.PacketNames.update(self.d['PacketNames'])
        
    #--------------------------------------------------------------    
    def test_all(self):
        packets.PacketFactory = self._origInfo['PacketFactory']
        packets.PacketNames = self._origInfo['PacketNames']
        
        for type_index in packets._TYPES:
            if packets.PacketFactory.has_key(type_index):
                self.packetCheck(type = packets.PacketFactory[type_index])

        class TestPacketList(packets.PacketList):
            def __init__(self):
                packets.PacketList.__init__(self, packets = [packets.Packet()])
        self.packetCheck(type = TestPacketList)

    def test_fieldlist(self):
        packets.PacketNames[253] = 'TestPacketFieldList'
        
        class TestPacketFieldList(packets.Packet):
            type = 253

            info = packets.Packet.info + ( ('serials', [1], 'Il'), )
            
            serials = []

            format_element = "!I"

            def __init__(self, *args, **kwargs):
                self.serials = kwargs.get("serials", [])

            def pack(self):
                block = packets.Packet.pack(self)
                block += self.packlist(self.serials, TestPacketFieldList.format_element)
                return block

            def unpack(self, block):
                block = packets.Packet.unpack(self, block)
                (block, self.serials) = self.unpacklist(block, TestPacketFieldList.format_element)
                return block

            def calcsize(self):
                return packets.Packet.calcsize(self) + self.calcsizelist(self.serials, TestPacketFieldList.format_element)

            def __str__(self):
                return packets.Packet.__str__(self) + " serials = %s" % self.serials

        self.packetCheck(type = TestPacketFieldList, serials = [1])

    def defineTestPacket(self):
        class TestPingPacket(packets.Packet):
            pass
        packets.Packet.infoDeclare(self.d, TestPingPacket, packets.Packet, 'TESTPING', 5)
        self.updatePacketDicts()
        
        class TestPacket(packets.Packet):
            info = packets.Packet.info + (
                ('b' , 10, 'B'),
                ('a', 20, 'I'),
                ('c', 'ABC', 's'),
                ('d', [1,2,3], 'Bl'),
                ('e', -1, 'b'),
                ('f', None, 'no net'),
                ('g', [{'a': [1,2]}, None, True], 'j'),
                ('h', [TestPingPacket(), TestPingPacket()], 'pl'),
                ('i', True, 'bool'),
                ('i1', False, 'bool'),
                ('j', 'n', 'cbool'),
                ('j1', 'y', 'cbool'),
                ('k', None, 'Bnone'),
                ('m', u'aü'.encode('utf-8'), 'u')
            )
            fields = (
                "\x0a", # type
                "\0\0", # length
                "\x02", # b
                "\0\0\0\x01", # a
                "\0\x03ABC", # c
                "\x03\x01\x02\x03", # d
                "\xff", # e
                '\x00\x17[{"a":[1,2]},null,true]', # g
                "\x00\x02\x05\x00\x03\x05\x00\x03", # h
                "\x01", # i
                "\x00", # i1
                "\x00", # j
                "\x01", # j1
                "\xff", # k
                "\x00\x03a\xc3\xbc", # m
            )
            bla = fields[0]
            binary = fields[0] + pack('!H', len("".join(fields))) + "".join(fields[2:])
        packets.Packet.infoDeclare(self.d, TestPacket, packets.Packet, 'NAME', 10)
        self.updatePacketDicts()
        return TestPacket

    def test_infoPack(self):
        type = self.defineTestPacket()
        packet = type()
        packet.a = 1
        packet.b = 2
        self.assertEqual(type.binary, packet.infoPack())

    def test_infoUnpack(self):
        type = self.defineTestPacket()
        packet = type()
        packet.infoUnpack(type.binary)
        self.assertEqual(1, packet.a)
        self.assertEqual(2, packet.b)

    def test_infoUnpackJSON(self):
        type = self.defineTestPacket()
        packet = type()
        class TestJSON:
            def decode(self,something):
                return something
        old_JSON = packets.Packet.JSON
        packets.Packet.JSON = TestJSON()
        packet.infoUnpack(type.binary)
        packets.Packet.JSON = old_JSON
        self.assertEqual(1, packet.a)
        self.assertEqual(2, packet.b)

    def test_infoCalcsize(self):
        type = self.defineTestPacket()
        packet = type()
        self.assertEqual(len(type.binary), packet.infoCalcsize())

    def test_infoDeclare(self):
        class TestPacketClass(packets.Packet):
            pass
        index = 11
        packets.Packet.infoDeclare(self.d, TestPacketClass, packets.Packet, 'NAME', index)
        self.updatePacketDicts()
        self.assertEqual(TestPacketClass, packets.PacketFactory[index])
        self.assertEqual('NAME', packets.PacketNames[index])
        self.assertEqual(TestPacketClass.type, index)
        test_packet = TestPacketClass()
        packet = packets.Packet()
        self.assertEqual(packet.calcsize(), test_packet.calcsize())
        self.assertEqual("NAME  type = 11 length = 3", str(test_packet))

    def test_unpackpackets_errors(self):
        _stdout, sys.stdout = sys.stdout, open('/dev/null', 'w')
        #
        # Unknown packet type
        #
        self.assertEqual(None, packets.Packet.unpackpackets('\x00\x01\xff\x00\x03'));
        #
        # Pretend there are 2 packets although only one is present
        #
        self.assertEqual(None, packets.Packet.unpackpackets('\x00\x02\x00\x00\x03'));
        sys.stdout = _stdout
        
    def test_infoStr(self):
        class TestPacketClass(packets.Packet):
            info = packets.Packet.info + (('string','','u'),)
        index = 11
        packets.Packet.infoDeclare(self.d, TestPacketClass, packets.Packet, 'NAME', index)
        self.updatePacketDicts()
        
        packet1 = TestPacketClass()
        packet2 = TestPacketClass(string=u'über')
        self.assertEqual('NAME  type = 11 length = 5 string = ', str(packet1))
        self.assertEqual('NAME  type = 11 length = 10 string = \xc3\xbcber', str(packet2))

#--------------------------------------------------------------
def GetTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PacketsTestCase))
    return suite
    
#--------------------------------------------------------------
def Run(verbose = 1):
    return unittest.TextTestRunner(verbosity=verbose).run(GetTestSuite())
    
#--------------------------------------------------------------
if __name__ == '__main__':
    if Run().wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
