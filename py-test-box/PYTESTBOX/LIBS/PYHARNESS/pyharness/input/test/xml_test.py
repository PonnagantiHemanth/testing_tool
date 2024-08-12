#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.input.test.xmltest

@brief Tests of the XmlTestProvider

@author christophe.roquebert

@date   2018/05/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.consts                   import DEFAULT_OUTPUT_DIRECTORY
from pyharness.input.test.providers_test     import DynamicTestCasesProviderTestMixin
from pyharness.input.test.providers_test     import PerfDataTestProviderTestMixin
from pyharness.input.test.providers_test     import TestProviderTestCase
from pyharness.input.test.providers_test     import TestStateTestProviderTestMixin
from pyharness.input.xmlui              import XmlTestProvider
from pyharness.arguments                import KeywordArguments
from os                                import makedirs
from os.path                           import join
from os.path                           import normpath

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

MOCK_XML_SUCCESS_BODY = '\n'.join(('<?xml version="1.0" ?>',
                                   '<testscript format="2.0"',
                                   '          fqn="mocktest.MockTest.test_Success"',
                                   '          startdate="2006-01-01 00:00:00"',
                                   '          state="success"',
                                   '          stopdate="2006-01-01 00:00:01">',
                                   '  <description>',
                                   '        ',
                                   '        Fake Successful test',
                                   '        ',
                                   '  </description>',
                                   '  <testcases/>',
                                   '  <perfdata/>',
                                   '</testscript>',
                                   ))

MOCK_XML_FAILURE_BODY = '\n'.join(('<?xml version="1.0" ?>',
                                   '<testscript format="2.0"',
                                   '          fqn="mocktest.MockTest.test_Failure"',
                                   '          startdate="2006-01-01 00:00:00"',
                                   '          state="failure"',
                                   '          stopdate="2006-01-01 00:00:01">',
                                   '  <description>',
                                   '        ',
                                   '        Fake Failed test',
                                   '        ',
                                   '  </description>',
                                   '  <message>',
                                   '    Fake failed test',
                                   '  </message>',
                                   '  <traceback>',
                                   '      File &quot;g:/PySetup/PROJECT/TEST/RUNTIME\\pyharness\\input\\test\\test.py&quot;, line 174, in testSaveLoad',
                                   '    &quot;Invalid coverage data serialization&quot;)',
                                   '',
                                   '  </traceback>',
                                   '  <testcases/>',
                                   '  <perfdata/>',
                                   '</testscript>',
                                   ))

MOCK_XML_ERROR_BODY = '\n'.join(('<?xml version="1.0" ?>',
                                   '<testscript format="2.0"',
                                   '          fqn="mocktest.MockTest.test_Error"',
                                   '          startdate="2006-01-01 00:00:00"',
                                   '          state="error"',
                                   '          stopdate="2006-01-01 00:00:01">',
                                   '  <description>',
                                   '        ',
                                   '        Fake Error test',
                                   '        ',
                                   '  </description>',
                                   '  <message>',
                                   '    Fake failed test',
                                   '  </message>',
                                   '  <traceback>',
                                   '      File &quot;g:/PySetup/PROJECT/TEST/RUNTIME\\pyharness\\input\\test\\test.py&quot;, line 174, in testSaveLoad',
                                   '    &quot;Invalid coverage data serialization&quot;)',
                                   '',
                                   '  </traceback>',
                                   '  <testcases/>',
                                   '  <perfdata/>',
                                   '</testscript>',
                                   ))

MOCK_XML_TESTCASES_BODY = '\n'.join(('<?xml version="1.0" ?>',
                                     '<testscript format="2.0"',
                                     '          fqn="mocktest.MockTest.test_0WithTestCase"',
                                     '          startdate="2006-01-01 00:00:00"',
                                     '          state="success"',
                                     '          stopdate="2006-01-01 00:00:01">',
                                     '  <description>',
                                     '        ',
                                     '        Fake testCase test',
                                     '        ',
                                     '  </description>',
                                     '  <testcases>',
                                     '    <testcase name="DYNAMIC_TESTCASE_ID1"/>',
                                     '    <testcase name="DYNAMIC_TESTCASE_ID2" author="user.test" comment="This is a comment"/>',
                                     '  </testcases>',
                                     '  <perfdata/>',
                                     '</testscript>',
                                     ))

