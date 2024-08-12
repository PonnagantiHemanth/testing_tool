#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.initoolstestcase

@brief File tools test

@author christophe Roquebert

@date   2018/10/23
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import os.path
if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(sys.argv[0]), '../../..')))
# end if

from pylibrary.tools.initools import IniTool
from unittest import TestCase
from unittest import main

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

DATA_GETINIPARAMETER = [("testIniParameter.ini", "section", "parameter", "value")]


class IniToolTestCase(TestCase):
    '''
    Test of the IniTool class
    '''

    def testIniParameter(self):
        '''
        Computes hasIniParameter, getIniParameter and setIniParameter tests
        '''
        for filename, section, parameter, value in DATA_GETINIPARAMETER:
            f = open(filename, 'a')
            f.close()

            obtained = IniTool.hasIniParameter(filename, section, parameter)
            self.assertEqual(obtained,
                              False,
                              "Invalid hasIniParameter computation with (%s, %s, %s) and obtained %s " % (filename, section, parameter, obtained))

            IniTool.setIniParameter(filename, section, parameter, value)
            obtained1 = IniTool.hasIniParameter(filename, section, parameter)
            self.assertEqual(obtained1,
                              True,
                              "Invalid setIniParameter computation with (%s, %s, %s) and obtained1 %s " % (filename, section, parameter, obtained1))

            obtained2 = IniTool.getIniParameter(filename, section, parameter)
            self.assertEqual(obtained2,
                              value,
                              "Invalid getIniParameter computation with (%s, %s, %s) and obtained2 %s " % (filename, section, parameter, obtained2))
            os.remove(filename)
        # end for
    # end def testIniParameter
# end class IniToolTestCase


if (__name__ == "__main__"):
    main()
# end if

# ------------------------------------------------------------------------------
#  END OF FILE
# ------------------------------------------------------------------------------
