#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.tools.reportgenerator.config.evt_typing
:brief: Evt Typing test config for Google Sheet API Report generator
:author: Gautham S B <gsb@logitech.com>
:date: 2024/02/12
"""


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class EvtTypingConfig(object):
    """
    Config class for Evt Typing Test
    """
    BUILD_NUMBER_CELL = "B1"
    TEST_RESULT_DATA_RANGE = "C4:J9"
    TEST_RESULT_TABLE_RANGE = "A1:K9"
    TEST_RESULT_TABLE_RANGE_AFTER_MOVING_DOWN = "A11:J19"
    TIMESTAMP_CELL = "C1"
    TYPING_SHEET_NAME = "Typing"

    class CellRange(object):
        """
        Range of cells for each test report in google sheet
        """
        ENDURANCE_KEY = 'C4:J4'
        FAST_TYPING_KEY = 'C5:J5'
        GAMING_KEY = 'C6:J6'
        NORMAL_TYPING_KEY = 'C7:J7'
        WAKE_UP_QUICK_KEY = 'C8:J8'
        WAKE_UP_SLOW_KEY = 'C9:J9'
    # end class CellRange
# end class EvtTypingConfig

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------