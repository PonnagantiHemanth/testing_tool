#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.reportui

@brief  Run report listener

@author christophe Roquebert

@date   2018/11/08
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path                 import abspath
from pyharness.arguments                 import KeywordArguments
from pyharness.core                      import TYPE_STOPRUN
from pyharness.core                      import TestListener
from os.path                            import expanduser
from os.path                            import join
from os.path                            import normpath
from os.path                            import sep
from threading                          import RLock
from time                               import strftime

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class RunReportTestListener(TestListener):
    '''
    A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    '''

    SYNCHRONIZATION_LOCK = RLock()

    def __resultDirPath(self):
        '''
        Builds the path to the directory containing the log files

        @return (str) The file path to the test log.
        '''
        result = abspath(self.outputdir)

        return result
    # end def __resultDirPath

    def attach(self, testResult):
        '''
        @copydoc pyharness.core.TestListener.attach
        '''
        with self.SYNCHRONIZATION_LOCK:
            testResult.addListener(TYPE_STOPRUN, self.stopRun)
        # end with
    # end def attach

    def detach(self, testResult):
        '''
        @copydoc pyharness.core.TestListener.detach
        '''
        with self.SYNCHRONIZATION_LOCK:
            testResult.removeListener(TYPE_STOPRUN, self.stopRun)
        # end with
    # end def detach

    def stopRun(self, result, suspended):                                                                               # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.stopRun
        '''
        if (    (not suspended)
            and (self.args[KeywordArguments.KEY_GENERATERUNREPORT])):

            argv = ['reportbuilder2test.py']
            import platform
            if (   (not self.args[KeywordArguments.KEY_NO_CHM])
                or (platform.system() == 'Linux')):
                argv.append('--no-hhc')
            # end if

            reportName = "Report_%(DATE)s_%(USER)s" % {
                           "DATE": strftime("%Y%m%d"),
                           "USER": normpath(expanduser('~')).rsplit(sep, 1)[-1]
                           }

            argv.append('--output=%s' % (join(self.__resultDirPath(), reportName),))
            argv.extend(self.__resultDirPath())

            from pyharness.tools.reportbuilder2 import Main
            def toolProc(argv, stdout, stderr):
                '''
                The tool threadProc

                @param  argv   [in] (tuple)  The program argv
                @param  stdout [in] (stream) The replacement stdout
                @param  stderr [in] (stream) The replacement stderr
                '''
                Main(argv, stdout, stderr)                                                                              # pylint:disable=E0602
            # end def toolProc

            from pyharness.ui.aui.dialogs import ProcessRunner
            process = ProcessRunner()
            process.launch(toolProc, argv)

        # end if
    # end def stopRun

# end class RunReportTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
