# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: logidevice.logidevicehandler
:brief:   User Interface for sending hid++ message and receiving hidmouse and hidkeyboard
:author:  Jerry Lin
:date:    2020/04/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import json
import sys
from os import path, remove
from os.path import isfile
from warnings import warn

FILE_PATH = path.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("TESTS")]
PYHID_DIR = path.join(WS_DIR, "LIBS", "PYHID")
PYHARNESS_DIR = path.join(WS_DIR, "LIBS", "PYHARNESS")
PYLIBRARY_DIR = path.join(WS_DIR, "LIBS", "PYLIBRARY")
PYRASPI_DIR = path.join(WS_DIR, "LIBS", "PYRASPI")
PYSETUP_DIR = path.join(WS_DIR, "LIBS", "PYSETUP", "PYTHON")
PYTRANSPORT_DIR = path.join(WS_DIR, "LIBS", "PYTRANSPORT")
LOGIUSB_DIR = path.join(WS_DIR, "LIBS", "PYTRANSPORT", "pytransport", "usb", "logiusbcontext", "logiusb")
PYCHANNEL_DIR = path.join(WS_DIR, "LIBS", "PYCHANNEL")
PYUSB_DIR = path.join(WS_DIR, "LIBS", "PYUSB")
TESTSUITES_DIR = path.join(WS_DIR, "TESTS", "TESTSUITES")
TOOLS_DIR = path.join(WS_DIR, "TESTS", "TOOLS")
if PYHID_DIR not in sys.path:
    sys.path.insert(0, PYHID_DIR)
# end if
if PYHARNESS_DIR not in sys.path:
    sys.path.insert(0, PYHARNESS_DIR)
# end if
if PYLIBRARY_DIR not in sys.path:
    sys.path.insert(0, PYLIBRARY_DIR)
# end if
if PYRASPI_DIR not in sys.path:
    sys.path.insert(0, PYRASPI_DIR)
# end if
if PYSETUP_DIR not in sys.path:
    sys.path.insert(0, PYSETUP_DIR)
# end if
if PYTRANSPORT_DIR not in sys.path:
    sys.path.insert(0, PYTRANSPORT_DIR)
# end if
if LOGIUSB_DIR not in sys.path:
    sys.path.insert(0, LOGIUSB_DIR)
# end if
if PYCHANNEL_DIR not in sys.path:
    sys.path.insert(0, PYCHANNEL_DIR)
# end if
if PYUSB_DIR not in sys.path:
    sys.path.insert(0, PYUSB_DIR)
# end if
if TESTSUITES_DIR not in sys.path:
    sys.path.insert(0, TESTSUITES_DIR)
# end if
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)
# end if

from pyhid.hiddispatcher import HIDDispatcher
from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from logidevice.frameworkadaptor import FrameworkAdapter
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthentication
from pychannel.channelinterfaceclasses import LogitechReportType


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


