"""
:package: pytestbox.base.loghelper
:brief: pytestbox Log Helper module
:author: Suresh Thiyagarajan/Martin Cryonnet <sthiyagarajan@logitech.com>/<mcryonnet@logitech.com>
:date: 2021/11/05
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import Enum
from sys import stdout


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
class LevelNames(Enum):
    """
    Level names
    """
    TITLE2 = 'TITLE 2'
    INFO = 'INFO'
    TRACE = 'TRACE'
# end class LevelNames


LEVEL_COLORS = {
    LevelNames.TITLE2: (160, 250, 150),  # 0xA0FA96 means light green
    LevelNames.INFO: (255, 255, 110),  # 0xFFFF6E means light yellow
    LevelNames.TRACE: (255, 190, 105),  # 0xFFBE69 means light orange
}


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class LogHelper:
    """
    Helper to handle logging in test cases
    """
    check_counter = 0
    step_counter = 0
    prerequisite_counter = 0
    post_requisite_counter = 0

    @classmethod
    def reset(cls):
        """
        Reset counters.
        """
        cls.check_counter = 0
        cls.step_counter = 0
        cls.prerequisite_counter = 0
        cls.post_requisite_counter = 0
    # end def reset

    @classmethod
    def log_prerequisite(cls, test_case, text):
        """
        Prerequisite Title 2 log writing.

        :param test_case: Current test case
        :type test_case: ``PyHarnessCase``
        :param text: log text
        :type text: ``str``
        """
        cls.prerequisite_counter += 1
        cls.log_title_2(test_case, f'Pre-requisite#{cls.prerequisite_counter}: {text}')
    # end def log_prerequisite

    @classmethod
    def log_post_requisite(cls, test_case, text):
        """
        Post requisite Title 2 log writing.

        :param test_case: Current test case
        :type test_case: ``PyHarnessCase``
        :param text: log text
        :type text: ``str``
        """
        cls.post_requisite_counter += 1
        cls.log_title_2(test_case, f'Post-requisite#{cls.post_requisite_counter}: {text}')
    # end def log_post_requisite

    @classmethod
    def log_step(cls, test_case, text):
        """
        Step Title 2 log writing.

        :param test_case: Current test case
        :type test_case: ``PyHarnessCase``
        :param text: log text
        :type text: ``str``
        """
        cls.step_counter += 1
        cls.log_title_2(test_case, f'Test Step {cls.step_counter}: {text}')
    # end def log_step

    @classmethod
    def log_check(cls, test_case, text):
        """
        Check Title 2 log writing.

        :param test_case: Current test case
        :type test_case: ``PyHarnessCase``
        :param text: log text
        :type text: ``str``
        """
        cls.check_counter += 1
        cls.log_title_2(test_case, f'Test Check {cls.check_counter}: {text}')
    # end def log_check

    @classmethod
    def log_title_2(cls, test_case, msg):
        """
        Wrapper to ``PyHarnessCase.logTitle2``.

        :param test_case: Current test case
        :type test_case: ``PyHarnessCase``
        :param msg: log text
        :type msg: ``str``
        """
        cls._verbose(test_case, LevelNames.TITLE2, msg)
        test_case.logTitle2(msg)
    # end def log_title_2

    @classmethod
    def log_info(cls, test_case, msg):
        """
        Wrapper to ``PyHarnessCase.logInfo``.

        :param test_case: Current test case
        :type test_case: ``PyHarnessCase``
        :param msg: log text
        :type msg: ``str``
        """
        cls._verbose(test_case, LevelNames.INFO, msg)
        test_case.logInfo(msg)
    # end def log_info

    @classmethod
    def log_data(cls, test_case, data):
        """
        Wrapper to ``PyHarnessCase.add_test_data``.

        :param test_case: Current test case
        :type test_case: ``PyHarnessCase``
        :param data: Test data
        :type data: ``str``
        """
        cls._verbose(test_case, LevelNames.INFO, data)
        test_case.add_test_data(data=data)
    # end def log_data

    @classmethod
    def log_metrics(cls, test_case, key, value):
        """
        Wrapper to ``PyHarnessCase.addPerformanceData``.

        :param test_case: Current test case
        :type test_case: ``PyHarnessCase``
        :param key: The measured target item
        :type key: ``str``
        :param value: Measured data
        :type value: ``str``
        """
        cls._verbose(test_case, LevelNames.INFO, f'{key} = {value}')
        test_case.addPerformanceData(key=key, value=value)
    # end def log_metrics

    @classmethod
    def log_trace(cls, test_case, msg):
        """
        Wrapper to ``PyHarnessCase.logTrace``.
        :param test_case: Current test case
        :type test_case: ``PyHarnessCase``
        :param msg: log text
        :type msg: ``str``
        """
        cls._verbose(test_case, LevelNames.TRACE, msg)
        test_case.logTrace(msg)
    # end def log_trace

    @classmethod
    def _verbose(cls, test_case, level, msg):
        """
        Handle LogHelper verbose.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param level: Level parameter
        :type level: ``LevelNames``
        :param msg: log text
        :type msg: ``str``
        """
        if test_case.f.LOGGING.F_LogHelperVerbose:
            if test_case.f.LOGGING.F_LogHelperVerboseColor:
                r = LEVEL_COLORS[level][0]
                g = LEVEL_COLORS[level][1]
                b = LEVEL_COLORS[level][2]
                stdout.write(f'\033[38;2;{r};{g};{b}m[{level.name}] {msg} \033[38;2;255;255;255m\n')
            else:
                stdout.write(f'[{level.name}] {msg}\n')
            # end if
        # end if
    # end def _verbose
# end class LogHelper

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
