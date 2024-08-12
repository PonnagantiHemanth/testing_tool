#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.ble_pro.interface
:brief: Validate Gatt Ble Pro services Interface test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/07/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.logiconstants import BleProAuthenticationValues
from pychannel.logiconstants import LogitechVendorUuid
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndName
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.ble.gatt.ble_pro.ble_pro import GattBleProApplicationTestCase
from pytestbox.device.ble.gatt.ble_pro.ble_pro import GattBleProBootloaderTestCase
from pytestbox.device.ble.gatt.ble_pro.ble_pro import GattBleProTestCase
from pytestbox.device.ble.gatt.ble_pro.ble_pro import attribute_value_format
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleinterfaceclasses import BleCharacteristicProperties
from pytransport.ble.bleinterfaceclasses import BleUuid
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sylvan Ieri"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattBleProInterfaceTestMixin(GattBleProTestCase):
    """
    Gatt BLE Pro Services Application mode Interface Test Cases
    """

    def _check_ble_pro_characteristics(self, mode):
        """
        Verify the properties, security level and default value of the characteristics
        of the Ble pro service in all mode

        :param: mode
        :type mode: ``DeviceInformation.EntityTypeV1``
        """
        self.gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.current_ble_device)
        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleUuid(BleUuidStandardService.LOGITECH_BLE_PRO))

        authentication_capability = 0

        if self.f.SHARED.DEVICES.F_PasskeyAuthMethod[0] == '1':
            authentication_capability |= BleProAuthenticationValues.KEYBOARD_PASSKEY
        # end if
        if self.f.SHARED.DEVICES.F_Passkey2ButtonsAuthMethod[0] == '1':
            authentication_capability |= BleProAuthenticationValues.TWO_BUTTONS_PASSKEY
        # end if

        # allow reporting 0 capability in bootloader
        if mode == DeviceInformation.EntityTypeV1.BOOTLOADER:
            authentication = [HexList(0), HexList(authentication_capability)]
        else:
            authentication = [HexList(authentication_capability)]
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Assume all device advertise support for HID latency suppression even if no effect "
                                 "(observed in reference devices)")
        # --------------------------------------------------------------------------------------------------------------
        attribute = attribute_value_format(suppressed_latency=True)

        if mode == DeviceInformation.EntityTypeV1.BOOTLOADER:
            device_type_val = Hidpp1Data.DeviceType.UNKNOWN
        else:
            device_type = self.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType

            if device_type == DeviceTypeAndName.TYPE.KEYBOARD:
                device_type_val = Hidpp1Data.DeviceType.KEYBOARD
            elif device_type == DeviceTypeAndName.TYPE.MOUSE:
                device_type_val = Hidpp1Data.DeviceType.MOUSE
            elif device_type == DeviceTypeAndName.TYPE.NUMPAD:
                device_type_val = Hidpp1Data.DeviceType.NUM_PAD
            elif device_type == DeviceTypeAndName.TYPE.PRESENTER:
                device_type_val = Hidpp1Data.DeviceType.PRESENTER
            elif device_type == DeviceTypeAndName.TYPE.REMOTECONTROL:
                device_type_val = Hidpp1Data.DeviceType.REMOTE_CONTROL
            elif device_type == DeviceTypeAndName.TYPE.TRACKBALL:
                device_type_val = Hidpp1Data.DeviceType.TRACK_BALL
            elif device_type == DeviceTypeAndName.TYPE.TRACKPAD:
                device_type_val = Hidpp1Data.DeviceType.TOUCH_PAD
            elif device_type == DeviceTypeAndName.TYPE.GAMEPAD:
                device_type_val = Hidpp1Data.DeviceType.GAME_PAD
            elif device_type == DeviceTypeAndName.TYPE.JOYSTICK:
                device_type_val = Hidpp1Data.DeviceType.JOYSTICK
            elif device_type == DeviceTypeAndName.TYPE.DIAL:
                device_type_val = Hidpp1Data.DeviceType.DIAL
            else:
                self.fail(f"Unknown device type {device_type}")
            # end if
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Assume product specific part of device information value is 0x00")
        # --------------------------------------------------------------------------------------------------------------
        device_information = HexList(device_type_val, 0x00)
        characteristics = {
            BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.BLE_PRO_SERVICE_INFORMATION_CHARACTERISTIC):
                (BleCharacteristicProperties(read=True), None, [HexList(0x10, 0x01), HexList(0x10,0x02)]),
            BleProtocolTestUtils.build_128_bits_uuid(
                LogitechVendorUuid.BLE_PRO_AUTHENTICATION_CAPABILITIES_CHARACTERISTIC):
                (BleCharacteristicProperties(read=True), None, authentication),
            BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.BLE_PRO_AUTHENTICATION_CONTROL_CHARACTERISTIC):
                (BleCharacteristicProperties(write=True), None, None),
            BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.BLE_PRO_DEVICE_INFORMATION_CHARACTERISTIC):
                (BleCharacteristicProperties(read=True), None, device_information),
            BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.BLE_PRO_ATTRIBUTE_CAPABILITY_CHARACTERISTIC):
                (BleCharacteristicProperties(read=True), None, attribute),
            BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.BLE_PRO_ATTRIBUTE_CONTROL_CHARACTERISTIC):
                (BleCharacteristicProperties(write=True), None, None),
        }
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)
    # end def _check_ble_pro_characteristics
# end class GattBleProInterfaceTestMixin


class GattBleProInterfaceApplicationTestCase(GattBleProApplicationTestCase, GattBleProInterfaceTestMixin):
    """
    Gatt BLE Pro Services Application mode Interface Application Test Cases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        GattBleProApplicationTestCase.setUp(self)
    # end def setUp

    @features('BLEProtocol')
    @features('BLEProProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_ble_pro_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics
        of the Ble Pro service in application mode
        """
        self._check_ble_pro_characteristics(DeviceInformation.EntityTypeV1.MAIN_APP)

        self.testCaseChecked("INT_GATT_BLE_PRO_0001", _AUTHOR)
    # end def test_ble_pro_characteristics
# end class GattBleProInterfaceApplicationTestCase


class GattBleProInterfaceBootloaderTestCase(GattBleProBootloaderTestCase, GattBleProInterfaceTestMixin):
    """
    Gatt BLE Pro Services Application mode Interface Test Cases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        GattBleProBootloaderTestCase.setUp(self)
    # end def setUp

    @features('BLEProtocol')
    @features('BLEProProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_ble_pro_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics
        of the GATT service in bootloader mode
        """
        self._check_ble_pro_characteristics(DeviceInformation.EntityTypeV1.BOOTLOADER)

        self.testCaseChecked("INT_GATT_BLE_PRO_0002", _AUTHOR)
    # end def test_ble_pro_characteristics
# end class GattBleProInterfaceBootloaderTestCase


# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
