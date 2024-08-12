#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.shared.base.dfucontrolutils
    :brief:  Helpers for dfu control feature
    :author: Christophe Roquebert
    :date: 2020/05/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import ChannelException
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyhid.hid.usbhidusagetable import MOUSE_HID_USAGE_TO_KEY_ID_MAP
from pyhid.hid.usbhidusagetable import KEYBOARD_HID_USAGE_TO_KEY_ID_MAP
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.dfucontrol import DfuControlFactory
from pyhid.hidpp.features.common.dfucontrol import DfuControl
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControlFactory, GetDfuControlResponseV1
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControl
from pyhid.hidpp.features.common.securedfucontrol import GetDfuControlResponseV0
from pyhid.hidpp.features.devicereset import ForceDeviceReset
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.enterupgrademode import ENTER_USB_UPGRADE_KEY
from pyhid.hidpp.hidpp1.registers.enterupgrademode import GetEnterUpgradeModeRequest
from pyhid.hidpp.hidpp1.registers.enterupgrademode import GetEnterUpgradeModeResponse
from pyhid.hidpp.hidpp1.registers.enterupgrademode import SetEnterUpgradeModeRequest
from pyhid.hidpp.hidpp1.registers.securedfucontrol import GetDfuControlRequest
from pyhid.hidpp.hidpp1.registers.securedfucontrol import GetDfuControlResponse
from pyhid.hidpp.hidpp1.registers.securedfucontrol import SetDfuControlRequest
from pyhid.hidpp.hidpp1.registers.securedfucontrol import SetDfuControlResponse
from pylibrary.tools.aliasing import aliased
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pytransport.transportcontext import TransportContextException
from pyusb.libusbdriver import LibusbDriver
from time import sleep


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DfuControlTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers on dfu control feature
    """
    ENTER_DFU_LOOP_MAX_COUNTER = 3

    @staticmethod
    def get_dfu_control_feature_id(test_case):
        """
        Extract DfuControl feature identifier from the test config starting from the most recent variant (0xC3 then
        0xC2 ...)
        Note that only one variant shall be supported by the device

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: Dfu Control featureId
        :rtype: ``int``
        """
        f = test_case.getFeatures()
        if f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled:
            return SecureDfuControl.FEATURE_ID
        elif f.PRODUCT.FEATURES.COMMON.DFU_CONTROL.F_Enabled:
            return DfuControl.FEATURE_ID
        else:
            test_case.skipTest('Dfu Control Feature not enabled in test configuration')
        # end if
    # end def get_dfu_control_feature_id

    @staticmethod
    def get_dfu_control(test_case, padding=None):
        """
        Get DFU control information.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param padding: The padding part of the request. If None, it will not be used. This parameter is ignored if the
                        request is using register 0xF0 on a receiver - OPTIONAL
        :type padding: ``int`` or ``HexList``

        :return: The response of the get request
        :rtype: ``HidppMessage``
        """
        if test_case.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            if test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled:
                dfu_control_index, dfu_control_interface, device_index, port_index = \
                    DeviceBaseTestUtils.HIDppHelper.get_parameters(test_case=test_case,
                                                                   feature_id=SecureDfuControl.FEATURE_ID,
                                                                   factory=SecureDfuControlFactory)
                get_dfu_control_class = dfu_control_interface.get_dfu_control_cls
                get_dfu_control_response_class = dfu_control_interface.get_dfu_control_response_cls
            elif test_case.f.PRODUCT.FEATURES.COMMON.DFU_CONTROL.F_Enabled:
                dfu_control_index, dfu_control_interface, device_index, port_index = \
                    DeviceBaseTestUtils.HIDppHelper.get_parameters(test_case=test_case,
                                                                   feature_id=DfuControl.FEATURE_ID,
                                                                   factory=DfuControlFactory)
                get_dfu_control_class = dfu_control_interface.get_dfu_status_cls
                get_dfu_control_response_class = dfu_control_interface.get_dfu_status_response_cls
            else:
                raise ValueError('Dfu Control Feature not enabled in test configuration')
            # end if
            get_dfu_control = get_dfu_control_class(device_index=device_index, feature_index=dfu_control_index)

            if padding is not None:
                get_dfu_control.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=get_dfu_control,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_dfu_control_response_class)
        elif test_case.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            if test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled:
                get_dfu_control = GetDfuControlRequest()
                get_dfu_control_response_class = GetDfuControlResponse

                if padding is not None:
                    get_dfu_control.padding = padding
                # end if
            else:
                get_dfu_control = GetEnterUpgradeModeRequest()
                get_dfu_control_response_class = GetEnterUpgradeModeResponse
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=get_dfu_control,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=get_dfu_control_response_class)
        else:
            raise ValueError(f'Unknown target configuration: {test_case.config_manager.current_target}')
        # end if
    # end def get_dfu_control

    @staticmethod
    @aliased(enable_dfu='enter_dfu')
    def set_dfu_control(test_case, enter_dfu=None, dfu_control_param=None,
                        dfu_magic_key=None, reserved_enable_dfu=None, reserved=None, padding=None, action_type=None):
        """
        Set DFU control to enable or disable DFU. If the one used is 0x00C2 (or 0x00C3 with action_typ = no action,
        device only) or 0xF0 (receiver only), None can be returned instead or the response.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param enter_dfu: Enable or disable DFU mode. If None, True will be used. This parameter is ignored if the
                          request is using register 0xF0 on a receiver - OPTIONAL
        :type enter_dfu: ``int`` or ``bool``
        :param dfu_control_param: The DFU control parameter. If None, 0 will be used. This will only be used for a
                                  device using HID++2.0, if not this parameter is ignored - OPTIONAL
        :type dfu_control_param: ``int``
        :param dfu_magic_key: The DFU Magic Key. If None, the right one for each command will be used - OPTIONAL
        :type dfu_magic_key: ``int`` or ``HexList``
        :param reserved_enable_dfu: The reserved part in the DFU control part. If None, it will not be used. This
                                    parameter is ignored if no action is required to enter DFU - OPTIONAL
        :type reserved_enable_dfu: ``int``
        :param reserved: The reserved part of the request. If None, it will not be used. This parameter is ignored if
                         the request is using register 0xF0 on a receiver - OPTIONAL
        :type padding: ``int`` or ``HexList``
        :param padding: The padding part of the request. If None, it will not be used. This parameter is ignored if the
                        request is using register 0xF0 on a receiver - OPTIONAL
        :type padding: ``int`` or ``HexList``
        :param action_type: The action type used in the device. If None, the one in the setting file will be used.
                        This parameter is ignored if the request is using register 0xF0 or feature 0x00C2 - OPTIONAL
        :type action_type: ``int`` or ``HexList``

        :return: The response of the set request, can be None is no response expected
        :rtype: ``HidppMessage``
        """
        if action_type is None:
            action_type = to_int(test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType)
        elif not isinstance(action_type, int):
            action_type = to_int(action_type)
        # end if

        if test_case.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            if test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled:
                dfu_control_index, dfu_control_interface, device_index, port_index = \
                    DeviceBaseTestUtils.HIDppHelper.get_parameters(test_case=test_case,
                                                                   feature_id=SecureDfuControl.FEATURE_ID,
                                                                   factory=SecureDfuControlFactory)
                set_dfu_control_class = dfu_control_interface.set_dfu_control_cls
                set_dfu_control_response_class = dfu_control_interface.set_dfu_control_response_cls
            elif test_case.f.PRODUCT.FEATURES.COMMON.DFU_CONTROL.F_Enabled:
                dfu_control_index, dfu_control_interface, device_index, port_index = \
                    DeviceBaseTestUtils.HIDppHelper.get_parameters(test_case=test_case,
                                                                   feature_id=DfuControl.FEATURE_ID,
                                                                   factory=DfuControlFactory)
                set_dfu_control_class = dfu_control_interface.start_dfu_cls
                set_dfu_control_response_class = dfu_control_interface.start_dfu_response_cls
            else:
                raise ValueError('Dfu Control Feature not enabled in test configuration')
            # end if

            set_dfu_control = set_dfu_control_class(
                device_index=device_index,
                feature_index=dfu_control_index,
                enter_dfu=enter_dfu if enter_dfu is not None else True,
                dfu_control_param=dfu_control_param if dfu_control_param is not None else 0,
                dfu_magic_key=dfu_magic_key if dfu_magic_key is not None else
                set_dfu_control_class.DEFAULT.DFU_MAGIC_KEY)

            if reserved_enable_dfu is not None:
                set_dfu_control.reserved_enable_dfu = reserved_enable_dfu
            # end if

            if reserved is not None:
                set_dfu_control.reserved = reserved
            # end if

            if padding is not None:
                set_dfu_control.padding = padding
            # end if

            if (dfu_magic_key is None or dfu_magic_key == set_dfu_control_class.DEFAULT.DFU_MAGIC_KEY) and \
                    (test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled or dfu_control_param is None or
                     dfu_control_param == 0) and \
                    (test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled or
                     test_case.f.PRODUCT.FEATURES.COMMON.DFU_CONTROL.F_NotAvailable == 0):
                if (test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled and
                        action_type != dfu_control_interface.get_dfu_control_response_cls.ACTION.NO_ACTION):
                    return ChannelUtils.send(
                        test_case=test_case,
                        report=set_dfu_control,
                        response_queue_name=HIDDispatcher.QueueName.COMMON,
                        response_class_type=set_dfu_control_response_class)
                else:
                    try:
                        ChannelUtils.send_only(test_case=test_case, report=set_dfu_control)
                    except TransportContextException as e:
                        if e.get_cause() not in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                                 TransportContextException.Cause.CONTEXT_ERROR_IO,
                                                 TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                            raise
                        # end if
                    # end try

                    # According to the specification, a response could be sent but not necessarily:
                    # "This command may not return a response. If it does, the response is empty
                    # (all bytes set to zero)."
                    response = None
                    try:
                        response = ChannelUtils.get_only(
                            test_case=test_case,
                            queue_name=HIDDispatcher.QueueName.COMMON,
                            class_type=set_dfu_control_response_class,
                            timeout=.5,
                            check_first_message=False,
                            allow_no_message=True)
                    except ChannelException as e:
                        if e.get_cause() != ChannelException.Cause.DEVICE_NOT_CONNECTED:
                            raise
                        # end if
                    # end try

                    return response
                # end if
            else:
                return ChannelUtils.send(
                    test_case=test_case,
                    report=set_dfu_control,
                    response_queue_name=HIDDispatcher.QueueName.ERROR,
                    response_class_type=ErrorCodes)
            # end if
        elif test_case.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            if test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled:
                set_dfu_control = SetDfuControlRequest(
                    enable_dfu=enter_dfu if enter_dfu is not None else True,
                    dfu_magic_key=dfu_magic_key if dfu_magic_key is not None else
                    SetDfuControlRequest.DEFAULT.DFU_MAGIC_KEY)

                if reserved_enable_dfu is not None:
                    set_dfu_control.reserved_enable_dfu = reserved_enable_dfu
                # end if

                if reserved is not None:
                    set_dfu_control.reserved = reserved
                # end if

                if padding is not None:
                    set_dfu_control.padding = padding
                # end if

                if action_type != GetDfuControlResponse.ACTION.NO_ACTION:
                    if dfu_magic_key is None or dfu_magic_key == SetDfuControlRequest.DEFAULT.DFU_MAGIC_KEY:
                        return ChannelUtils.send(
                            test_case=test_case,
                            report=set_dfu_control,
                            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                            response_class_type=SetDfuControlResponse)
                    else:
                        return ChannelUtils.send(
                            test_case=test_case,
                            report=set_dfu_control,
                            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                            response_class_type=Hidpp1ErrorCodes)
                    # end if
                else:
                    try:
                        ChannelUtils.send_only(test_case=test_case, report=set_dfu_control)
                    except TransportContextException as e:
                        if e.get_cause() not in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                                 TransportContextException.Cause.CONTEXT_ERROR_IO,
                                                 TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                            raise
                        # end if
                    # end try
                    sleep(.4)
                    return None
                # end if
            else:
                # According to the specification, no response is sent:
                # "No response, command timeout !"
                write_upgrade_mode = SetEnterUpgradeModeRequest(
                    key=dfu_magic_key if dfu_magic_key is not None else ENTER_USB_UPGRADE_KEY)

                try:
                    ChannelUtils.send_only(test_case=test_case, report=write_upgrade_mode)
                except TransportContextException as e:
                    if e.get_cause() not in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                             TransportContextException.Cause.CONTEXT_ERROR_IO,
                                             TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                        raise
                    # end if
                # end try
                sleep(.4)
                return None
            # end if
        else:
            raise ValueError(f'Unknown target configuration: {test_case.config_manager.current_target}')
        # end if
    # end def set_dfu_control

    @staticmethod
    def target_enter_into_dfu_mode(test_case, action_type=None, check_device_reconnection=True):
        """
        Method to make a target enter into DFU mode

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param action_type: The action type required. If None, it will be taken from
                            PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType - OPTIONAL
        :type action_type: ``int`` or ``None``
        :param check_device_reconnection: Flag indicating to wait for the device to reconnect - OPTIONAL
        :type check_device_reconnection: ``bool``
        """
        if action_type in [None, '']:
            action_type = test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType
        # end if

        DfuControlTestUtils.set_dfu_control(test_case=test_case, enter_dfu=1)

        if test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled and \
                action_type != GetDfuControlResponseV0.ACTION.NO_ACTION:
            # Retrieve DFU control information.
            get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=test_case)
            # Monitor enterDfu parameter
            loop_count = 0
            while (to_int(get_dfu_control_response.enable_dfu) == 0 and loop_count <
                   DfuControlTestUtils.ENTER_DFU_LOOP_MAX_COUNTER):
                # Enter DFU retry mechanism
                DfuControlTestUtils.set_dfu_control(test_case=test_case, enter_dfu=1)
                get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=test_case)

                loop_count += 1
            # end while

            if to_int(get_dfu_control_response.enable_dfu) != 1:
                raise ValueError(f'Could not manage to enable DFU mode even after '
                                 f'{DfuControlTestUtils.ENTER_DFU_LOOP_MAX_COUNTER} tries')
            # end if
        # end if

        DfuControlTestUtils.perform_action_to_enter_dfu_mode(
            test_case=test_case, action_type=action_type, check_device_reconnection=check_device_reconnection)
    # end def target_enter_into_dfu_mode

    @staticmethod
    def perform_action_to_enter_dfu_mode(test_case, action_type=None, action_data=None, ignore_action_index=None,
                                         add_user_actions=0, force_soft_reset=False, dfu_enabled=True,
                                         device_reset_feature_id=None, check_device_reconnection=True):
        """
        Perform the user action(s) required to enter DFU mode. If DFU control is not secure or if the action type is
        NO_ACTION (0), nothing will be done.
        This method is used for the tests for the features Secure DFU (0x00C3/0xF5). This is why some optional
        parameters that are there only to not enter DFU mode: ignore_action_index, force_soft_reset, dfu_enabled,
        device_reset_feature_id.
        If this function is to used as a utils function and not to tests different configuration the only 3
        parameters that matters: test_case (MANDATORY), action_type (OPTIONAL) and action_data (OPTIONAL).

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param action_type: The action type required. If None, it will be taken from
                            PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType - OPTIONAL
        :type action_type: ``int`` or ``HexList``
        :param action_data: The list of actions to do. If None, it will be taken from
                            PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionData - OPTIONAL
        :type action_data: ``list of int`` or ``int`` or ``HexList`` or ``bytes``
        :param ignore_action_index: The index(es) to ignore in the list of user actions to do. It will be used only
                                    with action types that need more user action than just off/on. This will
                                    only be used for a device, if not this parameter is ignored - OPTIONAL
        :type ignore_action_index: ``int`` or ``list of int``
        :param add_user_actions: Number of user actions to add to the one listed in action_data. This will
                                 only be used for a device, if not this parameter is ignored - OPTIONAL
        :type add_user_actions: ``int``
        :param force_soft_reset: Force the use of a soft reset instead of a hard reset - OPTIONAL
        :type force_soft_reset: ``bool``
        :param dfu_enabled: Has the DFU been enabled before performing the actions. This will only be used if Secure
                            DFU is used - OPTIONAL
        :type dfu_enabled: ``bool``
        :param device_reset_feature_id: If not None, it will be used to send a ForceReset (0x1802) instead of the
                                        hard reset - OPTIONAL
        :type device_reset_feature_id: ``int``
        :param check_device_reconnection: Does it wait for the device to reconnect or not - OPTIONAL
        :type check_device_reconnection: ``bool``
        """
        if action_type is None:
            action_type = to_int(test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType)
        elif isinstance(action_type, HexList):
            action_type = to_int(action_type)
        # end if

        if not test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled or \
                action_type == GetDfuControlResponseV0.ACTION.NO_ACTION:
            # 0 - No action required.
            # Verify the communication disconnection then reconnection
            # This distinction is only to be done here because this part will happen for all protocols except Unifying.
            # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it would be
            #  interesting to investigate a better solution
            if test_case.config_manager.current_protocol not in LogitechProtocol.unifying_protocols() and \
                    check_device_reconnection:
                DfuTestUtils.verify_communication_disconnection_then_reconnection(
                    test_case=test_case,
                    ble_service_changed_required=test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled)
            # end if
        else:
            if test_case.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
                # All the device connection event must be cleaned to get only the ones associated to the restart
                ChannelUtils.clean_messages(test_case=test_case,
                                            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                                            class_type=DeviceConnection)
            # end if

            # Extract the control actions to perform during the device reset
            if action_type == GetDfuControlResponseV0.ACTION.OFF_ON:
                if test_case.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER and \
                        test_case.debugger is None and LibusbDriver.discover_usb_hub():
                    port_index = ChannelUtils.get_port_index(test_case=test_case)
                    test_case.channel_disable(usb_port_index=port_index)
                    test_case.channel_enable(usb_port_index=port_index)
                elif (device_reset_feature_id is None or
                      test_case.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER):
                    if test_case.config_manager.current_protocol == LogitechProtocol.USB and \
                            test_case.current_channel.is_open:
                        ChannelUtils.close_channel(test_case=test_case)
                    # end if
                    # Device Off/On required or Receiver/corded device unplug/replug required.
                    # A soft reset can be tested
                    assert test_case.debugger is not None, "Cannot perform reset if debugger is not present"
                    test_case.debugger.reset(soft_reset=force_soft_reset)
                else:
                    force_device_reset = ForceDeviceReset(
                        deviceIndex=ChannelUtils.get_device_index(test_case=test_case),
                        featureId=device_reset_feature_id)
                    try:
                        ChannelUtils.send_only(test_case=test_case, report=force_device_reset)
                    except TransportContextException as e:
                        if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                             TransportContextException.Cause.CONTEXT_ERROR_IO,
                                             TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                            pass
                        else:
                            raise
                        # end if
                    # end try
                    # Check Error code message queue is empty
                    ChannelUtils.check_queue_empty(test_case=test_case,
                                                   queue_name=HIDDispatcher.QueueName.ERROR,
                                                   timeout=.4)
                    ChannelUtils.check_queue_empty(test_case=test_case,
                                                   queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                                                   timeout=.4)
                # end if

                if test_case.config_manager.current_protocol not in LogitechProtocol.unifying_protocols() and \
                        check_device_reconnection:
                    # Verify the communication disconnection then reconnection
                    DfuTestUtils.verify_communication_disconnection_then_reconnection(
                        test_case=test_case,
                        ble_service_changed_required=(not force_soft_reset and
                                                      device_reset_feature_id is None and
                                                      dfu_enabled))
                # end if
            elif (action_type == GetDfuControlResponseV0.ACTION.OFF_ON_KBD_KEYS
                  or action_type == GetDfuControlResponseV0.ACTION.OFF_ON_MSE_CLICKS):
                # For now the action types that require more user actions than just off/on are only for devices
                if action_data is None:
                    action_data = list(to_int(
                      test_case.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionData).to_bytes(3, "big"))
                elif isinstance(action_data, int):
                    action_data = list(action_data.to_bytes(3, "big"))
                elif isinstance(action_data, HexList):
                    action_data = list(action_data)
                # end if
                # 2 - Device Off/On required with up to three simultaneous keys pressed on the keyboard.
                # 3 - Device Off/On required with up to three simultaneous buttons pressed on the mouse.
                key_ids = [MOUSE_HID_USAGE_TO_KEY_ID_MAP[x]
                           if action_type == GetDfuControlResponseV0.ACTION.OFF_ON_MSE_CLICKS
                           else KEYBOARD_HID_USAGE_TO_KEY_ID_MAP[x] for x in action_data if x != 0]
                if ignore_action_index is not None:
                    if isinstance(ignore_action_index, int):
                        del key_ids[ignore_action_index]
                    elif isinstance(ignore_action_index, list):
                        for index_to_ignore in ignore_action_index:
                            del key_ids[index_to_ignore]
                        # end for
                    else:
                        test_case.log_warning(
                            message=f"Unknown ignore_action_index parameter type: {type(ignore_action_index)}")
                    # end if
                # end if

                if add_user_actions > 0:
                    hid_usage_to_key_id_map = MOUSE_HID_USAGE_TO_KEY_ID_MAP if action_type == \
                        GetDfuControlResponseV0.ACTION.OFF_ON_MSE_CLICKS else KEYBOARD_HID_USAGE_TO_KEY_ID_MAP
                    hid_usage_map_key_list = list(hid_usage_to_key_id_map.keys())
                    hid_usage_map_key_list.sort()
                    while add_user_actions > 0:
                        action_to_add = None
                        for hid_usage_map_key in hid_usage_map_key_list:
                            # Parse the map in sorted manner to get the first key not already used
                            if hid_usage_to_key_id_map[hid_usage_map_key] not in key_ids:
                                action_to_add = hid_usage_to_key_id_map[hid_usage_map_key]
                                break
                            # end if
                        # end for

                        assert action_to_add is not None, f"Could not find an action to add, action left to find " \
                                                          f"(this failed one included) = {add_user_actions}"

                        key_ids.append(action_to_add)
                        add_user_actions -= 1
                    # end while
                # end if

                test_case.button_stimuli_emulator.multiple_keys_press(key_ids)

                # After the reset there is a wait for 
                if device_reset_feature_id is None:
                    # Device Off/On required or Receiver/corded device unplug/replug required.
                    test_case.device_debugger.reset(soft_reset=force_soft_reset)
                else:
                    force_device_reset = ForceDeviceReset(
                        deviceIndex=ChannelUtils.get_device_index(test_case=test_case),
                        featureId=device_reset_feature_id)
                    try:
                        ChannelUtils.send_only(test_case=test_case, report=force_device_reset)
                    except TransportContextException as e:
                        if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                             TransportContextException.Cause.CONTEXT_ERROR_IO,
                                             TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                            pass
                        else:
                            raise
                        # end if
                    # end try
                    # Check Error code message queue is empty
                    ChannelUtils.check_queue_empty(test_case=test_case,
                                                   queue_name=HIDDispatcher.QueueName.ERROR,
                                                   timeout=.4)
                    ChannelUtils.check_queue_empty(test_case=test_case,
                                                   queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                                                   timeout=.4)
                # end if

                if check_device_reconnection:
                    # Verify the communication disconnection then reconnection
                    DfuTestUtils.verify_communication_disconnection_then_reconnection(
                        test_case=test_case,
                        ble_service_changed_required=(not force_soft_reset and
                                                      ignore_action_index is None and
                                                      dfu_enabled and
                                                      device_reset_feature_id is None))
                    test_case.button_stimuli_emulator.multiple_keys_release(key_ids)
                # end if
            # end if
            elif action_type == GetDfuControlResponseV1.ACTION.ON_SCREEN_CONFIRMATION:
                # Action Data is ignored at the moment by the implementation.
                test_case.button_stimuli_emulator.keystroke(
                    test_case.button_stimuli_emulator.keyword_key_ids["enter_dfu_action"])

                # Check Error code message queue is empty
                ChannelUtils.check_queue_empty(test_case=test_case,
                                               queue_name=HIDDispatcher.QueueName.ERROR,
                                               timeout=.4)
                ChannelUtils.check_queue_empty(test_case=test_case,
                                               queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                                               timeout=.4)

                if check_device_reconnection:
                    # Verify the communication disconnection then reconnection
                    DfuTestUtils.verify_communication_disconnection_then_reconnection(
                        test_case=test_case)
                # end if
        # end if
    # end def perform_action_to_enter_dfu_mode
# end class DfuControlTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
