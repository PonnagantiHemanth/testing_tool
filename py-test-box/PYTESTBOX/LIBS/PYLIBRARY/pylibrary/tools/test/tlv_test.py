#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.tlv

@brief  Tlv and TlvList test implementation

@author christophe Roquebert

@date   2018/09/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist            import HexList
from pylibrary.tools.tlv               import Tlv
from pylibrary.tools.tlv               import TlvError
from pylibrary.tools.tlv               import TlvList
from unittest                           import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class TlvTestCase(TestCase):
    '''
    Tlv implementation test.
    '''
    RefClass = Tlv

    @classmethod
    def _createInstance(cls, tag   = 0x01,
                             value = None,
                             mode  = Tlv.SIMPLE):
        '''
        Create an instance

        @option tag     [in]  (int) from 0x01 to 0xFE
        @option value   [in]  (HexList) The TLV value
        @option mode    [in]  (int) by default #SIMPLE

        @return (RefClass) RefClass instance
        '''
        if value is None:
            value = HexList(0x11) * 5
        # end if

        return cls.RefClass(tag, value, mode)
    # end def _createInstance

    def testCompactTags(self):
        '''
        Tests of the TLV tag values, when the type is COMPACT
        '''

        # tag = 0x01
        self.assertEqual(HexList(0x10),
                         self.RefClass(0x01, None, Tlv.COMPACT).__hexlist__(),
                         "Empty compact TLV does not match its expected value")

        # tag == 0x00
        self.assertRaises(TlvError,
                          self.RefClass, 0x00, None, Tlv.COMPACT)

        # tag > 0x0F
        self.assertRaises(TlvError,
                          self.RefClass, 0x10, None, Tlv.COMPACT)

        # tag matching BER encoding
        self.assertRaises(TlvError,
                          self.RefClass, 0x1F, None, Tlv.COMPACT)
    # end def testCompactTags

    def testSimpleTags(self):
        '''
        Tests of the TLV tag values, when the type is SIMPLE
        '''
        # tag == 0x00
        self.assertRaises(TlvError,
                          self.RefClass, 0x00, None, Tlv.SIMPLE)

        # tag == 0xFF
        self.assertRaises(TlvError,
                          self.RefClass, 0xFF, None, Tlv.SIMPLE)

        # tag > 0x100
        self.assertRaises(TlvError,
                          self.RefClass, 0x0100, None, Tlv.SIMPLE)
    # end def testSimpleTags

    def testBerTags(self):
        '''
        Tests of the TLV tag values, when the type is BER
        '''
        value = HexList(0x42) * 0x100

        # tag > 0x100
        self.assertEqual(HexList(0x1F, 0x81, 0x00, 0x82, 0x01, 0x00, value),
                         self._createInstance(0x1F8100, value, Tlv.BER_2).__hexlist__())

        # tag == 0x00
        self.assertRaises(TlvError,
                          self.RefClass, 0x00, None, Tlv.BER_AUTO)
    # end def testBerTags

    def testCompactLength(self):
        '''
        Tests of the length when the TLV is of type COMPACT
        '''
        # COMPACT
        self.assertEqual(HexList(0x10),
                         self.RefClass(0x01, None, Tlv.COMPACT).__hexlist__(),
                         "Empty compact TLV does not match its expected value")

        self.assertEqual(HexList(0x11, 0x01),
                         self._createInstance(0x01, 0x01, Tlv.COMPACT).__hexlist__(),
                         "One-byte compact TLV does not match its expected value")

        self.assertEqual(HexList(0x1F, "0102030405060708090A0B0C0D0E0F"),
                         self._createInstance(0x01, "0102030405060708090A0B0C0D0E0F", Tlv.COMPACT).__hexlist__(),
                         "Compact TLV does not match its expected value")

        # length > 0x0F
        self.assertRaises(TlvError,
                          self._createInstance, 0x01, "0102030405060708090A0B0C0D0E0F10", Tlv.COMPACT)
    # end def testCompactLength

    def testSimpleLength(self):
        '''
        Tests of the length when the TLV is of type SIMPLE
        '''

        # SIMPLE
        self.assertEqual(HexList(0x01, 0x00),
                         self.RefClass(0x01, None, Tlv.SIMPLE).__hexlist__())

        self.assertEqual(HexList(0x01, 0x01, 0x01),
                         self._createInstance(1, 0x01, Tlv.SIMPLE).__hexlist__())

        self.assertEqual(HexList(0x01, 0x10, "0102030405060708090A0B0C0D0E0F10"),
                         self._createInstance(1, "0102030405060708090A0B0C0D0E0F10", Tlv.SIMPLE).__hexlist__())

        # length > 0xFF
        self.assertRaises(TlvError,
                          self.RefClass, 0x01, 0x100 * HexList(0x00), Tlv.SIMPLE)
    # end def testSimpleLength

    def testBerLength(self):
        '''
        Tests of the length when the TLV is of type BER
        '''
        # 1 byte

        # BER auto
        self.assertEqual(HexList(0x01, 0x00),
                         self.RefClass(0x01, None, Tlv.BER_AUTO).__hexlist__())

        value = HexList(0x01)
        self.assertEqual(HexList(0x01, 0x01, value),
                         self._createInstance(1, value, Tlv.BER_AUTO).__hexlist__())

        value = HexList(0x01) * 0x7F
        self.assertEqual(HexList(0x01, 0x7F, value),
                         self._createInstance(1, value, Tlv.BER_AUTO).__hexlist__())

        # BER_0
        self.assertEqual(HexList(0x01, 0x00),
                         self.RefClass(0x01, None, Tlv.BER_0).__hexlist__())

        value = HexList(0x01)
        self.assertEqual(HexList(0x01, 0x01, value),
                         self._createInstance(1, value, Tlv.BER_0).__hexlist__())

        value = HexList(0x01) * 0x7F
        self.assertEqual(HexList(0x01, 0x7F, value),
                         self._createInstance(1, value, Tlv.BER_0).__hexlist__())

        # BER_1
        for length in (0x00, 0x7F, 0x80, 0xFF):

            value = HexList(0x02) * length

            self.assertEqual(HexList(0x01, 0x81, length, value),
                         self._createInstance(1, value, Tlv.BER_1).__hexlist__())
        # end for

        # length > 0xFF
        value = HexList(0x03) * 0x100
        self.assertRaises(TlvError,
                          self.RefClass, 1, value, Tlv.BER_1)

        # BER_2
        for length in (0x00, 0x7F, 0x80, 0xFF, 0x100, 0xFFFF):
            value = HexList(0x03) * length

            self.assertEqual(HexList(0x01, 0x82, length >> 8, length & 0xFF, value),
                             self._createInstance(1, value, Tlv.BER_2).__hexlist__())
        # end for

        # length > 0xFFFFFF
        value = HexList(0x04) * 0x10000
        self.assertRaises(TlvError,
                          self.RefClass, 1, value, Tlv.BER_2)
    # end def testBerLength

    def test_Str(self):
        ''' __str__ api
        '''

        tlv = self._createInstance(0x01, HexList('1234'), Tlv.COMPACT)

        self.assertEqual("1 2 1234", str(tlv))

        tlv.setMode(Tlv.SIMPLE)
        self.assertEqual("01 02 1234", str(tlv))

        tlv.setMode(Tlv.BER_0)
        self.assertEqual("01 02 1234", str(tlv))

        tlv.setMode(Tlv.BER_1)
        self.assertEqual("01 8102 1234", str(tlv))

        tlv.setMode(Tlv.BER_2)
        self.assertEqual('01 820002 1234', str(tlv))

        tlv = self._createInstance(0x0F, HexList('00112233445566778899AABBCCDDEE'), Tlv.COMPACT)

        self.assertEqual('F F 00112233445566778899AABBCCDDEE', str(tlv))

        tlv.setMode(Tlv.SIMPLE)
        self.assertEqual('0F 0F 00112233445566778899AABBCCDDEE', str(tlv))

        tlv.setMode(Tlv.BER_0)
        self.assertEqual('0F 0F 00112233445566778899AABBCCDDEE', str(tlv))

        tlv.setMode(Tlv.BER_1)
        self.assertEqual('0F 810F 00112233445566778899AABBCCDDEE', str(tlv))

        tlv.setMode(Tlv.BER_2)
        self.assertEqual('0F 82000F 00112233445566778899AABBCCDDEE', str(tlv))


        tlv = self._createInstance(0x10, HexList('00112233445566778899AABBCCDDEEFF'), Tlv.SIMPLE)
        self.assertEqual('10 10 00112233445566778899AABBCCDDEEFF', str(tlv))

        tlv.setMode(Tlv.BER_0)
        self.assertEqual('10 10 00112233445566778899AABBCCDDEEFF', str(tlv))

        tlv.setMode(Tlv.BER_1)
        self.assertEqual('10 8110 00112233445566778899AABBCCDDEEFF', str(tlv))

        tlv.setMode(Tlv.BER_2)
        self.assertEqual('10 820010 00112233445566778899AABBCCDDEEFF', str(tlv))



    # end def test_Str

    def test_GetTag(self):
        ''' getTag api '''
        self.assertEqual(0x01, self._createInstance(0x01).getTag())
    # end def test_GetTag

    def test_SetTag(self):
        ''' setTag api '''

        tlv = self.RefClass(0x01, None, Tlv.COMPACT)

        tlv.setTag(0x02)

        self.assertRaises(TlvError, tlv.setTag, 0x00)
        self.assertRaises(TlvError, tlv.setTag, 0x10)

        self.assertEqual(0x02, tlv.getTag())

        tlv.setMode(Tlv.SIMPLE)

        tlv.setTag(0x10)

        self.assertRaises(TlvError, tlv.setTag, 0xFF)
        self.assertRaises(TlvError, tlv.setTag, 0x100)

        self.assertEqual(0x10, tlv.getTag())
    # end def test_SetTag

    def test_GetLength(self):
        ''' getLength api '''

        tlv = self.RefClass(0x01, None)
        self.assertEqual(0x00, tlv.getLength())

        tlv.setValue(HexList(0x12, 0x34))
        self.assertEqual(0x02, tlv.getLength())
    # end def test_GetLength

    def test_GetTagLength(self):
        ''' getTagLength api '''

        tlv = self.RefClass(0x01, None, Tlv.COMPACT)
        self.assertEqual(HexList(0x10), tlv.getTagLength())

        tlv.setMode(Tlv.SIMPLE)
        self.assertEqual(HexList(0x01, 0x00), tlv.getTagLength())

        tlv.setMode(Tlv.BER_0)
        self.assertEqual(HexList(0x01, 0x00), tlv.getTagLength())

        tlv.setMode(Tlv.BER_1)
        self.assertEqual(HexList(0x01, 0x81, 0x00), tlv.getTagLength())

        tlv.setMode(Tlv.BER_2)
        self.assertEqual(HexList(0x01, 0x82, 0x00, 0x00), tlv.getTagLength())
    # end def test_GetTagLength

    def test_GetValue(self):
        ''' getValue api '''

        tlv = self._createInstance(0x01, HexList(0x12, 0x34))
        self.assertEqual(HexList(0x12, 0x34), tlv.getValue())
    # end def test_GetValue

    def test_ToHexList(self):
        ''' __hexlist__ api '''

        value = HexList(0xFF)

        tlv = self._createInstance(0x01, value, Tlv.COMPACT)
        self.assertEqual(HexList(0x11, value), tlv.__hexlist__())

        tlv.setMode(Tlv.SIMPLE)
        self.assertEqual(HexList(0x01, 0x01, value), tlv.__hexlist__())

        tlv.setMode(Tlv.BER_AUTO)
        self.assertEqual(HexList(0x01, 0x01, value), tlv.__hexlist__())

        value = value * 0x80
        tlv.setValue(value)

        tlv.setMode(Tlv.SIMPLE)
        self.assertEqual(HexList(0x01, 0x80, value), tlv.__hexlist__())

        tlv.setMode(Tlv.BER_1)
        self.assertEqual(HexList(0x01, 0x81, 0x80, value), tlv.__hexlist__())

        tlv.setMode(Tlv.BER_2)
        self.assertEqual(HexList(0x01, 0x82, 0x00, 0x80, value), tlv.__hexlist__())

        value = value * 0x02
        tlv.setValue(value)

        self.assertEqual(HexList(0x01, 0x82, 0x01, 0x00, value), tlv.__hexlist__())

        tlv.setMode(Tlv.BER_2)
        self.assertEqual(HexList(0x01, 0x82, 0x01, 0x00, value), tlv.__hexlist__())
    # end def test_ToHexList


    def test_FromHexList(self):
        ''' fromHexList api '''

        tlv = self.RefClass.fromHexList(HexList(0x10), mode=Tlv.COMPACT)

        self.assertEqual(0x01, tlv.getTag())
        self.assertEqual(0x00, tlv.getLength())
        self.assertEqual(HexList(), tlv.getValue())

        tlv = self.RefClass.fromHexList(HexList(0x12, 0x01, 0x02), mode=Tlv.COMPACT)

        self.assertEqual(0x01, tlv.getTag())
        self.assertEqual(0x02, tlv.getLength())
        self.assertEqual(HexList(0x01, 0x02), tlv.getValue())

        tlv = self.RefClass.fromHexList(HexList(0x12, 0x01, 0x02), mode=Tlv.SIMPLE)

        self.assertEqual(0x12, tlv.getTag())
        self.assertEqual(0x01, tlv.getLength())
        self.assertEqual(HexList(0x02), tlv.getValue())

        value = HexList(0x80) * 0x81

        tlv = self.RefClass.fromHexList(HexList(0x12, 0x81, value), mode=Tlv.SIMPLE)

        self.assertEqual(0x12, tlv.getTag())
        self.assertEqual(0x81, tlv.getLength())
        self.assertEqual(value, tlv.getValue())

        value = HexList(0x80) * 0x7F
        tlv = self.RefClass.fromHexList(HexList(0x12, 0x7F, value), mode=Tlv.BER_0)

        self.assertEqual(0x12, tlv.getTag())
        self.assertEqual(0x7F, tlv.getLength())
        self.assertEqual(value, tlv.getValue())

        value = HexList(0x80) * 0x81
        tlv = self.RefClass.fromHexList(HexList(0x12, 0x81, 0x81, value), mode=Tlv.BER_1)

        self.assertEqual(0x12, tlv.getTag())
        self.assertEqual(0x81, tlv.getLength())
        self.assertEqual(value, tlv.getValue())

        value[0:2] = (0x00, 0x7F)

        tlv = self.RefClass.fromHexList(HexList(0x12, 0x82, value), mode=Tlv.BER_2)

        self.assertEqual(0x12, tlv.getTag())
        self.assertEqual(0x7F, tlv.getLength())
        self.assertEqual(value[2:2+0x7F], tlv.getValue())

        value = HexList(0x66) * 0x10000
        tlv = self.RefClass.fromHexList(HexList(0x12, 0x83, 0x01, 0x00, 0x00, value), mode=Tlv.BER_AUTO)

        self.assertEqual(0x12, tlv.getTag())
        self.assertEqual(0x10000, tlv.getLength())
        self.assertEqual(value, tlv.getValue())

        # This error case should move to TlvList: It only fails because
        # 0x01 is interpreted as a tag.
        #self.assertRaises(TlvError,
        #                  Tlv.fromHexList,
        #                  HexList(0x10, 0x01), mode=Tlv.COMPACT)

        self.assertRaises(TlvError,
                          self.RefClass.fromHexList,
                          HexList(0x11), mode=Tlv.COMPACT)


        # This error case should move to TlvList: It only fails because
        # 0x01 is interpreted as a tag.
        #self.assertRaises(TlvError,
        #                  Tlv.fromHexList,
        #                  HexList(0x10, 0x00, 0x01), mode=Tlv.SIMPLE)

        self.assertRaises(TlvError,
                          self.RefClass.fromHexList,
                          HexList(0x10, 0x01), mode=Tlv.SIMPLE)


        value = HexList(0x00) * 0x80

        self.assertRaises(TlvError, self.RefClass.fromHexList,
                          HexList(0x10, 0x80, value), mode=Tlv.BER_AUTO)
    # end def test_FromHexList