class HIDPPDataLogger:
    """
    An logger to write the data to the file.
    """

    def __init__(self, file):
        """
        :param file: The output file. None representing not write the output file.
        :type file: ``str``
        """

        self._file = None
        self.file = file
    # end def __init__

    def write_file(self, msg):
        """
        Write message information to file.

        Output file name is 'prefix' + 'output_index' + '.txt'
        If prefix is None, do nothing.

        :param msg: A object that can be transform to JSON format.
        :type msg: ``object``
        """
        if self._file is not None and msg:
            f = open(self._file, 'a+')
            json.dump(msg, f)
            f.write("\n")
            f.close()
        # end if
    # end def write_file

    @property
    def file(self):
        return self._file
    # end def file

    @file.setter
    def file(self, file):
        """
        Set the output file name and delete it if it exist.

        :param file: The output file name, or None representing not write the output file.
        :type file: ``str``
        """
        if not isinstance(file, str) and file is not None:
            file = str(file)
        # end if
        self._file = file

        if self._file is not None:
            if isfile(self._file):
                remove(self._file)
            # end if
        # end if
    # end def file

    @staticmethod
    def message_to_dict(msg):
        """
        Get a dictionary containing the HID message data.

        :param msg: An HID message data
        :type msg: ``BitFieldContainerMixin``

        :return: The HID message data
        :rtype: ``dict``

        :raise ``AssertionError``: If msg is not an HID message
        """
        if msg is None:
            return dict()
        # end if

        assert isinstance(msg, BitFieldContainerMixin), "msg should a BitFieldContainerMixin."

        result = {"messageType": msg.name,
                  "rawData": '%s' % HexList(msg), }

        gen = (field for field in msg.FIELDS if
               (msg.hasValue(field.getFid())) or
               (field.has_default_value() and not field.is_optional(msg)))

        for i in gen:
            # value
            value = msg.getValue(i.getFid())
            if isinstance(value, HexList):
                value = value.toLong()
            elif isinstance(value, Numeral):
                value = value.value
            elif isinstance(value, BitFieldContainerMixin):
                value = value.__hexlist__().toLong()
            else:
                warn(f'Unknown value type: {type(value)}, value: {value}')
            # end if

            result[i.name] = value
        # end for

        return result
    # end message_to_dict
# end def HIDPPDataLogger


