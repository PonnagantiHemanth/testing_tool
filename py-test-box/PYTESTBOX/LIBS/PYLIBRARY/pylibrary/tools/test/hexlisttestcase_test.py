#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.hexlisttestcase

@brief HexList test implementation

@author christophe.roquebert

@date   2018/09/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.deprecation  import ignoredeprecation
from pylibrary.tools.hexlist       import HexList
from pylibrary.tools.hexlist       import HexListError
from pylibrary.tools.hexlist       import RandHexList
from pylibrary.tools.hexlist       import ReadOnlyHexList
from unittest                     import TestCase
import unittest

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class HexListTestCase(TestCase):                                                                                         # pylint:disable=R0904
    '''
    HexList test implementation.
    '''

    def setUp( self ):
        '''
        Initialize test
        '''
        TestCase.setUp(self)

        # Create
        self._hexBuf1 = HexList( 0x12, 2, 0x51, 0x56 )
        self._hexBuf2 = HexList( "   1402FFEB   " )
        self._hexBuf3 = HexList( self._hexBuf1 )
        self._hexBuf4 = self._hexBuf1+self._hexBuf2
        self._hexBuf5 = HexList(0x24, "122565", ( 1, 2, 3, 5 ), self._hexBuf1,
                               [12, 12, 12] )
        self._hexBuf5 = self._hexBuf5 + "45"
        self._hexBuf5 += "45"
    # end def setUp

    def test_Comparator(self):
        '''Tests the comparators'''
        hexBuf1 = HexList("01020304")
        hexBuf2 = HexList("01020304")
        hexBuf3 = HexList("04030201")

        self.assertNotEqual(hexBuf1, hexBuf3, "Invalid comparator")
        self.assertEqual(hexBuf1, hexBuf2, "Invalid comparator")
    # end def test_Comparator

    def test_Construction(self):
        '''Test the construction'''

        # String
        hexBuf1 = HexList("01020304")
        hexBuf2 = HexList(hexBuf1)
        self.assertEqual(hexBuf1, hexBuf2, "Invalid construction")

        # Spaces
        hexBuf2 = HexList( "   1402FFEB   " )
        expected = HexList("1402FFEB")
        self.assertEqual(expected, hexBuf2, "Invalid construction")

        # Integers
        hexBuf3 = HexList( 0x12, 2, 0x51, 0x56 )
        expected = HexList("12025156")
        self.assertEqual(expected, hexBuf3, "Invalid construction")

        hexBuf3 = HexList( 255 )
        expected = HexList("FF")
        self.assertEqual(expected, hexBuf3, "Invalid construction")

        # Mixed
        hexBuf4 = HexList(0x24, "122565", ( 1, 2, 3, 5 ), HexList("01020304"),
                         [12, 12, 12])
        expected = HexList("2412256501020305010203040C0C0C")
        self.assertEqual(expected, hexBuf4, "Invalid concatenation")

        class HexListable(object):
            '''
            Class that defined a __hexlist__ method, different from its str method
            '''

            def __hexlist__(self):                                                                                       # pylint: disable=R0201
                '''
                Converts the current object to an HexList.

                @return The current object, as an HexList
                '''
                return HexList("01020304")
            # end def __hexlist__

            def __str__(self):                                                                                          # pylint: disable=R0201
                '''
                Converts the current object to a string.

                @return The current object, as a string.
                '''
                return "05060708"
            # end def __str__
        # end class HexListable

        hexlistable = HexListable()
        hexBuf5 = HexList(hexlistable)
        expected = HexList("0102") + HexList("0304")
        self.assertEqual(expected,
                         hexBuf5,
                         "Invalid implicit construction")

    # end def test_Construction

    def test_Contains(self):
        '''
        Tests __contains__ method
        '''
        hexBuf = HexList("01 02 03 04 05 06 07 08 09")

        self.assertTrue(0x06 in hexBuf, 'Invalid item research')

        self.assertFalse(0x0A in hexBuf, 'Invalid item research')

        self.assertTrue(HexList('04 05') in hexBuf, 'Invalid sublist research')

        self.assertFalse(HexList('05 04') in hexBuf, 'Invalid sublist research')

    # end def test_Contains

    def test_Index(self):
        '''
        Tests index method
        '''
        hexBuf = HexList("00 01 02 06 04 05 06 07 06 04 05 06")

        self.assertEqual(3,
                         hexBuf.index(0x06),
                         'Invalid item research')

        self.assertEqual(8,
                         hexBuf.index(0x06, 7),
                         'Invalid item research')

        self.assertEqual(6,
                         hexBuf.index(0x06, 4, 7),
                         'Invalid item research')

        self.assertEqual(4,
                         hexBuf.index(HexList('04 05')),
                         'Invalid sublist research')

        self.assertEqual(9,
                         hexBuf.index(HexList('04 05'), 5),
                         'Invalid sublist research')

    # end def test_Index

    def test_Index_ValueError(self):
        '''
        Tests index method with wrong result
        '''
        hexBuf = HexList("00 01 02 06 04 05 06 07 06 04 05 06")

        self.assertRaises(ValueError,
                          hexBuf.index,
                          0x0A)

        self.assertRaises(ValueError,
                          hexBuf.index,
                          0x07,
                          8)

        self.assertRaises(ValueError,
                          hexBuf.index,
                          0x07,
                          6,
                          7)

        self.assertRaises(ValueError,
                          hexBuf.index,
                          HexList('05 04'))

        self.assertRaises(ValueError,
                          hexBuf.index,
                          HexList('04 05'),
                          10)

        self.assertRaises(ValueError,
                          hexBuf.index,
                          HexList('04 05'),
                          5,
                          9)

    # end def test_Index_ValueError

    def test_Construction_Performance_String(self):
        '''
        Tests some specific cases of performance on the construction
        '''


        hexBuf = HexList(0x96) * 1024 * 50

        #tick = time()
        obtained = HexList(hexBuf)
        #tock = time()

        # print "Time for construction: %fs" % (tock - tick)

        self.assertEqual(hexBuf,
                         obtained,
                         "Invalid copy construction")

        # String construction:
        referenceValues = ('"0102030405060708090A0B0C0D0E0F"',
                           '"%s"' % (''.join(['%02X' % (x % 256) for x in range(256)]),),
                           '"%s"' % (''.join(['%02X' % (x % 256) for x in range(1024)]),),
                           )

        # Methods: A tuple of dict(initialization, code)
        methods = ( {'name':            'Current implementation',
                     'initialization': 'from pylibrary.tools.hexlist import HexList\nvalue = %s',
                     'code':            'HexList(value)',
                     },
                    {'name':            'Parsing (original)',
                     'initialization' : 'from pylibrary.tools.hexlist import HexListError\nvalue = %s',
                     'code':            '\n'.join((
                                            'parseVal = []',
                                            'for offset in range(0, len(value), 2):',
                                            '    try:',
                                            '        parseVal.append(int(value[offset:offset+2], 16))',
                                            '    except:',
                                            '        raise HexListError("No hexadecimal representation (%s)!"',
                                            '                        % (value,))',
                                            '    # end try',
                                            '# end for',
                                            ))
                     },

                    {'name':            'Pre-computed values',
                     'initialization':  '\n'.join(( "from pylibrary.tools.hexlist import HexListError",
                                                    "srcDict =dict(zip(['%%02X'%%x for x in range(256)], [x for x in range(256)]))",
                                                    "value = %s",
                                                    )),
                     'code':            '\n'.join((
                                                    'parseVal = []',
                                                    'value = value.upper()',
                                                    'for offset in range(0, len(value), 2):',
                                                    '    try:',
                                                    '        parseVal.append(srcDict[value[offset:offset+2]])',
                                                    '    except:',
                                                    '        raise HexListError("No hexadecimal representation (%s)!"',
                                                    '                        % (value,))',
                                                    '    # end try',
                                                    '# end for',
                                                    )),
                             },
                    {'name':            'Pre-computed values, outer try',
                     'initialization' :  '\n'.join(("from pylibrary.tools.hexlist import HexListError",
                                                    "srcDict =dict(zip(['%%02X'%%x for x in range(256)], [x for x in range(256)]))",
                                                    "value = %s",
                                                    )),
                     'code':            '\n'.join(( 'parseVal = []',
                                                    'if (value.islower()):'
                                                    '    value = value.upper()',
                                                    'try:',
                                                    '    parseVal = [srcDict[value[offset:offset+2]] for offset in range(0, len(value), 2)]',
                                                    'except:',
                                                    '    raise HexListError("No hexadecimal representation (%s)!"',
                                                    '                    % (value,))',
                                                    '# end try',
                                                    ))
                     },
                    {'name':            'Computed',
                     'initialization': '\n'.join(("from pylibrary.tools.hexlist import HexListError",
                                                    "value = %s",
                                                    )),
                     'code':            '\n'.join(('parseVal = []',
                                                    'value = value.upper()',
                                                    'def h2d(h):',
                                                    '  h = ord(h)',
                                                    '  h = (h >= 65) and (h - 55) or (h - 30)',
                                                    '  return h',
                                                    'try:',
                                                    '    parseVal = [h2d(value[offset])*16 + h2d(value[offset+1]) for offset in range(0, len(value), 2)]',
                                                    'except:',
                                                    '    raise HexListError("No hexadecimal representation (%s)!"',
                                                    '                    % (value,))',
                                                    '# end try',
                                                    )),
                     },
                    {'name':            'binascii',
                     'initialization': "from binascii import a2b_hex\nvalue = %s\nfrom pylibrary.tools.hexlist import HexListError",
                     'code':            '\n'.join(( 'try:',
                                                    '    parseVal = [ord(x) for x in a2b_hex(value).decode("utf-8", "backslashreplace")]',
                                                    'except:',
                                                    '    raise HexListError("No hexadecimal representation (%s)!"',
                                                    '                    % (value,))',
                                                    '# end try',
                                                    )),
                     },
                    {'name':            'binascii arrays',
                     'initialization': "from binascii import a2b_hex\nfrom array import array\nvalue = %s\nfrom pylibrary.tools.hexlist import HexListError",
                     'code':            '\n'.join(( 'try:',
                                                    '    parseVal = array("B")',
                                                    '    parseVal.frombytes(a2b_hex(value))',
                                                    'except:',
                                                    '    raise',
                                                    '    raise HexListError("No hexadecimal representation (%s)!"',
                                                    '                    % (value,))',
                                                    '# end try',
                                                    )),
                     },
                   )
        # pylint:disable=W0612

        import timeit
        loopCount = 50

        for source in referenceValues:

            bestValue  = float(1000000 * 3600) # 1 hour...
            worstValue = 0

            for _, initialization, code in [(e['name'], e['initialization'], e['code']) for e in methods]:



                timer  = timeit.Timer(code, initialization % source)
                result = timer.timeit(number=loopCount)

                if (bestValue > result):
                    bestValue  = result
                # end if

                if (worstValue < result):
                    worstValue  = result
                # end if
            # end for
        # end for
    # end def test_Construction_Performance_String

    def test_Construction_Performance_Int(self):
        '''
        Tests some specific cases of performance on the construction
        '''


        hexBuf = HexList(0x96) * 1024 * 50
        obtained = HexList(hexBuf)
        self.assertEqual(hexBuf,
                         obtained,
                         "Invalid copy construction")

        # String construction:
        referenceValues = ('(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)',
                           '[%s]' % (','.join(['%d' % (x % 256) for x in range(256)]),),
                           '[%s]' % (','.join(['%d' % (x % 256) for x in range(1024)]),),
                           )

        # Methods: A tuple of dict(initialization, code)
        methods = ( {'name':            'Current implementation',
                     'initialization': 'from pylibrary.tools.hexlist import HexList\nvalue = %s',
                     'code':            'HexList(value)',
                     },
                    {'name':            'Returned list',
                     'initialization':  '\n'.join(( "from pylibrary.tools.hexlist import HexListError",
                                                    "value = %s",
                                                    )),
                     'code':            '\n'.join((
                                                    'parseVal = []',
                                                    'for element in value:',
                                                    '    parseVal.extend([element])',
                                                    '# end for',
                                                    )),
                             },
                    {'name':            'Collector',
                     'initialization':  '\n'.join(( "from pylibrary.tools.hexlist import HexListError",
                                                    "value = %s",
                                                    )),
                     'code':            '\n'.join((
                                                    'parseVal = []',
                                                    'for element in value:',
                                                    '    parseVal.append(element)',
                                                    '# end for',
                                                    )),
                             },
                   )
        # pylint:disable=W0612

        import timeit
        loopCount = 50

        for source in referenceValues:

            bestValue  = float(1000000 * 3600) # 1 hour...
            worstValue = 0

            for _, initialization, code in [(e['name'], e['initialization'], e['code']) for e in methods]:

                timer  = timeit.Timer(code, initialization % source)
                result = timer.timeit(number=loopCount)

                if (bestValue > result):
                    bestValue  = result
                # end if

                if (worstValue < result):
                    worstValue  = result
                # end if
            # end for
        # end for
    # end def test_Construction_Performance_Int

    def test_Concatenation(self):
        '''Test the concatenation'''

        hexBuf1 = HexList("01020304")
        hexBuf2 = HexList("05060708")

        # HexList concatenation
        expected = HexList("0102030405060708")
        self.assertEqual(expected, hexBuf1 + hexBuf2, "Invalid concatenation")

        hexBuf3 = hexBuf1[:]
        hexBuf3 += hexBuf2
        expected = HexList("0102030405060708")
        self.assertEqual(expected, hexBuf3, "Invalid concatenation")

        # Integer concatenation
        expected = HexList("0102030405")
        self.assertEqual(expected, hexBuf1 + 5, "Invalid concatenation")

        hexBuf4 = hexBuf1[:]
        hexBuf4 += 5
        self.assertEqual(expected, hexBuf4, "Invalid concatenation")

        # String concatenation
        expected = HexList("010203040506")
        self.assertEqual(expected, hexBuf1 + "0506", "Invalid concatenation")

        hexBuf5 = hexBuf1[:]
        hexBuf5 += "0506"
        self.assertEqual(expected, hexBuf5, "Invalid concatenation")

        # Mixed concatenation
        hexBuf6 = HexList()
        hexBuf6 = hexBuf6 + 0x24
        hexBuf6 = hexBuf6 + "122565"
        hexBuf6 = hexBuf6 + ( 1, 2, 3, 5 )
        hexBuf6 = hexBuf6 + HexList("01020304")
        hexBuf6 = hexBuf6 + [12, 12, 12]
        expected = HexList("2412256501020305010203040C0C0C")
        self.assertEqual(expected, hexBuf6, "Invalid concatenation")

        hexBuf7 = HexList()
        hexBuf7 += 0x24
        hexBuf7 += "122565"
        hexBuf7 += ( 1, 2, 3, 5 )
        hexBuf7 += HexList("01020304")
        hexBuf7 += [12, 12, 12]
        expected = HexList("2412256501020305010203040C0C0C")
        self.assertEqual(expected, hexBuf7, "Invalid concatenation")

        # append
        hexBuf8 = HexList("0102")
        hexBuf8.append(0x55)
        expected = HexList("010255")
        self.assertEqual(expected, hexBuf8, "Invalid concatenation")

        hexBuf9 = HexList("0102")
        hexBuf9.extend("AABB")
        expected = HexList("0102AABB")
        self.assertEqual(expected, hexBuf9, "Invalid concatenation")
    # end def test_Concatenation

    def test_Deletion(self):
        '''Test the deletion'''

        hexBuf1 = HexList("01020304")
        del hexBuf1[2:]
        expected = HexList("0102")
        self.assertEqual(expected, hexBuf1, "Invalid deletion")
    # end def test_Deletion

    def test_Insertion(self):
        '''Test the insertion'''

        hexBuf1 = HexList("0102030405")
        expected = HexList("0102AABBCCDD05")
        hexBuf1[2:4] = "AABBCCDD"
        self.assertEqual(expected, hexBuf1, "Invalid Replacement")

        hexBuf2 = HexList("0102030405")
        expected = HexList("0102AABB05")
        hexBuf2[2:4] = "AABB"
        self.assertEqual(expected, hexBuf2, "Invalid Replacement")

        hexBuf3 = HexList("0102030405")
        expected = HexList("0102AABBCCDD0405")
        hexBuf3[2] = "AABBCCDD"
        self.assertEqual(expected, hexBuf3, "Invalid Replacement")

        hexBuf4 = HexList("0102030405")
        expected = HexList("0102AABBCCDD030405")
        hexBuf4.insert(2, "AABBCCDD")
        self.assertEqual(expected, hexBuf4, "Invalid Insertion")
    # end def test_Insertion

    def test_Modification(self):
        '''Test the modification'''

        hexBuf1 = HexList("01020304")
        expected = HexList("01420304")

        hexBuf1[1] = 0x42
        self.assertEqual(expected, hexBuf1, "Invalid modification")
    # end def test_Modification

    def test_Extraction(self):
        '''Test the extraction'''

        hexBuf1 = HexList("01020304")
        expected = HexList("0203")
        self.assertEqual(expected, hexBuf1[1:3], "Invalid extraction")
    # end def test_Extraction

    def test_SliceExtraction(self):
        '''Test the extraction of a slice, with stepping'''

        hexBuf1 = HexList("01020304")
        expected = HexList("0103")
        obtained = hexBuf1[::2]
        self.assertEqual(expected,
                         obtained,
                         "Invalid extraction")

        self.assertTrue(isinstance(obtained, HexList),
                        'Invalid type for extracted slice')

        value = HexList('010203')
        expected = HexList('010203')
        obtained = value[-4:]
        self.assertEqual(expected,
                         obtained,
                         'invalid negative extraction')
        self.assertTrue(isinstance(obtained, HexList),
                        'Invalid type for extracted slice')

    # end def test_SliceExtraction

    def test_Display(self):
        '''Test string conversion'''

        hexBuf1 = HexList("0F1E2D3C4B5A69788796A5B4C3D2E1F0")
        expected = "0F1E2D3C4B5A69788796A5B4C3D2E1F0"

        self.assertEqual(expected, str(hexBuf1), "Invalid display")
    # end def test_Display

    def test_Representation(self):
        '''Test repr conversion'''

        hexBuf1 = HexList("0F1E2D3C4B5A69788796A5B4C3D2E1F0")
        expected = "HexList('0F1E2D3C4B5A69788796A5B4C3D2E1F0')"

        self.assertEqual(expected, repr(hexBuf1), "Invalid representation")
    # end def test_Representation

    def test_Multiplication(self):
        '''Test the multiplication'''

        hexBuf1 = HexList("01020304")
        expected = HexList("0102030401020304")
        self.assertEqual( expected, hexBuf1 * 2, "Invalid multiplication" )

        hexBuf2 = HexList("01020304")
        hexBuf2 *= 2
        expected = HexList("0102030401020304")
        self.assertEqual( expected, hexBuf2, "Invalid multiplication" )
    # end def test_Multiplication

    def test_TestBit(self):
        '''Test the testBit'''

        # testBit
        hexBuf1 = HexList("001000")
        expected = True
        self.assertEqual(expected, hexBuf1.testBit(12), "Invalid testBit" )

        hexBuf1 = HexList("FFEFFF")
        expected = False
        self.assertEqual(expected, hexBuf1.testBit(12), "Invalid testBit" )
    # end def test_TestBit

    def test_ClearBit(self):
        '''Test the clearBit'''

        hexBuf1 = HexList("001000")
        expected = HexList("000000")
        hexBuf1.clearBit(12)
        self.assertEqual(expected, hexBuf1, "Invalid clearBit" )

        hexBuf1 = HexList("FFFFFF")
        expected = HexList("FFEFFF")
        hexBuf1.clearBit(12)
        self.assertEqual(expected, hexBuf1, "Invalid clearBit" )
    # end def test_ClearBit

    def test_SetBit(self):
        '''Test the setBit'''

        hexBuf1 = HexList("000000")
        expected = HexList("001000")
        hexBuf1.setBit(12)
        self.assertEqual(expected, hexBuf1, "Invalid setBit" )

        hexBuf1 = HexList("FFEFFF")
        expected = HexList("FFFFFF")
        hexBuf1.setBit(12)
        self.assertEqual(expected, hexBuf1, "Invalid setBit" )
    # end def test_SetBit

    def test_UpdateBit(self):
        '''Test the updateBit'''

        hexBuf1 = HexList("000000")
        expected = HexList("001000")
        hexBuf1.updateBit(12, 1)
        self.assertEqual(expected, hexBuf1, "Invalid updateBit" )

        hexBuf1 = HexList("000000")
        expected = HexList("000000")
        hexBuf1.updateBit(12, 0)
        self.assertEqual(expected, hexBuf1, "Invalid updateBit" )

        hexBuf1 = HexList("FFFFFF")
        expected = HexList("FFEFFF")
        hexBuf1.updateBit(12, 0)
        self.assertEqual(expected, hexBuf1, "Invalid updateBit" )

        hexBuf1 = HexList("FFFFFF")
        expected = HexList("FFFFFF")
        hexBuf1.updateBit(12, 1)
        self.assertEqual(expected, hexBuf1, "Invalid updateBit" )
    # end def test_UpdateBit

    def test_InvertBit(self):
        '''Test the invertBit'''

        hexBuf1 = HexList("000000")
        expected = HexList("001000")
        hexBuf1.invertBit(12)
        self.assertEqual(expected, hexBuf1,
                         "Invalid invertBit")

        hexBuf1 = HexList("FFFFFF")
        expected = HexList("FFEFFF")
        hexBuf1.invertBit(12)
        self.assertEqual(expected, hexBuf1,
                         "Invalid invertBit")
    # end def test_InvertBit

    def test_HexToLong(self):
        '''Test the hexToLong'''

        hexBuf1 = HexList("FFFFFF")
        expected = 0xFFFFFF
        self.assertEqual(expected, hexBuf1.hexToLong(),
                         "Invalid hexToLong")

        hexBuf1 = HexList("FF00FF")
        expected = 0xFF00FF
        self.assertEqual(expected, hexBuf1.hexToLong(),
                         "Invalid hexToLong")

        hexBuf2 = HexList("112233")
        expected = 0x112233
        self.assertEqual(expected,
                         hexBuf2.hexToLong(False),
                         "Invalid big endian hexToLong ")

        hexBuf2 = HexList("112233")
        expected = 0x332211
        self.assertEqual(expected,
                         hexBuf2.hexToLong(True),
                         "Invalid little endian hexToLong")


    # end def test_HexToLong

    def test_FromLong(self):
        '''Test the fromLong static method'''

        # Value < 0
        self.assertRaises(ValueError,
                          HexList.fromLong,
                          -1,
                          1)

        # count > 0
        self.assertRaises(ValueError,
                          HexList.fromLong,
                          1,
                          0)


        referenceValues = ((0xFF,         1, HexList(0xFF)                   ),
                           (0x1234567,    2, HexList(0x45, 0x67)             ),
                           (0x123,        7, HexList("00000000000123")       ),
                           (0x00,      None, HexList(0x00)                   ),
                           (0x1234567, None, HexList(0x01, 0x23, 0x45, 0x67) ),
                           )

        for longValue, count, expected in referenceValues:
            self.assertEqual(expected,
                             HexList.fromLong(longValue, count),
                             "Invalid conversion from Long")
        # end for
    # end def test_FromLong


    def test_ToString(self):
        ''' Test the toString method '''
        referenceValues = (("Python", HexList(0x50, 0x79, 0x74, 0x68, 0x6F, 0x6E)),
                           ("", HexList()),
                           )

        for expected, hexBuf in referenceValues:
            self.assertEqual(expected,
                             hexBuf.toString(),
                             "Invalid conversion from HexList to String")
        # end for
    # end def test_ToString

    def test_FromString(self):
        ''' Test the fromString static method '''
        referenceValues = (("Python", HexList(0x50, 0x79, 0x74, 0x68, 0x6F, 0x6E)),
                           ("", HexList()),
                           )

        for msg, expected in referenceValues:
            self.assertEqual(expected,
                             HexList.fromString(msg),
                             "Invalid conversion from String to HexList")
        # end for
    # end def test_FromString

    def test_ToString_Performance(self):                                                                                # pylint:disable=R0201
        '''
        Tests the performance of various toString conversions methods
        '''
        referenceValues = ("(0x50, 0x79, 0x74, 0x68, 0x6F, 0x6E)",
                           "(%s)" % (', '.join(['0x%02X' % (x%256,) for x in range(256)])),
                           "(%s)" % (', '.join(['0x%02X' % (x%256,) for x in range(1024)])),
                           )
