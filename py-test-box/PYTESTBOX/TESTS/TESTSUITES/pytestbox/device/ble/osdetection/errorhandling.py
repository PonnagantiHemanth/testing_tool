#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.osdetection.errorhandling
:brief: Validate BLE OS detection error handling test cases
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
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import OsXModelName
from pytestbox.device.ble.osdetection.osdetection import OsDetectionTestCases
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
class OsDetectionErrorHandlingTestCases(OsDetectionTestCases):
    """
    BLE OS Detection ErrorHandling Test Cases
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
    @level('ErrorHandling')
    @services('BleContext')
    @services('Debugger')
    def test_manufacturer_name_too_long(self):
        """
        Verify the os detection mechanism when the Manufacturer name string is longer than the allowed size.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=self, text="Clear central gat table if it contains the DIS")
        # --------------------------------------------------------------------------------------------------------------
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
        if self.ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
            self.ble_context.reset_central_gatt_table()
        # end if
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Add DIS with Manufacturer Name String Longer than 23 bytes")
        # --------------------------------------------------------------------------------------------------------------
        dis = BleService(uuid=dis_uuid)
        BleProtocolTestUtils.customize_service_read(dis, [
            (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
             HexList(bytes("abcdefghijklmnopqrstuvwxyz", "utf-8"))),  # put 26 bytes when the limit is 23
        ])
        self.ble_context.add_service_to_central_gatt_table(dis)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check os is Undetermined after os detection")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.UNDETERMINED)
        self.testCaseChecked("ERR_OS_DETEC_0001", _AUTHOR)
    # end def test_manufacturer_name_too_long

    @features('OsDetection')
    @level('ErrorHandling')
    @services('BleContext')
    @services('Debugger')
    def test_vendor_id_source_outside_attributed(self):
        """
        Verify the os detection mechanism when the vendor id source string is outside the attributed values for USB and
        BLE.
        """
        LogHelper.log_prerequisite(test_case=self, text="Compute a list of vendor id source in its error range")
        # --------------------------------------------------------------------------------------------------------------
        list_of_wrong_ids = compute_wrong_range([BlePnPIdVendorSrc.BLUETOOTH_SIG, BlePnPIdVendorSrc.USB_IMPL_FORUM],
                                                min_value=0x0, max_value=0xFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over vendor_id contained in the list {list_of_wrong_ids}%')
        # --------------------------------------------------------------------------------------------------------------
        for vendor_id in list_of_wrong_ids:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case=self, text="Clear central gat table if it contains the DIS")
            # ----------------------------------------------------------------------------------------------------------
            dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)
            if self.ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
                self.ble_context.reset_central_gatt_table()
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case=self, text="Add DIS")
            # ----------------------------------------------------------------------------------------------------------
            dis = BleService(uuid=dis_uuid)
            BleProtocolTestUtils.customize_service_read(dis, [
                (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
                 HexList(bytes(ManufacturerDataName.APPLE_INC.value, "utf-8"))),
                (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING),
                 HexList(bytes(OsXModelName.MAC_BOOK.value, "utf-8"))),
                (BleUuid(value=BleUuidStandardCharacteristicAndObjectType.PNP_ID),
                 HexList(PnPId(
                     vendor_id_src=HexList(vendor_id),
                     vendor_id=HexList(
                         to_endian_list(ManufacturerDataCompanyId.APPLE_INC.value, little_endian=True, byte_count=2)),
                     # dummy values to fill the pnp_id
                     product_id=RandHexList(2),
                     fw_build=RandHexList(2))))])
            self.ble_context.add_service_to_central_gatt_table(dis)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case=self, text="Check os is OSX after os detection")
            # ----------------------------------------------------------------------------------------------------------
            self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.OSX)
            self._reset_os_detection_test()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_OS_DETEC_0002", _AUTHOR)
    # end def test_vendor_id_source_outside_attributed

# end class OsDetectionErrorHandlingTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
