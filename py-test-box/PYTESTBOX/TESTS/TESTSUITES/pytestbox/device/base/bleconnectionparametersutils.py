#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.bleconnectionparametersutils
:brief:  Helpers for BLE Connection Parameters (applicable to device targets only)
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/11/22
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.logiconstants import LogitechBleConnectionParameters
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndName
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytransport.ble.bleinterfaceclasses import BleGapConnectionParameters
from pytransport.ble.bleinterfaceclasses import BleGapConnectionParametersRange


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BleConnectionParametersTestUtils(DeviceBaseTestUtils):
    """
    Test utils for BLE Connection Parameters (applicable to device targets only)
    """
    VALIDITY_RANGE_MS = 500
    CONNECTION_INTERVAL_GRANULARITY = 1.25
    RCI_MIN = 7.5
    SUPERVISION_TIMEOUT_GRANULARITY = 10
    SLAVE_LATENCY_GRANULARITY = 1
    MIN_CONNECTION_INTERVAL_EXTENDED_RANGE = 7.5
    MAX_2BYTES = (2 ** 16) - 1
    CONNECTION_INTERVAL_ABSOLUTE_MAX = MAX_2BYTES * CONNECTION_INTERVAL_GRANULARITY
    SUPERVISION_TIMEOUT_ABSOLUTE_MAX = MAX_2BYTES * SUPERVISION_TIMEOUT_GRANULARITY
    SLAVE_LATENCY_ABSOLUTE_MAX = MAX_2BYTES * SLAVE_LATENCY_GRANULARITY

    @staticmethod
    def get_default_os_connection_parameters(test_case):
        """
        Get the default OS (any OS but iOS/iPadOS) connection parameters. It will be different if the device is a
        pointer (Mouse, Presenter, Gamepad, Touchpad) or a keyboard.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The BLE requested connection parameters
        :rtype: ``BleGapConnectionParameters``

        :raise ``RuntimeError``: if an unknown device type is defined in the HID++ 0x0005 feature test settings
        """
        if test_case.f.PRODUCT.PROTOCOLS.BLE.CONNECTION_PARAMETERS.F_OverrideDefaultOS:
            return BleGapConnectionParameters(
                min_connection_interval=
                    test_case.f.PRODUCT.PROTOCOLS.BLE.CONNECTION_PARAMETERS.F_DefaultOSMinConnectionInterval,
                max_connection_interval=
                    test_case.f.PRODUCT.PROTOCOLS.BLE.CONNECTION_PARAMETERS.F_DefaultOSMaxConnectionInterval,
                supervision_timeout=
                    test_case.f.PRODUCT.PROTOCOLS.BLE.CONNECTION_PARAMETERS.F_DefaultOSSupervisionTimeout,
                slave_latency=test_case.f.PRODUCT.PROTOCOLS.BLE.CONNECTION_PARAMETERS.F_DefaultOSSlaveLatency)
        elif test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType == DeviceTypeAndName.TYPE.KEYBOARD:
            return BleGapConnectionParameters(
                min_connection_interval=LogitechBleConnectionParameters.DEFAULT_OS_KEYBOARD_CONNECTION_INTERVAL_MIN_MS,
                max_connection_interval=LogitechBleConnectionParameters.DEFAULT_OS_KEYBOARD_CONNECTION_INTERVAL_MAX_MS,
                supervision_timeout=LogitechBleConnectionParameters.DEFAULT_OS_KEYBOARD_SUPERVISION_TIMEOUT_MS,
                slave_latency=LogitechBleConnectionParameters.DEFAULT_OS_KEYBOARD_SLAVE_LATENCY)
        elif test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType in [
                DeviceTypeAndName.TYPE.MOUSE, DeviceTypeAndName.TYPE.PRESENTER, DeviceTypeAndName.TYPE.TRACKPAD,\
                DeviceTypeAndName.TYPE.DIAL]:
            return BleGapConnectionParameters(
                min_connection_interval=LogitechBleConnectionParameters.DEFAULT_OS_POINTER_CONNECTION_INTERVAL_MIN_MS,
                max_connection_interval=LogitechBleConnectionParameters.DEFAULT_OS_POINTER_CONNECTION_INTERVAL_MAX_MS,
                supervision_timeout=LogitechBleConnectionParameters.DEFAULT_OS_POINTER_SUPERVISION_TIMEOUT_MS,
                slave_latency=LogitechBleConnectionParameters.DEFAULT_OS_POINTER_SLAVE_LATENCY)
        else:
            device_type = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType
            if device_type in DeviceTypeAndName.TYPE:
                device_type = DeviceTypeAndName.TYPE(device_type)
            # end if
            raise RuntimeError(f"Unknown device type for connection parameters: {device_type}")
        # end if
    # end def get_default_os_connection_parameters

    @classmethod
    def get_default_os_supervision_timeout_valid_range(cls, test_case):
        """
        Get the default OS (any OS but iOS/iPadOS) supervision timeout valid range. It will be different if the
        device is a pointer (Mouse, Presenter, Gamepad, Touchpad) or a keyboard.

        This is according to the spec Section 2.1.2, see: https://spaces.logitech.com/x/8g7oCQ

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The minimum and maximum values of the valid range
        :rtype: ``tuple[int, int]``

        :raise ``RuntimeError``: if an unknown device type is defined in the HID++ 0x0005 feature test settings
        """
        if test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType == DeviceTypeAndName.TYPE.KEYBOARD:
            return LogitechBleConnectionParameters.DEFAULT_OS_KEYBOARD_SUPERVISION_TIMEOUT_MS - cls.VALIDITY_RANGE_MS,\
                   LogitechBleConnectionParameters.DEFAULT_OS_KEYBOARD_SUPERVISION_TIMEOUT_MS + cls.VALIDITY_RANGE_MS
        elif test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType in [
                DeviceTypeAndName.TYPE.MOUSE, DeviceTypeAndName.TYPE.PRESENTER, DeviceTypeAndName.TYPE.GAMEPAD,
                DeviceTypeAndName.TYPE.TRACKPAD,DeviceTypeAndName.TYPE.DIAL]:
            return LogitechBleConnectionParameters.DEFAULT_OS_POINTER_SUPERVISION_TIMEOUT_MS - cls.VALIDITY_RANGE_MS,\
                   LogitechBleConnectionParameters.DEFAULT_OS_POINTER_SUPERVISION_TIMEOUT_MS + cls.VALIDITY_RANGE_MS
        else:
            device_type = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType
            if device_type in DeviceTypeAndName.TYPE:
                device_type = DeviceTypeAndName.TYPE(device_type)
            # end if
            raise RuntimeError(f"Unknown device type for connection parameters: {device_type}")
        # end if
    # end def get_default_os_supervision_timeout_valid_range

    @classmethod
    def get_default_os_slave_latency_valid_range(cls, test_case, connection_interval=None):
        """
        Get the default OS (any OS but iOS/iPadOS) slave latency valid range. It will be different if the
        device is a pointer (Mouse, Presenter, Gamepad, Touchpad) or a keyboard.

        This is according to the spec Section 2.1.1, see: https://spaces.logitech.com/x/8g7oCQ

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param connection_interval: The connection interval used. If it is ``None``, the maximum of its valid range
                                    will be used - OPTIONAL
        :type connection_interval: ``int`` or ``float``

        :return: The minimum and maximum values of the valid range
        :rtype: ``tuple[int, int]``

        :raise ``RuntimeError``: if an unknown device type is defined in the HID++ 0x0005 feature test settings
        """
        if test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType == DeviceTypeAndName.TYPE.KEYBOARD:
            sl = LogitechBleConnectionParameters.DEFAULT_OS_KEYBOARD_SLAVE_LATENCY
            rci_max = LogitechBleConnectionParameters.DEFAULT_OS_KEYBOARD_CONNECTION_INTERVAL_MAX_MS
            min_valid_value = \
                LogitechBleConnectionParameters.DEFAULT_OS_KEYBOARD_SLAVE_LATENCY - cls.SLAVE_LATENCY_GRANULARITY
        elif test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType in [
                DeviceTypeAndName.TYPE.MOUSE, DeviceTypeAndName.TYPE.PRESENTER, DeviceTypeAndName.TYPE.GAMEPAD,\
                DeviceTypeAndName.TYPE.TRACKPAD,DeviceTypeAndName.TYPE.DIAL]:
            sl = LogitechBleConnectionParameters.DEFAULT_OS_POINTER_SLAVE_LATENCY
            rci_max = LogitechBleConnectionParameters.DEFAULT_OS_POINTER_CONNECTION_INTERVAL_MAX_MS
            min_valid_value = \
                LogitechBleConnectionParameters.DEFAULT_OS_POINTER_SLAVE_LATENCY - cls.SLAVE_LATENCY_GRANULARITY
        else:
            device_type = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType
            if device_type in DeviceTypeAndName.TYPE:
                device_type = DeviceTypeAndName.TYPE(device_type)
            # end if
            raise RuntimeError(f"Unknown device type for connection parameters: {device_type}")
        # end if

        ci = connection_interval if connection_interval is not None else rci_max
        max_valid_value = int((((sl * ci) + (max(min(ci, rci_max), cls.RCI_MIN)) / 2) / max(
            min(ci, rci_max), cls.RCI_MIN)) + 1)
        return min_valid_value, max_valid_value
    # end def get_default_os_slave_latency_valid_range

    @staticmethod
    def get_ios_ipados_connection_parameters(test_case):
        """
        Get the iOS/iPadOS connection parameters. NB: They have an identical value whether it is a pointer
        (Mouse, Presenter, Gamepad, Touchpad) or a keyboard.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The BLE requested connection parameters
        :rtype: ``BleGapConnectionParameters``

        :raise ``RuntimeError``: if an unknown device type is defined in the HID++ 0x0005 feature test settings
        """
        if test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType in [
                DeviceTypeAndName.TYPE.MOUSE, DeviceTypeAndName.TYPE.PRESENTER, DeviceTypeAndName.TYPE.GAMEPAD,
                DeviceTypeAndName.TYPE.TRACKPAD, DeviceTypeAndName.TYPE.KEYBOARD]:
            return BleGapConnectionParameters(
                min_connection_interval=LogitechBleConnectionParameters.IOS_IPADOS_CONNECTION_INTERVAL_MIN_MS,
                max_connection_interval=LogitechBleConnectionParameters.IOS_IPADOS_CONNECTION_INTERVAL_MAX_MS,
                supervision_timeout=LogitechBleConnectionParameters.IOS_IPADOS_SUPERVISION_TIMEOUT_MS,
                slave_latency=LogitechBleConnectionParameters.IOS_IPADOS_SLAVE_LATENCY)
        else:
            device_type = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType
            if device_type in DeviceTypeAndName.TYPE:
                device_type = DeviceTypeAndName.TYPE(device_type)
            # end if
            raise RuntimeError(f"Unknown device type for connection parameters: {device_type}")
        # end if
    # end def get_ios_ipados_connection_parameters

    @classmethod
    def get_ios_ipados_supervision_timeout_valid_range(cls, test_case):
        """
        Get the iOS/iPadOS supervision timeout valid range. NB: They have an identical value whether it is a pointer
        (Mouse, Presenter, Gamepad, Touchpad) or a keyboard.

        This is according to the spec Section 2.1.2, see: https://spaces.logitech.com/x/8g7oCQ

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The minimum and maximum values of the valid range
        :rtype: ``tuple[int, int]``

        :raise ``RuntimeError``: if an unknown device type is defined in the HID++ 0x0005 feature test settings
        """
        if test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType in [
                DeviceTypeAndName.TYPE.MOUSE, DeviceTypeAndName.TYPE.PRESENTER, DeviceTypeAndName.TYPE.GAMEPAD,
                DeviceTypeAndName.TYPE.TRACKPAD, DeviceTypeAndName.TYPE.KEYBOARD,DeviceTypeAndName.TYPE.DIAL]:
            return LogitechBleConnectionParameters.IOS_IPADOS_SUPERVISION_TIMEOUT_MS - cls.VALIDITY_RANGE_MS,\
                   LogitechBleConnectionParameters.IOS_IPADOS_SUPERVISION_TIMEOUT_MS + cls.VALIDITY_RANGE_MS
        else:
            device_type = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType
            if device_type in DeviceTypeAndName.TYPE:
                device_type = DeviceTypeAndName.TYPE(device_type)
            # end if
            raise RuntimeError(f"Unknown device type for connection parameters: {device_type}")
        # end if
    # end def get_ios_ipados_supervision_timeout_valid_range

    @classmethod
    def get_ios_ipados_slave_latency_valid_range(cls, test_case, connection_interval=None):
        """
        Get the iOS/iPadOS slave latency valid range. Get the iOS/iPadOS connection parameters. NB: They have an
        identical value whether it is a pointer (Mouse, Presenter, Gamepad, Touchpad) or a keyboard.

        This is according to the spec Section 2.1.1, see: https://spaces.logitech.com/x/8g7oCQ

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param connection_interval: The connection interval used. If it is ``None``, the maximum of its valid range
                                    will be used - OPTIONAL
        :type connection_interval: ``int`` or ``float``

        :return: The minimum and maximum values of the valid range
        :rtype: ``tuple[int, int]``

        :raise ``RuntimeError``: if an unknown device type is defined in the HID++ 0x0005 feature test settings
        """
        if test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType in [
                DeviceTypeAndName.TYPE.MOUSE, DeviceTypeAndName.TYPE.PRESENTER, DeviceTypeAndName.TYPE.GAMEPAD,
                DeviceTypeAndName.TYPE.TRACKPAD, DeviceTypeAndName.TYPE.KEYBOARD,DeviceTypeAndName.TYPE.DIAL]:
            sl = LogitechBleConnectionParameters.IOS_IPADOS_SLAVE_LATENCY
            rci_max = LogitechBleConnectionParameters.IOS_IPADOS_CONNECTION_INTERVAL_MAX_MS
            min_valid_value = LogitechBleConnectionParameters.IOS_IPADOS_SLAVE_LATENCY - cls.SLAVE_LATENCY_GRANULARITY
        else:
            device_type = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType
            if device_type in DeviceTypeAndName.TYPE:
                device_type = DeviceTypeAndName.TYPE(device_type)
            # end if
            raise RuntimeError(f"Unknown device type for connection parameters: {device_type}")
        # end if

        ci = connection_interval if connection_interval is not None else rci_max
        max_valid_value = int((((sl * ci) + (max(min(ci, rci_max), cls.RCI_MIN)) / 2) / max(
            min(ci, rci_max), cls.RCI_MIN)) + 1)
        return min_valid_value, max_valid_value
    # end def get_ios_ipados_slave_latency_valid_range

    @staticmethod
    def get_bootloader_connection_parameters(test_case):
        """
        Get the Bootloader connection parameters. NB: They have an identical value whether it is a pointer
        (Mouse, Presenter, Gamepad, Touchpad) or a keyboard.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The BLE requested connection parameters
        :rtype: ``BleGapConnectionParameters``

        :raise ``RuntimeError``: if an unknown device type is defined in the HID++ 0x0005 feature test settings
        """
        if test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType in [
            DeviceTypeAndName.TYPE.MOUSE, DeviceTypeAndName.TYPE.PRESENTER, DeviceTypeAndName.TYPE.GAMEPAD,
            DeviceTypeAndName.TYPE.TRACKPAD, DeviceTypeAndName.TYPE.KEYBOARD]:
            return BleGapConnectionParameters(
                min_connection_interval=LogitechBleConnectionParameters.BOOTLOADER_CONNECTION_INTERVAL_MIN_MS,
                max_connection_interval=LogitechBleConnectionParameters.BOOTLOADER_CONNECTION_INTERVAL_MAX_MS,
                supervision_timeout=LogitechBleConnectionParameters.BOOTLOADER_SUPERVISION_TIMEOUT_MS,
                slave_latency=LogitechBleConnectionParameters.BOOTLOADER_SLAVE_LATENCY)
        else:
            device_type = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType
            if device_type in DeviceTypeAndName.TYPE:
                device_type = DeviceTypeAndName.TYPE(device_type)
            # end if
            raise RuntimeError(f"Unknown device type for connection parameters: {device_type}")
        # end if
    # end def get_bootloader_connection_parameters

    @classmethod
    def get_any_os_incorrect_connection_parameters(cls, test_case):
        """
        Get any OS incorrect connection parameters. NB: They have an identical value whether it is a pointer
        (Mouse, Presenter, Gamepad, Touchpad) or a keyboard.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The connection interval, supervision timeout and slave latency out of their valid ranges
        :rtype: ``BleGapConnectionParameters``
        """
        correct_parameters = BleConnectionParametersTestUtils.get_default_os_connection_parameters(test_case=test_case)
        incorrect_connection_interval = correct_parameters.max_connection_interval + cls.CONNECTION_INTERVAL_GRANULARITY
        incorrect_supervision_timeout = max(
            BleConnectionParametersTestUtils.get_default_os_supervision_timeout_valid_range(test_case=test_case)[1],
            BleConnectionParametersTestUtils.get_ios_ipados_supervision_timeout_valid_range(
                test_case=test_case)[1]) + cls.SUPERVISION_TIMEOUT_GRANULARITY
        incorrect_slave_latency = max(
            BleConnectionParametersTestUtils.get_default_os_slave_latency_valid_range(test_case=test_case)[1],
            BleConnectionParametersTestUtils.get_ios_ipados_slave_latency_valid_range(
                test_case=test_case)[1]) + cls.SLAVE_LATENCY_GRANULARITY
        return BleGapConnectionParameters(min_connection_interval=incorrect_connection_interval,
                                          max_connection_interval=incorrect_connection_interval,
                                          supervision_timeout=incorrect_supervision_timeout,
                                          slave_latency=incorrect_slave_latency)
    # end def get_any_os_incorrect_connection_parameters

    @classmethod
    def get_always_acceptable_host_range(cls):
        """
        Get a range of parameters the host accepts wider than any device should send

        :return: The connection interval, supervision timeout and slave latency ranges wider than their valid ranges
        :rtype: ``BleGapConnectionParameters``
        """
        # TODO put in constant
        return BleGapConnectionParametersRange(
            min_connection_interval=0,
            max_connection_interval=cls.CONNECTION_INTERVAL_ABSOLUTE_MAX,
            min_supervision_timeout=0,
            max_supervision_timeout=cls.SUPERVISION_TIMEOUT_ABSOLUTE_MAX,
            min_slave_latency=0,
            max_slave_latency=cls.SLAVE_LATENCY_ABSOLUTE_MAX
        )
    # end def get_always_acceptable_host_range

    @classmethod
    def get_slave_latency_valid_range(cls, connection_parameters, connection_interval=None, is_extended_range=False):
        """
        Get the slave latency valid range based on specific connection parameters.

        This is according to the spec Section 2.1.1, see: https://spaces.logitech.com/x/8g7oCQ

        :param connection_parameters: The connection parameters used as start point
        :type connection_parameters: ``BleGapConnectionParameters``
        :param connection_interval: The connection interval used. If it is ``None``, the maximum of its valid range
                                    will be used - OPTIONAL
        :type connection_interval: ``int`` or ``float`` or ``None``
        :param is_extended_range: Flag indicating the expected parameters are for extended range - OPTIONAL
        :type is_extended_range: ``bool``

        :return: The minimum and maximum values of the valid range
        :rtype: ``tuple[int, int]``
        """
        sl = connection_parameters.slave_latency
        rci_max = connection_parameters.max_connection_interval
        min_valid_value = connection_parameters.slave_latency - cls.SLAVE_LATENCY_GRANULARITY
        ci = connection_interval if connection_interval / cls.CONNECTION_INTERVAL_GRANULARITY is not None else rci_max
        rci_min = cls.RCI_MIN / cls.CONNECTION_INTERVAL_GRANULARITY

        if is_extended_range:
            max_valid_value = int(((sl * rci_max) + (ci / 2)) / ci)
            min_valid_value = max_valid_value
        else:
            max_valid_value = int((((sl * rci_max) + ((max(min(ci, rci_max), rci_min)) / 2)) / max(
                min(ci, rci_max), rci_min)) + 1)
        # end if
        return min_valid_value, max_valid_value
    # end def get_slave_latency_valid_range

    @classmethod
    def get_supervision_timeout_valid_range(cls, connection_parameters, is_extended_range=False):
        """
        Get the supervision timeout valid range based on specific connection parameters.

        This is according to the spec Section 2.1.1, see: https://spaces.logitech.com/x/8g7oCQ

        :param connection_parameters: The connection parameters used as start point
        :type connection_parameters: ``BleGapConnectionParameters``
        :param is_extended_range: Flag indicating the expected parameters are for extended range - OPTIONAL
        :type is_extended_range: ``bool``

        :return: The minimum and maximum values of the valid range
        :rtype: ``tuple[int, int]``
        """
        if is_extended_range:
            return connection_parameters.supervision_timeout, connection_parameters.supervision_timeout
        else:
            return connection_parameters.supervision_timeout - cls.VALIDITY_RANGE_MS, \
                   connection_parameters.supervision_timeout + cls.VALIDITY_RANGE_MS
        # end if

    # end def get_supervision_timeout_valid_range

    @classmethod
    def get_extended_range_recommended(cls, connection_parameters, connection_interval=None):
        """
        Get the extended range parameters based on specific recommended connection parameters.

        This is according to the spec Section 2.2, see: https://spaces.logitech.com/x/8g7oCQ

        :param connection_parameters: The connection parameters used as start point
        :type connection_parameters: ``BleGapConnectionParameters``
        :param connection_interval: The connection interval used. If it is ``None``, the minimum of extended range
                                    will be used - OPTIONAL
        :type connection_interval: ``int`` or ``float`` or ``None``

        :return: The connection interval, supervision timeout and slave latency recomanded for extended range
        :rtype: ``BleGapConnectionParameters``
        """
        ci = connection_interval if connection_interval is not None else cls.MIN_CONNECTION_INTERVAL_EXTENDED_RANGE
        rsl = connection_parameters.slave_latency
        rci_max = connection_parameters.max_connection_interval

        slave_latency = int((((rsl*rci_max)+(ci/2))/ci))

        return BleGapConnectionParameters(min_connection_interval=ci,
                                          max_connection_interval=ci,
                                          supervision_timeout=connection_parameters.supervision_timeout,
                                          slave_latency=slave_latency)
    # end def get_extended_range_recommended

# end class BleConnectionParametersTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