#        stepSize = 256
#        referenceValues = [("(%s)" % (', '.join(['0x%02X' % (x%256,) for x in range(size)]))) for size in range(stepSize, 1024 * 10, stepSize)]
        # pylint:disable=W0612

        # Methods: A tuple of dict(initialization, code)
        methods = (  {'name':            'Formatting (original)',
                      'initialization':  "value = %s",
                      'code':            "''.join(['%02X' % (item,) for item in value])",
                      },
                     {'name':           'Pre-computed values (dict)',
                      'initialization': "srcDict =dict(zip([x for x in range(256)], ['%%02X'%%x for x in range(256)]))\nvalue = %s",
                      'code':           "''.join([srcDict[item] for item in value])",
                      },
                     {'name':           'Pre-computed values (list)',
                      'initialization': "srcList = list(['%%02X'%%x for x in range(256)])\nvalue = %s",
                      'code':           "''.join([srcList[item] for item in value])",
                      },
                     {'name':           'Pre-computed values (tuple)',
                      'initialization': "srcList = tuple(['%%02X'%%x for x in range(256)])\nvalue = %s",
                      'code':           "''.join([srcList[item] for item in value])",
                      },
                     {'name':           'binascii',
                      'initialization': "from binascii import b2a_hex\nvalue = %s",
                      'code':           "b2a_hex(''.join([chr(x) for x in value]).encode('utf-8')).upper()",
                      },
                     {'name':           'reduce/format',
                      'initialization': "from functools import reduce\nvalue = %s",
                      'code':           "('%%0%dX' % (len(value)*2,)) % reduce(lambda x,y: (x<<8)|y, value, 0)",
                      },
                     {'name':           'binascii array',
                      'initialization': "from binascii import b2a_hex\nfrom functools import reduce\nfrom array import array\nvalue = list(%s)",
                      'code':           '\n'.join(("b2a_hex(array('B', value).tobytes()).upper()",
                                                   )),
                      },
                     {'name':           'binascii pack',
                      'initialization': "from binascii import b2a_hex\nfrom struct import pack\nvalue = list(%s)",
                      'code':           '\n'.join(("b2a_hex(pack('%dB' % (len(value),), *value)).upper()",
                                                   )),
                      },
                     )

        import timeit
        loopCount = 50
        printIt = False

        resultsLine = [x['name'] for x in methods]
        resultsLine.insert(0, 'HexList size')
        resultsArray = [resultsLine]
        # Method 0: current implementation
        for source in referenceValues:

            if (printIt):
                print('\n')
            # end if
            bestValue  = float(1000000 * 3600) # 1 hour...
            worstValue = 0
            bestMethod  = "Unknown"
            worstMethod = "Unknown"

            sourceLen = len(eval(source))

            resultsLine = [str(sourceLen)]
            for name, initialization, code in [(e['name'], e['initialization'], e['code']) for e in methods]:

                initialization = initialization % source

                timer  = timeit.Timer(code, initialization)
                result = timer.timeit(number=loopCount)

                if (printIt):
                    print(("%.4f ms/pass, %.6f ms/pass/byte (%s)" % (
                                                       1000 * result/loopCount,
                                                       1000 * result/(loopCount * sourceLen),
                                                       name,)))
                # end if

                if (bestValue > result):
                    bestValue  = result
                    bestMethod = name
                # end if

                if (worstValue < result):
                    worstValue  = result
                    worstMethod = name
                # end if

                resultsLine.append(str(result))
            # end for
            resultsArray.append(resultsLine)

            if (printIt):
                print(("--- Best result for a sequence of %d bytes: %s (%.4f ms/pass, %.6f ms/pass/byte)" % \
                    (sourceLen,
                     bestMethod,
                     1000 * bestValue / loopCount,
                     1000 * bestValue / (loopCount * sourceLen),
                     )))
                print(("--- Worst result for a sequence of %d bytes: %s (%.4f ms/pass, %.6f ms/pass/byte)" % \
                    (sourceLen,
                     worstMethod,
                     1000 * worstValue / loopCount,
                     1000 * worstValue / (loopCount * sourceLen),
                     )))

                print(("--- Ratio betwen best and worst implementations: %.4f" % (bestValue / worstValue,)))
            # end if
        # end for

        if (printIt):
            print('Excel CSV:')
            for resultLine in resultsArray:
                print((', '.join(resultLine)))
            # end for
        # end if
    # end def test_ToString_Performance

    @ignoredeprecation
    def test_Xor(self):
        '''Test the __xor__'''

        hexBuf1 = HexList("FF00FF")
        expected = HexList("00FF00")
        self.assertEqual(expected, hexBuf1 ^ HexList("FFFFFF"),
                         "Invalid xor result: %s" % (hexBuf1 ^ HexList("FFFFFF")))

        hexBuf1 = HexList("00FF")
        expected = HexList("FFFF00")
        hexBuf1 ^= HexList("FFFFFF")
        self.assertEqual(expected, hexBuf1,
                         "Invalid xor result: %s" % hexBuf1)

        hexBuf1 = HexList("1100FF")
        expected = HexList("11FF00")
        hexBuf1 ^= HexList("FFFF")
        self.assertEqual(expected, hexBuf1,
                         "Invalid xor result: %s" % hexBuf1)
    # end def test_Xor

    def test_XorPerformance(self):
        '''
        Tests a XOR on a huge HexList
        '''
        length = 1024
        hexBuf1 = HexList(0x96) * length
        hexBuf2 = HexList(0x69) * length

        expected = HexList(0xFF) * length

        #tick = time()
        obtained = hexBuf1 ^ hexBuf2
        #tock = time()

        # print "Time for a complete XOR: %fs" % (tock - tick)

        self.assertEqual(expected,
                         obtained,
                         "Invalid massive XOR")
    # end def test_XorPerformance


    def test_ReadOnly(self):
        '''
        Tests a read-only HexList
        '''
        value = HexList(0xFF)
        value.setReadOnly()

        self.assertRaises(HexListError,
                          value.setBit,
                          1)

        self.assertRaises(HexListError,
                          value.clearBit,
                          1)

        self.assertRaises(HexListError,
                          value.__setitem__,
                          1, 2)

        self.assertRaises(HexListError,
                          value.__setslice__,
                          1, 2, (3,4))

        def callback():
            '''
            Callback for bytecode access through STORE_SUBSCR:
            Should redirect to __setitem__
            '''
            value[1] = 0x99
        # end def callback
        self.assertRaises(HexListError,
                          callback)
    # end def test_ReadOnly

    @ignoredeprecation
    def test_And(self):
        '''
        Test the __and__
        '''

        hexBuf1 = HexList("FF00FF")
        expected = HexList("000000")
        self.assertEqual(expected, hexBuf1 & "00FF00",
                         "Invalid and result: %s" % (hexBuf1 & "00FF00"))

        hexBuf1 = HexList("00FF")
        expected = HexList("00FF")
        hexBuf1 &= HexList("FFFFFF")
        self.assertEqual(expected, hexBuf1,
                         "Invalid and result: %s" % hexBuf1)

        hexBuf1 = HexList("777777")
        expected = HexList("11")
        hexBuf1 &= HexList("19")
        self.assertEqual(expected, hexBuf1,
                         "Invalid and result: %s" % hexBuf1)
    # end def test_And

    @ignoredeprecation
    def test_Or(self):
        '''Test the __or__'''

        hexBuf1 = HexList("FF00FF")
        expected = HexList("FFFFFF")
        self.assertEqual(expected, hexBuf1 | "00FF00",
                         "Invalid or result: %s" % (hexBuf1 | "00FF00"))

        hexBuf1 = HexList("00FF")
        expected = HexList("FF00FF")
        hexBuf1 |= HexList("FF00FF")
        self.assertEqual(expected, hexBuf1,
                         "Invalid or result: %s" % hexBuf1)

        hexBuf1 = HexList("777777")
        expected = HexList("77777F")
        hexBuf1 |= HexList("19")
        self.assertEqual(expected, hexBuf1,
                         "Invalid or result: %s" % hexBuf1)
    # end def test_Or

    def test_Invert(self):
        '''Test the __invert__'''

        hexBuf1 = HexList("FF00FF")
        expected = HexList("00FF00")
        self.assertEqual(expected, ~hexBuf1,
                         "Invalid invert result: %s" % (~hexBuf1))

        hexBuf1 = HexList("777777")
        expected = HexList("888888")
        self.assertEqual(expected, ~hexBuf1,
                         "Invalid invert result: %s" % (~hexBuf1))
    # end def test_Invert

    def test_InvertPerformance(self):
        '''Test the performance of the __invert__ method'''
        hexBuf   = HexList(0x96) * 1024 * 50
        expected = HexList(0x69) * 1024 * 50

        #tick = time()
        obtained = ~hexBuf
        #tock = time()

        # print "Time for a complete inversion: %fs" % (tock - tick)


        self.assertEqual(expected,
                         obtained,
                         "Unexpected inversion")
    # end def test_InvertPerformance

    def test_AddPadding(self):
        '''Test the addPadding'''

        hexBuf1 = HexList(1)
        expected = "00000001"
        hexBuf1.addPadding(4)
        self.assertEqual(expected, str(hexBuf1),
                         "Invalid addPadding")

        hexBuf1 = HexList(1)
        expected = "01000000"
        hexBuf1.addPadding(4, fromLeft=False)
        self.assertEqual(expected, str(hexBuf1),
                         "Invalid addPadding")

        hexBuf1 = HexList(1)
        expected = HexList("88888801")
        hexBuf1.addPadding(4, 0x88)
        self.assertEqual(expected, hexBuf1,
                         "Invalid addPadding")

        hexBuf1 = HexList(1)
        expected = HexList("01888888")
        hexBuf1.addPadding(4, 0x88, False)
        self.assertEqual(expected, hexBuf1,
                         "Invalid addPadding")
    # end def test_AddPadding

    def test_Copy(self):
        '''Test the copy'''

        hexBuf1 = HexList("001000")
        expected = HexList("001000")
        hexBuf2 = hexBuf1.copy()
        self.assertEqual(expected, hexBuf2, "Invalid copy" )

        hexBuf1 = HexList("FFEFFF")
        expected = HexList("FFEFFF")
        hexBuf2 = hexBuf1.copy()
        self.assertEqual(expected, hexBuf2, "Invalid copy" )
    # end def test_Copy

    def test_Exceptions(self):
        '''Test non-nominal cases: Exceptions'''

        # Exception
        try:
            HexList("1002FZEB")
            self.fail("HexListError should have been raised (illegal character)")
        except HexListError:
            pass
        # end try

        try:
            HexList("102FFEB")
            self.fail("HexListError should have been raised (parity)")
        except HexListError:
            pass
        # end try

        try:
            HexList(self.__init__)
            self.fail("HexListError should have been raised (type)")
        except HexListError:
            pass
        # end try

        try:
            HexList("112233").addPadding(2)
            self.fail("HexListError should have been raised (lg)")
        except HexListError:
            pass
        # end try

        try:
            HexList("112233").updateBit(2, 2)
            self.fail("HexListError should have been raised (updateBit value)")
        except HexListError:
            pass
        # end try

        try:
            HexList( 256 )
            self.fail("HexListError should have been raised (no byte)")
        except HexListError:
            pass
        # end try
    # end def test_Exceptions

