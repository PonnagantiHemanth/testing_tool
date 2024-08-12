#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.osdetection.functionality
:brief: Validate BLE OS detection Functionality test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2022/07/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.devicereset import DeviceReset
from pyhid.hidpp.features.devicereset import ForceDeviceReset
from pylibrary.mcu.nrf52.blenvschunks import BleNvsChunks
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import to_endian_list
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import IosModelName
from pytestbox.device.base.bleprotocolutils import OsXModelName
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.ble.osdetection.osdetection import OS_DETECT_DELAY
from pytestbox.device.ble.osdetection.osdetection import OsDetectionTestCases
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytransport.ble.bleconstants import AncsUuids
from pytransport.ble.bleconstants import BleMacBookDis
from pytransport.ble.bleconstants import BlePnPIdVendorSrc
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleconstants import ManufacturerDataCompanyId
from pytransport.ble.bleconstants import ManufacturerDataName
from pytransport.ble.bleinterfaceclasses import BleService
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.bleinterfaceclasses import PnPId
from pyusb.libusbdriver import ChannelIdentifier

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------

_AUTHOR = "Sylvana Ieri"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class OsDetectionFunctionalityTestCases(OsDetectionTestCases):
    """
    BLE OS Detection Functionality Test Cases
    """
    
    @features('OsDetection')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_dis_full(self):
        """
        Verify the OS detected in NVS is OSX when the dis has all the characteristics filled in
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text=f"Change host OS emulation to OSX with dis full")
        # --------------------------------------------------------------------------------------------------------------
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)
        if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
            ble_context.reset_central_gatt_table()
        # end if

        dis = BleService(uuid=dis_uuid)

        characteristics = [
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
             HexList(bytes(ManufacturerDataName.APPLE_INC.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING),
             HexList(bytes(OsXModelName.MAC_BOOK.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.SERIAL_NUMBER_STRING),
             HexList(bytes(BleMacBookDis.SERIAL_NUMBER.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.HARDWARE_REVISION_STRING),
             HexList(bytes(BleMacBookDis.HARDWARE_REVISION_STRING.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.FIRMWARE_REVISION_STRING),
             HexList(bytes(BleMacBookDis.FIRMWARE_REVISION_STRING.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.SOFTWARE_REVISION_STRING),
             HexList(bytes(BleMacBookDis.SOFTWARE_REVISION_STRING.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.SYSTEM_ID),
             HexList(BleMacBookDis.SYSTEM_ID.value)),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.IEEE_11073_20601_REGULATORY_CERTIFICATION_DATA_LIST),
             HexList(BleMacBookDis.IEEE_REGULATORY_CERT_DATA_LIST.value)),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
             HexList(PnPId(
                 vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG,
                 vendor_id=HexList(
                     to_endian_list(ManufacturerDataCompanyId.APPLE_INC.value, little_endian=True, byte_count=2)),
                 # dummy values to fill in the pid
                 product_id=RandHexList(2),
                 fw_build=RandHexList(2))))
        ]

        BleProtocolTestUtils.customize_service_read(dis, characteristics)

        ble_context.add_service_to_central_gatt_table(service=dis)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check that the os detected is OSX")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.OSX)
        self.testCaseChecked("FUN_OS_DETEC_0001", _AUTHOR)
    # end def test_dis_full

    @features('OsDetection')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_usb_as_vendor_source_pnp_id(self):
        """
        Verify the OS detected in NVS is OSX When the PNP_ID vendor source is not Bluetooth sig
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text=f"Change host OS emulation to OSX with USB as vendor id source")
        # --------------------------------------------------------------------------------------------------------------

        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)
        if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
            ble_context.reset_central_gatt_table()
        # end if

        dis = BleService(uuid=dis_uuid)
        characteristics = [
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
             HexList(bytes(ManufacturerDataName.APPLE_INC.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING),
             HexList(bytes(OsXModelName.MAC_BOOK.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
             HexList(PnPId(
                 vendor_id_src=BlePnPIdVendorSrc.USB_IMPL_FORUM,
                 vendor_id=HexList(
                     to_endian_list(ManufacturerDataCompanyId.APPLE_INC.value, little_endian=True, byte_count=2)),
                 # dummy values to fill in the pid
                 product_id=RandHexList(2),
                 fw_build=RandHexList(2)
             )))
        ]
        BleProtocolTestUtils.customize_service_read(dis, characteristics)

        ble_context.add_service_to_central_gatt_table(service=dis)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check that the os detected is OSX")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.OSX)
        self.testCaseChecked("FUN_OS_DETEC_0002", _AUTHOR)
    # end def test_usb_as_vendor_source_pnp_id

    @features('OsDetection')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_osx_without_apple_vendor_id(self):
        """
        Verify the OS detected in NVS is OSX when vendor id doesn't match apples
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text=f"Change host OS emulation to OSX but with Amazon vendor id")
        # --------------------------------------------------------------------------------------------------------------

        ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)

        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)

        if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
            ble_context.reset_central_gatt_table()
        # end if

        dis = BleService(uuid=dis_uuid)
        characteristics = [
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
             HexList(bytes(ManufacturerDataName.APPLE_INC.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING),
             HexList(bytes(OsXModelName.MAC_BOOK.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
             HexList(PnPId(
                 vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG,
                 vendor_id=HexList(
                     to_endian_list(ManufacturerDataCompanyId.AMAZON_SERVICES.value, little_endian=True, byte_count=2)),
                 # dummy values to fill in the pid
                 product_id=RandHexList(2),
                 fw_build=RandHexList(2))))
        ]
        BleProtocolTestUtils.customize_service_read(dis, characteristics)

        ble_context.add_service_to_central_gatt_table(service=dis)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check that the os detected is OSX")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.OSX)
        self.testCaseChecked("FUN_OS_DETEC_0003", _AUTHOR)
    # end def test_osx_without_apple_vendor_id

    @features('OsDetection')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_apple_detection_without_ancs_present_and_wrong_name(self):
        """
        Verify the OS detected in NVS is OSX when the host ANCS notification is absent and the name is not from apple's
        approved name list
        """
        ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)

        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)

        dis = BleService(uuid=dis_uuid)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self,
                           text=f"Change host OS emulation to IOS, without ANCS service and with wrong name")
        # --------------------------------------------------------------------------------------------------------------

        if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
            ble_context.reset_central_gatt_table()
        # end if

        characteristics = [
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
             HexList(bytes(ManufacturerDataName.APPLE_INC.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING),
             HexList(bytes("Wrong name", "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
             HexList(PnPId(
                 vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG,
                 vendor_id=HexList(
                     to_endian_list(ManufacturerDataCompanyId.APPLE_INC.value, little_endian=True, byte_count=2)),
                 # dummy values to fill in the pid
                 product_id=RandHexList(2),
                 fw_build=RandHexList(2))))
        ]
        BleProtocolTestUtils.customize_service_read(dis, characteristics)

        ble_context.add_service_to_central_gatt_table(service=dis)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check that the os detected is OSX")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.OSX)
        self._reset_os_detection_test()
        self.testCaseChecked("FUN_OS_DETEC_0004", _AUTHOR)
    # end def test_apple_detection_without_ancs_present_and_wrong_name

    @features('OsDetection')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_ios_detection_with_ancs_present_and_wrong_name(self):
        """
        Verify the OS detected in NVS is IOS when the host ANCS notification present and the name isn't part of Apple's,
        set list
        """
        ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)

        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        ancs_uuid = BleProtocolTestUtils.build_128_bits_uuid(AncsUuids.ANCS)

        if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid) or \
                ble_context.is_service_in_central_gatt_table(service_uuid=ancs_uuid):
            ble_context.reset_central_gatt_table()
        # end if
        dis = BleService(uuid=dis_uuid)
        ancs = BleService(uuid=ancs_uuid)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self,
                           text=f"Change host OS emulation to IOS, with ANCS service and with the wrong name")
        # --------------------------------------------------------------------------------------------------------------

        if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
            ble_context.reset_central_gatt_table()
        # end if

        characteristics = [
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
             HexList(bytes(ManufacturerDataName.APPLE_INC.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING),
             HexList(bytes("Wrong name", "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
             HexList(PnPId(
                 vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG,
                 vendor_id=HexList(
                     to_endian_list(ManufacturerDataCompanyId.APPLE_INC.value, little_endian=True, byte_count=2)),
                 # dummy values to fill in the pid
                 product_id=RandHexList(2),
                 fw_build=RandHexList(2))))
        ]
        BleProtocolTestUtils.customize_service_read(dis, characteristics)

        ble_context.add_service_to_central_gatt_table(service=dis)
        ble_context.add_service_to_central_gatt_table(service=ancs)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check that the os detected is IOS")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.IOS)
        self._reset_os_detection_test()
        self.testCaseChecked("FUN_OS_DETEC_0005", _AUTHOR)
    # end def test_ios_detection_with_ancs_present_and_wrong_name

    @features('OsDetection')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_ios_detection_without_ancs_present(self):
        """
        Verify the OS detected in NVS is IOS when the host ANCS notification is absent
        """
        ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)

        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)

        dis = BleService(uuid=dis_uuid)
        for name in IosModelName:
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case=self,
                               text=f"Change host OS emulation to IOS, without ANCS service and with name {name}")
            # --------------------------------------------------------------------------------------------------------------

            if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
                ble_context.reset_central_gatt_table()
            # end if

            characteristics = [
                (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
                 HexList(bytes(ManufacturerDataName.APPLE_INC.value, "utf-8"))),
                (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING),
                 HexList(bytes(name.value, "utf-8"))),
                (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
                 HexList(PnPId(
                     vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG,
                     vendor_id=HexList(
                         to_endian_list(ManufacturerDataCompanyId.APPLE_INC.value, little_endian=True, byte_count=2)),
                     # dummy values to fill in the pid
                     product_id=RandHexList(2),
                     fw_build=RandHexList(2))))
            ]
            BleProtocolTestUtils.customize_service_read(dis, characteristics)

            ble_context.add_service_to_central_gatt_table(service=dis)
            # --------------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case=self, text="Check that the os detected is IOS")
            # --------------------------------------------------------------------------------------------------------------
            self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.IOS)
            self._reset_os_detection_test()
        # end for
        self.testCaseChecked("FUN_OS_DETEC_0006", _AUTHOR)
    # end def test_ios_detection_without_ancs_present

    @features('OsDetection')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_ios_detection_with_ancs_full(self):
        """
        Verify the OS detected in NVS is IOS when the host ANCS notification is set but the model name doesn't match
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text=f"Change host OS emulation to IOS, and fill the ANCS service")
        # --------------------------------------------------------------------------------------------------------------

        ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)

        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        ancs_uuid = BleProtocolTestUtils.build_128_bits_uuid(AncsUuids.ANCS)

        if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid) or \
                ble_context.is_service_in_central_gatt_table(service_uuid=ancs_uuid):
            ble_context.reset_central_gatt_table()
        # end if

        dis = BleService(uuid=dis_uuid)
        ancs = BleService(uuid=ancs_uuid)
        characteristics = [
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
             HexList(bytes(ManufacturerDataName.APPLE_INC.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING),
             HexList(bytes("Wrong Name", "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
             HexList(PnPId(
                 vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG,
                 vendor_id=HexList(
                     to_endian_list(ManufacturerDataCompanyId.APPLE_INC.value, little_endian=True, byte_count=2)),
                 # dummy values to fill in the pid
                 product_id=RandHexList(2),
                 fw_build=RandHexList(2))))
        ]
        BleProtocolTestUtils.customize_service_read(dis, characteristics)

        BleProtocolTestUtils.customize_service_write(ancs, [
            BleProtocolTestUtils.build_128_bits_uuid(AncsUuids.CONTROL_POINT)])

        BleProtocolTestUtils.customize_service_notify(ancs, [
            BleProtocolTestUtils.build_128_bits_uuid(AncsUuids.NOTIFICATION_SOURCE),
            BleProtocolTestUtils.build_128_bits_uuid(AncsUuids.DATA_SOURCE)])

        ble_context.add_service_to_central_gatt_table(service=dis)
        ble_context.add_service_to_central_gatt_table(service=ancs)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check that the os detected is IOS")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.IOS)
        self.testCaseChecked("FUN_OS_DETEC_0007", _AUTHOR)
    # end def test_ios_detection_with_ancs_full

    @features('OsDetection')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_detection_with_stack_failure_reconnection(self):
        """
        Verify the OS detection isn't done during reconnection after a BLE stack failure
        """

        self._prerequisite_set_ios(reconnect=False, open_channel=False)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text='Connect to the BLE device')
        # --------------------------------------------------------------------------------------------------------------

        self.button_stimuli_emulator.user_action()

        self._connect_and_encrypt()

        # Add a small delay to let the device perform OS detection in case it does it
        sleep(OS_DETECT_DELAY)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check that the os detected in the device hasn't change and is IOS")
        # --------------------------------------------------------------------------------------------------------------
        self.read_os_detection(BleNvsChunks.OsDetectedType.IOS)
        self.testCaseChecked("FUN_OS_DETEC_0008", _AUTHOR)
    # end def test_detection_with_stack_failure_reconnection

    @features('OsDetection')
    @features("Feature1830")
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_detection_with_dut_wake_up(self):
        """
        Verify the OS detection isn't regenerated after deep sleep
        """
        self._prerequisite_set_ios()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text=f"Put DUT on deep sleep")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)
        self.current_channel.close()
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Perform an user action to wake-up the DUT')
        # ----------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text=f"Reconnect to the device")
        # --------------------------------------------------------------------------------------------------------------
        ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)
        self.assertTrue(ble_context.is_direct_advertising_device_present(self.current_ble_device),
                        "device not advertising")

        self._connect_and_encrypt()
        # Add a small delay to let the device perform OS detection in case it does it
        sleep(OS_DETECT_DELAY)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check that the os detected in the device hasn't change and is IOS")
        # --------------------------------------------------------------------------------------------------------------
        self.read_os_detection(BleNvsChunks.OsDetectedType.IOS)
        self.testCaseChecked("FUN_OS_DETEC_0009", _AUTHOR)
    # end def test_detection_with_dut_wake_up

    @features('OsDetection')
    @features('Feature1802')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    def test_detection_persistent_with_reset(self):
        """
        Verify the OS detection isn't regenerated after a device reset
        """
        self._prerequisite_set_ios()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable Hidden Feature')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get reset feature ID')
        # --------------------------------------------------------------------------------------------------------------
        device_reset_feature_id = ChannelUtils.update_feature_mapping(self, feature_id=DeviceReset.FEATURE_ID)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset the device')
        # ----------------------------------------------------------------------------------------------------------
        force_device_reset = ForceDeviceReset(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                              featureId=device_reset_feature_id)
        ChannelUtils.send_only(self, report=force_device_reset)
        self.current_channel.close()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text=f"Reconnect to the device")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        self._connect_and_encrypt()
        # Add a small delay to let the device perform OS detection in case it does it
        sleep(OS_DETECT_DELAY)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check that the os detected in the device hasn't change and is IOS")
        # --------------------------------------------------------------------------------------------------------------
        self.read_os_detection(BleNvsChunks.OsDetectedType.IOS)
        self.testCaseChecked("FUN_OS_DETEC_0010", _AUTHOR)
    # end def test_detection_persistent_with_reset

    @features('OsDetection')
    @features('Feature1814')
    @level('Functionality')
    @services('BLEProReceiver')
    @services('BleContext')
    @services('Debugger')
    def test_detection_persistent_with_change_host(self):
        """
        Verify the OS detection isn't regenerated after an host change
        """
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)
        self.ble_pro_receiver_port_indexes = ReceiverTestUtils.get_receiver_port_indexes(
            self,
            ReceiverTestUtils.USB_PID_MEZZY_BLE_PRO,
            skip=[ChannelUtils.get_port_index(test_case=self)])

        self._prerequisite_set_ios()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=self, text="Cleanup all pairing slots except the first one")
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.clean_pairing_data(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text=f"Perform an host change action to host 1 "
                                                f"and pair to the BLE Pro receiver")
        # --------------------------------------------------------------------------------------------------------------

        dispatcher_to_dump = self.backup_dut_channel.hid_dispatcher
        DevicePairingTestUtils.pair_device_slot_to_other_receiver(
            test_case=self,
            device_slot=1,
            other_receiver_port_index=self.host_number_to_port_index(1),
            hid_dispatcher_to_dump=dispatcher_to_dump
        )

        ChangeHostTestUtils.HIDppHelper.set_current_host(
            self, device_index=1, host_index=1)

        DeviceManagerUtils.switch_channel(
            test_case=self,
            new_channel_id=ChannelIdentifier(port_index=self.host_number_to_port_index(1), device_index=1),
            close_associated_channel=True,
            open_associated_channel=True)

        sleep(OS_DETECT_DELAY)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text=f"Check os detected is BLE_PRO")
        # --------------------------------------------------------------------------------------------------------------
        self.read_os_detection(BleNvsChunks.OsDetectedType.LOGITECH_BLE_PRO)
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an host change action back to host 0")
        # ----------------------------------------------------------------------------------------------------------
        ChangeHostTestUtils.HIDppHelper.set_current_host(self, host_index=0)
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Bond to the device")
        # ----------------------------------------------------------------------------------------------------------
        self._connect_and_encrypt()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check that the os detected in the device hasn't change and is IOS")
        # --------------------------------------------------------------------------------------------------------------
        self.read_os_detection(BleNvsChunks.OsDetectedType.IOS)
        self.testCaseChecked("FUN_OS_DETEC_0011", _AUTHOR)
    # end def test_detection_persistent_with_change_host

    @features('OsDetection')
    @level('Functionality')
    @services('BleContext')
    @services('Debugger')
    @services('PowerSupply')
    def test_detection_with_battery_critical(self):
        """
        Verify the OS detection is done when the battery is critical
        """
        os_wanted = BleNvsChunks.OsDetectedType.OSX
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set battery critical level')
        # ---------------------------------------------------------------------------
        critical_state_of_charge = UnifiedBatteryTestUtils.get_state_of_charge_by_name(self, 'critical')
        battery_critical = UnifiedBatteryTestUtils.get_voltage_by_state_of_charge(self, critical_state_of_charge)
        self.power_supply_emulator.set_voltage(battery_critical)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text=f"Change host OS emulation to OSX with name MacBook")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.change_host_os_emulation(
            test_case=self, os_emulation_type=os_wanted, name=OsXModelName.MAC_BOOK)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text='Check that the os detected in the device is OSX')
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(os_wanted)
        self.testCaseChecked("FUN_OS_DETEC_00012", _AUTHOR)
    # end def test_detection_with_battery_critical
# end class OsDetectionFunctionalityTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
