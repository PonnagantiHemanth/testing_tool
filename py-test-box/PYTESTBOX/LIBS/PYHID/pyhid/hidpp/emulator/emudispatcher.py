#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidpp.emulator.emudispatcher

@brief  Emulator dispatcher class

@author Stanislas Cottard

@date   2019/06/13
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hiddispatcher import HidMessageQueue
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.emulator.triggerevents import TriggerEvents
from pyhid.hidpp.emulator.triggerevents import GetTriggerCountResponse as GetTriggerCount
from pyhid.hidpp.emulator.triggerevents import ClearTriggerResponse as ClearTrigger
from pyhid.hidpp.emulator.triggerevents import TriggerSequenceResponse as TriggerSequence
from pyhid.hidpp.emulator.triggerevents import TriggerSingleResponse as TriggerSingle
from pyhid.hidpp.emulator.triggerevents import TriggerListResponse as TriggerList
from pyhid.hidpp.emulator.triggerevents import EndOfSequenceEvent
from pyhid.hidpp.emulator.loadopticalsensordata import LoadOpticalSensorData
from pyhid.hidpp.emulator.loadopticalsensordata import CreateImmediateDisplacementResponse \
                                                        as CreateImmediateDisplacement
from pyhid.hidpp.emulator.loadopticalsensordata import SensorPolledEvent
from pyhid.hidpp.emulator.configurebuttons import ConfigureButtons
from pyhid.hidpp.emulator.configurebuttons import GetButtonTableInfoResponse as GetButtonTableInfo
from pyhid.hidpp.emulator.configurebuttons import CreateSimpleEventResponse as CreateSimpleEvent
from pyhid.hidpp.emulator.configurebuttons import CreateWaveformEventResponse as CreateWaveformEvent
from pyhid.hidpp.emulator.configurebuttons import ConfigureWaveformPointsResponse as ConfigureWaveformPoints

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class EmuDispatcher(HIDDispatcher):
    """
    Dispatcher for HID messages coming from the emulation device.
    """
    
    def __init__(self):
        """
        Init command parameters.
        """
        super(EmuDispatcher, self).__init__()

        # Feature table following the format:
        #   (feature id, supported versions, function index): Implementation class
        # For example:
        #   (0xA002, tuple(0,), 0): GetButtonTableInfoResponse class
        self._featureTable = {
            # 0xA000 TriggerEvents
            (TriggerEvents.FEATURE_ID, GetTriggerCount.VERSION, GetTriggerCount.FUNCTION_INDEX): GetTriggerCount,
            (TriggerEvents.FEATURE_ID, ClearTrigger.VERSION, ClearTrigger.FUNCTION_INDEX): ClearTrigger,
            (TriggerEvents.FEATURE_ID, TriggerSequence.VERSION, TriggerSequence.FUNCTION_INDEX): TriggerSequence,
            (TriggerEvents.FEATURE_ID, TriggerSingle.VERSION, TriggerSingle.FUNCTION_INDEX): TriggerSingle,
            (TriggerEvents.FEATURE_ID, TriggerList.VERSION, TriggerList.FUNCTION_INDEX): TriggerList,
            # 0xA001 LoadOpticalSensorData
            (LoadOpticalSensorData.FEATURE_ID, CreateImmediateDisplacement.VERSION,
             CreateImmediateDisplacement.FUNCTION_INDEX): CreateImmediateDisplacement,
            # 0xA002 ConfigureButtons
            (ConfigureButtons.FEATURE_ID, GetButtonTableInfo.VERSION, GetButtonTableInfo.FUNCTION_INDEX):
                GetButtonTableInfo,
            (ConfigureButtons.FEATURE_ID, CreateSimpleEvent.VERSION, CreateSimpleEvent.FUNCTION_INDEX):
                CreateSimpleEvent,
            (ConfigureButtons.FEATURE_ID, CreateWaveformEvent.VERSION, CreateWaveformEvent.FUNCTION_INDEX):
                CreateWaveformEvent,
            (ConfigureButtons.FEATURE_ID, ConfigureWaveformPoints.VERSION, ConfigureWaveformPoints.FUNCTION_INDEX):
                ConfigureWaveformPoints,
        }

        self._eventTable = {
            # 0xA000 TriggerEvents
            (TriggerEvents.FEATURE_ID, EndOfSequenceEvent.VERSION, EndOfSequenceEvent.FUNCTION_INDEX):
                EndOfSequenceEvent,
            # 0xA001 LoadOpticalSensorData
            (LoadOpticalSensorData.FEATURE_ID, SensorPolledEvent.VERSION, SensorPolledEvent.FUNCTION_INDEX):
                SensorPolledEvent,
        }

        # List of all active handlers
        self._handlers = []

        """
        Add queues to store messages by feature.
        """
        # Pre-register queue for features
        self.queue_list = []

        # HID++ Important messages
        self.queue_list.append(self.important_message_queue)

        # HID++ Test messages
        self.testMessageQueue = HidMessageQueue(accepted_messages=(GetTriggerCount,
                                                                   ClearTrigger,
                                                                   TriggerSequence,
                                                                   TriggerSingle,
                                                                   TriggerList,
                                                                   CreateImmediateDisplacement,
                                                                   GetButtonTableInfo,
                                                                   CreateSimpleEvent,
                                                                   CreateWaveformEvent,
                                                                   ConfigureWaveformPoints,))
        self.queue_list.append(self.testMessageQueue)

        # HID++ Event messages
        self.event_message_queue = HidMessageQueue(accepted_messages=(EndOfSequenceEvent,
                                                                      SensorPolledEvent,))
        self.queue_list.append(self.event_message_queue)

        # HID++ Error messages
        self.error_message_queue = HidMessageQueue(accepted_messages=(ErrorCodes,))
        self.queue_list.append(self.error_message_queue)

        for my_queue in self.queue_list:
            self.add_handler(my_queue)
        # end for
    # end def __init__
# end class EmuDispatcher

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
