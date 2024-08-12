# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: logidevice.frameworkadaptor
:brief:   Utility for sending hid++ message and receiving hidmouse and hidkeyboard
:author:  Jerry Lin
:date:    2020/04/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os import access, path, R_OK, remove
from os.path import abspath, isfile
import sys
from time import sleep
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
LIBUSB_INI = WS_DIR + "TESTS/LOCAL/Libusb.ini"

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


from pyusb.libusbdriver import LibusbDriver
from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pyharness.arguments import KeywordArguments
from pyharness.context import ContextLoader
from pyharness.context import RootContext
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hiddispatcher import HidMessageQueue
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.features.enablehidden import EnableHiddenModel
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.bitstruct import BitStruct
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils

# Feature Model pyhid @PYTESTBOX/LIBS/PYHID/pyhid
from pyhid.hidpp.features.root import RootModel #0x0000
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationModel  # 0x0003
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndNameModel  # 0x0005
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryModel  # 0x1004
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthenticationModel  # 0x1602
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibrationModel  # 0x1861
from pyhid.hidpp.features.common.powermodes import PowerModesModel  # 0x1830
from pyhid.hidpp.features.common.rftest import RFTestModel  # 0x1890
from pyhid.hidpp.features.common.rftestble import RFTestBLEModel  # 0x1891
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuthModel  # 0x1E02
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpiModel  # 0x2201
from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessControlModel  # 0x8040
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffectsModel  # 0x8071


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FrameworkAdapter:
    """
    Adapter to control Logitech devices via pytestbox test framework.

    Implement the communication with DUT based on pytestbox.base.basetest.BaseTestCase
    """
    # {Feature_ID : Feature Model }
    MODEL_MAP = {0x0000: RootModel,
                 0x0003: DeviceInformationModel,
                 0x0005: DeviceTypeAndNameModel,
                 0x1004: UnifiedBatteryModel,
                 0x1602: PasswordAuthenticationModel,
                 0x1830: PowerModesModel,
                 0x1861: BatteryLevelsCalibrationModel,
                 0x1890: RFTestModel,
                 0x1891: RFTestBLEModel,
                 0x1E00: EnableHiddenModel,
                 0x1E02: ManageDeactivatableFeaturesAuthModel,
                 0x2201: AdjustableDpiModel,
                 0x8040: BrightnessControlModel,
                 0x8071: RGBEffectsModel}

    QUEUE_NAME_MAP = {0x0000: HIDDispatcher.QueueName.IMPORTANT,
                      0x0003: HIDDispatcher.QueueName.COMMON,
                      0x0005: HIDDispatcher.QueueName.COMMON,
                      0x1004: HIDDispatcher.QueueName.COMMON,
                      0x1602: HIDDispatcher.QueueName.COMMON,
                      0x1830: HIDDispatcher.QueueName.COMMON,
                      0x1861: HIDDispatcher.QueueName.COMMON,
                      0x1890: HIDDispatcher.QueueName.COMMON,
                      0x1891: HIDDispatcher.QueueName.COMMON,
                      0x1E00: HIDDispatcher.QueueName.COMMON,
                      0x1E02: HIDDispatcher.QueueName.COMMON,
                      0x2201: HIDDispatcher.QueueName.MOUSE,
                      0x8040: HIDDispatcher.QueueName.GAMING,
                      0x8071: HIDDispatcher.QueueName.GAMING}

    # Feature that might disconnect and send connection message
    DISCONNECT = [0x1890, 0x1891, ]

    # Functions that needs more time to get response
    # {
    #       Feature_ID : {
    #           Function_ID : lambda to get timeout
    #       }
    # }
    TIMEOUT = {
        0x1890: {
            0: lambda kwargs: to_int(kwargs["nbmsg"]) * to_int(kwargs["period"]) / 1000,
            3: lambda kwargs: to_int(kwargs["nb_sweep"])
                              * (to_int(kwargs["channel_max"]) - to_int(kwargs["channel_min"]) + 1)
                              * to_int(kwargs["sweep_period"]) / 100,
            4: lambda kwargs: to_int(kwargs["nb_sweep"])
                              * (to_int(kwargs["channel_max"]) - to_int(kwargs["channel_min"]) + 1)
                              * to_int(kwargs["sweep_period"]) / 100,
        },
        0x1891: {
            0: lambda kwargs: to_int(kwargs["nbmsg"]) * to_int(kwargs["period"]) / 1000,
            3: lambda kwargs: to_int(kwargs["nb_sweep"])
                              * (to_int(kwargs["channel_max"]) - to_int(kwargs["channel_min"]) + 1)
                              * to_int(kwargs["sweep_period"]) / 100,
            4: lambda kwargs: to_int(kwargs["nb_sweep"])
                              * (to_int(kwargs["channel_max"]) - to_int(kwargs["channel_min"]) + 1)
                              * to_int(kwargs["sweep_period"]) / 100,
        },
    }

    # Default parameter for functions
    # {
    #     Feature_ID: {
    #         Function_ID : {key: value}
    #     }
    # }
    DEFAULT_PARAM = {
        0x1890: {
            0: {"address": HexList("0000000000")},
            5: {"address": HexList("0000000000")},
            6: {"address": HexList("0000000000")},
        },
        0x1891: {
            0: {"address": HexList("0000000000")},
            5: {"address": HexList("0000000000")},
            6: {"address": HexList("0000000000")},
        },
    }

    PASSWORD_MANUF = "6162636465666768696A6B6C6D6E6F70"
    PASSWORD_COMPL = "30313233343536373839414243444546"
    PASSWORD_GOTHA = "6162636465666768696A6B6C6D6E6F70"

    def __init__(self, variant, pid, tid):
        """
        :param variant: The path of the .ini device setting file. None for default file.
        :type variant: ``str`` or ``None``
        :param pid: The product ID of the device. None for the pid in variant.
        :type pid: ``str`` or ``None``
        :param tid: The transport ID of the device. None for the tid in variant.
        :type tid: ``str`` or ``None``
        """
        # When comparing with Hexlist in libusbdriver, only upper case is acceptable
        if isinstance(pid, str):
            pid = pid.upper()
        # end if
        if isinstance(tid, str):
            tid = tid.upper()
        # end if

        self.variant = variant
        self.pid = pid
        self.tid = tid

        # Device Under Test (DUT) handle
        self.framework = BaseTestCase('run')
        # A boolean variable indicating if the receiver is connecting to the device
        self.connecting = False
        # An int variable recording the last sending feature
        self.last_feature_id = 0
        # A list of hidden feature ID
        self.hidden_features_cache = []
        # A list of normal feature ID
        self.normal_features_cache = []
        # A list of feature ID which the device doesn't support
        self.unsupported_features_cache = []
        # A dictionary which key is feature id and value is feature index and its version
        self.feature_id_to_index_and_version_cache = dict()  # {feature_id: (feature_index, feature_version)}
    # end def __init__

    def start(self):
        """
        Set up the framework.

        Remove the libuse.ini file to force the libusb liarary to search the device again, and then create the context
        and call the setUp of self.framework(BaseTestCase.setUp()). If the setUp fails, it will close before throwing
        the exception.
        """
        # force libusb to search device again
        if isfile(LIBUSB_INI):
            remove(LIBUSB_INI)
        # end if

        self.framework._currentContext = self.create_context(self.variant, self.pid, self.tid)

        try:
            self.framework.setUp()
            self.connecting = True
        except Exception as e:
            self.framework.tearDown()
            self.framework._currentContext.close()
            raise e
        # end try
    # end def start

    def reset(self):
        """
        Reset the device.

        Calling the reset in BaseTestCase. If there is power supply board, it will also do the hardware reset.
        Set self.connecting to true even if the framework doesn't get the message of reconnection(Calling
            BaseTestCase.reset() will clear all messages).
        """
        if self.last_feature_id in self.DISCONNECT:
            self.clear_connection_message()
        # end if
        self.check_queues()

        self.framework.reset(hardware_reset=self.framework.power_supply_emulator is not None,
                             verify_connection_reset=False)
        self.connecting = True
    # end def reset

    def device_restart(self, task_bitmap=LinkEnablerInfo.ALL_MASK):
        """
        restart device with specified task.

        :param task_bitmap: bitmap of active tasks - OPTIONAL
        :type task_bitmap: ``LinkEnablerInfo`` or ``int``
        """
        ChannelUtils.close_channel(test_case=self.framework)
        ChannelUtils.open_channel(test_case=self.framework, link_enabler=BitStruct(Numeral(task_bitmap)))
    # end def device_restart

    def close(self):
        """
        Tear down the framework.

        Calling BaseTestCase.teardown() and close the context.
        """
        if self.last_feature_id in self.DISCONNECT:
            self.clear_connection_message()
        # end if

        self.framework.tearDown()
        self.framework._currentContext.close()
        self.connecting = False
        LibusbDriver.IS_CONFIGURED = False
        # Clear feature cache when closing the framework handler
        LibusbDriver.FEATURE_CACHE = {}
    # end close

    def is_connecting(self):
        """
        Check if the DUT is connecting to the receiver.

        Get the message from receiver_connection_event_queue to check the connectivity of the receiver and DUT.
        If the last feature might cause the disconnection, it will clear the connection message and not warn.
        """
        if self.last_feature_id in self.DISCONNECT:
            self.clear_connection_message()
        # end if

        return self.connecting
    # end def is_connecting

    def __bool__(self):
        """Return if the DUT is connecting to the receiver."""
        return self.is_connecting()
    # end def __bool__

    def send_message(self, feature_id, function_id, ignore_response=False, **kwargs):
        """
        Send hid++ message to device.

        :param feature_id: The feature ID of the desired HID++ message.
        :type feature_id: ``int``
        :param function_id: The function ID of the desired HID++ message.
        :type function_id: ``int``
        :param ignore_response: Flag indicating if the function returns without waiting for the response - OPTIONAL
        :type ignore_response: ``bool``
        :param kwargs: The arguments for the desired HID++ message. - OPTIONAL
        :type kwargs: ``dict``

        :return: The message got from the queue.
        :rtype: ``response_class_type`` or ``None``

        :raise ``AttributeError``: If the adapter doesn't support the feature.
        :raise ``RuntimeError``: If the adapter doesn't support the feature version from the device or the function ID
                                 exceeds the max function ID of the feature version from the device.
        :raise ``HexListError``: If the user gives odd-length string for the message argument.
        """
        if feature_id not in self.MODEL_MAP:
            raise AttributeError(F"The framework adapter does not support feature {feature_id:04X}.")
        # end if
        feature_index, version = self.get_feature_index_and_version_from_dut(feature_id=feature_id)

        feature_model = self.MODEL_MAP[feature_id]
        if version not in feature_model._get_data_model()["versions"]:
            raise RuntimeError(F"The framework does not support version {version} of feature {feature_id:04X}.")
        # end if

        max_function_index = feature_model.get_main_cls(version)().get_max_function_index()
        if function_id > max_function_index:
            raise RuntimeError(F"The function index({function_id}) exceeds the max function index({max_function_index})"
                               F" of version {version} of featureId {feature_id:04X}.")
        # end if

        # message
        param = {}
        if feature_id in self.DEFAULT_PARAM and function_id in self.DEFAULT_PARAM[feature_id]:
            param.update(self.DEFAULT_PARAM[feature_id][function_id])
        # end if
        param.update(kwargs)

        report = feature_model.get_request_cls(version, function_id)\
            (ChannelUtils.get_device_index(self.framework), feature_index, **param)
        response = feature_model.get_response_cls(version, function_id)

        message = None
        if response is None or ignore_response:
            ChannelUtils.send_only(test_case=self.framework, report=report, timeout=0)
        else:
            timeout = 1
            if feature_id in self.TIMEOUT and function_id in self.TIMEOUT[feature_id]:
                timeout += self.TIMEOUT[feature_id][function_id](param)
            # end if
            message = ChannelUtils.send(
                test_case=self.framework,
                report=report,
                response_queue_name=self.QUEUE_NAME_MAP[feature_id],
                response_class_type=response,
                get_timeout=timeout)
        # end if

        if feature_id in self.DISCONNECT:
            self.clear_connection_message()
        # end if

        self.last_feature_id = feature_id
        return message
    # end def send_message

    def get_queue_message(self, queue_name, timeout=2):
        """
        Get messages from the specific queue.

        If the queue is receiver_connection_event_queue, handle the connecting status for each message.

        :param queue_name: The queue name (names can be found in ``HIDDispatcher.QueueName``). If None, it bypasses the
                           dispatcher and get the first new HID++ message (old messages already processed by the
                           dispatcher are not considered) received as a ``TransportMessage`` - OPTIONAL
        :type queue_name: ``str``
        :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
        :type timeout: ``float``

        :return: A list containing messages got from the queue.
        :rtype: ``list``
        """
        result = []

        msg = ChannelUtils.get_only(test_case=self.framework, queue_name=queue_name, timeout=timeout,
                                    allow_no_message=True)
        if msg is not None:
            result.append(msg)
        # end if
        while msg is not None:
            msg = ChannelUtils.get_only(test_case=self.framework, queue_name=queue_name, timeout=timeout,
                                        allow_no_message=True)
            if msg is not None:
                result.append(msg)
            # end if
        # end while

        return result
    # end get_queue_message

    @staticmethod
    def clear_queue(queue):
        """
        clear messages in the specific queue.

        :param queue: The queue which is taken.
        :type queue: ``HidMessageQueue``
        """
        with queue.mutex:
            queue.queue.clear()
        # end with
    # end def clear_queue

    @staticmethod
    def create_context(variant, pid, tid):
        """
        Create the context to get the device.

        :param variant: The path of the .ini device setting file. None for default file.
        :type variant: ``str`` or ``None``
        :param pid: The product ID of the device. None for the pid in variant.
        :type pid: ``str`` or ``None``
        :param tid: The transport ID of the device. None for the tid in variant.
        :type tid: ``str`` or ``None``

        :return: A context containing the information of the device.
        :rtype: ``RootContext``

        :raise ``ValueError``: If the root path is invalid.
        """

        root = KeywordArguments.DEFAULT_ARGUMENTS[KeywordArguments.KEY_ROOT]
        root = abspath(root)

        overrides = []
        if variant is not None:
            overrides.append('VARIANT.value=' + variant)
        # end if
        # overrides.append('PRODUCT.value=PYTESTBOX')

        # If the root path can be accessed, create a new context, that
        # works on this root path (extracting versions, etc...)
        if access(root, R_OK):
            root_paths = [root]
            root_paths.extend(KeywordArguments.DEFAULT_ARGUMENTS[KeywordArguments.KEY_EXTENDEDROOTS])
            context_loader = ContextLoader()
            config = context_loader.loadConfig(root_paths, overrides)
            context = context_loader.createContext(config,
                                                   manualUi=KeywordArguments.DEFAULT_ARGUMENTS[
                                                      KeywordArguments.KEY_MANUALUI],
                                                   additionalSubSystemInstantiations=tuple())
        else:
            raise ValueError("Unable to accesspath <%s>" % (root,))
        # end if

        if not context.getFeatures().PRODUCT.F_Enabled:
            context.close()
            raise ValueError(F"Invalid variant: {variant}")
        # end if

        if pid is not None:
            context.getFeatures().PRODUCT._AbstractSubSystem__readOnlyAttr.remove('F_ProductID')
            context.getFeatures().PRODUCT.F_ProductID = pid
            context.getFeatures().PRODUCT.makeReadOnly('F_ProductID')
        # end if

        if tid is not None:
            context.getFeatures().PRODUCT._AbstractSubSystem__readOnlyAttr.remove('F_TransportID')
            context.getFeatures().PRODUCT.F_TransportID = tid
            context.getFeatures().PRODUCT.makeReadOnly('F_TransportID')
        # end if

        # Wired DUT does not support set idle
        if context.getFeatures().PRODUCT.F_ProductID == context.getFeatures().PRODUCT.F_TransportID:
            context.getFeatures().PRODUCT.USB_COMMUNICATION._AbstractSubSystem__readOnlyAttr\
                .remove('F_SetIdleSupported')
            context.getFeatures().PRODUCT.USB_COMMUNICATION.F_SetIdleSupported = False
            context.getFeatures().PRODUCT.USB_COMMUNICATION.makeReadOnly('F_SetIdleSupported')
        # end if

        return context
    # end def create_context

    def handle_connection_queue(self):
        """
        Change the connecting status based on the DeviceConnection message
        """
        device_connection = ChannelUtils.get_only(
                                test_case=self.framework,
                                channel=ChannelUtils.get_receiver_channel(test_case=self.framework),
                                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, timeout=0,
                                allow_no_message=True)

        if device_connection is None:
            return
        # end if

        device_info_class = BaseTestCase.get_device_info_bit_field_structure_in_device_connection(device_connection)
        device_info = device_info_class.fromHexList(HexList(device_connection.information))
        link_status = int(Numeral(device_info.device_info_link_status))
        self.connecting = link_status == DeviceConnection.LinkStatus.LINK_ESTABLISHED
        # end if
    # end def handle_connection_queue

    def check_queues(self):
        """
        Check if all of the queue in hidDispatcher are empty.

        If one of them is not empty, show warning on the console.
        When checking receiver_connection_event_queue, also handle the connection status.
        """
        # Check other queues are empty
        if hasattr(self.framework.current_channel, 'hid_dispatcher') and \
                self.framework.current_channel.hid_dispatcher is not None:

            for queue in self.framework.current_channel.hid_dispatcher.queue_list:
                if queue == self.framework.current_channel.hid_dispatcher.receiver_connection_event_queue:
                    self.get_queue_message(queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)
                else:
                    while not ChannelUtils.warn_queue_not_empty(test_case=self.framework, queue_name=queue.name):
                        pass
                    # end while
                # end if
            # end for
        # end if
    # end def check_queues

    def clear_connection_message(self):
        """
        Clean the message causing by reconnection and disconnection.

        Clean all the messages in receiver_connection_event_queue and hid_message_queue.
        Handle the connection status by the messages in receiver_connection_event_queue.
        Ignore the messages with all zero in hid_message_queue, and warn if there is some not all zero.
        """
        if hasattr(self.framework.current_channel, 'hid_dispatcher') and \
                self.framework.current_channel.hid_dispatcher is not None:
            sleep(.7)  # wait for the response message

            # connection information
            self.get_queue_message(queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)

            # HidMouse HidKeyBoard
            while True:
                hid_message = ChannelUtils.get_only(
                                test_case=self.framework, queue_name=HIDDispatcher.QueueName.HID, allow_no_message=True)
                if hid_message is None:
                    break
                else:
                    for i in hid_message.FIELDS:
                        value = hid_message.getValue(i.getFid())
                        if isinstance(value, HexList):
                            value = value.toLong()
                        # end if

                        if value != 0:
                            warn("Warning: %s queue not empty (%s returned)" % (
                                str(self.framework.current_channel.hid_dispatcher.hid_message_queue), str(hid_message)))
                            break
                        # end if
                    # end for
                # end if
            # end while
        # end if
    # end def clear_connection_message

    def get_response_queue(self, response_class_type):
        """
        Find the corresponding queue in hidDispatcher to response_class_type.

        :param response_class_type: The type of response message.
        :type response_class_type: ``HidppMessage``

        :return: The queue in hid_dispatcher which accepts response_class_type
        :rtype: ``HidMessageQueue``

        :raise ``AttributeError``: If can't find the queue for the response_class_type.
        """
        if hasattr(self.framework.current_channel, 'hid_dispatcher') and\
                self.framework.current_channel.hid_dispatcher is not None:
            for queue in self.framework.current_channel.hid_dispatcher.queue_list:
                if response_class_type in queue._accepted_messages:
                    return queue
                # end if
            # end for
        # end if

        raise AttributeError('Can not found the queue for the response: %s' % response_class_type)
    # end def get_response_queue

    def get_feature_index_and_version_from_dut(self, feature_id):
        """
        Get the feature index and its version from the DUT by given feature ID.

        Find the feature in the cache first. If find the feature in the cache, check the hidDispatcher and add it if
        hidDispatcher does not store the feature. If the feature can not find in the cache, ask the DUT and store the
        result in the cache.

        :param feature_id: The feature ID of the desired HID++ message.
        :type feature_id: ``int``

        :return: The feature index and feature version.
        :rtype: ``tuple``

        :raise ``RuntimeError``: If the device dose not support the feature
        """
        if feature_id in self.unsupported_features_cache:
            raise RuntimeError(F"The device does not support feature {feature_id:04X}.")
        # end if

        if feature_id not in self.feature_id_to_index_and_version_cache:
            feature_index = ChannelUtils.update_feature_mapping(test_case=self.framework, feature_id=feature_id)
            if feature_id != 0 and feature_index == 0:
                self.unsupported_features_cache.append(feature_id)
                raise RuntimeError(F"The device does not support feature {feature_id:04X}.")
            # end if

            version = ChannelUtils.get_feature_version(test_case=self.framework, feature_index=feature_index)
            self.feature_id_to_index_and_version_cache[feature_id] = (feature_index, version)
        else:
            self.framework.current_channel.hid_dispatcher.add_feature_entry(
                feature_id=feature_id,
                feature_index=self.feature_id_to_index_and_version_cache[feature_id][0],
                feature_version=self.feature_id_to_index_and_version_cache[feature_id][1])
        # end if

        return self.feature_id_to_index_and_version_cache[feature_id]
    # end def get_feature_index_and_version_from_dut
# end class FrameworkAdapter
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
