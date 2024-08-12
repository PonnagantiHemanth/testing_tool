#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.osdetection.interface
:brief: Validates BLE OS detection Interface test cases
:author: Stanislas Cottard <scottard@logitech.com>
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
from pylibrary.tools.util import compute_inf_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.ble.osdetection.osdetection import OsDetectionTestCases
from pytransport.ble.bleconstants import AncsUuids
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

_AUTHOR = "Stanislas Cottard"

STRING_TO_CUT = "a 23 byte string to cut"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class OsDetectionInterfaceTestCases(OsDetectionTestCases):
    """
    BLE OS Detection Interface Test Cases
    """
    
    @features('OsDetection')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_manufacturer_name_size(self):
        """
        Verify the OS detected in NVS is UNDETERMINED for all the range of possible manufacturer name size
        """
        name_base = STRING_TO_CUT
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get BLE context")
        # --------------------------------------------------------------------------------------------------------------
        ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)

        dis = BleService(uuid=dis_uuid)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Compute a set of lengths between 0 and 23 to test")
        # --------------------------------------------------------------------------------------------------------------
        lengths = compute_inf_values(value=23, is_equal=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over samples lengths of the name in valid range sampled between 0 and 23:'
                  f'{lengths}%')
        # --------------------------------------------------------------------------------------------------------------
        for name_length in lengths:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case=self, text="Change host OS emulation to 'Undetermined', with manufacturer "
                                                    f"name string being {name_length} bytes long")
            # ----------------------------------------------------------------------------------------------------------
            if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
                ble_context.reset_central_gatt_table()
            # end if
            BleProtocolTestUtils.customize_service_read(dis, [(
                BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MANUFACTURER_NAME_STRING),
                HexList(bytes(name_base[0:name_length], "utf-8"))
            )])

            ble_context.add_service_to_central_gatt_table(service=dis)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case=self, text="Check that the os detected is UNDETERMINED")
            # ----------------------------------------------------------------------------------------------------------
            self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.UNDETERMINED)
            self._reset_os_detection_test()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("INT_OS_DETEC_0001", _AUTHOR)
    # end def test_manufacturer_name_size

    @features('OsDetection')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_model_number_size(self):
        """
        Verify the OS detected in NVS is UNDETERMINED for all the range of possible model number name size
        """

        name_base = STRING_TO_CUT
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get BLE context")
        # --------------------------------------------------------------------------------------------------------------
        ble_context = BleProtocolTestUtils.get_ble_context(test_case=self)
        dis_uuid = BleUuid(value=BleUuidStandardService.DEVICE_INFORMATION)

        dis = BleService(uuid=dis_uuid)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Compute a set of lengths between 0 and 23 to test")
        # --------------------------------------------------------------------------------------------------------------
        lengths = compute_inf_values(value=23, is_equal=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over samples lengths of the name in valid range sampled between 0 and 23:'
                  f'{lengths}%')
        # --------------------------------------------------------------------------------------------------------------
        for name_length in lengths:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case=self, text=f"Change host OS emulation to undetermined, with model number "
                                                    f"string being {name_length} bytes long")
            # ----------------------------------------------------------------------------------------------------------
            if ble_context.is_service_in_central_gatt_table(service_uuid=dis_uuid):
                ble_context.reset_central_gatt_table()
            # end if

            BleProtocolTestUtils.customize_service_read(dis, [(
                BleUuid(value=BleUuidStandardCharacteristicAndObjectType.MODEL_NUMBER_STRING),
                HexList(bytes(name_base[0:name_length], "utf-8"))
            )])

            ble_context.add_service_to_central_gatt_table(service=dis)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case=self, text="Check that the os detected is UNDETERMINED")
            # ----------------------------------------------------------------------------------------------------------
            self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.UNDETERMINED)
            self._reset_os_detection_test()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("INT_OS_DETEC_0002", _AUTHOR)
    # end def test_model_number_size

    @features('OsDetection')
    @level('Interface')
    @services('BleContext')
    @services('Debugger')
    def test_ios_detection_with_ancs(self):
        """
        Verify the OS detected in NVS is IOS when the host ANCS notification is set but the model name doesn't match
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Change host OS emulation to IOS, with a wrong model name")
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

        BleProtocolTestUtils.customize_service_notify(ancs, [
            BleProtocolTestUtils.build_128_bits_uuid(AncsUuids.NOTIFICATION_SOURCE)])

        ble_context.add_service_to_central_gatt_table(service=dis)
        ble_context.add_service_to_central_gatt_table(service=ancs)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text="Check that the os detected is IOS")
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.IOS)
        self.testCaseChecked("INT_OS_DETEC_0003", _AUTHOR)
    # end def test_ios_detection_with_ancs
# end class OsDetectionInterfaceTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
