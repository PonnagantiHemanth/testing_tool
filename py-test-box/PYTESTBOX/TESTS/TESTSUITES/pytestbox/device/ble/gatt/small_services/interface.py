#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.small_services.interface
:brief: Validate Gatt small services Interface test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/01/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.logiconstants import LogitechBleConnectionParameters
from pychannel.logiconstants import LogitechVendorUuid
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndName
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_endian_list
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import DEVICE_TYPE_TO_BLE_APPEARANCE
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.ble.gatt.small_services.small_services import GattSmallServiceApplicationTestCase
from pytestbox.device.ble.gatt.small_services.small_services import GattSmallServiceBootloaderTestCase
from pytransport.ble.bleconstants import BleAppearance
from pytransport.ble.bleconstants import BleMessageSize
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardDescriptor
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleconstants import GoogleFastPairCharacteristic
from pytransport.ble.bleinterfaceclasses import BleCharacteristicProperties
from pytransport.ble.bleinterfaceclasses import BleService
from pytransport.ble.bleinterfaceclasses import BleUuid

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"

FULL_BATTERY_VALUE = 100


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattSmallServiceInterfaceTestCaseMixin(DeviceBaseTestCase):
    """
    BLE OS Gatt Small Service Interface Test Cases common class
    """
    gatt_table: list

    def _check_presences(self, mode):
        """
        Check the presence of all expected services, characteristics and descriptors
        
        :param mode: indicate the expected device mode to use for the check
        :type mode: ``DeviceInformation.EntityTypeV1``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Gatt table read:\n{BleProtocolTestUtils.gatt_table_to_string(self.gatt_table)}")
        # --------------------------------------------------------------------------------------------------------------
        expected_services, optional_characteristics_services = self._build_expected_services(mode)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop on gatt table services")
        # --------------------------------------------------------------------------------------------------------------
        for service in self.gatt_table:
            self._check_service_presence(expected_services, optional_characteristics_services, service)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End test Loop on gatt table services")
        LogHelper.log_check(self, "Check every expected services were found")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=len(expected_services), msg=f"Expected service not found in the gat table: {expected_services}")
    # end def _check_presences

    def _check_service_presence(self, expected_services, optional_characteristics_services, service):
        """
        Check if a service presence is expected and then check its characteristics and descriptors presence

        :param expected_services: The list of services
        :type expected_services: ``dict``
        :param optional_characteristics_services: the lists of optional characteristics
        :type optional_characteristics_services: ``dict``
        :param service: the service to check
        :type service: ``BleService``
        """
        service_uuid = service.uuid
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check services if {service_uuid} is expected")
        # ----------------------------------------------------------------------------------------------------------
        self.assertIn(member=service_uuid,
                      container=expected_services.keys(),
                      msg=f"Unexpected service found: UUID: {service_uuid}")
        expected_characteristics_and_descriptors = expected_services[service_uuid]
        expected_characteristics = [x[0] for x in expected_characteristics_and_descriptors]
        expected_descriptors = [x[1] for x in expected_characteristics_and_descriptors]
        optional_characteristics = optional_characteristics_services.get(service_uuid)
        self._check_characteristics_presence(expected_characteristics, expected_descriptors, optional_characteristics,
                                             service)

        # remove the service from the expected ones as it's ticked off
        expected_services.pop(service_uuid)
    # end def _check_service_presence

    def _check_characteristics_presence(self, expected_characteristics, expected_descriptors, optional_characteristics,
                                        service):
        """
        Check the presence of characteristics contained in a service

        :param expected_characteristics: the expected characteristics of this service
        :type expected_characteristics: ``list``
        :param expected_descriptors: the expected descriptors for each characteristic
        :type expected_descriptors: ``list``
        :param optional_characteristics: list of optional characteristics
        :type optional_characteristics: ``list`` or ``None``
        :param service:  the service to check
        :type service: ``BleService``
        """
        service_uuid = service.uuid
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop on service {service_uuid}'s characteristics")
        # --------------------------------------------------------------------------------------------------------------
        for characteristic in service.characteristics:
            characteristic.uuid = characteristic.uuid.to_array()
            # Reports are a characteristic that can appear multiple time, not covered by this test
            if not (characteristic.uuid == BleUuid(BleUuidStandardCharacteristicAndObjectType.REPORT).to_array()
                    and service_uuid == BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check on characteristics on service {service_uuid}, "
                                          f"if characteristic 0x{HexList(characteristic.uuid)} is expected")
                # ------------------------------------------------------------------------------------------------------
                self.assertIn(characteristic.uuid,
                              expected_characteristics,
                              msg=f"Unexpected characteristic found in 0x{service_uuid}: "
                                  f"0x{HexList(characteristic.uuid)}")
                descriptors = expected_descriptors.pop(expected_characteristics.index(characteristic.uuid))
                self._check_descriptors(characteristic, descriptors, service_uuid)
                expected_characteristics.remove(characteristic.uuid)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"End Test Loop on service {service_uuid}'s characteristics")
        LogHelper.log_check(self, f"Check every expected characteristics of service were found")
        # --------------------------------------------------------------------------------------------------------------
        if optional_characteristics is not None:
            for characteristic_uuid in optional_characteristics:
                if characteristic_uuid in expected_characteristics:
                    expected_characteristics.remove(characteristic_uuid)
                # end if
            # end for
        # end if

        self.assertEqual(expected=0,
                         obtained=len(expected_characteristics),
                         msg=f"Characteristic(s) not found in service 0x{service_uuid}:"
                             f" {[characteristic for characteristic in expected_characteristics]}")
    # end def _check_characteristics_presence

    def _check_descriptors(self, characteristic, expected_descriptors, service_uuid):
        """
        Check the presence of descriptors contained in a characteristic

        :param characteristic: The characteristic to check
        :type characteristic: ``BleCharacteristic``
        :param expected_descriptors: List of expected descriptors in that characteristic, empty if none are expected
        :type expected_descriptors: ``list``
        :param service_uuid: The uuid of the service containing the characteristic
        :type service_uuid: ``BleUuid``
        """

        # ----------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop on descriptors in service {service_uuid}, "
                                 f"characteristic 0x{characteristic.uuid}")
        # ----------------------------------------------------------------------------------------------
        for descriptor in characteristic.descriptors:
            descriptor_uuid = descriptor.uuid.to_array()
            # --------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check descriptors on service {service_uuid}, "
                                      f"characteristic 0x{characteristic.uuid} "
                                      f"if descriptor {HexList(descriptor_uuid)} is expected")
            # --------------------------------------------------------------------------------------
            self.assertIn(descriptor_uuid,
                          expected_descriptors,
                          f"Unexpected descriptor found in service 0x{service_uuid},"
                          f" characteristic 0x{characteristic.uuid}: "
                          f"0x{HexList(descriptor_uuid)}")
            expected_descriptors.remove(descriptor_uuid)
        # end for
        # ----------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"End test Loop on descriptors in service {service_uuid}, "
                                 f"characteristic 0x{characteristic.uuid}")
        LogHelper.log_check(self, f"Check every expected descriptors in "
                                  f"characteristic 0x{characteristic.uuid}"
                                  f"of service {service_uuid} was found")
        # ----------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=len(expected_descriptors),
                         msg=f"Descriptor(s) not found in service 0x{service_uuid},"
                             f" characteristic 0x{characteristic.uuid}: "
                             f"{[HexList(descriptor) for descriptor in expected_descriptors]}")
    # end def _check_descriptors

    def _build_expected_services(self, mode):
        """
        Build a list of expected services based on the settings for the test and the mode the device is on.

        :param mode: The mode the device is in (Application/Bootloader)
        :type mode: ``DeviceInformation.EntityTypeV1``
        :return: tuple of two dictionaries, first one  of expected service, linking to a list of expected
                 characteristics and descriptors for each
                 and second one has lists of characteristics that are contained in the expected ones but allowed to be
                 missing because they are optional, indexed by the service containing them.
        :rtype: ``tuple(dict,dict)``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Build list of expected service for current mode")
        # --------------------------------------------------------------------------------------------------------------
        optional_characteristics_services={}
        expected_services = {
            BleUuid(BleUuidStandardService.GENERIC_ACCESS): [
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.DEVICE_NAME).to_array()), []),
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.APPEARANCE).to_array()), []),
                (HexList(BleUuid(
                    BleUuidStandardCharacteristicAndObjectType.PERIPHERAL_PREFERRED_CONNECTION_PARAMETERS).to_array()),
                 []),
            ],
            BleUuid(BleUuidStandardService.GENERIC_ATTRIBUTE): [
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.SERVICE_CHANGED).to_array()),
                 [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()]),
            ],
            BleUuid(BleUuidStandardService.DEVICE_INFORMATION): [
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING).to_array()), []),
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING).to_array()), []),
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.SERIAL_NUMBER_STRING).to_array()), []),
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.FIRMWARE_REVISION_STRING).to_array()), []),
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.SOFTWARE_REVISION_STRING).to_array()), []),
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.PNP_ID).to_array()), []),
            ],

        }


        if self.hasFeature("BLEProProtocol"):
            expected_services[BleUuid(BleUuidStandardService.LOGITECH_BLE_PRO)] = [
                (HexList(BleProtocolTestUtils.build_128_bits_uuid(
                    LogitechVendorUuid.BLE_PRO_SERVICE_INFORMATION_CHARACTERISTIC).to_array()),[]),
                (HexList(BleProtocolTestUtils.build_128_bits_uuid(
                    LogitechVendorUuid.BLE_PRO_AUTHENTICATION_CAPABILITIES_CHARACTERISTIC).to_array()),[]),
                (HexList(BleProtocolTestUtils.build_128_bits_uuid(
                    LogitechVendorUuid.BLE_PRO_AUTHENTICATION_CONTROL_CHARACTERISTIC).to_array()),[]),
                (HexList(BleProtocolTestUtils.build_128_bits_uuid(
                    LogitechVendorUuid.BLE_PRO_DEVICE_INFORMATION_CHARACTERISTIC).to_array()),[]),
                (HexList(BleProtocolTestUtils.build_128_bits_uuid(
                    LogitechVendorUuid.BLE_PRO_ATTRIBUTE_CAPABILITY_CHARACTERISTIC).to_array()),[]),
                (HexList(BleProtocolTestUtils.build_128_bits_uuid(
                    LogitechVendorUuid.BLE_PRO_ATTRIBUTE_CONTROL_CHARACTERISTIC).to_array()),[]),
            ]
            optional_characteristics_services[BleUuid(BleUuidStandardService.LOGITECH_BLE_PRO)] = []
            if mode == DeviceInformation.EntityTypeV1.BOOTLOADER:
                optional_characteristics_services[BleUuid(BleUuidStandardService.LOGITECH_BLE_PRO)].extend( [
                    HexList(BleProtocolTestUtils.build_128_bits_uuid(
                        LogitechVendorUuid.BLE_PRO_DEVICE_INFORMATION_CHARACTERISTIC).to_array()),])
            # end if

            # when no authentication is required, the authentication related characteristics are optional
            no_authentication = not (self.f.SHARED.PAIRING.F_PasskeyAuthenticationMethod or
                                     self.f.SHARED.PAIRING.F_Passkey2ButtonsAuthenticationMethod)
            if no_authentication:
                optional_characteristics_services[BleUuid(BleUuidStandardService.LOGITECH_BLE_PRO)].extend([
                    HexList(BleProtocolTestUtils.build_128_bits_uuid(
                        LogitechVendorUuid.BLE_PRO_AUTHENTICATION_CAPABILITIES_CHARACTERISTIC).to_array()),
                    HexList(BleProtocolTestUtils.build_128_bits_uuid(
                        LogitechVendorUuid.BLE_PRO_AUTHENTICATION_CONTROL_CHARACTERISTIC).to_array()),
                ])
            # end if
            # when no attribute is required, the attribute related characteristics are optional
            no_attribute = not self.f.SHARED.PAIRING.F_BLELatencyRemoval
            if no_attribute:
                optional_characteristics_services[BleUuid(BleUuidStandardService.LOGITECH_BLE_PRO)].extend([
                    HexList(BleProtocolTestUtils.build_128_bits_uuid(
                        LogitechVendorUuid.BLE_PRO_ATTRIBUTE_CAPABILITY_CHARACTERISTIC).to_array()),
                    HexList(BleProtocolTestUtils.build_128_bits_uuid(
                        LogitechVendorUuid.BLE_PRO_ATTRIBUTE_CONTROL_CHARACTERISTIC).to_array()),
                ])
            # end if
        # end if

        if mode == DeviceInformation.EntityTypeV1.MAIN_APP:
            expected_services[BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.APPLICATION_SERVICE)] = [
                (BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.APPLICATION_CHARACTERISTIC).to_array(),
                 [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()])
            ]
            self._append_application_hids(expected_services)

            if self.f.PRODUCT.PROTOCOLS.BLE.ADVERTISING.F_FastPairCapability:
                expected_services[BleUuid(BleUuidStandardService.GOOGLE_FAST_PAIR)] = [
                    (BleProtocolTestUtils.build_128_bits_uuid(GoogleFastPairCharacteristic.MODEL_ID).to_array(),
                     []),
                    (BleProtocolTestUtils.build_128_bits_uuid(GoogleFastPairCharacteristic.KEY_BASED_PAIRING).to_array(),
                     [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()]),
                    (BleProtocolTestUtils.build_128_bits_uuid(GoogleFastPairCharacteristic.PASSKEY).to_array(),
                     [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()]),
                    (BleProtocolTestUtils.build_128_bits_uuid(GoogleFastPairCharacteristic.ACCOUNT_KEY).to_array(),
                     []),
                    (BleProtocolTestUtils.build_128_bits_uuid(GoogleFastPairCharacteristic.ADITIONAL_DATA).to_array(),
                     [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()])
                ]
            # end if

            expected_services[BleUuid(BleUuidStandardService.BATTERY_SERVICE)]= [
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL).to_array()),
                 [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()]),
            ]

            if self.f.PRODUCT.PROTOCOLS.BLE.F_BAS_Version == "1.1":
                expected_services[BleUuid(BleUuidStandardService.BATTERY_SERVICE)].extend([
                    (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL_STATUS).to_array()),
                     [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()]),
                    (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_INFORMATION).to_array()),
                     [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()]),
                ])
            # end if

        elif mode == DeviceInformation.EntityTypeV1.BOOTLOADER:
            if self.f.PRODUCT.PROTOCOLS.BLE.F_BAS_Version is None:
                # before patch https://goldenpass.logitech.com:8443/c/ccp_fw/quark/+/11142 CCCD was exposed
                expected_services[BleUuid(BleUuidStandardService.BATTERY_SERVICE)] = [
                    (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL).to_array()),
                     [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()]),
                ]
            else:
                expected_services[BleUuid(BleUuidStandardService.BATTERY_SERVICE)] = [
                    (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL).to_array()),
                     []),
                ]
            # end if

            expected_services[BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE)] = [
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.HID_INFORMATION).to_array()), []),
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.REPORT_MAP).to_array()), []),
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.HID_CONTROL_POINT).to_array()), []),
            ]
            expected_services[BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.BOOTLOADER_SERVICE)] = [
                (BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.BOOTLOADER_CHARACTERISTIC).to_array(),
                 [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()])
            ]
        # end if
        return expected_services, optional_characteristics_services
    # end def _build_expected_services

    def _append_application_hids(self, expected_services):
        """
        Append the HIDS application to an expected service list

        Note: support only platforms, mices, presenters, gamepad, keyboards. No effect if device is touchpad
        :param expected_services: the list of expected service to extend
        :type expected_services: ``list``
        """
        characteristics = [
            (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.HID_INFORMATION).to_array()), []),
            (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.REPORT_MAP).to_array()), []),
            (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.HID_CONTROL_POINT).to_array()), []),
            (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.PROTOCOL_MODE).to_array()), []),
        ]
        device_type = self.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType
        if device_type == DeviceTypeAndName.TYPE.TRACKPAD:
            return
        # end if

        if self.f.PRODUCT.F_IsPlatform:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Using platform configuration for expected HIDS")
            # ----------------------------------------------------------------------------------------------------------
            characteristics.extend([
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_MOUSE_INPUT_REPORT).to_array()),
                 [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()]),
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_INPUT_REPORT).to_array()),
                 [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()]),
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_OUTPUT_REPORT).to_array()),
                 [])
            ])
            # end if
        elif device_type in [DeviceTypeAndName.TYPE.MOUSE, DeviceTypeAndName.TYPE.PRESENTER,
                             DeviceTypeAndName.TYPE.GAMEPAD, DeviceTypeAndName.TYPE.DIAL]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Using mouse configuration for expected HIDS")
            # ----------------------------------------------------------------------------------------------------------
            characteristics.extend([
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_MOUSE_INPUT_REPORT).to_array()),
                 [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()])
            ])
        elif device_type == DeviceTypeAndName.TYPE.KEYBOARD:  # default, keyboard
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Using keyboard configuration for expected HIDS")
            # ----------------------------------------------------------------------------------------------------------

            characteristics.extend([
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_INPUT_REPORT).to_array()),
                 [BleUuid(BleUuidStandardDescriptor.CLIENT_CHARACTERISTIC_CONFIGURATION).to_array()]),
                (HexList(BleUuid(BleUuidStandardCharacteristicAndObjectType.BOOT_KEYBOARD_OUTPUT_REPORT).to_array()),
                 [])
            ])
        # end if
        expected_services[BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE)] = characteristics
    # end def _append_application_hids

    def _get_battery_level_and_status(self):
        """
        Get the current battery level and status reported by feature 1004.

        :return: the current state of charge (0-100), and the expected battery level status data based on feature 1004
        :rtype: ``tuple(int,  BatteryLevelStatus)``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get the current battery level with feature 1004 or assume 100% charge "
                                 "if feature not available")
        # --------------------------------------------------------------------------------------------------------------
        feature_1004_index, feature_1004, _, _ = UnifiedBatteryTestUtils.HIDppHelper.get_parameters(
            self, skip_not_found=True)
        get_status = feature_1004.get_status_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=feature_1004_index)

        status_1004 = ChannelUtils.send(
            test_case=self,
            report=get_status,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=feature_1004.get_status_response_cls)

        state_of_charge = status_1004.state_of_charge
        status = UnifiedBatteryTestUtils.get_ble_bas_battery_level_status(status_1004)

        return state_of_charge, status
    # end def _get_battery_level_and_status
# end class GattSmallServiceInterfaceTestCaseMixin


class GattSmallServicesApplicationInterfaceTestCase(GattSmallServiceApplicationTestCase,
                                                    GattSmallServiceInterfaceTestCaseMixin):
    """
    BLE OS Gatt Small Service Interface Test Cases application class
    """
    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get whole gatt table")
        # --------------------------------------------------------------------------------------------------------------
        self.gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)
    # end def setUp

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    @bugtracker('AdvertisingShortLocalName')
    def test_gatt_presences(self):
        """
        Verify that the Gatt table contains all the expected services, characteristics and descriptors in application mode
        """
        if self.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType == DeviceTypeAndName.TYPE.TRACKPAD:
            expected_service_other_than_hids, optional_characteristics_services\
                = self._build_expected_services(DeviceInformation.EntityTypeV1.MAIN_APP)
            hid_services_found = 0
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Test Loop on gatt table services")
            # ----------------------------------------------------------------------------------------------------------
            for service in self.gatt_table:
                service_uuid = service.uuid

                if service_uuid == BleUuid(BleUuidStandardService.HUMAN_INTERFACE_DEVICE):
                    hid_services_found += 1
                else:
                    self._check_service_presence(expected_service_other_than_hids, optional_characteristics_services,
                                                 service)
                # end if
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End test Loop on gatt table services")
            LogHelper.log_check(self, f"Check every expected services were found")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=0, obtained=len(expected_service_other_than_hids),
                             msg=f"Expected service not found in the gatt table: {expected_service_other_than_hids}")
            self.assertEqual(expected=3, obtained=hid_services_found,
                             msg="Number of found human interface device service found in the gatt "
                                 "table differ from the expected 3")
        else:
            self._check_presences(DeviceInformation.EntityTypeV1.MAIN_APP)
        # end if

        self.testCaseChecked("INT_BLE_GATT_SSRV_0001", _AUTHOR)
    # end def test_gatt_presences

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_gap_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics of the GAP service in application mode
        """
        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleUuid(BleUuidStandardService.GENERIC_ACCESS))
        mse_tpd_connection_parameters = HexList(
            to_endian_list(LogitechBleConnectionParameters.MSE_TPD_APPLICATION_CHARACTERISTIC_VALUE_INTERVAL_MIN,
                           byte_count=2, little_endian=True),
            to_endian_list(LogitechBleConnectionParameters.MSE_TPD_APPLICATION_CHARACTERISTIC_VALUE_INTERVAL_MAX,
                           byte_count=2, little_endian=True),
            to_endian_list(LogitechBleConnectionParameters.MSE_TPD_APPLICATION_CHARACTERISTIC_VALUE_LATENCY,
                           byte_count=2, little_endian=True),
            to_endian_list(LogitechBleConnectionParameters.MSE_TPD_APPLICATION_CHARACTERISTIC_VALUE_TIMEOUT,
                           byte_count=2, little_endian=True))
        kbd_connection_parameters = HexList(
            to_endian_list(LogitechBleConnectionParameters.KBD_APPLICATION_CHARACTERISTIC_VALUE_INTERVAL_MIN,
                           byte_count=2, little_endian=True),
            to_endian_list(LogitechBleConnectionParameters.KBD_APPLICATION_CHARACTERISTIC_VALUE_INTERVAL_MAX,
                           byte_count=2, little_endian=True),
            to_endian_list(LogitechBleConnectionParameters.KBD_APPLICATION_CHARACTERISTIC_VALUE_LATENCY,
                           byte_count=2, little_endian=True),
            to_endian_list(LogitechBleConnectionParameters.KBD_APPLICATION_CHARACTERISTIC_VALUE_TIMEOUT,
                           byte_count=2, little_endian=True))

        device_type = self.f.PRODUCT.FEATURES.COMMON.DEVICE_TYPE_AND_NAME.F_DeviceType
        appearance = DEVICE_TYPE_TO_BLE_APPEARANCE[device_type]

        if device_type == DeviceTypeAndName.TYPE.KEYBOARD:
            if self.f.PRODUCT.F_IsPlatform:
                connection_parameters = mse_tpd_connection_parameters
            else:
                connection_parameters = kbd_connection_parameters
            # end if
        else:
            connection_parameters = mse_tpd_connection_parameters
        # end if

        characteristics = {
            BleUuid(BleUuidStandardCharacteristicAndObjectType.DEVICE_NAME):
                (BleCharacteristicProperties(read=True, write=True), None, HexList.fromString(self.f.SHARED.DEVICES.F_Name[0])),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.APPEARANCE):
                (BleCharacteristicProperties(read=True), None, HexList(to_endian_list(appearance.value, little_endian=True))),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.PERIPHERAL_PREFERRED_CONNECTION_PARAMETERS):
                (BleCharacteristicProperties(read=True), None, connection_parameters),
        }
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)

        self.testCaseChecked("INT_BLE_GATT_SSRV_0004", _AUTHOR)
    # end def test_gap_characteristics

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_gatt_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics of the GATT service in application mode
        """
        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleUuid(BleUuidStandardService.GENERIC_ATTRIBUTE))
        characteristics = {
            BleUuid(BleUuidStandardCharacteristicAndObjectType.SERVICE_CHANGED):
                (BleCharacteristicProperties(indicate=True), None, None),
        }
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)

        self.testCaseChecked("INT_BLE_GATT_SSRV_0005", _AUTHOR)
    # end def test_gatt_characteristics

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_battery_service_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics of the Battery service in application mode
        """
        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleUuid(BleUuidStandardService.BATTERY_SERVICE))
        state_of_charge, status = self._get_battery_level_and_status()

        if self.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_CapabilitiesFlags[0] == '1':
            information = HexList("000002")
        else:
            information = HexList("000001")
        # end if

        characteristics = {
            BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL):
                (BleCharacteristicProperties(read=True, notify=True), None,
                 HexList(state_of_charge)),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL_STATUS):
                (BleCharacteristicProperties(read=True, notify=True), None,
                 HexList(status)),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_INFORMATION):
                (BleCharacteristicProperties(read=True, indicate=True), None,
                 information),
        }
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)

        self.testCaseChecked("INT_BLE_GATT_SSRV_0006", _AUTHOR)
    # end def test_battery_service_characteristics

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_blepp_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics of the Ble++ service in application mode
        """
        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.APPLICATION_SERVICE))

        characteristics = {
            BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.APPLICATION_CHARACTERISTIC):
                (BleCharacteristicProperties(read=True, write=True, write_wo_resp=True,  notify=True), None,
                 HexList(HexList(to_endian_list(0, byte_count=BleMessageSize.BLEPP_MESSAGE_SIZE)))),

        }
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)

        self.testCaseChecked("INT_BLE_GATT_SSRV_0007", _AUTHOR)
    # end def test_blepp_characteristics

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def _test_scpc_characteristics(self):
        """
        Note: disabled as service not implemented in devices
        Verify the properties, security level and default value of the characteristics of the ScPS service in application mode
        """
        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleUuid(BleUuidStandardService.SCAN_PARAMETERS))

        characteristics = {
            BleUuid(BleUuidStandardCharacteristicAndObjectType.SCAN_INTERVAL_WINDOW):
                (BleCharacteristicProperties(write=True), None,
                 None),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.SCAN_REFRESH):
                (BleCharacteristicProperties(notify=True), None,
                 None),
        }
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)
    # end def _test_scpc_characteristics
# end class GattSmallServicesApplicationInterfaceTestCase


@features.class_decorator("BootloaderBLESupport")
class GattSmallServicesBootloaderInterfaceTestCase(GattSmallServiceBootloaderTestCase,
                                                   GattSmallServiceInterfaceTestCaseMixin):
    """
    BLE OS Gatt Small Service Interface Test Cases bootloader class
    """
    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get whole gatt table")
        # --------------------------------------------------------------------------------------------------------------
        self.gatt_table = self.ble_context.get_gatt_table(ble_context_device=self.ble_context_device_used)
    # end def setUp

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    @bugtracker('BLE_HID_Bootloader_Protocol_Mode_Present')
    def test_gatt_configuration(self):
        """
        Verify that the Gatt table contains all the expected services, characteristics and descriptors in bootloader mode
        """
        self._check_presences(DeviceInformation.EntityTypeV1.BOOTLOADER)

        self.testCaseChecked("INT_BLE_GATT_SSRV_0002", _AUTHOR)
    # end def test_gatt_configuration

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    @bugtracker('BLE_GAP_Appearance_Bootloader')
    def test_gap_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics of the GAP service in bootloader mode
        """
        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleUuid(BleUuidStandardService.GENERIC_ACCESS))
        connection_parameters = HexList(
            to_endian_list(LogitechBleConnectionParameters.BOOTLOADER_CHARACTERISTIC_VALUE_INTERVAL_MIN,
                           byte_count=2,
                           little_endian=True),
            to_endian_list(LogitechBleConnectionParameters.BOOTLOADER_CHARACTERISTIC_VALUE_INTERVAL_MAX,
                           byte_count=2,
                           little_endian=True),
            to_endian_list(LogitechBleConnectionParameters.BOOTLOADER_CHARACTERISTIC_VALUE_LATENCY,
                           byte_count=2,
                           little_endian=True),
            to_endian_list(LogitechBleConnectionParameters.BOOTLOADER_CHARACTERISTIC_VALUE_TIMEOUT,
                           byte_count=2,
                           little_endian=True),
        )

        characteristics = {
            BleUuid(BleUuidStandardCharacteristicAndObjectType.DEVICE_NAME):
                (BleCharacteristicProperties(read=True, write=True), None,
                 HexList.fromString(self.f.SHARED.DEVICES.F_Name[0]+'*')),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.APPEARANCE):
                (BleCharacteristicProperties(read=True),
                 None,
                 HexList(to_endian_list(BleAppearance.UNKNOWN.value, byte_count=BleMessageSize.APPEARANCE_SIZE,
                                        little_endian=True))),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.PERIPHERAL_PREFERRED_CONNECTION_PARAMETERS):
                (BleCharacteristicProperties(read=True), None, connection_parameters),
        }
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)

        self.testCaseChecked("INT_BLE_GATT_SSRV_0008", _AUTHOR)
    # end def test_gap_characteristics

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_gatt_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics of the GATT service in bootloader mode
        """
        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleUuid(BleUuidStandardService.GENERIC_ATTRIBUTE))
        characteristics = {
            BleUuid(BleUuidStandardCharacteristicAndObjectType.SERVICE_CHANGED):
                (BleCharacteristicProperties(indicate=True), None, None),
        }
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)

        self.testCaseChecked("INT_BLE_GATT_SSRV_0009", _AUTHOR)
    # end def test_gatt_characteristics

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_battery_service_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics of the Battery service in bootloader mode
        """
        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleUuid(BleUuidStandardService.BATTERY_SERVICE))
        state_of_charge = 100

        notify = self.f.PRODUCT.PROTOCOLS.BLE.F_BAS_Version is None
        characteristics = {
            BleUuid(BleUuidStandardCharacteristicAndObjectType.BATTERY_LEVEL):
                (BleCharacteristicProperties(read=True, notify=notify), None,
                 HexList(state_of_charge)),
        }
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)

        self.testCaseChecked("INT_BLE_GATT_SSRV_0010", _AUTHOR)
    # end def test_battery_service_characteristics

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_blepp_characteristics(self):
        """
        Verify the properties, security level and default value of the characteristics of the Ble++ in bootloader mode
        """
        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleProtocolTestUtils.build_128_bits_uuid(
                                                               LogitechVendorUuid.BOOTLOADER_SERVICE))

        characteristics = {
            BleProtocolTestUtils.build_128_bits_uuid(LogitechVendorUuid.BOOTLOADER_CHARACTERISTIC):
                (BleCharacteristicProperties(read=True, write=True, write_wo_resp=True, notify=True), None,
                 HexList(to_endian_list(0, byte_count=18))),

        }
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)

        self.testCaseChecked("INT_BLE_GATT_SSRV_0011", _AUTHOR)
    # end def test_blepp_characteristics

    @features('BLEProtocol')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def _test_scpc_characteristics(self):
        """
        Note: disabled as service not implemented in devices
        Verify the properties, security level and default value of the characteristics of the ScPS service in bootloader mode
        """
        service = BleProtocolTestUtils.get_service_in_gatt(self.gatt_table,
                                                           BleUuid(BleUuidStandardService.SCAN_PARAMETERS))

        characteristics = {
            BleUuid(BleUuidStandardCharacteristicAndObjectType.SCAN_INTERVAL_WINDOW):
                (BleCharacteristicProperties(write=True), None,
                 None),
            BleUuid(BleUuidStandardCharacteristicAndObjectType.SCAN_REFRESH):
                (BleCharacteristicProperties(notify=True), None,
                 None),
        }
        BleProtocolTestUtils.check_characteristics(self, service=service, expected_characteristics=characteristics)
    # end def _test_scpc_characteristics
# end class GattSmallServicesBootloaderInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