MOCK_XML_NOTESTCASES_BODY = '\n'.join(('<?xml version="1.0" ?>',
                                       '<testscript format="2.0"',
                                       '          fqn="mocktest.MockTest.test_1WithoutTestCase"',
                                       '          startdate="2006-01-01 00:00:00"',
                                       '          state="success"',
                                       '          stopdate="2006-01-01 00:00:01">',
                                       '  <description>',
                                       '        ',
                                       '        Fake testCase test',
                                       '        ',
                                       '  </description>',
                                       '  <testcases/>',
                                       '  <perfdata/>',
                                       '</testscript>',
                                       ))

MOCK_XML_NOPERFDATA_BODY = '\n'.join(('<?xml version="1.0" ?>',
                                   '<testscript format="2.0"',
                                   '          fqn="mocktest.MockTest.test_PerfData0"',
                                   '          startdate="2006-01-01 00:00:00"',
                                   '          state="success"',
                                   '          stopdate="2006-01-01 00:00:01">',
                                   '  <description>',
                                   '        ',
                                   '        Fake perfdata test',
                                   '        ',
                                   '  </description>',
                                   '  <testcases/>',
                                   '  <perfdata/>',
                                   '</testscript>',
                                   ))

MOCK_XML_PERFDATA_BODY = '\n'.join(('<?xml version="1.0" ?>',
                                   '<testscript format="2.0"',
                                   '          fqn="mocktest.MockTest.test_PerfData1"',
                                   '          startdate="2006-01-01 00:00:00"',
                                   '          state="success"',
                                   '          stopdate="2006-01-01 00:00:01">',
                                   '  <description>',
                                   '        ',
                                   '        Fake perfdata test',
                                   '        ',
                                   '  </description>',
                                   '  <testcases/>',
                                   '  <perfdata>',
                                   '    <entry key="PERF_1" value="1" unit="s"/>',
                                   '  </perfdata>',
                                   '</testscript>',
                                   ))

XML_FILES = (('mocktest.MockTest.test_Success',           MOCK_XML_SUCCESS_BODY),
             ('mocktest.MockTest.test_Failure',           MOCK_XML_FAILURE_BODY),
             ('mocktest.MockTest.test_Error',             MOCK_XML_ERROR_BODY),
             ('mocktest.MockTest.test_0WithTestCase',     MOCK_XML_TESTCASES_BODY),
             ('mocktest.MockTest.test_1WithoutTestCase',  MOCK_XML_NOTESTCASES_BODY),
             ('mocktest.MockTestCase.test_PerfData0',     MOCK_XML_NOPERFDATA_BODY),
             ('mocktest.MockTestCase.test_PerfData1',     MOCK_XML_PERFDATA_BODY),
             )

class XmlTestProviderTestCase(TestStateTestProviderTestMixin,
                              DynamicTestCasesProviderTestMixin,
                              PerfDataTestProviderTestMixin,
                              TestProviderTestCase):
    '''
    Tests of the XmlTestProvider
    '''

    def setUp(self):
        '''
        Test initialization
        '''
        TestProviderTestCase.setUp(self)

        xmlFilePathElements = [self._tempDirPath,
                               DEFAULT_OUTPUT_DIRECTORY,
                               self.getContext().getCurrentProduct(),
                               self.getContext().getCurrentVariant(),
                               self.getContext().getCurrentTarget(),
                               "xml"]

        # The VARIANT may need to be normalized
        xmlFilePath = normpath(join(*xmlFilePathElements))
        makedirs(xmlFilePath)
        for testId, body in XML_FILES:
            with open(join(xmlFilePath, '%sTestScript.xml' % testId), "w+") as xmlFile:
                xmlFile.write(body)
            # end with
        # end for
    # end def setUp

    def _getTestProvider(self):
        '''
        @copydoc pyharness.input.test.providers.TestProviderTestCase._getTestProvider
        '''
        kwArgs = {}
        kwArgs.update(KeywordArguments.DEFAULT_ARGUMENTS)
        kwArgs[KeywordArguments.KEY_ROOT] = self._tempDirPath

        return XmlTestProvider(kwArgs)
    # end def _getTestProvider

# end class XmlTestProviderTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