class LogiDeviceHandler:
    """
    An user interface to control the Logitech device via test framework adapter.
    """

    VARIANT = "PRODUCT"

    def __init__(self, pid, tid, file=None):
        """
        :param pid: The product ID of the device. None for the default PID
        :type pid: ``str`` or ``None``
        :param tid: The transport ID of the device. None for the default TID
        :type tid: ``str`` or ``None``
        :param file: The prefix of the output file. None for no output file.
        :type file: ``str`` or ``None``

        :raise ``AssertionError``: If the type of the argument is invalid.
        """
        assert isinstance(pid, str) or pid is None, "argument \'pid\' should be string or none."
        assert isinstance(tid, tuple) or tid is None, "argument \'tid\' should be tuple or none."

        self.framework_adapter = FrameworkAdapter(variant=LogiDeviceHandler.VARIANT, pid=pid, tid=tid)
        self.data_logger = HIDPPDataLogger(file=file)
        self.open = False
    # end def __init__

    def start(self):
        """
        To set up the adapter.
        """
        if self.is_open():
            warn("LH@Start:The device handler has already been running.")
        else:
            self.framework_adapter.start()
            self.open = True
        # end if
    # end def start

    def reset(self):
        """
        To reset the device.
        """

        if not self.is_open():
            warn("LH@reset:The device handler is not running.")
        else:
            self.framework_adapter.reset()
        # end if
    # end def reset

    def hidpp_reset(self, task_bitmap=LinkEnablerInfo.HID_PP_MASK):
        """
        Restart the device with only the HID++ task enabled.

        :param task_bitmap: bitmap of active tasks - OPTIONAL
        :type task_bitmap: ``LinkEnablerInfo`` or ``int``
        """

        if not self.is_open():
            if task_bitmap == LinkEnablerInfo.HID_PP_MASK:
                warn("hidpp_reset: The device handler is not running.")
            elif task_bitmap == LinkEnablerInfo.MOUSE_MASK | LinkEnablerInfo.HID_PP_MASK:
                warn("mouse_reset: The device handler is not running.")
            elif task_bitmap == LinkEnablerInfo.KEYBOARD_MASK | LinkEnablerInfo.HID_PP_MASK:
                warn("keyboard_reset: The device handler is not running.")
            elif task_bitmap == LinkEnablerInfo.ALL_MASK:
                warn("all_reset: The device handler is not running.")
            else:
                warn("unknown_reset: The device handler is not running.")
        else:
            self.framework_adapter.device_restart(
                task_bitmap=task_bitmap)
        # end if
    # end def hidpp_reset

    def mouse_reset(self):
        """
        Restart the device with only the Mouse & HID++ tasks enabled.
        """

        self.hidpp_reset(task_bitmap=LinkEnablerInfo.MOUSE_MASK | LinkEnablerInfo.HID_PP_MASK)
    # end def mouse_reset

    def keyboard_reset(self):
        """
        Restart the device with only the Keyboard & HID++ tasks enabled.
        """

        self.hidpp_reset(task_bitmap=LinkEnablerInfo.KEYBOARD_MASK | LinkEnablerInfo.HID_PP_MASK)
    # end def keyboard_reset

    def close(self):
        """
        To close the adapter.
        """
        if not self.is_open():
            warn("LH@close:The device handler has already been closed.")
        else:
            self.framework_adapter.close()
            self.open = False
        # end if
    # end def close

    def is_open(self):
        """
        Return if the adapter is set up or not

        :return: Flag indicating if the adapter is set up or not
        :rtype: ``bool``
        """
        return self.open
    # end def is_open

    def is_connecting(self):
        """
        Return if the receiver is connecting to the device.

        The adapter only updates the connecting status when calling this function.

        :return: Flag indicating if the receiver is connecting to the device
        :rtype: ``bool``
        """
        self.framework_adapter.handle_connection_queue()

        return self.is_open() and self.framework_adapter.is_connecting()

    def send_message(self, feature_id, function_id, ignore_response=False, **kwargs):
        """
        Send hid++ message to device.

        :param feature_id: The feature ID of the desired HID++ message.
        :type feature_id: ``int`` or ``str``
        :param function_id: The function ID of the desired HID++ message.
        :type function_id: ``int`` or ``str``
        :param ignore_response: Flag indicating if the function returns without waiting for the response - OPTIONAL
        :type ignore_response: ``bool``
        :param kwargs: The arguments for the desired HID++ message. - OPTIONAL
        :type kwargs: ``dict`` or ``str`` or ``int`` or ``HexList``

        :return: The message got from the queue, with feature_id, version and timestamp.
        :rtype: ``dict``

        :raise ``AttributeError``: If the user gives invalid argument or the adapter has not been set up.
        :raise ``AttributeError``: If the adapter doesn't support the feature.
        :raise ``RuntimeError``: If the adapter doesn't support the feature version from the device or the function ID
                                 exceeds the max function ID of the feature version from the device.
        :raise ``TypeError``: If missing the argument of the HID++ function
        :raise ``HexListError``: If the user gives odd-length string for the message argument.
        """
        if isinstance(feature_id, str):
            feature_id = int(feature_id, 16)
        # end if
        if isinstance(function_id, str):
            function_id = int(function_id, 16)
        # end if

        assert isinstance(feature_id, int), "feature_id should be int or string."
        assert isinstance(function_id, int), "function_id should be int or string."

        assert self.is_open(), "The device handler is not running."
        if not self.framework_adapter.is_connecting():
            warn("The device handler might not connecting to the device.")
        # end if

        for key in kwargs:
            if isinstance(kwargs[key], str) and kwargs[key].startswith('0x'):
                kwargs[key] = HexList(kwargs[key][2:])
            else:
                if isinstance(kwargs[key], str) and kwargs[key].upper() == "FALSE":
                    kwargs[key] = 0
                elif isinstance(kwargs[key], str) and kwargs[key].upper() == "TRUE":
                    kwargs[key] = 1
                elif feature_id == PasswordAuthentication.FEATURE_ID:
                    kwargs[key] = HexList(kwargs[key])
                else:
                    kwargs[key] = to_int(kwargs[key])
                # end if
        # end for

        msg = self.framework_adapter.send_message(
            feature_id=feature_id,
            function_id=function_id,
            ignore_response=ignore_response,
            **kwargs)

        result = HIDPPDataLogger.message_to_dict(msg)
        if result:
            result['feature_id'] = feature_id
            result['version'] = self.framework_adapter.get_feature_index_and_version_from_dut(feature_id=feature_id)[1]
            result['time_stamp'] = msg.timestamp
        # end if

        self.data_logger.write_file(result)
        return result
    # end send_message

    def get_hid_message(self):
        """
        Get the HidMouse and HidKeyboard message from the device.

        :return: The messages got from the queue
        :rtype: ``list``
        """
        result = self.framework_adapter.get_queue_message(queue_name=HIDDispatcher.QueueName.HID, timeout=0)

        timestamped_messages = []
        for msg in result:
            data = HIDPPDataLogger.message_to_dict(msg)
            if data['messageType'] in ['HidMouse', 'HidMouseNvidiaExtension']:
                data['time_stamp'] = msg.timestamp
            # end if
            timestamped_messages.append(data)
        # end for
        self.data_logger.write_file(timestamped_messages)

        return timestamped_messages
    # end def get_hid_message

    def get_hid_message_from_hid_queue(self, report_type=None):
        """
        Get the HidMouse or HidKeyboard message from the HID queue directly.

        :param report_type: The report type of message to use
        :type report_type: ``LogitechReportType``

        :return: The messages got from the queue
        :rtype: ``list``

        :raise ``ValueError``: If the report_type is None
        """
        if report_type is None:
            raise ValueError('report type should not be None')
        # end if

        result = []

        dispatcher_queue = \
            self.framework_adapter.framework.current_channel.hid_dispatcher.get_queue_by_name(
                name=HIDDispatcher.QueueName.HID)
        self.framework_adapter.framework.current_channel.process_all_report_type_in_dispatcher(report_type=report_type)
        queue = self.framework_adapter.framework.current_channel.receiver_channel.hid_dispatcher.get_queue_by_name(
            name=dispatcher_queue.name)
        msg = queue.get_no_wait_first_message_filter(filter_method=None, skip_error=True)

        while msg is not None:
            result.append(msg)
            msg = queue.get_no_wait_first_message_filter(filter_method=None, skip_error=True)
        # end while

        timestamped_messages = []

        for msg in result:
            data = HIDPPDataLogger.message_to_dict(msg)
            if data['messageType'] in ['HidMouse', 'HidMouseNvidiaExtension']:
                data['time_stamp'] = msg.timestamp
            # end if
            timestamped_messages.append(data)
        # end for

        return timestamped_messages
    # end def get_hid_message_from_hid_queue

    def clear_hid_message(self):
        """
        Clear messages in the hid message queue.
        """
        self.framework_adapter.clear_queue(queue=self.framework_adapter.framework.hidDispatcher.hid_message_queue)
    # end def clear_hid_message

    def get_hidpp_event(self):
        """
        Get messages in the event queue

        :return: A list containing messages got from the event queue.
        :rtype: ``list``
        """
        return self.framework_adapter.get_queue_message(queue_name=HIDDispatcher.QueueName.EVENT)
    # end def get_hidpp_event

    @property
    def output_name(self):
        """
        Get the output file name

        :return: The output file name, or None representing not write the output file.
        :rtype: ``str``
        """
        return self.data_logger.file
    # end def output_prefix

    @output_name.setter
    def output_name(self, name):
        """
        Set the output file name

        :param name: The output file name, or None representing not write the output file.
        :type name: ``str``

        :raise ``AssertionError``: If the name is not a string or None
        """
        self.data_logger.file = name
    # end def output_prefix

    def __enter__(self):
        """
        Support 'with' statement.

        If the adapter has not been set up, set it up.
        """
        if not self.is_open():
            self.start()
        # end if

        return self
    # end def __enter__

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Support 'with' statement.

        Close when leaving 'with' statement in any reasons.
        """
        if self.is_open():
            self.close()
        # end if
    # end def __exit__

    def __bool__(self):
        """
        Return if the adapter has been set up or not.
        """
        return self.is_open()
    # end def __bool__
# end def LogiDeviceHandler

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
