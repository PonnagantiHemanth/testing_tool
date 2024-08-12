#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.configui

@brief JRL-specialized TestListener

@author christophe.roquebert

@date   2018/12/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

from os.path                      import abspath
from pylibrary.tools.config       import ConfigParser
from pyharness.arguments          import KeywordArguments
from pyharness.core               import TestListener
from os                           import F_OK
from os                           import access
from os                           import makedirs
from os                           import remove
from os.path                      import join
from threading                    import RLock

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class ConfigTestListener(TestListener):
    '''
    A test listener class that dumps the contents of the config to a Settings.ini
    file, at the root of the output directory.
    '''

    SYNCHRONIZATION_LOCK = RLock()

    ## This TestListener is one of the few mandatory listeners
    MANDATORY = True
    VISIBLE   = False

    def __init__(self, descriptions, verbosity, outputdir, args):
        '''
        Constructor.

        @copydoc pyharness.core.TestListener.__init__
        '''
        super(ConfigTestListener, self).__init__(descriptions, verbosity, outputdir, args)

        outputdir = self.__resultDirPath()
        if (not access(outputdir, F_OK)):
            makedirs(outputdir)
        # end if

        self._configPath = join(outputdir, 'Settings.ini')
    # end def __init__

    def __resultDirPath(self):
        '''
        Builds the path to the directory containing the log files

        @return The file path to the test log.
        '''
        result = abspath(self.outputdir)

        return result
    # end def __resultDirPath

    def startRun(self, context, resumed):                                                                               # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.startRun

        Clear if needed the log file.
        Only internal cache is cleared.
        '''

        if ((not resumed) and (self.args[KeywordArguments.KEY_ERASELOGS])):
            if (access(self._configPath, F_OK)):
                remove(self._configPath)
            # end if
        # end if

        if (not resumed):
            config = ConfigParser()

            config.add_section('MODE')
            config.set('MODE', 'value', context.getCurrentMode())

            config.add_section('PRODUCT')
            config.set('PRODUCT', 'value', context.getCurrentProduct())

            config.add_section('VARIANT')
            config.set('VARIANT', 'value', context.getCurrentVariant())

            config.add_section('TARGET')
            config.set('TARGET', 'value', context.getCurrentTarget())

            config.write(self._configPath)
        # end if
    # end def startRun
# end class ConfigTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
