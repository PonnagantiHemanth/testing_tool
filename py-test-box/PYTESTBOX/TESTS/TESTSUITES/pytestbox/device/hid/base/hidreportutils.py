#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.xydisplacementutils
:brief:  Helpers for X and Y displacement feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/01/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from enum import auto

from pyhid.hid import HidCallStateManagementControl
from pyhid.hid.hidconsumer import HidConsumer
from pyhid.hid.hidkeyboard import HidKeyboard
from pyhid.hid.hidkeyboardbitmap import HidKeyboardBitmap
from pyhid.hid.hidmouse import HidMouse
from pyhid.hid.hidmouse import HidMouseNvidiaExtension
from pyhid.hid.hidsystemcontrol import HidSystemControl
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper


# ----------------------------------------------------------------------------
# constant
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
def to_signed_int(value, little_endian=False):
    """
    Transform a value to a signed ``int`` format

    :param value: Value to transform to ``int``
    :type value: ``HexList`` or ``Numeral``
    :param little_endian: Flag indicating if the value is in little endian (``False`` means big endian) - OPTIONAL
    :type little_endian: ``bool``

    :return: ``int`` format of the given value
    :rtype: ``int``
    """
    signed_int = int(Numeral(value, littleEndian=little_endian))
    # 1 byte: positive if value <= 127 else negative
    # 2 bytes: positive if value <= 32767 else negative
    if signed_int > ((1 << ((len(value) * 8) - 1)) - 1):
        signed_int -= (1 << (len(value) * 8))
    # end if
    return signed_int
# end def to_signed_int


