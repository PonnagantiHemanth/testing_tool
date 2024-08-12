#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.osdetection.robustness
:brief: Validates BLE OS detection robustsness test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2022/07/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.mcu.nrf52.blenvschunks import BleNvsChunks
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import to_endian_list
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import IosModelName
from pytestbox.device.base.bleprotocolutils import OsXModelName
from pytestbox.device.ble.osdetection.osdetection import OsDetectionTestCases
from pytransport.ble.bleconstants import AncsUuids, BleChromePNPID
from pytransport.ble.bleconstants import BlePnPIdVendorSrc
from pytransport.ble.bleconstants import BleUuidStandardCharacteristicAndObjectType
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleconstants import ManufacturerDataCompanyId
from pytransport.ble.bleconstants import ManufacturerDataName
from pytransport.ble.bleinterfaceclasses import BleService
from pytransport.ble.bleinterfaceclasses import BleUuid
from pytransport.ble.bleinterfaceclasses import PnPId


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class OsDetectionRobustnessTestCases(OsDetectionTestCases):
    """
    BLE OS Detection Robustness Test Cases
    """

    def setUp(self):
        # See ``OsDetectionTestCases.setUp``
        super().setUp()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=self, text="Get Ble context")
        # --------------------------------------------------------------------------------------------------------------
        self.ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)
    # end def setUp

    @features('OsDetection')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_dis_absent(self):
        """
        Verify the OS detected in NVS is UNDETERMINED when the dis is absent
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=self, text="Clear central gat table if it contains the DIS")
        # --------------------------------------------------------------------------------------------------------------
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        if self.ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
            self.ble_context.reset_central_gatt_table()
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Discover and _scan_connect_and_encrypt to the BLE device")
        LogHelper.log_check(test_case=self, text="Check the os detected is 'Undetermined' after a successful bonding")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.UNDETERMINED)
        self.testCaseChecked("ROB_OS_DETEC_0001", _AUTHOR)
    # end def test_dis_absent

    @features('OsDetection')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_dis_empty(self):
        """
        Verify the OS detected in NVS is UNDETERMINED when the dis is empty
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=self, text="Clear central gat table if it contains the DIS")
        # --------------------------------------------------------------------------------------------------------------
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        if self.ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
            self.ble_context.reset_central_gatt_table()
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Add empty DIS")
        # --------------------------------------------------------------------------------------------------------------
        dis = BleService(uuid=dis_uuid)
        self.ble_context.add_service_to_central_gatt_table(dis)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check os is `Undetermined` after a successful bonding")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.UNDETERMINED)
        self.testCaseChecked("ROB_OS_DETEC_0002", _AUTHOR)
    # end def test_dis_empty

    @features('OsDetection')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_dis_manufacturer_name_null(self):
        """
        Verify the OS detected in NVS is UNDETERMINED when the manufacturer name is absent
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=self, text="Clear central gat table if it contains the DIS")
        # --------------------------------------------------------------------------------------------------------------
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        if self.ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
            self.ble_context.reset_central_gatt_table()
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Add DIS without a manufacturer string name")
        # --------------------------------------------------------------------------------------------------------------
        dis = BleService(uuid=dis_uuid)
        BleProtocolTestUtils.customize_service_read(service=dis, characteristics=[
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
             None),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
             HexList(PnPId(
                           vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG,
                           vendor_id=HexList(
                               to_endian_list(ManufacturerDataCompanyId.MICROSOFT.value, little_endian=True, byte_count=2)),
                           # dummy values to fill the pnp_id
                           product_id=HexList(RandHexList(2)),
                           fw_build=HexList(RandHexList(2))
                        )))])
        self.ble_context.add_service_to_central_gatt_table(dis)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check os is undetermined after a successful bonding")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.UNDETERMINED)
        self.testCaseChecked("ROB_OS_DETEC_0003", _AUTHOR)
    # end def test_dis_manufacturer_name_null

    @features('OsDetection')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_chrome_os_priority(self):
        """
        Verify the os detected when a mix of apple and google's device characteristics is used, ChromeOS should have the
        priority
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=self, text="Clear central gat table if it contains the DIS or ANCS")
        # --------------------------------------------------------------------------------------------------------------
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        ancs_uuid = BleProtocolTestUtils.build_128_bits_uuid(AncsUuids.ANCS)
        if self.ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid) \
                or self.ble_context.is_service_in_central_gatt_table(service_uuid=ancs_uuid):
            self.ble_context.reset_central_gatt_table()
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Add DIS with only a mix of IOS and Chrome values")
        # --------------------------------------------------------------------------------------------------------------
        dis = BleService(uuid=dis_uuid)
        BleProtocolTestUtils.customize_service_read(dis, [
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
             HexList(bytes(ManufacturerDataName.APPLE_INC.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING),
             HexList(bytes(IosModelName.IPHONE.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
             HexList(PnPId(
                 vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG,
                 vendor_id=HexList(
                     to_endian_list(ManufacturerDataCompanyId.GOOGLE.value, little_endian=True, byte_count=2)),
                 product_id=HexList(to_endian_list(BleChromePNPID.PRODUCT_ID, little_endian=True, byte_count=2)),
                 fw_build=HexList(to_endian_list(BleChromePNPID.FW_BUILD, little_endian=True, byte_count=2))
             )))
        ])
        self.ble_context.add_service_to_central_gatt_table(dis)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Add ancs")
        # --------------------------------------------------------------------------------------------------------------
        ancs = BleService(uuid=ancs_uuid)
        self.ble_context.add_service_to_central_gatt_table(ancs)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check the os detected is Chrome after a successful bonding")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.CHROME)
        self.testCaseChecked("ROB_OS_DETEC_0004", _AUTHOR)
    # end def test_chrome_os_priority

    @features('OsDetection')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_ancs_priority(self):
        """
        Verify the os detected when a mix of apple and microsoft device characteristics is used, IOS should have the
        priority due to the presence of the ANCS
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=self, text="Clear central gat table if it contains the DIS or ANCS")
        # --------------------------------------------------------------------------------------------------------------
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        ancs_uuid = BleProtocolTestUtils.build_128_bits_uuid(AncsUuids.ANCS)
        if self.ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid) \
                or self.ble_context.is_service_in_central_gatt_table(service_uuid=ancs_uuid):
            self.ble_context.reset_central_gatt_table()
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Add DIS with only a mix of Apple and Microsoft values")
        # --------------------------------------------------------------------------------------------------------------
        dis = BleService(uuid=dis_uuid)
        BleProtocolTestUtils.customize_service_read(dis, [
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
             HexList(bytes(ManufacturerDataName.MICROSOFT.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
             HexList(PnPId(
                 vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG,
                 vendor_id=HexList(
                     to_endian_list(ManufacturerDataCompanyId.MICROSOFT.value, little_endian=True, byte_count=2)),
                 # dummy values to fill the pnp_id
                 product_id=RandHexList(2),
                 fw_build=RandHexList(2)
             )))
        ])
        self.ble_context.add_service_to_central_gatt_table(dis)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Add ancs")
        # --------------------------------------------------------------------------------------------------------------
        ancs = BleService(uuid=ancs_uuid)
        self.ble_context.add_service_to_central_gatt_table(ancs)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check os is IOS after a successful bonding")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.IOS)
        self.testCaseChecked("ROB_OS_DETEC_0005", _AUTHOR)
    # end def test_ancs_priority

    @features('OsDetection')
    @level('Robustness')
    @services('BleContext')
    @services('Debugger')
    def test_osx_priority(self):
        """
        Verify the os detected when a mix of OSX and IOS device characteristics is used, OSX should have the
        priority despite to the presence of the ANCS, due to the device name
        """

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=self, text="Clear central gat table if it contains the DIS or ANCS")
        # --------------------------------------------------------------------------------------------------------------
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        ancs_uuid = BleProtocolTestUtils.build_128_bits_uuid(AncsUuids.ANCS)
        if self.ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid) \
                or self.ble_context.is_service_in_central_gatt_table(service_uuid=ancs_uuid):
            self.ble_context.reset_central_gatt_table()
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Add DIS with OSX values")
        # --------------------------------------------------------------------------------------------------------------
        dis = BleService(uuid=dis_uuid)
        BleProtocolTestUtils.customize_service_read(dis, [
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
             HexList(bytes(ManufacturerDataName.APPLE_INC.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING),
             HexList(bytes(OsXModelName.MAC_BOOK.value, "utf-8"))),
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
             HexList(PnPId(
                 vendor_id_src=BlePnPIdVendorSrc.BLUETOOTH_SIG,
                 vendor_id=HexList(
                     to_endian_list(ManufacturerDataCompanyId.APPLE_INC.value, little_endian=True, byte_count=2)),
                 product_id=RandHexList(2),
                 # dummy values to fill the pnp_id
                 fw_build=RandHexList(2))))])
        self.ble_context.add_service_to_central_gatt_table(dis)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Add ancs")
        # --------------------------------------------------------------------------------------------------------------
        ancs = BleService(uuid=ancs_uuid)
        self.ble_context.add_service_to_central_gatt_table(ancs)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check os is OSX after a successful bonding")
        # ------------------------------------------------------------------------------<--------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.OSX)
        self.testCaseChecked("ROB_OS_DETEC_0006", _AUTHOR)
    # end def test_osx_priority
# end class OsDetectionRobustnessTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
