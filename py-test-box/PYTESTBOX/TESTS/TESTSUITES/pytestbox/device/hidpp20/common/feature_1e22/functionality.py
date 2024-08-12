#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1e22.functionality
:brief: HID++ 2.0 ``SPIDirectAccess`` functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/11/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.spidirectaccess import SPIDirectAccess
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.base.spidirectaccessutils import OpticalSensorName
from pytestbox.device.base.spidirectaccessutils import SPIDirectAccessTestUtils
from pytestbox.device.base.spidirectaccessutils import SPI_DATA_MAX_LEN
from pytestbox.device.base.spidirectaccessutils import SPI_PERIPHERAL_REGISTER_DICT
from pytestbox.device.hidpp20.common.feature_1e22.spidirectaccess import SPIDirectAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SPIDirectAccessFunctionalityTestCase(SPIDirectAccessTestCase):
    """
    Validate ``SPIDirectAccess`` functionality test cases
    """

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @level("Functionality")
    @services("OpticalSensor")
    def test_disabled_enable_fw_access(self):
        """
        Verify the MCU FW can't communicate/can communicate with the selected SPI peripheral when the disableFwAccess
        is disabled/enabled
        """
        device_idx = 0
        self.access_config.disable_fw_access = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        response = SPIDirectAccessTestUtils.HIDppHelper.select_device(test_case=self,
                                                                      device_idx=device_idx,
                                                                      access_config=self.access_config)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Wait selectDevice response and check the accessConfig equal to {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        access_config_check_map = SPIDirectAccessTestUtils.AccessConfigChecker.get_check_map(
            access_config=self.access_config)
        check_map.update({
            "device_idx": (checker.check_device_idx, device_idx),
            "access_config": (checker.check_access_config, access_config_check_map)
        })
        checker.check_fields(self, response, self.feature_1e22.select_device_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform user actions from the corresponding SPI peripheral (i.e mouse movement)")
        # --------------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=1, dy=1)
        self.motion_emulator.commit_actions()
        # Start Sensor Emulator model update
        self.motion_emulator._kosmos.dt.pes.execute(action=self.motion_emulator.module.action_event.START)
        # Wait until Sensor Emulator finishes its sequence
        self.motion_emulator._kosmos.dt.pes.wait(action=self.motion_emulator.module.resume_event.FIFO_UNDERRUN)
        # Run test sequence
        self.motion_emulator._kosmos.dt.sequencer.play_sequence(block=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check no corresponding HID report is received from the DUT")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=2)

        self.access_config.disable_fw_access = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        response = SPIDirectAccessTestUtils.HIDppHelper.select_device(test_case=self,
                                                                      device_idx=device_idx,
                                                                      access_config=self.access_config)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Wait selectDevice response and check the accessConfig equal to {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        access_config_check_map = SPIDirectAccessTestUtils.AccessConfigChecker.get_check_map(
            access_config=self.access_config)
        check_map.update({
            "device_idx": (checker.check_device_idx, device_idx),
            "access_config": (checker.check_access_config, access_config_check_map)
        })
        checker.check_fields(self, response, self.feature_1e22.select_device_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the corresponding HID report is received from the DUT")
        # --------------------------------------------------------------------------------------------------------------
        hid_report = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID)
        self.assertNotNone(obtained=hid_report, msg='No HID report received')

        self.testCaseChecked("FUN_1E22_0001", _AUTHOR)
    # end def test_disabled_enable_fw_access

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @features("RequiredOpticalSensors", (OpticalSensorName.HERO2, OpticalSensorName.HERO,
                                         OpticalSensorName.TCOB_TRACKBALL, OpticalSensorName.TCOB_NO_TRACKBALL,
                                         OpticalSensorName.PAW3333, OpticalSensorName.TOG6, OpticalSensorName.PLUTO))
    @level("Functionality")
    def test_enable_atomic_cs(self):
        """
        Verify the MCU can get the 'ProductID' by sending spiDirectAccess request, when the enableAtomicCS is enabled
        """
        device_idx = 0
        self.access_config.enable_atomic_cs = 1
        optical_sensor_name = self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        response = SPIDirectAccessTestUtils.HIDppHelper.select_device(test_case=self,
                                                                      device_idx=device_idx,
                                                                      access_config=self.access_config)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Wait selectDevice response and check the accessConfig equal to {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        access_config_check_map = SPIDirectAccessTestUtils.AccessConfigChecker.get_check_map(
            access_config=self.access_config)
        check_map.update({
            "device_idx": (checker.check_device_idx, device_idx),
            "access_config": (checker.check_access_config, access_config_check_map)
        })
        checker.check_fields(self, response, self.feature_1e22.select_device_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over n_bytes in range [1..15]")
        # --------------------------------------------------------------------------------------------------------------
        for n_bytes in range(1, 16):
            data_in = [SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['product_id']['address']] * n_bytes
            data_out = [SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['product_id']['value']] * n_bytes + \
                       [0] * (SPI_DATA_MAX_LEN - n_bytes)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self,
                               f"Send spiDirectAccess with nBytes = {n_bytes}, DataIn = {data_in}")
            # ----------------------------------------------------------------------------------------------------------
            # This step might trigger watchdog reset due to hardware limitation of the SPI peripheral.
            response = SPIDirectAccessTestUtils.send_spi_command(test_case=self, command=data_in, n_bytes=n_bytes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait spiDirectAccess response and check DataOut value match the ProductID of"
                                      "the SPI peripheral")
            # ----------------------------------------------------------------------------------------------------------
            checker = SPIDirectAccessTestUtils.SpiDirectAccessResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "n_bytes": (checker.check_n_bytes, n_bytes),
                "data_out_1": (checker.check_data_out_1, data_out[0]),
                "data_out_2": (checker.check_data_out_2, data_out[1]),
                "data_out_3": (checker.check_data_out_3, data_out[2]),
                "data_out_4": (checker.check_data_out_4, data_out[3]),
                "data_out_5": (checker.check_data_out_5, data_out[4]),
                "data_out_6": (checker.check_data_out_6, data_out[5]),
                "data_out_7": (checker.check_data_out_7, data_out[6]),
                "data_out_8": (checker.check_data_out_8, data_out[7]),
                "data_out_9": (checker.check_data_out_9, data_out[8]),
                "data_out_10": (checker.check_data_out_10, data_out[9]),
                "data_out_11": (checker.check_data_out_11, data_out[10]),
                "data_out_12": (checker.check_data_out_12, data_out[11]),
                "data_out_13": (checker.check_data_out_13, data_out[12]),
                "data_out_14": (checker.check_data_out_14, data_out[13]),
                "data_out_15": (checker.check_data_out_15, data_out[14]),
            })
            checker.check_fields(self, response, self.feature_1e22.spi_direct_access_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1E22_0002", _AUTHOR)
    # end def test_enable_atomic_cs

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @level("Functionality")
    def test_disable_atomic_cs(self):
        """
        Verify the MCU FW can get the 'ProductID' by sending spiDirectAccess request, when the enableAtomicCS is
        disabled
        """
        device_idx = 0
        optical_sensor_name = self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        response = SPIDirectAccessTestUtils.HIDppHelper.select_device(test_case=self,
                                                                      device_idx=device_idx,
                                                                      access_config=self.access_config)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Wait selectDevice response and check the accessConfig equal to {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        access_config_check_map = SPIDirectAccessTestUtils.AccessConfigChecker.get_check_map(
            access_config=self.access_config)
        check_map.update({
            "device_idx": (checker.check_device_idx, device_idx),
            "access_config": (checker.check_access_config, access_config_check_map)
        })
        checker.check_fields(self, response, self.feature_1e22.select_device_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over n_bytes in range [1..15]")
        # --------------------------------------------------------------------------------------------------------------
        for n_bytes in range(1, 16):
            data_in = [SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['product_id']['address']] * n_bytes
            data_out = [SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['product_id']['value']] * n_bytes + \
                       [0] * (SPI_DATA_MAX_LEN - n_bytes)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self,
                               f"Send spiDirectAccess with nBytes = {n_bytes}, DataIn = {data_in}")
            # ----------------------------------------------------------------------------------------------------------
            response = SPIDirectAccessTestUtils.send_spi_command(test_case=self, command=data_in, n_bytes=n_bytes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait spiDirectAccess response and check DataOut value match the ProductID of"
                                      "the SPI peripheral")
            # ----------------------------------------------------------------------------------------------------------
            checker = SPIDirectAccessTestUtils.SpiDirectAccessResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "n_bytes": (checker.check_n_bytes, n_bytes),
                "data_out_1": (checker.check_data_out_1, data_out[0]),
                "data_out_2": (checker.check_data_out_2, data_out[1]),
                "data_out_3": (checker.check_data_out_3, data_out[2]),
                "data_out_4": (checker.check_data_out_4, data_out[3]),
                "data_out_5": (checker.check_data_out_5, data_out[4]),
                "data_out_6": (checker.check_data_out_6, data_out[5]),
                "data_out_7": (checker.check_data_out_7, data_out[6]),
                "data_out_8": (checker.check_data_out_8, data_out[7]),
                "data_out_9": (checker.check_data_out_9, data_out[8]),
                "data_out_10": (checker.check_data_out_10, data_out[9]),
                "data_out_11": (checker.check_data_out_11, data_out[10]),
                "data_out_12": (checker.check_data_out_12, data_out[11]),
                "data_out_13": (checker.check_data_out_13, data_out[12]),
                "data_out_14": (checker.check_data_out_14, data_out[13]),
                "data_out_15": (checker.check_data_out_15, data_out[14]),
            })
            checker.check_fields(self, response, self.feature_1e22.spi_direct_access_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1E22_0003", _AUTHOR)
    # end def test_disable_atomic_cs

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @level("Functionality")
    @bugtracker("SelectDevice_MismatchDeviceIndex")
    def test_spi_direct_access_with_all_available_device(self):
        """
        Verify the spiDirectAccess request with all available SPI peripherals
        """
        supported_spi_peripherals = self.config.F_SpiPeripherals if self.config.F_SpiPeripherals is not None \
            else [self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]
        default_access_config = SPIDirectAccess.AccessConfig(enable_atomic_cs=0, disable_fw_access=0)
        self.access_config.disable_fw_access = 1
        self.access_config.enable_atomic_cs = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over device_idx in range [0..{self.config.F_NumberOfDevices}]")
        # --------------------------------------------------------------------------------------------------------------
        for device_idx in range(0, self.config.F_NumberOfDevices):
            if supported_spi_peripherals[device_idx] in SPI_PERIPHERAL_REGISTER_DICT.keys():
                register_name = list(SPI_PERIPHERAL_REGISTER_DICT[supported_spi_peripherals[device_idx]].items())[0][1]
                n_bytes = 1
                data_in = [register_name['address']] * n_bytes
                data_out = [register_name['value']] * n_bytes + [0] * (SPI_DATA_MAX_LEN - n_bytes)
            else:
                raise ValueError("Unsupported SPI peripheral")
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {self.access_config}")
            # ----------------------------------------------------------------------------------------------------------
            response = SPIDirectAccessTestUtils.HIDppHelper.select_device(test_case=self,
                                                                          device_idx=device_idx,
                                                                          access_config=self.access_config)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f"Wait selectDevice response and check the accessConfig equal to {self.access_config}")
            # ----------------------------------------------------------------------------------------------------------
            checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
            check_map = checker.get_default_check_map(self)
            access_config_check_map = SPIDirectAccessTestUtils.AccessConfigChecker.get_check_map(
                access_config=self.access_config)
            check_map.update({
                "device_idx": (checker.check_device_idx, device_idx),
                "access_config": (checker.check_access_config, access_config_check_map)
            })
            checker.check_fields(self, response, self.feature_1e22.select_device_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self,
                               f"Send spiDirectAccess with nBytes = {n_bytes}, DataIn = {data_in}")
            # ----------------------------------------------------------------------------------------------------------
            response = SPIDirectAccessTestUtils.send_spi_command(test_case=self, command=data_in, n_bytes=n_bytes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Wait spiDirectAccess response and check DataOut value match the ProductID of"
                                      "the SPI peripheral")
            # ----------------------------------------------------------------------------------------------------------
            checker = SPIDirectAccessTestUtils.SpiDirectAccessResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "n_bytes": (checker.check_n_bytes, n_bytes),
                "data_out_1": (checker.check_data_out_1, data_out[0]),
                "data_out_2": (checker.check_data_out_2, data_out[1]),
                "data_out_3": (checker.check_data_out_3, data_out[2]),
                "data_out_4": (checker.check_data_out_4, data_out[3]),
                "data_out_5": (checker.check_data_out_5, data_out[4]),
                "data_out_6": (checker.check_data_out_6, data_out[5]),
                "data_out_7": (checker.check_data_out_7, data_out[6]),
                "data_out_8": (checker.check_data_out_8, data_out[7]),
                "data_out_9": (checker.check_data_out_9, data_out[8]),
                "data_out_10": (checker.check_data_out_10, data_out[9]),
                "data_out_11": (checker.check_data_out_11, data_out[10]),
                "data_out_12": (checker.check_data_out_12, data_out[11]),
                "data_out_13": (checker.check_data_out_13, data_out[12]),
                "data_out_14": (checker.check_data_out_14, data_out[13]),
                "data_out_15": (checker.check_data_out_15, data_out[14]),
            })
            checker.check_fields(self, response, self.feature_1e22.spi_direct_access_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send selectDevice request to reset the accessConfig to the default value")
            # ----------------------------------------------------------------------------------------------------------
            response = SPIDirectAccessTestUtils.HIDppHelper.select_device(test_case=self,
                                                                          device_idx=device_idx,
                                                                          access_config=default_access_config)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, f"Wait selectDevice response and check the accessConfig equal to {default_access_config}")
            # ----------------------------------------------------------------------------------------------------------
            checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
            check_map = checker.get_default_check_map(self)
            access_config_check_map = SPIDirectAccessTestUtils.AccessConfigChecker.get_check_map(
                access_config=default_access_config)
            check_map.update({
                "device_idx": (checker.check_device_idx, device_idx),
                "access_config": (checker.check_access_config, access_config_check_map)
            })
            checker.check_fields(self, response, self.feature_1e22.select_device_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1E22_0004", _AUTHOR)
    # end def test_spi_direct_access_with_all_available_device

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @level("Functionality")
    @bugtracker("SelectDevice_MismatchDeviceIndex")
    def test_get_access_config_from_selected_device(self):
        """
        Verify the getSelectedDevice request can return the latest change of accessConfig that changed by
        selectedDevice request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over access_config in range [0..3]")
        # --------------------------------------------------------------------------------------------------------------
        for access_config in range(0, 4):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Test Loop over device_idx in range [0..{self.config.F_NumberOfDevices}]")
            # ----------------------------------------------------------------------------------------------------------
            for device_idx in range(0, self.config.F_NumberOfDevices):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {access_config}")
                # ------------------------------------------------------------------------------------------------------
                response = SPIDirectAccessTestUtils.HIDppHelper.select_device(test_case=self,
                                                                              device_idx=device_idx,
                                                                              access_config=access_config)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Wait selectDevice response and check the accessConfig equal to {access_config}")
                # ------------------------------------------------------------------------------------------------------
                checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
                check_map = checker.get_default_check_map(self)
                access_config_check_map = SPIDirectAccessTestUtils.AccessConfigChecker.get_check_map(
                    access_config=access_config)
                check_map.update({
                    "device_idx": (checker.check_device_idx, device_idx),
                    "access_config": (checker.check_access_config, access_config_check_map)
                })
                checker.check_fields(self, response, self.feature_1e22.select_device_response_cls, check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send getSelectedDevice request")
                # ------------------------------------------------------------------------------------------------------
                response = SPIDirectAccessTestUtils.HIDppHelper.get_selected_device(test_case=self)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                    self, f"Wait getSelectedDevice response and check the accessConfig = {access_config}")
                # ------------------------------------------------------------------------------------------------------
                checker = SPIDirectAccessTestUtils.GetSelectedDeviceResponseChecker
                check_map = checker.get_default_check_map(self)
                access_config_check_map = SPIDirectAccessTestUtils.AccessConfigChecker.get_check_map(
                    access_config=access_config)
                check_map.update({
                    "device_idx": (checker.check_device_idx, device_idx),
                    "access_config": (checker.check_access_config, access_config_check_map)
                })
                checker.check_fields(self, response, self.feature_1e22.get_selected_device_response_cls, check_map)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Send selectDevice request with accessConfig = 0 to restore the accessConfig "
                                         "to its initial state")
                # ------------------------------------------------------------------------------------------------------
                SPIDirectAccessTestUtils.HIDppHelper.select_device(test_case=self,
                                                                   device_idx=device_idx,
                                                                   access_config=0)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "End Test Loop")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1E22_0005", _AUTHOR)
    # end def test_get_access_config_from_selected_device

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @level("Functionality")
    @services("RequiredKeys", (KEY_ID.BUTTON_1,))
    def test_access_config_reset_after_deep_sleep(self):
        """
        Verify the accessConfig settings are reset to the default value, after the device is wake-up from the
        deep-sleep mode
        """
        device_idx = 0
        self.access_config.disable_fw_access = 1
        self.access_config.enable_atomic_cs = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        response = SPIDirectAccessTestUtils.HIDppHelper.select_device(
            test_case=self, device_idx=device_idx, access_config=self.access_config)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Wait selectDevice request and check the accessConfig equal to {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        access_config_check_map = SPIDirectAccessTestUtils.AccessConfigChecker.get_check_map(
            access_config=self.access_config)
        check_map.update({
            "device_idx": (checker.check_device_idx, device_idx),
            "access_config": (checker.check_access_config, access_config_check_map)
        })
        checker.check_fields(self, response, self.feature_1e22.select_device_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send 0x1830.setPowerMode request with powerMode = 3 (deep-sleep mode)")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to wake up the device")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSelectedDevice request with accessConfig")
        # --------------------------------------------------------------------------------------------------------------
        response = SPIDirectAccessTestUtils.HIDppHelper.get_selected_device(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getSelectedDevice response and check the accessConfig is reset")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.GetSelectedDeviceResponseChecker
        checker.check_fields(self, response, self.feature_1e22.get_selected_device_response_cls)

        self.testCaseChecked("FUN_1E22_0006", _AUTHOR)
    # end def test_access_config_reset_after_deep_sleep

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @level("Functionality")
    def test_access_config_reset_after_power_cycle(self):
        """
        Verify the accessConfig settings are reset to the default value, after a device power cycle
        """
        device_idx = 0
        self.access_config.disable_fw_access = 1
        self.access_config.enable_atomic_cs = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        response = SPIDirectAccessTestUtils.HIDppHelper.select_device(
            test_case=self, device_idx=device_idx, access_config=self.access_config)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Wait selectDevice request and check the accessConfig equal to {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        access_config_check_map = SPIDirectAccessTestUtils.AccessConfigChecker.get_check_map(
            access_config=self.access_config)
        check_map.update({
            "device_idx": (checker.check_device_idx, device_idx),
            "access_config": (checker.check_access_config, access_config_check_map)
        })
        checker.check_fields(self, response, self.feature_1e22.select_device_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power OFF -> ON the device")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSelectedDevice request with accessConfig")
        # --------------------------------------------------------------------------------------------------------------
        response = SPIDirectAccessTestUtils.HIDppHelper.get_selected_device(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getSelectedDevice response and check the accessConfig is reset")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.GetSelectedDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_idx": (checker.check_device_idx, device_idx)
        })
        checker.check_fields(self, response, self.feature_1e22.get_selected_device_response_cls, check_map)

        self.testCaseChecked("FUN_1E22_0007", _AUTHOR)
    # end def test_access_config_reset_after_power_cycle

    @features("Feature1E22")
    @features("Feature1E22WithSpiPeripheral")
    @level("Functionality")
    def test_enable_fw_access_and_atomic_cs(self):
        """
        Verify the user can access a SPI device thru spiDirectAccess, when the disableFwAccess and enableAtomicCS are
        enabled.
        """
        device_idx = 0
        self.access_config.disable_fw_access = 1
        self.access_config.enable_atomic_cs = 1
        optical_sensor_name = self.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send selectDevice request with accessConfig = {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        response = SPIDirectAccessTestUtils.HIDppHelper.select_device(test_case=self,
                                                                      device_idx=device_idx,
                                                                      access_config=self.access_config)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Wait selectDevice response and check the accessConfig equal to {self.access_config}")
        # --------------------------------------------------------------------------------------------------------------
        checker = SPIDirectAccessTestUtils.SelectDeviceResponseChecker
        check_map = checker.get_default_check_map(self)
        access_config_check_map = SPIDirectAccessTestUtils.AccessConfigChecker.get_check_map(
            access_config=self.access_config)
        check_map.update({
            "device_idx": (checker.check_device_idx, device_idx),
            "access_config": (checker.check_access_config, access_config_check_map)
        })
        checker.check_fields(self, response, self.feature_1e22.select_device_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self,
                           f"Send spiDirectAccess with nBytes = 1, "
                           f"DataIn = {SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['product_id']['address']}")
        # --------------------------------------------------------------------------------------------------------------
        product_id = SPIDirectAccessTestUtils.get_product_id(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait spiDirectAccess response and check DataOut value match the ProductID of the"
                                  "SPI peripheral")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['product_id']['value'],
                         obtained=product_id,
                         msg='The obtained product_id is different from the expected.')

        self.testCaseChecked("FUN_1E22_0008", _AUTHOR)
    # end def test_enable_fw_access_and_atomic_cs
# end class SPIDirectAccessFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
