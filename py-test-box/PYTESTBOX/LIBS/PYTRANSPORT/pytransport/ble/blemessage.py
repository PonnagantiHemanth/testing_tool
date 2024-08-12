#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytransport.ble.blemessage
:brief: BLE message declaration
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/02/18
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.threadutils import QueueWithFilter
from pytransport.ble.bleconstants import BleContextEventDataType
from pytransport.ble.bleconstants import BleContextEventType
from pytransport.transportmessage import TransportMessage


# ------------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------
class BleMessage(TransportMessage):
    """
    BLE Data container
    """
    pass
# end class BleMessage


class BleContextEvent:
    """
    BLE Context Event container
    """

    def __init__(self, event_type, event_data, timestamp):
        """
        :param event_type: The wanted event type
        :type event_type: ``BleContextEventType`` or ``int``
        :param event_data: The data associated with the event
        :type event_data: ``dict[BleContextEventDataType, object]``
        :param timestamp: The timestamp associated with the event (monotonic, in nanoseconds)
        :type timestamp: ``int``

        :raise ``AssertionError``: The ``event_type`` parameter is not in ``BleContextEventType``
        """
        # Sanity check
        assert event_type in BleContextEventType, f"Unknown BLE context event type: {event_type}"
        assert isinstance(event_data, dict), \
            f"The type of event_data is {type(event_data).__name__}, it should be a dict"

        self.event_type = BleContextEventType(event_type)
        self.event_data = event_data
        self.timestamp = timestamp
    # end def __init__

    def __str__(self):
        return f"{type(self).__name__}(event_type = {self.event_type!r}, event_data = {self.event_data!r}, " \
               f"timestamp = {self.timestamp}ns)"
    # end def __str__

    __repr__ = __str__

    def __format__(self, format_spec):
        return str(self)
    # end def __format__
# end class BleContextEvent


class BleEventQueue(QueueWithFilter):
    """
    Queue used for BLE event to be able to get the wanted event type
    """

    def get_first_event_of_a_type(self, event_type, timeout=2, skip_error=False):
        """
        Get the first event with the requested event type in the queue

        :param event_type: The wanted event type
        :type event_type: ``BleContextEventType`` or ``int``
        :param timeout: The timeout of this action in seconds (``None`` disables it) - OPTIONAL
        :type timeout: ``float`` or ``None``
        :param skip_error: Flag to enable (default) / disable exception when the requested object is not
                           found - OPTIONAL
        :type skip_error: ``bool``

        :return: Expected object or ``None`` if not found and ``skip_error`` is ``True``
        :rtype: ``BleContextEvent`` or ``None``

        :raise ``AssertionError``: The ``event_type`` parameter is not in ``BleContextEventType``
        """
        assert event_type in BleContextEventType, f"Unknown BLE context event type: {event_type}"

        def filter_method(event_received):
            """

            :param event_received: BLE context event in the queue
            :type event_received: ``BleContextEvent``

            :return: Flag indicating that the event has the right type
            :rtype: ``bool``
            """
            # Sanity check
            if not isinstance(event_received, BleContextEvent):
                return False
            # end if
            return event_received.event_type == event_type
        # end def filter_method

        return self.get_first_message_filter(timeout=timeout, filter_method=filter_method, skip_error=skip_error)
    # end def get_first_event_of_a_type

    def clear_all_events_of_a_type(self, event_type):
        """
        Clear all events with the requested event type in the queue and return them in a list

        :param event_type: The wanted event type
        :type event_type: ``BleContextEventType`` or ``int``

        :return: The list of events
        :rtype: ``list[BleContextEvent]``
        """
        events_cleared = []

        event = self.get_first_event_of_a_type(event_type=event_type, timeout=None, skip_error=True)
        while event is not None:
            events_cleared.append(event)
            event = self.get_first_event_of_a_type(event_type=event_type, timeout=None, skip_error=True)
        # end while

        return events_cleared
    # end def clear_all_events_of_a_type
# end class BleEventQueue
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