#    def testIaddPerformance(self):
#        '''
#        Tests the performance of huge IADD
#        '''
#        value = HexList()
#        adder = HexList(1,2,3)
#        count = 300
#        from time import time
#        tick = time()
#        for _ in range(count):
#            value += adder
#        # end for
#        tock = time()
#
#        print 'Appended %d %d-byte hexlists in %.3fs' % (count, len(adder), (tock - tick))
#    # end def testIaddPerformance


# end class HexListTestCase

class RandHexListTestCase(TestCase):
    '''
    RandHexList test implementation.
    '''

    def test_Init(self):
        '''Tests the Construtor'''

        self.assertEqual(5, len(RandHexList(5)),
                         "Incorrect size")

        randHexList1 = RandHexList(1000)
        randHexList2 = RandHexList(1000)
        self.assertNotEqual(randHexList1, randHexList2,
                            "Incorrect random creation")

        randHexList1 = RandHexList(1000, maxVal=5)
        self.assertEqual([], [x for x in randHexList1 if x>5],
                         "Rand greater than maxVal created")

        randHexList1 = RandHexList(1000, minVal=5)
        self.assertEqual([], [x for x in randHexList1 if x<5],
                         "Rand greater than maxVal created")
    # end def test_Init
# end class RandHexListTestCase

class ReadyOnlyHexListTestCase(TestCase):
    '''
    Test of the read-only HexList class
    '''
    def testReadOnly(self):
        '''
        Test read-only access
        '''
        h1 = ReadOnlyHexList(1, 2, 3)
        self.assertRaises(Exception,
                          h1.__setitem__,
                          0,
                          1)

        def callback():
            '''
            A callback for testing slice assignment
            '''
            h1[0] = 5
        # end def callback
        self.assertRaises(Exception,
                          callback)
    # end def testReadOnly

    def testCopy(self):
        '''
        Test read-only copy
        '''
        expected = ReadOnlyHexList(1, 2, 3)
        obtained = expected.copy()

        self.assertEqual(expected,
                         obtained,
                         'Invalid read-only copy')

        self.assertRaises(Exception,
                          obtained.__setitem__,
                          0,
                          1)
    # end def testCopy

# end class ReadyOnlyHexListTestCase

if __name__ == '__main__':
    unittest.main()
    
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