# end class TlvTestCase



class TlvListTestCase(TestCase):
    '''
    TlvList implementation test.
    '''

    def setUp(self):
        '''
        Test setup
        '''
        TestCase.setUp(self)

        self._tlvs = TlvList(Tlv(0x01, None, Tlv.COMPACT),
                             Tlv(0x20, None, Tlv.SIMPLE),
                             TlvList(Tlv(0x30, None, Tlv.BER_0),
                                     Tlv(0x40, None, Tlv.BER_1),
                                     Tlv(0x50, None, Tlv.BER_2)))
    # end def setUp


    def test_Init(self):
        ''' __init__ api '''

        self.assertRaises(TlvError, TlvList, 0x10)
    # end def test_Init

    def test_Str(self):
        ''' __str__ api '''
        self.assertEqual("1 0  20 00  30 00  40 8100  50 820000 ",
                         str(self._tlvs))
    # end def test_Str


    def test_Contains(self):
        ''' __contains__ api '''

        for tag in (0x01, 0x20, 0x30, 0x40, 0x50):
            self.assertEqual(True, tag in self._tlvs)
        # end for

        self.assertEqual(False, 0x00 in self._tlvs)
    # end def test_Contains


    def test_ToHexList(self):
        ''' __hexlist__ api '''

        self.assertEqual(HexList(0x10,
                                0x20, 0x00,
                                0x30, 0x00,
                                0x40, 0x81, 0x00,
                                0x50, 0x82, 0x00, 0x00),
                         self._tlvs.__hexlist__())
    # end def test_ToHexList


    def test_FromHexList(self):
        ''' fromHexList api '''

        tlvs = TlvList.fromHexList(HexList(0x11, 0x01), mode=Tlv.COMPACT)

        self.assertEqual(1,
                         len(tlvs),
                         "Unexpected length")

        tlvs = TlvList.fromHexList(HexList(0x11, 0x01, 0x20), mode=Tlv.COMPACT)

        self.assertEqual(2, len(tlvs))
    # end def test_FromHexList
# end class TlvListTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
