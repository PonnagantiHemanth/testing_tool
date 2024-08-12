#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.warning

@brief  Deprecation warnings testing module

@author christophe Roquebert

@date   2018/02/14
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from io                          import StringIO
from pylibrary.tools.warning           import ignorewarning
from unittest                           import TestCase
import sys
import warnings

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class IgnoreWarningTestCase(TestCase):
    '''
    Tests the behavior of the IgnoreWarning classes
    '''
    _CATEGORY = Warning

    def setUp(self):
        '''
        Constructor
        '''
        super(IgnoreWarningTestCase, self).setUp()

        self.backupStderr = sys.stderr
        sys.stderr.flush()
        sys.stderr = StringIO()

        self._message = 'Warning of category: %s' % self._CATEGORY.__name__

        warnings.filterwarnings("always", category = self._CATEGORY)

    # end def setUp

    def tearDown(self):
        '''
        TearDown of IgnoreWarning tests
        '''
        warnings.resetwarnings()
        sys.stderr.close()
        sys.stderr = self.backupStderr
        super(IgnoreWarningTestCase, self).tearDown()
    # end def tearDown

    def generateWarning(self):
        '''
        Warn method
        '''
        warnings.warn(self._message,
                      category = self._CATEGORY)
    # end def generateWarning

    def checkWarningPresent(self):
        '''
        Check the warning as been catch
        '''
        assert self._CATEGORY.__name__ in sys.stderr.getvalue(), 'Wrong warning category'
        assert self._message in sys.stderr.getvalue(), 'Wrong warning message'
        sys.stderr.flush()
        sys.stderr = StringIO()
    # end def checkWarningPresent

    @staticmethod
    def checkWarningNotPresent():
        '''
        Check no warning as been catch
        '''
        assert sys.stderr.getvalue() == '', 'No warning should be raised'
    # end def checkWarningNotPresent

    def ignoreWarning(self):
        '''
        Ignore the generated warning
        '''
        raise NotImplementedError
    # end def ignoreWarning

    def test_IgnoreWarning(self):
        '''
        Tests ignorewarning(Warning) method
        '''
        if (self.__class__.__name__ != IgnoreWarningTestCase.__name__):
            self.generateWarning()
            self.checkWarningPresent()

            self.ignoreWarning()
            self.checkWarningNotPresent()

        # end if

    # end def test_IgnoreWarning

# end class IgnoreWarningTestCase

class IgnoreImportWarningTestCase(IgnoreWarningTestCase):
    '''
    Tests the behavior of the IgnoreWarning class
    '''
    _CATEGORY = ImportWarning

    @ignorewarning(ImportWarning)
    def ignoreWarning(self):
        '''
        @copydoc pylibrary.tools.test.warning.IgnoreWarningTestCase.ignoreWarning
        '''
        self.generateWarning()
    # end def ignoreWarning

# end class IgnoreImportWarningTestCase

class IgnoreDeprecationWarningTestCase(IgnoreWarningTestCase):
    '''
    Tests the behavior of the IgnoreWarning class
    '''
    _CATEGORY = DeprecationWarning

    @ignorewarning(DeprecationWarning)
    def ignoreWarning(self):
        '''
        @copydoc pylibrary.tools.test.warning.IgnoreWarningTestCase.ignoreWarning
        '''
        self.generateWarning()
    # end def ignoreWarning

# end class IgnoreDeprecationWarningTestCase

class IgnoreUserWarningTestCase(IgnoreWarningTestCase):
    '''
    Tests the behavior of the IgnoreWarning class
    '''
    _CATEGORY = UserWarning

    @ignorewarning(UserWarning)
    def ignoreWarning(self):
        '''
        @copydoc pylibrary.tools.test.warning.IgnoreWarningTestCase.ignoreWarning
        '''
        self.generateWarning()
    # end def ignoreWarning

# end class IgnoreUserWarningTestCase

class IgnoreFutureWarningTestCase(IgnoreWarningTestCase):
    '''
    Tests the behavior of the IgnoreWarning class
    '''
    _CATEGORY = FutureWarning

    @ignorewarning(FutureWarning)
    def ignoreWarning(self):
        '''
        @copydoc pylibrary.tools.test.warning.IgnoreWarningTestCase.ignoreWarning
        '''
        self.generateWarning()
    # end def ignoreWarning

# end class IgnoreFutureWarningTestCase

class IgnorePendingDeprecationWarningTestCase(IgnoreWarningTestCase):
    '''
    Tests the behavior of the IgnoreWarning class
    '''
    _CATEGORY = PendingDeprecationWarning

    @ignorewarning(PendingDeprecationWarning)
    def ignoreWarning(self):
        '''
        @copydoc pylibrary.tools.test.warning.IgnoreWarningTestCase.ignoreWarning
        '''
        self.generateWarning()
    # end def ignoreWarning

# end class IgnorePendingDeprecationWarningTestCase

class IgnoreSyntaxWarningTestCase(IgnoreWarningTestCase):
    '''
    Tests the behavior of the IgnoreWarning class
    '''
    _CATEGORY = SyntaxWarning

    @ignorewarning(SyntaxWarning)
    def ignoreWarning(self):
        '''
        @copydoc pylibrary.tools.test.warning.IgnoreWarningTestCase.ignoreWarning
        '''
        self.generateWarning()
    # end def ignoreWarning

# end class IgnoreSyntaxWarningTestCase

class IgnoreUnicodeWarningTestCase(IgnoreWarningTestCase):
    '''
    Tests the behavior of the IgnoreWarning class
    '''
    _CATEGORY = UnicodeWarning

    @ignorewarning(UnicodeWarning)
    def ignoreWarning(self):
        '''
        @copydoc pylibrary.tools.test.warning.IgnoreWarningTestCase.ignoreWarning
        '''
        self.generateWarning()
    # end def ignoreWarning

# end class IgnoreUnicodeWarningTestCase

class IgnoreRuntimeWarningTestCase(IgnoreWarningTestCase):
    '''
    Tests the behavior of the IgnoreWarning class
    '''
    _CATEGORY = RuntimeWarning

    @ignorewarning(RuntimeWarning)
    def ignoreWarning(self):
        '''
        @copydoc pylibrary.tools.test.warning.IgnoreWarningTestCase.ignoreWarning
        '''
        self.generateWarning()
    # end def ignoreWarning

# end class IgnoreRuntimeWarningTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