class HidReportTestUtils(CommonBaseTestUtils):
    """
    Define a not instanstiatable super class providing methods related to HId report manipulation
    """

    class EventId(IntEnum):
        LEFT_CLICK = auto()
        RIGHT_CLICK = auto()
        MIDDLE_BUTTON = auto()
        BACKWARD = auto()
        FORWARD = auto()
        BUTTON6 = auto()
        X_MOTION = auto()
        Y_MOTION = auto()
        HORIZONTAL_SCROLL = auto()
        VERTICAL_SCROLL = auto()
    # end class EventId

    EVENT_FIELD_MAP = {
        EventId.LEFT_CLICK: 'button1',
        EventId.RIGHT_CLICK: 'button2',
        EventId.MIDDLE_BUTTON: 'button3',
        EventId.BACKWARD: 'button4',
        EventId.FORWARD: 'button5',
        EventId.BUTTON6: 'button6',
        EventId.X_MOTION: 'x',
        EventId.Y_MOTION: 'y',
        EventId.HORIZONTAL_SCROLL: 'wheel',
        EventId.VERTICAL_SCROLL: 'ac_pan',
    }

    KEY_ID_EVENT_MAP = {
        KEY_ID.LEFT_BUTTON: EventId.LEFT_CLICK,
        KEY_ID.RIGHT_BUTTON: EventId.RIGHT_CLICK,
        KEY_ID.MIDDLE_BUTTON: EventId.MIDDLE_BUTTON,
        KEY_ID.BACK_BUTTON: EventId.BACKWARD,
        KEY_ID.FORWARD_BUTTON: EventId.FORWARD,
        KEY_ID.BUTTON_6: EventId.BUTTON6,
    }

    class Event:
        """
        Event class implementation
        """
        def __init__(self, event_type, value=0):
            """
            :param event_type: The type of event triggering the HID Mouse report
            :type event_type: ``HidReportTestUtils.EventId``
            :param value: The value associated to the event - OPTIONAL
            :type value: ``int``
            """
            self.event_type = event_type
            self.value = value
        # end def __init__

        def __str__(self):
            return f'({str(self.event_type)}, state: {self.value})'
        # end def __str__

        def __repr__(self):
            return self.__str__()
        # end def __repr__
    # end class Event

    @classmethod
    def reset_last_reports(cls, test_case):
        """
        Reset the last HID reports stored in the test case

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        test_case.last_reports = {
            "HidCallStateManagementControl": HidCallStateManagementControl(),
            "HidConsumer": HidConsumer(),
            "HidKeyboard": HidKeyboard(),
            "HidKeyboardBitmap": HidKeyboardBitmap(),
            "HidMouse": HidMouse(),
            "HidMouseNvidiaExtension": HidMouseNvidiaExtension(),
            "HidSystemControl": HidSystemControl(),
        }
    # end def reset_last_reports

    @classmethod
    def get_last_report(cls, test_case, report_class):
        """
        Check the HID report associated to a key pressed or released stimulus.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param report_class: Key internal unique reference
        :type report_class: ``HidKeyboard`` or ``HidConsumer`` or ``HidKeyboardBitmap``

        :return: The last HID report returned to the host
        :rtype: ``HidKeyboard`` or ``HidConsumer`` or ``HidKeyboardBitmap`` or ``HidMouse`` or
                ``HidMouseNvidiaExtension``
        """
        if not hasattr(test_case, 'last_reports'):
            cls.reset_last_reports(test_case)
        # end if
        return test_case.last_reports[report_class.__name__]
    # end def get_last_report

    @classmethod
    def get_expected_report(cls, test_case, events):
        """
        Get the HID mouse report associated to an event.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param events: The list of events triggering the HID report
        :type events: ``list[HidReportTestUtils.Event]``

        :return: The expected HID report returned to the host
        :rtype: ``HidKeyboard`` or ``HidConsumer`` or ``HidKeyboardBitmap`` or ``HidMouse`` or
                ``HidMouseNvidiaExtension``
        """
        # Extract the expected HID parameters from table
        fields_name = [cls.EVENT_FIELD_MAP[x.event_type] for x in events]
        fields_value = [x.value for x in events]

        # Retrieve the previous HID report
        mouse_report_class = globals()[test_case.f.PRODUCT.HID_REPORT.F_HidMouseType]
        expected_report = cls.get_last_report(test_case, report_class=mouse_report_class)

        for j in range(len(fields_name)):
            # If field length is greater than 8 bits, the value shall be converted in little endian
            if expected_report.get_field_from_name(fields_name[j].lower()).length > 8 and fields_value[j] >= 0:
                # +1 -> HexList("0001") ; +2 -> HexList("0002") ; ...
                value = HexList(Numeral(fields_value[j], 2))
            elif expected_report.get_field_from_name(fields_name[j].lower()).length > 8 and fields_value[j] < 0:
                # -1 -> HexList("FFFF") ; -2 -> HexList("FFFE")
                value = HexList(Numeral(0x10000 + fields_value[j]))
            else:
                value = fields_value[j]
            # end if
            expected_report.setValue(expected_report.getFidFromName(fields_name[j].lower()), value)
        # end for
        return expected_report
    # end def get_expected_report

    @classmethod
    def get_missing_report_counter(cls, test_case, increment=False):
        """
        Increment the counter of missing HID report.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param increment: Flag to increment the counter - OPTIONAL
        :type increment: ``bool``

        :return: The counter of missing HID report
        :rtype: ``int``
        """
        if not hasattr(test_case, 'missing_hid_report_counter'):
            test_case.missing_hid_report_counter = 0
        # end if
        if increment:
            test_case.missing_hid_report_counter += 1
        # end if
        return test_case.missing_hid_report_counter
    # end def get_missing_report_counter

    @classmethod
    def dut_mismached_reports(cls, test_case, report=None):
        """
        Save the list of missing HID reports coming from the DUT.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param report: HID report from DUT which is not matching - OPTIONAL
        :type report: ``HexList``

        :return: The list of missing HID reports
        :rtype: ``list[HexList]``
        """
        if not hasattr(test_case, 'dut_mismached_reports'):
            test_case.dut_mismached_reports = []
        # end if
        if report is not None:
            test_case.dut_mismached_reports.append(report)
        # end if
        return test_case.dut_mismached_reports
    # end def dut_mismached_reports

    @classmethod
    def check_hid_report_by_event(cls, test_case, events, raise_exception=True):
        """
        Check the HID Mouse report associated to an event.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param events: The list of events triggering the HID Mouse report
        :type events: ``list[HidReportTestUtils.Event]``
        :param raise_exception: Flag enabling to raise an exception when a failure occurs - OPTIONAL
        :type raise_exception: ``bool``

        :return: Success status
        :rtype: ``bool``

        :raise ``NoMessageReceived``: Exception thrown by ``HidMessageQueue`` when the expected message hasn't been
        received.
        """
        success = True

        # Retrieve the previous HID report
        mouse_report_class = globals()[test_case.f.PRODUCT.HID_REPORT.F_HidMouseType]
        last_report = cls.get_expected_report(test_case=test_case, events=events)

        # Retrieve the next HID report
        hid_packet = ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                           class_type=mouse_report_class, check_first_message=False)

        test_case.logTrace(f'{mouse_report_class.__name__}: {str(hid_packet)}\n')
        if not last_report == hid_packet:
            cls.get_missing_report_counter(test_case, increment=True)
            LogHelper.log_info(test_case, f'The expected report {HexList(last_report)} differs from the one '
                                          f'received {HexList(hid_packet)}')
            cls.dut_mismached_reports(test_case, report=HexList(hid_packet))
            if raise_exception:
                test_case.fail(f'Error on report verification {hid_packet} != {last_report}')
            # end if
        # end if

        return success
    # end def check_hid_report_by_event

    @classmethod
    def check_motion_accumulation(cls, test_case, events, raise_exception=True):
        """
        Check the HID Mouse report associated to an event.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param events: The list of events triggering the HID Mouse report
        :type events: ``list[HidReportTestUtils.Event]``
        :param raise_exception: Flag enabling to raise an exception when a failure occurs - OPTIONAL
        :type raise_exception: ``bool``

        :return: Success status
        :rtype: ``bool``

        :raise ``NoMessageReceived``: Exception thrown by ``HidMessageQueue`` when the expected message hasn't been
        received.
        """
        success = True
        mouse_report_class = globals()[test_case.f.PRODUCT.HID_REPORT.F_HidMouseType]

        expected_x = 0
        expected_y = 0
        expected_buttons = []
        button_id = None
        button = None
        for event in events:
            if event.event_type == HidReportTestUtils.EventId.X_MOTION:
                expected_x += event.value
            elif event.event_type == HidReportTestUtils.EventId.Y_MOTION:
                expected_y += event.value
            elif event.event_type in HidReportTestUtils.KEY_ID_EVENT_MAP:
                expected_buttons.append((HidReportTestUtils.EVENT_FIELD_MAP[event.event_type], event.value))
            # end if
        # end for

        accumulated_x = 0
        accumulated_y = 0
        while expected_x != accumulated_x or expected_y != accumulated_y:
            # Retrieve the next HID report
            hid_packet = ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                               class_type=mouse_report_class, check_first_message=False,
                                               skip_error_message=True, allow_no_message=True)
            if hid_packet is not None:
                accumulated_x += to_signed_int(hid_packet.getValue(hid_packet.getFidFromName('x')))
                accumulated_y += to_signed_int(hid_packet.getValue(hid_packet.getFidFromName('y')))
                for button_id, expected_value in expected_buttons:
                    button_value = hid_packet.getValue(hid_packet.getFidFromName(button_id))
                    if raise_exception and button_value != expected_value:
                        test_case.fail(f'Error on button {button_id} state validation: '
                                       f'{expected_value} != {button_value} while accumulated_x={accumulated_x} and '
                                       f'accumulated_y={accumulated_y}')
                    # end if
                # end for
            else:
                break
            # end if
        # end while

        if not (expected_x == accumulated_x and expected_y == accumulated_y):
            LogHelper.log_info(test_case, f'The expected XY displacement {expected_x}/{expected_y} differs from the '
                                          f'one received {accumulated_x}/{accumulated_y}')
            if raise_exception:
                test_case.fail(f'Error on accumulation verification {expected_x}/{expected_y} != '
                               f'{accumulated_x}/{accumulated_y}')
            # end if
        # end if

        return success
    # end def check_motion_accumulation

# end class HidReportTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
