#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.strutilstestcase

@brief StrUtils tests

@author christophe Roquebert

@date   2018/09/27
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.strutils import pythonify
from unittest                  import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class ConversionTestCase(TestCase):
    '''
    Tests the escaping of non-python characters (windows character set)
    '''

    def testConversion(self):
        '''
        Tests the conversion from the Windows character set.
        '''
        # Attempt a connection on a non-existent port
        from socket import socket
        try:
            sock = socket()
            sock.connect(('localhost', 12345))
            self.fail('The socket was able to connect, which should not have happened')
        except Exception: #pylint:disable=W0703
            try:
                from sys import exc_info
                value = exc_info()
                value = repr(value[1])
                str(value)
            except Exception: #pylint:disable=W0703
                self.fail('Unexpected Exception raised')
            # end try
        # end try
    # end def testConversion
# end class ConversionTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
