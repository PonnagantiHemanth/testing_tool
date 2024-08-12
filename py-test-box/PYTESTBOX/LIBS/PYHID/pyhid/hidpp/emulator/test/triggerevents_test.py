#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
@package pyhid.hidpp.emulator.test.triggerevents_test

@brief  HID++ 2.0 TriggerEvents test module

@author Stanislas Cottard

@date   2019/05/27
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.emulator.triggerevents import TriggerEvents
from pyhid.hidpp.emulator.triggerevents import GetTriggerCount
from pyhid.hidpp.emulator.triggerevents import GetTriggerCountResponse
from pyhid.hidpp.emulator.triggerevents import ClearTrigger
from pyhid.hidpp.emulator.triggerevents import ClearTriggerResponse
from pyhid.hidpp.emulator.triggerevents import TriggerSequence
from pyhid.hidpp.emulator.triggerevents import TriggerSequenceResponse
from pyhid.hidpp.emulator.triggerevents import TriggerSingle
from pyhid.hidpp.emulator.triggerevents import TriggerSingleResponse
from pyhid.hidpp.emulator.triggerevents import TriggerList
from pyhid.hidpp.emulator.triggerevents import TriggerListResponse
from pyhid.hidpp.emulator.triggerevents import EndOfSequenceEvent
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class TriggerEventsTestCase(TestCase):
    """
    TriggerEvents testing class
    """

    @staticmethod
    def test_trigger_events():
        """
        Tests TriggerEvents class instantiation
        """
        my_class = TriggerEvents(deviceIndex=0,
                                 featureIndex=0)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_trigger_events

    @staticmethod
    def test_get_trigger_count():
        """
        Tests GetTriggerCount class instantiation
        """
        my_class = GetTriggerCount(deviceIndex=0,
                                   featureId=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_trigger_count

    @staticmethod
    def test_clear_trigger():
        """
        Tests ClearTrigger class instantiation
        """
        my_class = ClearTrigger(deviceIndex=0,
                                featureId=0,
                                trigger_index=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_clear_trigger

    @staticmethod
    def test_trigger_sequence():
        """
        Tests TriggerSequence class instantiation
        """
        my_class = TriggerSequence(deviceIndex=0,
                                   featureId=0,
                                   first_trigger_index=0,
                                   last_trigger_index=0,
                                   delay=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_trigger_sequence

    @staticmethod
    def test_trigger_single():
        """
        Tests TriggerSingle class instantiation
        """
        my_class = TriggerSingle(deviceIndex=0,
                                 featureId=0,
                                 trigger_index=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_trigger_single

    @staticmethod
    def test_trigger_list():
        """
        Tests TriggerList class instantiation
        """
        my_class = TriggerList(deviceIndex=0,
                               featureId=0,
                               stimuli_count=0,
                               delay=0)

        RootTestCase._long_function_class_checker(my_class)

        # Test also with other values than the default ones
        my_class = TriggerList(deviceIndex=0,
                               featureId=0,
                               stimuli_count=0,
                               delay=0,
                               trigger_index_0=1,
                               trigger_index_1=1,
                               trigger_index_2=1,
                               trigger_index_3=1,
                               trigger_index_4=1,
                               trigger_index_5=1,
                               trigger_index_6=1,
                               trigger_index_7=1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_trigger_list

    @staticmethod
    def test_get_trigger_count_response():
        """
        Tests GetTriggerCountResponse class instantiation
        """
        my_class = GetTriggerCountResponse(deviceIndex=0,
                                           featureId=0,
                                           trigger_count=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_trigger_count_response

    @staticmethod
    def test_clear_trigger_response():
        """
        Tests ClearTriggerResponse class instantiation
        """
        my_class = ClearTriggerResponse(deviceIndex=0,
                                        featureId=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_clear_trigger_response

    @staticmethod
    def test_trigger_sequence_response():
        """
        Tests TriggerSequenceResponse class instantiation
        """
        my_class = TriggerSequenceResponse(deviceIndex=0,
                                           featureId=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_trigger_sequence_response

    @staticmethod
    def test_trigger_single_response():
        """
        Tests TriggerSingleResponse class instantiation
        """
        my_class = TriggerSingleResponse(deviceIndex=0,
                                         featureId=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_trigger_single_response

    @staticmethod
    def test_trigger_list_response():
        """
        Tests TriggerListResponse class instantiation
        """
        my_class = TriggerListResponse(deviceIndex=0,
                                       featureId=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_trigger_list_response

    @staticmethod
    def test_end_of_sequence_event():
        """
        Tests EndOfSequenceEvent class instantiation
        """
        my_class = EndOfSequenceEvent(deviceIndex=0,
                                      featureId=0,
                                      status=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_end_of_sequence_event
# end class TriggerEventsTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
