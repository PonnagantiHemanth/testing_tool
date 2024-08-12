#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.binaryfilestestcase

@brief Binary file parsing test case

@author christophe.roquebert

@date   2018/02/14
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path import join
from shutil import rmtree
from unittest import TestCase

from pylibrary.tools.hexlist import HexList
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class BinaryFileTestCase(TestCase):                                                                                     # pylint:disable=R0901
    '''
    Generic tests on a binary file format
    '''

    def setUp(self):
        '''
        Creates a temporary directory.
        '''
        TestCase.setUp(self)

        self._tempDirPath = mkdtemp("", "test_%s" % self.id())
    # end def setUp

    def tearDown(self):
        '''
        Cleans up the temporary directory
        '''
        rmtree(self._tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    def _getBinaryFileClass(self):
        '''
        Obtains the type of binary file under test.
        '''
        raise NotImplementedError
    # end def _getBinaryFileClass

    def isAbstract(self):
        '''
        Tests whether the current object is abstract or not

        @return Whether the current is abstract
        '''
        try:
            self._getBinaryFileClass()
            return False
        except NotImplementedError:
            return True
        # end try
    # end def isAbstract

    def test_Load_Performance(self):
        '''
        Loads a binary file, measuring performance
        '''
        if (not self.isAbstract()):

            printIt = False

            # A tuple<tuple<tuple<offset, data>>> containing the test vectors
            vectors = ( ('1 Kb bytes',  (   (0,    [x & 0xFF for x in range(1024)]), ), ),
                        ('2 Kb, split', (   (0,    [x & 0xFF for x in range(1024)]),
                                            (4096, [x & 0xFF for x in range(1024)]), ), ),
                        ('10 Kb',       (   (0,    [x & 0xFF for x in range(10240)]),), ),
                        # ('1 Mb',        (   (0,    [x & 0xFF for x in range(1*1024*1024)]),), ),
                        )

            binaryFileClass = self._getBinaryFileClass()

            import timeit
            loopCount = 50

            for index, (name, blocks) in enumerate(vectors):

                bestValue  = float(1000000 * 3600) # 1 hour...
                worstValue = 0
                # bestMethod  = "Unknown"
                # worstMethod = "Unknown"

                sourceLen = sum([len(v) for _, v in blocks])

                binaryFile = binaryFileClass(defaultValue=None)
                for offset, value in blocks:
                    binaryFile[offset:offset+len(value)] = value
                # end for

                tempFilePath = join(self._tempDirPath, 'test_%d.bin' % index)
                binaryFile.save(tempFilePath)

                initialization = '\n'.join(('from pylibrary.tools.importutils import importFqn',
                                            'binaryFileClass = importFqn("%s.%s")' % (binaryFileClass.__class__.__module__,
                                                                                      binaryFileClass.__class__.__name__)
                                            ))
                code = 'binaryFile = binaryFileClass("%s")' % (tempFilePath.replace('\\', '\\\\'),)

                timer  = timeit.Timer(code, initialization)
                result = timer.timeit(number=loopCount)

                if (printIt):
                    print(("%.4f ms/pass, %.6f ms/pass/byte (%s)" % (1000 * result/loopCount,
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

                if (printIt):
                    print(("--- Best result for a string of %d bytes: %s (%.4f ms/pass, %.6f ms/pass/byte)" % \
                          (sourceLen,
                           bestMethod,
                           1000 * bestValue / loopCount,
                           1000 * bestValue / (loopCount * sourceLen),
                           )))
                    print(("--- Worst result for a string of %d bytes: %s (%.4f ms/pass, %.6f ms/pass/byte)" % \
                          (sourceLen,
                           worstMethod,
                           1000 * worstValue / loopCount,
                           1000 * worstValue / (loopCount * sourceLen),
                           )))
                # end if
            # end for
        # end if
    # end def test_Load_Performance

    def test_ReadBlocks_Performance(self):
        '''
        Saves a binary file, measuring performance
        '''
        if (not self.isAbstract()):

            printIt = False

            maxPowerOf2 = 5
            # A tuple<tuple<tuple<offset, data>>> containing the test vectors
            vectors = [ (('%d Kb' % (1 << x)),   (   (0,    ((1 << x) * 1024)), )) for x in range(maxPowerOf2)]

            binaryFileClass = self._getBinaryFileClass()

            import timeit
            loopCount = 50

            for index, (name, blocks) in enumerate(vectors):

                bestValue  = float(1000000 * 3600) # 1 hour...
                worstValue = 0
                # bestMethod  = "Unknown"
                # worstMethod = "Unknown"

                sourceLen = sum([v for _, v in blocks])

                initializations = ['from pylibrary.tools.importutils import importFqn',
                                  'binaryFileClass = importFqn("%s.%s")' % (binaryFileClass.__module__,
                                                                            binaryFileClass.__name__),
                                  'binaryFile = binaryFileClass()',
                                  ]

                initializations.extend(['binaryFile[%d:%d] = [x & 0xFF for x in range(%d)]' % (offset, offset+length, length)
                                       for offset, length in blocks])
                initializations.append('tempFilePath = "%s"' % join(self._tempDirPath, 'test_%d.bin' % index).replace('\\', '/'))

                initialization = '\n'.join(initializations)
                code = 'binaryFile._readBlocks(None, None)'

                # Test it...
                timer  = timeit.Timer(code, initialization)
                result = timer.timeit(number=loopCount)

                if (sourceLen != 0):
                    if (printIt):
                        print(("%.4f ms/pass, %.6f ms/pass/byte (%s)" % (1000 * result/loopCount,
                                                                        1000 * result/(loopCount * sourceLen),
                                                                        name,)))
                    # end if
                # end if

                if (bestValue > result):
                    bestValue  = result
                    bestMethod = name
                # end if

                if (worstValue < result):
                    worstValue  = result
                    worstMethod = name
                # end if

                if (sourceLen != 0):
                    if (printIt):
                        print(("Best result for a string of %d bytes: %s (%.4f ms/pass, %.6f ms/pass/byte)" % \
                              (sourceLen,
                               bestMethod,
                               1000 * bestValue / loopCount,
                               1000 * bestValue / (loopCount * sourceLen),
                               )))
                        print(("--- Worst result for a string of %d bytes: %s (%.4f ms/pass, %.6f ms/pass/byte)" % \
                              (sourceLen,
                               worstMethod,
                               1000 * worstValue / loopCount,
                               1000 * worstValue / (loopCount * sourceLen),
                               )))
                    # end if
                # end if

                if (printIt):
                    print(("Ratio betwen best and worst implementations: %.4f" % (bestValue / worstValue,)))
                # end if
            # end for
        # end if
    # end def test_ReadBlocks_Performance

    def test_Save_Performance(self):
        '''
        Saves a binary file, measuring performance
        '''
        if (not self.isAbstract()):

            printIt = False

            maxPowerOf2 = 4
            # A tuple<tuple<tuple<offset, data>>> containing the test vectors
            vectors = [ (('%d Kb' % (1 << x)),   (   (0,    ((1 << x) * 1024)), )) for x in range(maxPowerOf2)]

            binaryFileClass = self._getBinaryFileClass()

            import timeit
            loopCount = 50

            for index, (name, blocks) in enumerate(vectors):

                bestValue  = float(1000000 * 3600) # 1 hour...
                worstValue = 0
                # bestMethod  = "Unknown"
                # worstMethod = "Unknown"

                sourceLen = sum([v for _, v in blocks])

                initializations = ['from pylibrary.tools.importutils import importFqn',
                                  'binaryFileClass = importFqn("%s.%s")' % (binaryFileClass.__module__,
                                                                            binaryFileClass.__name__),
                                  'binaryFile = binaryFileClass()',
                                  ]

                initializations.extend(['binaryFile[%d:%d] = [x & 0xFF for x in range(%d)]' % (offset, offset+length, length)
                                       for offset, length in blocks])
                initializations.append('tempFilePath = "%s"' % join(self._tempDirPath, 'test_%d.bin' % index).replace('\\', '/'))

                initialization = '\n'.join(initializations)
                code = 'binaryFile.save(tempFilePath)'

                # Test it...
                timer  = timeit.Timer(code, initialization)
                result = timer.timeit(number=loopCount)

                if (sourceLen != 0):
                    print(("%.4f ms/pass, %.6f ms/pass/byte (%s)" % (1000 * result/loopCount,
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

                if (sourceLen != 0):
                    if (printIt):
                        print(("Best result for a string of %d bytes: %s (%.4f ms/pass, %.6f ms/pass/byte)" % \
                                    (sourceLen,
                                     bestMethod,
                                     1000 * bestValue / loopCount,
                                     1000 * bestValue / (loopCount * sourceLen),
                                     )))
                        print(("--- Worst result for a string of %d bytes: %s (%.4f ms/pass, %.6f ms/pass/byte)" % \
                                    (sourceLen,
                                     worstMethod,
                                     1000 * worstValue / loopCount,
                                     1000 * worstValue / (loopCount * sourceLen),
                                     )))
                    # end if
                # end if

                if (printIt):
                    print(("Ratio betwen best and worst implementations: %.4f" % (bestValue / worstValue,)))
                # end if
            # end for
        # end if
    # end def test_Save_Performance

    def test_SaveLoad(self):
        '''
        Saves and loads a binary file.

        The contents must be consistent.
        '''

        if (not self.isAbstract()):

            binaryFileClass = self._getBinaryFileClass()
            binaryFile = binaryFileClass(defaultValue=None)
            value = HexList(list(range(5)))
            binaryFile[0x1234:0x1234+5] = value

            value = HexList([x & 0xFF for x in range(4096)])
            binaryFile[0x10000:0x10000+len(value)] = value

            tempFilePath = join(self._tempDirPath, 'test.s28')
            binaryFile.save(tempFilePath, 0x1234, 0x10000+len(value) - 0x1234)

            newBinaryFile = binaryFileClass(tempFilePath, defaultValue=None)
            self.assertEqual(binaryFile,
                             newBinaryFile,
                             "Binary files do not match")

            # Check that the default value has not been written/read
            self.assertEqual(True,
                             newBinaryFile[0x5000] is None,
                             "Interblock values set to the default value")
        # end if
    # end def test_SaveLoad

    def test_DeleteBlock(self):
        '''
        Deletes a block in a file
        '''
        if (not self.isAbstract()):

            binaryFileClass = self._getBinaryFileClass()
            binaryFile = binaryFileClass()
            value = HexList(list(range(5)))
            binaryFile[0x1234:0x1234+5] = value


            del binaryFile[0x1235:0x1236]
            del binaryFile[0x1238]

            tempFilePath = join(self._tempDirPath, 'test.s28')
            binaryFile.save(tempFilePath)

            newBinaryFile = binaryFileClass(tempFilePath)
            self.assertEqual(binaryFile,
                             newBinaryFile,
                             "Binary files do not match")
        # end if
    # end def test_DeleteBlock

    def test_Cmp(self):
        '''
        Comparison of two binary files
        '''
        if (not self.isAbstract()):

            binaryFileClass = self._getBinaryFileClass()
            value = HexList(list(range(5)))

            binaryFile1 = binaryFileClass()
            binaryFile1[0x1234:0x1234+5] = value

            binaryFile2 = binaryFileClass()
            binaryFile2[0x1234:0x1234+5] = value

            self.assertEqual(binaryFile1,
                             binaryFile2,
                             "Objects should compare to equality")

            del binaryFile1[0x1236]

            self.assertNotEqual(binaryFile1,
                                binaryFile2,
                               "Objects should NOT compare to equality")
        # end if
    # end def test_Cmp

    def test_Contains(self):
        '''
        Tests the 'in' operator
        '''
        if (not self.isAbstract()):

            binaryFileClass = self._getBinaryFileClass()
            value = HexList(list(range(5)))

            binaryFile1 = binaryFileClass()
            binaryFile1[0x1234:0x1234+5] = value

            self.assertTrue(0x1234 in binaryFile1,
                            "Included address not found")

            self.assertFalse(0x1233 in binaryFile1,
                            "Non-included address found")
        # end if
    # end def test_Contains

    def test_Update(self):
        '''
        Tests the 'in' operator
        '''
        if (not self.isAbstract()):

            binaryFileClass = self._getBinaryFileClass()
            value = HexList(list(range(10)))

            binaryFile1 = binaryFileClass()
            binaryFile1[0x1234:0x1234+10] = value

            binaryFile2  = binaryFileClass()
            binaryFile2[0x1234+5:0x1234+5+10] = value

            binaryFile3 = binaryFileClass()
            binaryFile3[0x1234:0x1234+5]      = value[:5]
            binaryFile3[0x1234+5:0x1234+5+10] = value

            binaryFile1.update(binaryFile2)

            expected = binaryFile3
            obtained = binaryFile1
            self.assertEqual(expected,
                              obtained,
                              'Inconsistent binary file after update')
        # end if
    # end def test_Update
# end class BinaryFileTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
