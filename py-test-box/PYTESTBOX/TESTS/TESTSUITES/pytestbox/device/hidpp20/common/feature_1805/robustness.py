#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1805.robustness
:brief: HID++ 2.0 ``OobState`` robustness test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2023/03/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.usbchannel import UsbChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibrationFactory
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDeviceProperties
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.oobstate import OobState
from pyhid.hidpp.features.common.uniqueidentifier32bytes import RegenId
from pyhid.hidpp.features.common.uniqueidentifier32bytes import RegenIdResponse
from pyhid.hidpp.features.common.uniqueidentifier32bytes import UniqueIdentifier32Bytes
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeatures
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeaturesResponse
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pyraspi.services.powersupply import PowerSupplyConstant
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.batterylevelscalibrationutils import BatteryLevelsCalibrationTestUtils
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.configurabledevicepropertiesutils import ConfigurableDevicePropertiesTestUtils
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicemanagedeactivatablefeaturesauthutils import \
    DeviceManageDeactivatableFeaturesAuthTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.oobstateutils import OobStateTestUtils
from pytestbox.device.base.tdeaccesstonvmutils import TdeAccessToNvmTestUtils
from pytestbox.device.hidpp20.common.feature_1805.oobstate import OobStateTestCase
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.equaddeviceconnectionutils import EQuadDeviceConnectionUtils
from pyusb.libusbdriver import ChannelIdentifier

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_SEND_OOB = "Send SetOobState request"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OobStateRobustnessTestCase(OobStateTestCase):
    """
    Validate ``OobState`` robustness test cases
    """

    @features("Feature1805")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_set_oob_state_software_id(self):
        """
        Validate ``SetOobState`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(OobState.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetOobState request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = OobStateTestUtils.HIDppHelper.set_oob_state(
                test_case=self,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetOobStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1805.set_oob_state_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1805_0001#1", _AUTHOR)
    # end def test_set_oob_state_software_id

    @features("Feature1805")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_set_oob_state_padding(self):
        """
        Validate ``SetOobState`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1805.set_oob_state_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetOobState request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = OobStateTestUtils.HIDppHelper.set_oob_state(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetOobStateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1805.set_oob_state_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1805_0002#1", _AUTHOR)
    # end def test_set_oob_state_padding

    @features("Feature1805")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_check_oob_when_hidden_features_disabled(self):
        """
        Goal: Check setOobState is not allowed if Hidden Features are not enabled
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable Hidden Features")
        # --------------------------------------------------------------------------------------------------------------
        self.enable_hidden_feature_id = ChannelUtils.update_feature_mapping(test_case=self,
                                                                            feature_id=EnableHidden.FEATURE_ID)
        report = SetEnableHiddenFeatures(device_index=ChannelUtils.get_device_index(test_case=self),
                                         feature_index=self.enable_hidden_feature_id,
                                         enable_byte=EnableHidden.DISABLED)
        ChannelUtils.send(test_case=self, report=report, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=SetEnableHiddenFeaturesResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send OOB request and validate NOT_ALLOWED error is returned")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1805.set_oob_state_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1805_index)

        OobStateTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_wireless_device_status_broadcast_event=False,
                   verify_connection_reset=False, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Check device reconnection")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self)

        self.testCaseChecked("ROB_1805_0003", _AUTHOR)
    # end def test_check_oob_when_hidden_features_disabled

    @features("Feature1805")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_connection_not_lost_before_power_reset(self):
        """
        Goal: Check the connection with the host generating the command is NOT lost, before next power on
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Pair DUT with multiple host")
        # --------------------------------------------------------------------------------------------------------------
        for host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            if host + 1 != HOST.CH1:
                OobStateTestUtils.pair_device(self, host=host)
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Reconnect back to HOST 1")
        # --------------------------------------------------------------------------------------------------------------
        curr_port_index = ChannelUtils.get_port_index(self)
        if self.f.PRODUCT.DEVICE.F_NbHosts > 1:
            ChangeHostTestUtils.HIDppHelper.set_current_host(self, HOST.CH1 - 1)

            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=curr_port_index, device_index=HOST.CH1),
                close_associated_channel=True,
                open_associated_channel=True)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        oob_response = OobStateTestUtils.HIDppHelper.set_oob_state(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check valid response")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.MessageChecker.check_fields(
            test_case=self, message=oob_response, expected_cls=self.feature_1805.set_oob_state_response_cls,
            check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Emulate user action and verify a HID report can be received")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over remaining Hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host in range(HOST.CH2 - 1, self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Set current host with host index {host + 1}")
            # ----------------------------------------------------------------------------------------------------------

            ChangeHostTestUtils.HIDppHelper.set_current_host(self, host)
            DeviceManagerUtils.switch_channel(
                test_case=self,
                new_channel_id=ChannelIdentifier(port_index=curr_port_index, device_index=host + 1),
                close_associated_channel=True,
                open_associated_channel=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Emulate user action and verify a HID report can be received")
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.ButtonHelper.check_user_action(self)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_wireless_device_status_broadcast_event=False,
                   verify_connection_reset=False, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        if not isinstance(self.current_channel, UsbChannel):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check connection is lost")
            # ----------------------------------------------------------------------------------------------------------
            DevicePairingTestUtils.check_link_not_established_notification(
                test_case=self, expected_pairing_slot=self.current_channel.device_index)
        # end if

        self.testCaseChecked("ROB_1805_0004", _AUTHOR)
    # end def test_connection_not_lost_before_power_reset

    @features("Feature1805")
    @features("Feature1806")
    @features("NvsChunkID", "NVS_SERIAL_NB_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_serial_number_nvs_retained_on_1806_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check Serial Number does not
        change

        Use 0x1806 to set Serial Number
        """
        self.post_requisite_reload_nvs = True
        property_id = ConfigurableDeviceProperties.PropertyIdV8.SERIAL_NUMBER

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set serial number")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDevicePropertiesTestUtils.SetDevicePropertiesHelper.HIDppHelper.write(
            self, property_id, flag=0, sub_data_index=0, property_data=HexList(0x00))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Serial Number is not erased/reset in NVS (NVS_SERIAL_NB_ID)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check Serial Number is not erased/reset in NVS (NVS_SERIAL_NB_ID)")

        self.testCaseChecked("ROB_1805_0005#1", _AUTHOR)
    # end def test_serial_number_nvs_retained_on_1806_reset

    @features("Feature1805")
    @features("Feature1807")
    @features("NvsChunkID", "NVS_DEVICE_NAME_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_serial_number_nvs_retained_on_1807_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check Serial Number does not
        change

        Use 0x1807 to set Serial Number
        """
        self.post_requisite_reload_nvs = True
        property_id = ConfigurableProperties.PropertyId.SERIAL_NUMBER

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 1807")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_1807, _, _ = ConfigurablePropertiesTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set serial number")
        # --------------------------------------------------------------------------------------------------------------
        select_property_response = ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)
        write_property_response = ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, HexList(0x00))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SelectPropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        checker.check_fields(self, select_property_response, self.feature_1807.select_property_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WritePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        checker.check_fields(self, write_property_response, self.feature_1807.write_property_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Serial Number is not erased/reset in NVS (NVS_SERIAL_NB_ID)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check Serial Number is not erased/reset in NVS (NVS_SERIAL_NB_ID)")

        self.testCaseChecked("ROB_1805_0005#2", _AUTHOR)
    # end def test_serial_number_nvs_retained_on_1807_reset

    @features("Feature1805")
    @features("Feature1806")
    @features("NvsChunkID", "NVS_DEVICE_NAME_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_device_name_nvs_retained_on_1806_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check Device Name does not
        change

        Use 0x1806 to set Device Name
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set Device Name")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDevicePropertiesTestUtils.SetDeviceNameHelper.HIDppHelper.write(
            self, char_index=0, device_name="NEW_DEVICE_NAME")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Device Name is not erased/reset in NVS (NVS_DEVICE_NAME_ID)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check Device Name is not erased/reset in NVS (NVS_DEVICE_NAME_ID)")

        self.testCaseChecked("ROB_1805_0006#1", _AUTHOR)
    # end def test_device_name_nvs_retained_on_1806_reset

    @features("Feature1805")
    @features("Feature1807")
    @features("NvsChunkID", "NVS_DEVICE_NAME_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_device_name_nvs_retained_on_1807_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check Device Name does not
        change

        Use 0x1807 to set Device Name
        """
        self.post_requisite_reload_nvs = True
        property_id_config = ConfigurableProperties.PropertyId.HIDPP_DEVICE_NAME

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set Device Name")
        # --------------------------------------------------------------------------------------------------------------
        select_property_response = ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id_config)
        write_property_response = ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self,
                                                                                         HexList("NEW_DEVICE_NAME"))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SelectPropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        checker.check_fields(self, select_property_response, self.feature_1807.select_property_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WritePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        checker.check_fields(self, write_property_response, self.feature_1807.write_property_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Device Name is not erased/reset in NVS (NVS_DEVICE_NAME_ID)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check Device Name is not erased/reset in NVS (NVS_DEVICE_NAME_ID)")

        self.testCaseChecked("ROB_1805_0006#2", _AUTHOR)
    # end def test_device_name_nvs_retained_on_1807_reset

    @features("Feature1805")
    @features("Feature1EB0")
    @features("NvsChunkID", "NVS_TDE_MFG_ACCESS_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_tde_data_nvs_retained_on_1eb0_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check TDE Data do not change

        Use x1EB0 to write TDE Data
        """
        self.post_requisite_reload_nvs = True
        num_of_data_to_write = 14

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable TDE Manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1EB0")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_1eb0, _, _ = TdeAccessToNvmTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write TDE Data (0x1eb0.TdeWriteData)")
        # --------------------------------------------------------------------------------------------------------------
        TdeAccessToNvmTestUtils.HIDppHelper.tde_write_data(self, starting_position=0,
                                                           number_of_bytes_to_read_or_write=num_of_data_to_write,
                                                           data_byte_0=0xAA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send TdeReadData request")
        # --------------------------------------------------------------------------------------------------------------
        read_data_response = TdeAccessToNvmTestUtils.HIDppHelper.tde_read_data(
            self, starting_position=0, number_of_bytes_to_read=num_of_data_to_write)

        expected = HexList("00") + HexList(num_of_data_to_write) + HexList("AA") + \
            HexList([0] * (num_of_data_to_write - 1))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Validate TdeReadData.dataValues ({HexList(expected)})")
        # --------------------------------------------------------------------------------------------------------------
        checker = TdeAccessToNvmTestUtils.TdeReadDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "starting_position": (checker.check_starting_position, expected[0]),
            "number_of_bytes_to_read_or_write": (checker.check_number_of_bytes_to_read_or_write, expected[1]),
            "data_byte_0": (checker.check_data_byte_0, expected[2]),
            "data_byte_1": (checker.check_data_byte_1, expected[3]),
            "data_byte_2": (checker.check_data_byte_2, expected[4]),
            "data_byte_3": (checker.check_data_byte_3, expected[5]),
            "data_byte_4": (checker.check_data_byte_4, expected[6]),
            "data_byte_5": (checker.check_data_byte_5, expected[7]),
            "data_byte_6": (checker.check_data_byte_6, expected[8]),
            "data_byte_7": (checker.check_data_byte_7, expected[9]),
            "data_byte_8": (checker.check_data_byte_8, expected[10]),
            "data_byte_9": (checker.check_data_byte_9, expected[11]),
            "data_byte_10": (checker.check_data_byte_10, expected[12]),
            "data_byte_11": (checker.check_data_byte_11, expected[13]),
            "data_byte_12": (checker.check_data_byte_12, expected[14]),
            "data_byte_13": (checker.check_data_byte_13, expected[15]),
        })
        checker.check_fields(self, read_data_response, self.feature_1eb0.tde_read_data_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check TDE Data is not erased/reset in NVS (NVS_TDE_MFG_ACCESS_ID)")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        nvs_chunk = self.memory_manager.get_active_chunk_by_name(chunk_name="NVS_TDE_MFG_ACCESS_ID",
                                                                 active_bank_only=True)
        self.assertEqual(expected=expected[2:], obtained=HexList(nvs_chunk.data[:num_of_data_to_write]))

        self.testCaseChecked("ROB_1805_0007", _AUTHOR)
    # end def test_tde_data_nvs_retained_on_1eb0_reset

    @features("Feature1805")
    @features("Feature1861")
    @features("NvsChunkID", "NVS_BATT_CALIBRATION_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_battery_calibration_nvs_retained_on_1861_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check Battery calibration
        does not change

        Use x1861 to perform battery calibration
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_cutoff = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1861 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1861_index, self.feature_1861, _, _ = DeviceBaseTestUtils.HIDppHelper.get_parameters(
            self, feature_id=BatteryLevelsCalibration.FEATURE_ID, factory=BatteryLevelsCalibrationFactory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Perform battery calibration (0x1861.MeasureBattery, 0x1861.StoreCalibration,"
                                 "0x1861.ReadCalibration)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Disable cutoff')
        # --------------------------------------------------------------------------------------------------------------
        BatteryLevelsCalibrationTestUtils.HIDppHelper.set_cutoff_state(
            self, cutoff_change_state_requested=True, cutoff_desired_state=BatteryLevelsCalibration.CUTOFF_DISABLE,
            state_to_check=BatteryLevelsCalibration.CUTOFF_DISABLE)

        get_batt_calibration_info = self.feature_1861.get_battery_calibration_info_cls(
            device_index=HexList(ChannelUtils.get_device_index(self)), feature_index=self.feature_1861_index)

        get_batt_calibration_info_response = ChannelUtils.send(
            self, get_batt_calibration_info, HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1861.get_battery_calibration_info_response_cls)

        precision_to_10_mv = PowerSupplyConstant.VOLTAGE_SIGNIFICANT_DIGITS - 1
        calibration_points_list = [
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_0)) / 1000, precision_to_10_mv),
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_1)) / 1000, precision_to_10_mv),
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_2)) / 1000, precision_to_10_mv),
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_3)) / 1000, precision_to_10_mv),
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_4)) / 1000, precision_to_10_mv),
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_5)) / 1000, precision_to_10_mv),
            round(int(Numeral(get_batt_calibration_info_response.calibration_point_6)) / 1000, precision_to_10_mv)]

        calibration_points_list_to_store = [0] * 7

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_title_2(self, 'Test Loop over battery voltage values from full to cutoff by step of 0.1')
        # --------------------------------------------------------------------------------------------------------------
        """
         nRF52832 Power Reset
         A step increase in supply voltage of 300 mV or more, with rise time of 300 ms or less, within the valid supply
         range, may result in a system reset.

         So the testing voltage values cannot be [cut-off, full]. Shall reverse it to [full, cut-off] to avoid trigger
         MCU power reset mechanism.

         Reference: nRF52832 datasheet "nRF52832_PS_v1.0", page 80 for more details.
         """
        for i in reversed(range(int(Numeral(get_batt_calibration_info_response.calibration_points_nb)))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send MeasureBattery with tuning the voltage to the requested "
                                     f"calibration point '{str(calibration_points_list[i])} V")
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(calibration_points_list[i])
            measure_battery = self.feature_1861.measure_battery_cls(
                device_index=HexList(ChannelUtils.get_device_index(self)), feature_index=self.feature_1861_index)
            measure_battery_response = ChannelUtils.send(self, measure_battery, HIDDispatcher.QueueName.COMMON,
                                                         response_class_type=self.feature_1861.
                                                         measure_battery_response_cls)

            calibration_points_list_to_store[i] = int(Numeral(measure_battery_response.measure))
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send StoreCalibration with the value gotten from MeasureBattery')
        # --------------------------------------------------------------------------------------------------------------
        store_calibration = self.feature_1861.store_calibration_cls(
            device_index=HexList(ChannelUtils.get_device_index(self)), feature_index=self.feature_1861_index,
            calibration_points_nb=get_batt_calibration_info_response.calibration_points_nb,
            calibration_point_0=calibration_points_list_to_store[0],
            calibration_point_1=calibration_points_list_to_store[1],
            calibration_point_2=calibration_points_list_to_store[2],
            calibration_point_3=calibration_points_list_to_store[3],
            calibration_point_4=calibration_points_list_to_store[4],
            calibration_point_5=calibration_points_list_to_store[5],
            calibration_point_6=calibration_points_list_to_store[6])
        ChannelUtils.send(self, report=store_calibration, response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=self.feature_1861.store_calibration_response_cls, )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send ReadCalibration request')
        # --------------------------------------------------------------------------------------------------------------
        read_calibration = self.feature_1861.read_calibration_cls(device_index=HexList(ChannelUtils.get_device_index(
            self)),
                                                             feature_index=self.feature_1861_index)

        ChannelUtils.send(self, report=read_calibration,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=self.feature_1861.store_calibration_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Battery Calibration is not erased/reset in NVS (NVS_BATT_CALIBRATION_ID)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check Battery Calibration is not erased/reset in NVS (NVS_BATT_CALIBRATION_ID)")

        self.testCaseChecked("ROB_1805_0008", _AUTHOR)
    # end def test_battery_calibration_nvs_retained_on_1861_reset

    @features("Feature1805")
    @features("Feature1A20")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_als_calibration_nvs_retained_on_1a20_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check Ambient Light
        Calibration does not change

        On keyboard, use x1A20 to perform ALS Calibration
        """
        raise NotImplementedError("Feature 0x1A20 was not yet available during 0x1805 test scripts implementation")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1A20 index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform Ambient Light Calibration (0x1A20.MeasureLight, 0x1A20.StoreCalibration,"
                                 "0x1A20.ReadCalibration)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Ambient Light Calibration is not erased/reset in NVS (NVS_ALS_CALIBRATION_ID)")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1805_0009", _AUTHOR)
    # end def test_als_calibration_nvs_retained_on_1a20_reset

    @features("Feature1805")
    @features("Feature1816")
    @features("NvsChunkID", "NVS_BLE_PRO_PRE_PAIRING_ID_X")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_pre_pairing_nvs_retained_on_1816_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check Pre Pairing data do
        not change

        Use 0x1816 to perform pre pairing
        """
        raise NotImplementedError("NVS_BLE_PRO_PRE_PAIRING_ID_X was not available during 0x1805 test scripts "
                                  "implementation")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1816 index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform pre pairing sequence")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Pre Pairing is not erased/reset in NVS (NVS_BLE_PRO_PRE_PAIRING_ID_X)")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1805_0010#1", _AUTHOR)
    # end def test_pre_pairing_nvs_retained_on_1816_reset

    @features("Feature1805")
    @features("Feature1817")
    @features("NvsChunkID", "NVS_BLE_PRO_PRE_PAIRING_ID_X")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_pre_pairing_nvs_retained_on_1817_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check Pre Pairing data do
        not change

        Use 0x1817 to perform pre pairing
        """
        raise NotImplementedError("NVS_BLE_PRO_PRE_PAIRING_ID_X was not available during 0x1805 test scripts "
                                  "implementation")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform pre pairing sequence")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check valid response")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Pre Pairing is not erased/reset in NVS (NVS_BLE_PRO_PRE_PAIRING_ID_X)")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1805_0010#2", _AUTHOR)
    # end def test_pre_pairing_nvs_retained_on_1817_reset

    @features("Feature1805")
    @features("NvsChunkID", "NVS_APP_SECUR_LVL_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_secure_level_nvs_retained_on_reset(self):
        """
        Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check Secure Level do not change

        Force NVS to set App and SD secure levels
        NVS Chunk:
        * NVS_APP_SECUR_LVL_ID
        * NVS_SD_SECUR_LVL_ID
        """
        raise NotImplementedError("NVS_APP_SECUR_LVL_ID was not available during 0x1805 test scripts "
                                  "implementation")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set App and SD Secure Levels (Write NVS)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check App and SD Secure Levels are not erased/reset in NVS (NVS_APP_SECUR_LVL_ID"
                                  "and NVS_SD_SECUR_LVL_ID)")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1805_0011", _AUTHOR)
    # end def test_secure_level_nvs_retained_on_reset

    @features("Feature1805")
    @features("ManageDeactivatableFeaturesAuth")
    @features("NvsChunkID", "NVS_X1E02_STATE_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_deactivate_state_nvs_retained_on_1e02_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check X1E02 State do not
        change

        Use x1E02 to enable/disable features
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable persistent features")
        # --------------------------------------------------------------------------------------------------------------
        persistant_bitmap = DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_info(self).persist_bit_map
        manufacturing = True if persistant_bitmap.manufacturing else False
        compliance = True if persistant_bitmap.compliance else False
        gothard = True if persistant_bitmap.gothard else False

        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing, compliance, gothard)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check X1E02 State is not erased/reset in NVS (NVS_X1E02_STATE_ID)")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        chunk_data = self.memory_manager.get_active_chunk_by_name(chunk_name='NVS_X1E02_STATE_ID',
                                                                  active_bank_only=True)
        if any((manufacturing, compliance, gothard)):
            expected = int(f'0b{int(gothard)}{int(compliance)}{int(manufacturing)}', 2)
            self.assertEqual(expected=HexList(expected), obtained=chunk_data.state_bit_map,
                             msg='NVS_X1E02_STATE_ID should be persistent in NVS')
        else:
            self.assertNone(chunk_data, "No chunk should be stored in NVS for feature 0x1E02 as nothing is persistent")
        # end if

        self.testCaseChecked("ROB_1805_0012", _AUTHOR)
    # end def test_deactivate_state_nvs_retained_on_1e02_reset

    @features("Feature1805")
    @features("Feature1806")
    @features("NvsChunkID", "NVS_EXTENDED_MODEL_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_extended_model_id_nvs_retained_on_1806_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check Extended Model ID does
        not change

        Use 0x1806 to set Device Extended Model ID
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set Device Extended Model Id")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDevicePropertiesTestUtils.SetDeviceExtendModelIDHelper.HIDppHelper.write(
            self, extended_model_id=HexList(0x0))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Device Extended Model Id is not erased/reset in NVS (NVS_EXTENDED_MODEL_ID)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check Device Extended Model Id is not erased/reset in NVS (NVS_EXTENDED_MODEL_ID)")

        self.testCaseChecked("ROB_1805_0013#1", _AUTHOR)
    # end def test_extended_model_id_nvs_retained_on_1806_reset

    @features("Feature1805")
    @features("Feature1807")
    @features("NvsChunkID", "NVS_EXTENDED_MODEL_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_extended_model_id_nvs_retained_on_1807_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check Extended Model ID does
        not change

        Use 0x1807 to set Device Extended Model ID
        """
        self.post_requisite_reload_nvs = True
        property_id = ConfigurableProperties.PropertyId.EXTENDED_MODEL_ID

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set Device Extended Model Id")
        # --------------------------------------------------------------------------------------------------------------
        select_property_response = ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)
        write_property_response = ConfigurablePropertiesTestUtils.HIDppHelper.write_data(self, HexList(0x00))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SelectPropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        checker.check_fields(self, select_property_response, self.feature_1807.select_property_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WritePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        checker.check_fields(self, write_property_response, self.feature_1807.write_property_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Device Extended Model Id is not erased/reset in NVS (NVS_EXTENDED_MODEL_ID)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check Device Extended Model Id is not erased/reset in NVS (NVS_EXTENDED_MODEL_ID)")

        self.testCaseChecked("ROB_1805_0013#2", _AUTHOR)
    # end def test_extended_model_id_nvs_retained_on_1807_reset

    @features("Feature1805")
    @features("Feature1806")
    @features("NvsChunkID", "NEW_EQUAD_NAME")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_equad_short_name_nvs_retained_on_1806_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check EQuad short name does
        not change

        Use 0x1806 to set device properties
        """
        self.post_requisite_reload_nvs = True
        property_id = ConfigurableDeviceProperties.PropertyIdV8.EQUAD_SHORT_NAME

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set EQuad Short Name")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDevicePropertiesTestUtils.SetDevicePropertiesHelper.HIDppHelper.write(
            self, property_id, flag=0, sub_data_index=0, property_data="NEW_EQUAD_NAME")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check EQuad short name is not erased/reset in NVS (NVS_EQUAD_SHORT_NAME_ID)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check EQuad short name is not erased/reset in NVS (NVS_EQUAD_SHORT_NAME_ID)")

        self.testCaseChecked("ROB_1805_0014#1", _AUTHOR)
    # end def test_equad_short_name_nvs_retained_on_1806_reset

    @features("Feature1805")
    @features("Feature1807")
    @features("NvsChunkID", "NVS_EQUAD_SHORT_NAME_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_equad_short_name_nvs_retained_on_1807_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check EQuad short name does
        not change

        Use 0x1807 to set device properties
        """
        self.post_requisite_reload_nvs = True
        property_id = ConfigurableProperties.PropertyId.EQUAD_ID

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set EQuad Short Name")
        # --------------------------------------------------------------------------------------------------------------
        select_property_response = ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)
        write_property_response = ConfigurablePropertiesTestUtils.HIDppHelper.write_data(
            self, data=HexList("NEW_EQUAD_NAME"))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SelectPropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        checker.check_fields(self, select_property_response, self.feature_1807.select_property_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WritePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        checker.check_fields(self, write_property_response, self.feature_1807.write_property_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check EQuad short name is not erased/reset in NVS (NVS_EQUAD_SHORT_NAME_ID)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check EQuad short name is not erased/reset in NVS (NVS_EQUAD_SHORT_NAME_ID)")

        self.testCaseChecked("ROB_1805_0014#2", _AUTHOR)
    # end def test_equad_short_name_nvs_retained_on_1807_reset

    @features("Feature1805")
    @features("Feature1806")
    @features("NvsChunkID", "NVS_BLE_LONG_NAME_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_ble_long_name_nvs_retained_on_1806_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check BLE Long Name does not
        change

        Use 0x1806 to set device properties
        """
        self.post_requisite_reload_nvs = True
        property_id = ConfigurableDeviceProperties.PropertyIdV8.BLE_LONG_NAME

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set BLE Long Name")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurableDevicePropertiesTestUtils.SetDevicePropertiesHelper.HIDppHelper.write(
            self, property_id=property_id, flag=0, sub_data_index=0, property_data="NEW_BLE_LONG_NAME")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check BLE Long Name is not erased/reset in NVS (NVS_BLE_LONG_NAME_ID)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check BLE Long Name is not erased/reset in NVS (NVS_BLE_LONG_NAME_ID)")

        self.testCaseChecked("ROB_1805_0015#1", _AUTHOR)
    # end def test_ble_long_name_nvs_retained_on_1806_reset

    @features("Feature1805")
    @features("Feature1807")
    @features("NvsChunkID", "NVS_BLE_LONG_NAME_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_ble_long_name_nvs_retained_on_1807_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check BLE Long Name does not
        change

        Use 0x1807 to set device properties
        """
        self.post_requisite_reload_nvs = True
        property_id = ConfigurableProperties.PropertyId.BLE_GAP_BL_NAME

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set BLE Long Name")
        # --------------------------------------------------------------------------------------------------------------
        select_property_response = ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id)
        write_property_response = ConfigurablePropertiesTestUtils.HIDppHelper.write_data(
            self, HexList.fromString("NEW_BTLE_LONG_NAME"))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SelectPropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        checker.check_fields(self, select_property_response, self.feature_1807.select_property_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check WritePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.MessageChecker
        checker.check_fields(self, write_property_response, self.feature_1807.write_property_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check BLE Long Name is not erased/reset in NVS (NVS_BLE_LONG_NAME_ID)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check BLE Long Name is not erased/reset in NVS (NVS_BLE_LONG_NAME_ID)")

        self.testCaseChecked("ROB_1805_0015#2", _AUTHOR)
    # end def test_ble_long_name_nvs_retained_on_1807_reset

    @features("Feature0021")
    @features("Feature1805")
    @features("NvsChunkID", "NVS_X0021_32BYTE_ID")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_unique_id_nvs_retained_on_0021_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check Unique Identifier does
        not change

        Use x0021 - regenId to set unique identifier
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0021 index")
        # --------------------------------------------------------------------------------------------------------------
        feature_0021_index = ChannelUtils.update_feature_mapping(self, feature_id=UniqueIdentifier32Bytes.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set Unique Identifier (0x0021.regenId)")
        # --------------------------------------------------------------------------------------------------------------
        regen_id = RegenId(device_index=HexList(ChannelUtils.get_device_index(self)),
                           feature_index=feature_0021_index)
        ChannelUtils.send(self, report=regen_id, response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=RegenIdResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Unique Identifier is not erased/reset in NVS (NVS_X0021_32BYTE_ID)")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check Unique Identifier is not erased/reset in NVS (NVS_X0021_32BYTE_ID)")

        self.testCaseChecked("ROB_1805_0016", _AUTHOR)
    # end def test_unique_id_nvs_retained_on_0021_reset

    @features("Feature1805")
    @features("Feature9209")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_mlx903_calibration_nvs_retained_on_9209_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check MLX903 calibration
        does not change

        Use x9209 to perform calibration
        """
        raise NotImplementedError("Feature 0x9209 was not yet available during 0x1805 script implementation")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x9209 index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform MLX903 calibration (0x9209.Calibrate)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_wireless_device_status_broadcast_event=False,
                   delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check MLX9209 calibration is not erased/reset in NVS (NVS_MLX903_CALIBRATION_ID)")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1805_0017", _AUTHOR)
    # end def test_mlx903_calibration_nvs_retained_on_9209_reset

    @features("Feature1805")
    @features("Feature9203")
    @level("Robustness")
    @services("Debugger")
    @services("HardwareReset")
    def test_iqs624_calibration_nvs_retained_on_9203_reset(self):
        """
        Goal: Check all NVS chunks which should NOT be erased/reset are NOT erased/reset: check IQS624 calibration
        does not change

        Use x9203 to perform calibration
        """
        raise NotImplementedError("Feature 0x9203 was not yet available during 0x1805 test scripts implementation")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x9203 index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform IQS624 calibration (0x9203.StartCalibration, 0x9203.StopCalibration)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check IQS624 calibration is not erased/reset in NVS (NVS_IQS624_CALIBRATION_ID)")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1805_0018", _AUTHOR)
    # end def test_iqs624_calibration_nvs_retained_on_9203_reset

    @features("Feature1805")
    @features("Keyboard")
    @level("Robustness")
    @services("HardwareReset")
    @services("RequiredKeys", (KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_B, KEY_ID.KEYBOARD_LEFT_SHIFT,
              KEY_ID.KEYBOARD_TAB))
    def test_keyboard_corrupted_sequence_does_not_reset_dut(self):
        """
        [Keyboard]

        Goal: Check keyboard corrupted sequence doesn't enter OOB state
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_pair_device = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press Shift+O+Esc+O+Esc+B")
        # --------------------------------------------------------------------------------------------------------------
        for key in [KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O,
                    KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_B]:
            self.button_stimuli_emulator.key_press(key_id=key)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press Esc+O+Shift+O+Esc+B")
        # --------------------------------------------------------------------------------------------------------------
        for key in [KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_O,
                    KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_B]:
            self.button_stimuli_emulator.key_press(key_id=key)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press Esc+O+Esc+O+Shift+B")
        # --------------------------------------------------------------------------------------------------------------
        for key in [KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O,
                    KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_B]:
            self.button_stimuli_emulator.key_press(key_id=key)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press Esc+0+Esc+0+Esc+0")
        # --------------------------------------------------------------------------------------------------------------
        for key in [KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O,
                    KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O]:
            self.button_stimuli_emulator.key_press(key_id=key)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press Tab+O+Esc+O+Esc+B")
        # --------------------------------------------------------------------------------------------------------------
        for key in [KEY_ID.KEYBOARD_TAB, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O,
                    KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_B]:
            self.button_stimuli_emulator.key_press(key_id=key)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power Off/On DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        self.testCaseChecked("ROB_1805_0019", _AUTHOR)
    # end def test_keyboard_corrupted_sequence_does_not_reset_dut
# end class OobStateRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
