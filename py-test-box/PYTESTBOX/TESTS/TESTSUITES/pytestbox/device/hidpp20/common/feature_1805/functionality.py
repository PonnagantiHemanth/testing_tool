#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1805.functionality
:brief: HID++ 2.0 ``OobState`` functionality test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/09/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings
from itertools import zip_longest
from random import choices
from string import ascii_uppercase
from string import digits
from time import perf_counter
from time import sleep

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HID_REPORTS
from pyhid.hid.usbhidusagetable import STANDARD_KEYS
from pyhid.hiddata import HidData
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.backlight import Backlight
from pyhid.hidpp.features.common.changehost import GetCookiesResponse
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyName
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyNameFactory
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomization
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControl
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControlFactory
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtons
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsFactory
from pyhid.hidpp.features.configchange import ConfigChange
from pyhid.hidpp.features.configchange import GetConfigurationCookie
from pyhid.hidpp.features.configchange import GetConfigurationCookieResponse
from pyhid.hidpp.features.configchange import SetConfigurationComplete
from pyhid.hidpp.features.configchange import SetConfigurationCompleteResponse
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.features.hireswheel import HiResWheel
from pyhid.hidpp.features.hireswheel import HiResWheelFactory
from pyhid.hidpp.features.keyboard.disablekeys import DisableKeys
from pyhid.hidpp.features.keyboard.disablekeys import DisableKeysFactory
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeysByUsage
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeysByUsageFactory
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pyhid.hidpp.features.mouse.analysismode import AnalysisMode
from pyhid.hidpp.features.mouse.ratchetwheel import RatchetWheel
from pyhid.hidpp.features.mouse.smartshift import SmartShift
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunable
from pyhid.hidpp.features.mouse.thumbwheel import Thumbwheel
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.ledid import CONNECTIVITY_STATUS_LEDS
from pylibrary.emulator.ledid import LED_ID
from pylibrary.mcu.connectchunks import ConnectIdChunkData
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pyraspi.services.kosmos.leds.leddataparser import SchemeType
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.adjustabledpiutils import AdjustableDpiTestUtils
from pytestbox.device.base.analysismodeutils import AnalysisModeTestUtils
from pytestbox.device.base.backlightutils import BacklightTestUtils
from pytestbox.device.base.brightnesscontrolutils import BrightnessControlTestUtils
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.changehostutils import get_cookie_list
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicefriendlynameutils import DeviceFriendlyNameTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.disablekeysbyusageutils import DisableKeysByUsageTestUtils
from pytestbox.device.base.disablekeysutils import DisableKeysUtils
from pytestbox.device.base.extendedadjustabledpiutils import ExtendedAdjustableDpiTestUtils
from pytestbox.device.base.extendedadjustablereportrateutils import ExtendedAdjustableReportRateTestUtils
from pytestbox.device.base.fninversionformultihostdevicesutils import FnInversionForMultiHostDevicesTestUtils
from pytestbox.device.base.fullkeycustomizationutils import FullKeyCustomizationTestUtils
from pytestbox.device.base.hostsinfoutils import HostsInfoTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.multiplatformutils import MultiPlatformTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.oobstateutils import OobStateTestUtils
from pytestbox.device.base.perkeylightingutils import PerKeyLightingTestUtils
from pytestbox.device.base.ratchetwheelutils import RatchetWheelTestUtils
from pytestbox.device.base.reportrateutils import ReportRateTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.base.smartshiftunableutils import SmartShiftTunableTestUtils
from pytestbox.device.base.thumbwheelutils import ThumbwheelTestUtils
from pytestbox.device.hidpp20.common.feature_1805.oobstate import OobStateTestCase
from pytestbox.device.hidpp20.mouse.feature_2110_interface import set_ratchet_control_mode
from pytestbox.device.hidpp20.mouse.feature_2110_interface import verify_ratchet_control_mode
from pytestbox.receiver.base.receiverbasetestutils import ReceiverBaseTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.equaddeviceconnectionutils import EQuadDeviceConnectionUtils
from pytestbox.shared.base.specialkeysmsebuttonsutils import SpecialKeysMseButtonsTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_SEND_OOB = "Send SetOobState"
_SEND_OOB_AND_POWER_CYCLE = "Send SetOobState and Power Cycle"
_CHECK_LED_FAST_BLINK = "Check all LEDs blink fast"
_POWER_CYCLE = "Power Off/On DUT"
_CONNECTION_LOST = "Check connection is lost"
_END_LOOP = "End test loop"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OobStateFunctionalityTestCase(OobStateTestCase):
    """
    Validate ``OobState`` functionality test cases
    """
    ONE_SECOND = 1
    FIVE_SECONDS = 5
    TWENTY_SECONDS = 20
    SEC_TO_MILLI_SEC = 1000

    @features("Feature1805")
    @features("Feature1814")
    @features("MultipleChannels")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_check_all_hosts_connection_lost_on_power_cycle(self):
        """
        Validate the connections with all hosts are lost, at next power on
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        self.feature_1814_index, self.feature_1814, _, _ = ChangeHostTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Pair DUT with multiple host")
        # --------------------------------------------------------------------------------------------------------------
        for host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            if host + 1 != HOST.CH1:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Pair device with host {host + 1}")
                # ------------------------------------------------------------------------------------------------------
                OobStateTestUtils.pair_device(self, host=host)
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over paired hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host_index in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send SetCurrentHost with hostIndex={host_index}')
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1814.set_current_host_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1814_index,
                host_index=host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check connection is lost, i.e. check ERR_CONNECT_FAIL received on HID++ request")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.clean_messages(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                class_type=Hidpp1ErrorCodes
            )
            error_response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)
            self.assertEqual(error_response.ERROR_CODE, Hidpp1ErrorCodes.ERR_CONNECT_FAIL)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0001", _AUTHOR)
    # end def test_check_all_hosts_connection_lost_on_power_cycle

    @features("Feature1805")
    @features("NoUSB")
    @features("NoUnifying")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_ble_pairing_data_erased(self):
        """
        Validate all pairing data are erased or loaded with default values, for BT/BTLE

        Perform pairing, then set OOB State and check pairing data in NVS are erased
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        nvs_list = ['NVS_CONNECT_ID', 'NVS_BTLDR_CONNECT_ID', 'NVS_BLE_LAST_GAP_ADDR_USED']

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check pairing data in NVS are erased/reset")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        for nvs_chunk in nvs_list:
            chunk_data = self.memory_manager.get_chunks_by_name(chunk_name=nvs_chunk, active_bank_only=True)
            if nvs_chunk == 'NVS_CONNECT_ID':
                if self.f.PRODUCT.DEVICE.F_NbHosts == 3:
                    self.assertEqual(obtained=chunk_data[0].data.pairing_src_1,
                                     expected=HexList(ConnectIdChunkData.PairingSrc.NONE),
                                     msg=f'{nvs_chunk}.data.pairing_src_1 should be None in NVS')
                    self.assertEqual(obtained=chunk_data[0].data.scheme_host_1,
                                     expected=HexList(ConnectIdChunkData.STATUS.OOB),
                                     msg=f'{nvs_chunk}.data.scheme_host_1 Data should be Unpaired in NVS')
                    self.assertEqual(obtained=chunk_data[0].data.pairing_src_2,
                                     expected=HexList(ConnectIdChunkData.PairingSrc.NONE),
                                     msg=f'{nvs_chunk}.data.pairing_src_2 Data should be None in NVS')
                    self.assertEqual(obtained=chunk_data[0].data.scheme_host_2,
                                     expected=HexList(ConnectIdChunkData.STATUS.OOB),
                                     msg=f'{nvs_chunk}.data.scheme_host_2 should be Unpaired in NVS')
                # end if

                self.assertEqual(obtained=chunk_data[0].data.pairing_src_0,
                                 expected=HexList(ConnectIdChunkData.PairingSrc.NONE),
                                 msg=f'{nvs_chunk}.data.pairing_src_0 Data should be empty in NVS'),
                self.assertEqual(obtained=chunk_data[0].data.scheme_host_0,
                                 expected=HexList(ConnectIdChunkData.STATUS.OOB),
                                 msg=f'{nvs_chunk}.data.scheme_host_0 should be Unpaired in NVS')

            elif nvs_chunk == 'NVS_BTLDR_CONNECT_ID':
                self.assertEqual(obtained=chunk_data[0].host_idx, expected=HexList("00"),
                                 msg=f'{nvs_chunk}.host_idx should be 0 in NVS')
                expected_protocol = HexList(ConnectIdChunkData.Protocol.BLE)
                self.assertEqual(obtained=chunk_data[0].protocol, expected=expected_protocol,
                                 msg=f'{nvs_chunk}.protocol should be {expected_protocol} in NVS')

            elif nvs_chunk == 'NVS_BLE_LAST_GAP_ADDR_USED':
                if self.last_ble_address is not None:
                    min_addr = Numeral(HexList(reversed(self.last_ble_address)))
                    curr_address = Numeral(HexList(reversed(chunk_data[-1].device_bluetooth_address)))
                    self.assertFalse(
                        min_addr <= curr_address <= (min_addr + DiscoveryTestUtils.AUTH_BLE_ADDR_COUNT),
                        f"Bluetooth address {Numeral(HexList(reversed(chunk_data[-1].device_bluetooth_address)))}"
                        f" shall not be in the range {min_addr} - {min_addr + DiscoveryTestUtils.AUTH_BLE_ADDR_COUNT}")
                # end if

            elif chunk_data is not None:
                self.assertEqual(obtained=len(chunk_data),
                                 expected=0,
                                 msg=f'{nvs_chunk} should be empty in NVS')
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _END_LOOP)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0002", _AUTHOR)
    # end def test_ble_pairing_data_erased

    @features("Feature0007")
    @features("Feature1805")
    @features("NvsChunkID", "NVS_DEVICE_FRIENDLY_NAME_ID")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_device_friendly_name_on_0007_reset_nvs(self):
        """
        Validate all NVS chunks which should be erased/reset are erased/reset: check Device Friendly Name is reset

        Use feature 0x0007 to set Friendly Name, then set OOB State and check Friendly Name is deleted
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0007 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0007_index, self.feature_0007, _, _ = DeviceFriendlyNameTestUtils.HIDppHelper.get_parameters(
            self, DeviceFriendlyName.FEATURE_ID, DeviceFriendlyNameFactory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetFriendlyName request with new name")
        # --------------------------------------------------------------------------------------------------------------
        # Size of name_chunk to read/write coming from 0x1807 properties if any, else from 0x0007 settings
        friendly_name_len = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(
            self, ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME)
        if friendly_name_len == 0:
            friendly_name_len = self.f.PRODUCT.FEATURES.COMMON.DEVICE_FRIENDLY_NAME.F_NameMaxLength
        # end if

        payload_size = self.feature_0007.set_friendly_name_cls.LEN.NAME_CHUNK // 8
        if friendly_name_len > payload_size:
            warnings.warn("Tests scripts might not cover this case correctly yet. TODO: if this becomes necessary, "
                          "please check scripts and update.")
        # end if

        name_chunk_length = min(payload_size, friendly_name_len)
        test_name_chunk = ''.join(choices(ascii_uppercase + digits, k=name_chunk_length))
        DeviceFriendlyNameTestUtils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(
            self, byte_index=0, name_chunk=test_name_chunk)
        friendly_name = DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.HIDppHelper.get_friendly_name(
            self, byte_index=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate new friendly name and friendly name length is set as expected")
        # --------------------------------------------------------------------------------------------------------------
        DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.MessageChecker.check_length(
            self, len(friendly_name), len(test_name_chunk))
        DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.MessageChecker.check_name_match(
            self, friendly_name, test_name_chunk)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Friendly Name is deleted in NVS")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        chunk_data = self.memory_manager.get_chunks_by_name(chunk_name='NVS_DEVICE_FRIENDLY_NAME_ID')
        self.assertEqual(expected=0, obtained=len(chunk_data),
                         msg='NVS_DEVICE_FRIENDLY_NAME_ID should be empty in NVS')

        self.testCaseChecked("FUN_1805_0003", _AUTHOR)
    # end def test_device_friendly_name_on_0007_reset_nvs

    @features("Feature1805")
    @features("Feature1814")
    @features("NvsChunkID", "NVS_1814_COOKIES_ID")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_cookies_on_1814_reset_nvs(self):
        """
        [Multi Host]
        Validate all NVS chunks which should be erased/reset are erased/reset: check 0x1814 Cookies are reset

        Use feature 0x1814 to set cookies, then set OOB State and check cookies are deleted
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1814 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1814_index, self.feature_1814, _, _ = ChangeHostTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            if host + 1 != HOST.CH1:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Pair device with host {host + 1}")
                # ------------------------------------------------------------------------------------------------------
                OobStateTestUtils.pair_device(self, host=host)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetCookies request with cookie value greater than 0")
            # ----------------------------------------------------------------------------------------------------------
            if self.f.PRODUCT.DEVICE.F_NbHosts == 1:
                host_index = 0
            else:
                host_index = ChangeHostTestUtils.HIDppHelper.get_host_info(self).curr_host
            # end if

            ChangeHostTestUtils.HIDppHelper.set_cookie(test_case=self, host_index=host_index, cookie=HexList("01"))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Cookies are saved in NVS")
            # ----------------------------------------------------------------------------------------------------------
            self.memory_manager.read_nvs()
            chunk_data = self.memory_manager.get_chunks_by_name(chunk_name='NVS_1814_COOKIES_ID',
                                                                active_bank_only=True)
            self.assertNotEqual(obtained=len(chunk_data),
                                unexpected=0,
                                msg='NVS_1814_COOKIES_ID should not be empty in NVS')
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported hosts")
        # --------------------------------------------------------------------------------------------------------------
        self.last_ble_address = None
        for host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Pair device with host {host + 1}")
            # ----------------------------------------------------------------------------------------------------------
            OobStateTestUtils.pair_device(self, host=host)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check Cookies are deleted in NVS")
            # ----------------------------------------------------------------------------------------------------------
            self.memory_manager.read_nvs()
            chunk_data = self.memory_manager.get_chunks_by_name(chunk_name='NVS_1814_COOKIES_ID',
                                                                active_bank_only=True)
            self.assertEqual(obtained=len(chunk_data),
                             expected=0,
                             msg='NVS_1814_COOKIES_ID should not be empty in NVS')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0004#1", _AUTHOR)
    # end def test_cookies_on_1814_reset_nvs

    @features("Feature1805")
    @features("Feature1814")
    @features("NvsChunkID", "NVS_1814_COOKIES_ID")
    @level("Functionality")
    @services("HardwareReset")
    def test_cookies_on_1814_reset(self):
        """
        [Multi Host]
        Validate the cookies parameter linked to the 0x1814 feature are restored to their default values

        Use 0x1814 to set cookie and get cookies
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1814")
        # --------------------------------------------------------------------------------------------------------------
        _, feature_1814, _, _ = ChangeHostTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Delete Cookie from NVS")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.nvs_parser.delete_chunk("NVS_1814_COOKIES_ID")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            if host + 1 != HOST.CH1:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Pair device with host {host + 1}")
                # ------------------------------------------------------------------------------------------------------
                OobStateTestUtils.pair_device(self, host=host)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetCookie request with cookie value greater than 0")
            # ----------------------------------------------------------------------------------------------------------
            if self.f.PRODUCT.DEVICE.F_NbHosts == 1:
                host_index = 0
            else:
                host_index = ChangeHostTestUtils.HIDppHelper.get_host_info(self).curr_host
            # end if

            ChangeHostTestUtils.HIDppHelper.set_cookie(test_case=self, host_index=host_index, cookie=HexList('01'))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetCookies request")
            # ----------------------------------------------------------------------------------------------------------
            response = ChangeHostTestUtils.HIDppHelper.get_cookies(
                self, device_index=ChannelUtils.get_device_index(test_case=self))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCookies.cookie[0..nbHost-1] value")
            # ----------------------------------------------------------------------------------------------------------
            cookies_list = get_cookie_list(response, self.f.PRODUCT.DEVICE.F_NbHosts)
            self.assertEqual(expected=0x01, obtained=int(cookies_list[host], 16),
                             msg='The cookies[' + str(host) + '] parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported hosts")
        # --------------------------------------------------------------------------------------------------------------
        self.last_ble_address = None
        for host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Pair device with host {host + 1}")
            # ----------------------------------------------------------------------------------------------------------
            OobStateTestUtils.pair_device(self, host=host)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetCookies request")
            # ----------------------------------------------------------------------------------------------------------
            response = ChangeHostTestUtils.HIDppHelper.get_cookies(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the Cookie returned is 0")
            # ----------------------------------------------------------------------------------------------------------
            checker = ChangeHostTestUtils.GetCookiesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "cookies": (checker.check_cookies, HexList("00" * (GetCookiesResponse.LEN.COOKIES // 8)))
                }
            )
            checker.check_fields(self, response, feature_1814.get_cookies_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0004#2", _AUTHOR)
    # end def test_cookies_on_1814_reset

    @features("Feature1805")
    @features("SecureDfuControlUseNVS")
    @features("NvsChunkID", "NVS_DFU_ID")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_dfu_control_on_00c3_reset_nvs(self):
        """
        Validate all NVS chunks which should be erased/reset are erased/reset: check DFU Control is reset

        Use x00C3 to set DFU Control
        """
        self.post_requisite_reload_nvs = True

        if self.current_channel.protocol in LogitechProtocol.gaming_protocols() and \
                self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Switch to USB Channel if DFU is done over USB")
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_unplug_usb_cable = True
            ProtocolManagerUtils.switch_to_usb_channel(self)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x00C3 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_00c3_index, self.feature_00c3, _, _ = DeviceBaseTestUtils.HIDppHelper.get_parameters(
            test_case=self, feature_id=SecureDfuControl.FEATURE_ID, factory=SecureDfuControlFactory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetDFUControl request")
        # --------------------------------------------------------------------------------------------------------------
        set_dfu_control_response = DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1,
                                                                       dfu_control_param=0xFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate all bytes in the response set to zero')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(set_dfu_control_response.padding),
                         msg='The padding parameter differs from the expected one')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DFU chunk is restored to default value in NVS")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        dfu_chunk = self.memory_manager.get_active_chunk_by_name(chunk_name='NVS_DFU_ID')
        self.assertEqual(expected=0, obtained=to_int(dfu_chunk.enable),
                         msg='enable should be reset to default in NVS')
        self.assertEqual(expected=0, obtained=to_int(dfu_chunk.param),
                         msg='param should be reset to default in NVS')

        self.testCaseChecked("FUN_1805_0005", _AUTHOR)
    # end def test_dfu_control_on_00c3_reset_nvs

    @features("Feature1805")
    @features("Feature2110")
    @features("NvsChunkID", "NVS_ROLLER_ID")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_wheel_ratchet_mode_reset_2110_nvs(self):
        """
        Goal: Check all NVS chunks which should be erased/reset are erased/reset: check Roller is reset

        Use 0x2110 to set wheel/ratchet mode
        """
        self.post_requisite_reload_nvs = True
        smart_shift_config = self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2110 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_2110_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=SmartShift.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRatchetControlMode request with non default values for  wheel and ratchet")
        # --------------------------------------------------------------------------------------------------------------
        wheel_mode = SmartShift.WheelMode.FreeSpin if smart_shift_config.F_WheelMode == SmartShift.WheelMode.Ratchet \
            else SmartShift.WheelMode.Ratchet
        auto_disengage = smart_shift_config.F_AutoDisengage - 1 if smart_shift_config.F_AutoDisengage > 0 \
            else smart_shift_config.F_AutoDisengage
        auto_disengage_default = smart_shift_config.F_AutoDisengageDefault - 1 \
            if smart_shift_config.F_AutoDisengageDefault > 0 else smart_shift_config.F_AutoDisengageDefault
        response = set_ratchet_control_mode(
            test_case=self,
            wheel_mode=wheel_mode,
            auto_disengage=auto_disengage,
            auto_disengage_default=auto_disengage_default)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Validate returned values are the echo of the request")
        # --------------------------------------------------------------------------------------------------------------
        verify_ratchet_control_mode(test_case=self, response=response, wheel_mode=wheel_mode,
                                    auto_disengage=auto_disengage, auto_disengage_default=auto_disengage_default)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Roller chunk is deleted in NVS")
        # --------------------------------------------------------------------------------------------------------------
        chunk_data = self.memory_manager.get_chunks_by_name(chunk_name='NVS_ROLLER_ID')
        self.assertEqual(expected=0, obtained=len(chunk_data),
                         msg='NVS_ROLLER_ID should be empty in NVS')

        self.testCaseChecked("FUN_1805_0006#1", _AUTHOR)
    # end def test_wheel_ratchet_mode_reset_2110_nvs

    @features("Feature1805")
    @features("Feature2111")
    @features("NvsChunkID", "NVS_ROLLER_ID")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_wheel_ratchet_mode_reset_2111_nvs(self):
        """
        Goal: Check all NVS chunks which should be erased/reset are erased/reset: check Roller is reset

        Use 0x2111 to set wheel/ratchet mode
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2111 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_2111_index = ChannelUtils.update_feature_mapping(test_case=self,
                                                                      feature_id=SmartShiftTunable.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetWheelMode request with ratchet mode")
        # --------------------------------------------------------------------------------------------------------------
        wheel_mode = SmartShiftTunable.WheelModeConst.RATCHET if \
            self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE.F_WheelModeDefault == \
            SmartShiftTunable.WheelModeConst.FREESPIN else SmartShiftTunable.WheelModeConst.FREESPIN
        SmartShiftTunableTestUtils.HIDppHelper.set_wheel_mode(test_case=self, wheel_mode=wheel_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Send GetRatchetControlMode request to check wheel mode is reflecting correctly")
        # --------------------------------------------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self, expected=wheel_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Roller chunk is deleted in NVS")
        # --------------------------------------------------------------------------------------------------------------
        chunk_data = self.memory_manager.get_chunks_by_name(chunk_name='NVS_ROLLER_ID')
        self.assertEqual(expected=0, obtained=len(chunk_data),
                         msg='NVS_ROLLER_ID should be empty in NVS')

        self.testCaseChecked("FUN_1805_0006#2", _AUTHOR)
    # end def test_wheel_ratchet_mode_reset_2111_nvs

    @features("Feature1805")
    @features("Feature2121")
    @features("NvsChunkID", "NVS_ROLLER_ID")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_wheel_ratchet_mode_reset_2121_nvs(self):
        """
        Goal: Check all NVS chunks which should be erased/reset are erased/reset: check Roller is reset

        Use 0x2121 to set wheel/ratchet mode
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2121 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_2121_index, self.feature_2121, _, _ = DeviceBaseTestUtils.HIDppHelper.get_parameters(
            test_case=self, feature_id=HiResWheel.FEATURE_ID, factory=HiResWheelFactory,
            device_index=None, port_index=None, skip_not_found=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetWheelMode request with non default values")
        # --------------------------------------------------------------------------------------------------------------
        set_wheel_mode = self.feature_2121.set_wheel_mode_cls(
            deviceIndex=HexList(ChannelUtils.get_device_index(self)), featureId=self.feature_2121_index,
            reserved=HiResWheel.DEFAULT_RESERVED, analytics=HiResWheel.ANALYTIC, invert=HiResWheel.INVERT,
            resolution=HiResWheel.HIGH_RESOLUTION, target=HiResWheel.HIDPP)

        set_wheel_mode_response = ChannelUtils.send(
            test_case=self, report=set_wheel_mode, response_queue_name=HIDDispatcher.QueueName.MOUSE,
            response_class_type=self.feature_2121.set_wheel_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetWheelMode response")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HiResWheel.HIDPP,
                         obtained=int(set_wheel_mode_response.target),
                         msg='The target parameter differs from the one expected')
        self.assertEqual(expected=HiResWheel.HIGH_RESOLUTION,
                         obtained=int(set_wheel_mode_response.resolution),
                         msg='The resolution parameter differs from the one expected')
        self.assertEqual(expected=HiResWheel.INVERT,
                         obtained=int(set_wheel_mode_response.invert),
                         msg='The invert parameter differs from the one expected')
        if self.f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_Version_1:
            self.assertEqual(expected=HiResWheel.ANALYTIC,
                             obtained=int(set_wheel_mode_response.analytics),
                             msg='The analytics parameter differs from the one expected')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Roller chunk is deleted in NVS")
        # --------------------------------------------------------------------------------------------------------------
        chunk_data = self.memory_manager.get_chunks_by_name(chunk_name='NVS_ROLLER_ID')
        self.assertEqual(expected=0, obtained=len(chunk_data),
                         msg='NVS_ROLLER_ID should be empty in NVS')

        self.testCaseChecked("FUN_1805_0006#3", _AUTHOR)
    # end def test_wheel_ratchet_mode_reset_2121_nvs

    @features("Feature1805")
    @features("Feature2150")
    @features("NvsChunkID", "NVS_ROLLER_ID")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_wheel_ratchet_mode_reset_2150_nvs(self):
        """
        Goal: Check all NVS chunks which should be erased/reset are erased/reset: check Roller is reset

        Use 0x2150 to set wheel/ratchet mode
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2150 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_2150_index, self.feature_2150, _, _ = ThumbwheelTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetThumbwheelReporting request with non deafault values")
        # --------------------------------------------------------------------------------------------------------------
        ThumbwheelTestUtils.HIDppHelper.set_thumbwheel_reporting(
            test_case=self, reporting_mode=Thumbwheel.REPORTING_MODE.HIDPP,
            invert_direction=ThumbwheelTestUtils.INVERTED_DIR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Roller chunk is deleted in NVS")
        # --------------------------------------------------------------------------------------------------------------
        chunk_data = self.memory_manager.get_chunks_by_name(chunk_name='NVS_ROLLER_ID')
        self.assertEqual(expected=0, obtained=len(chunk_data),
                         msg='NVS_ROLLER_ID should be empty in NVS')

        self.testCaseChecked("FUN_1805_0006#4", _AUTHOR)
    # end def test_wheel_ratchet_mode_reset_2150_nvs

    @features("Feature1805")
    @features("Feature1815")
    @features("NvsChunkID", "NVS_HOSTSINFO_INFO_ID")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_host_friendly_name_on_1815_reset_nvs(self):
        """
        Validate all NVS chunks which should be erased/reset are erased/reset: check Host friendly name and OS
        versions is reset

        Use 0x1815 to set Host Info
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1815 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1815_index, self.feature_1815, _, _ = HostsInfoTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetHostFriendlyName and SetHostOSVersion request with non-default values")
        # --------------------------------------------------------------------------------------------------------------
        HostsInfoTestUtils.HIDppHelper.set_host_friendly_name(
            test_case=self, host_index=HOST.CH1 - 1, name='HostNameTest')
        HostsInfoTestUtils.HIDppHelper.set_host_os_version(
            test_case=self, host_index=HOST.CH1 - 1, os_type=0, os_version=0, os_revision=0, os_build=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Host Info chunk is deleted in NVS")
        # --------------------------------------------------------------------------------------------------------------
        chunk_data = self.memory_manager.get_chunks_by_name(chunk_name='NVS_HOSTSINFO_INFO_ID')
        self.assertEqual(expected=0, obtained=len(chunk_data),
                         msg='NVS_HOSTSINFO_INFO_ID should be empty in NVS')

        self.testCaseChecked("FUN_1805_0007", _AUTHOR)
    # end def test_host_friendly_name_on_1815_reset_nvs

    @features("Feature1805")
    @features("Feature2201")
    @features("NvsChunkID", "NVS_DPI_ID")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_dpi_values_on_2201_reset_nvs(self):
        """
        Validate all NVS chunks which should be erased/reset are erased/reset: check DPI values is reset

        Use 0x2201 to set sensor DPI
        """
        self.post_requisite_reload_nvs = True
        adjustable_dpi_config = self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2201 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_2201_index, self.feature_2201, _, _ = AdjustableDpiTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get a dpi value from DpiListReport_RANGE or DpiListReport_LIST')
        # --------------------------------------------------------------------------------------------------------------
        if adjustable_dpi_config.F_DpiDefault != adjustable_dpi_config.F_DpiMax:
            new_dpi_value = adjustable_dpi_config.F_DpiMax
        else:
            new_dpi_value = adjustable_dpi_config.F_DpiMin
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetSensorDPIRequest request with non-default dpi value")
        # --------------------------------------------------------------------------------------------------------------
        set_sensor_dpi_resp = AdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi(test_case=self, sensor_idx=0,
                                                                                dpi=int(new_dpi_value), dpi_level=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the response data from SetSensorDpi')
        # --------------------------------------------------------------------------------------------------------------
        checker = AdjustableDpiTestUtils.SetSensorDpiResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "dpi": (checker.check_dpi, new_dpi_value)
        })
        AdjustableDpiTestUtils.SetSensorDpiResponseChecker.check_fields(
            self, set_sensor_dpi_resp, self.feature_2201.set_sensor_dpi_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DPI chunk is deleted in NVS")
        # --------------------------------------------------------------------------------------------------------------
        raise NotImplementedError("Check DPI chunk is deleted in NVS")

        self.testCaseChecked("FUN_1805_0008", _AUTHOR)
    # end def test_dpi_values_on_2201_reset_nvs

    @features("Feature1805")
    @features("Feature8040")
    @features("NvsChunkID", "NVS_LED_BRIGHTNESS_ID")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_led_brightness_on_8040_reset_nvs(self):
        """
        Validate all NVS chunks which should be erased/reset are erased/reset: check LED brightness is reset

        Use 0x8040 to set brightness
        """
        self.post_requisite_reload_nvs = True
        default_brightness = self.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL.F_DefaultBrightness
        non_default_brightness = self.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL.F_MaxBrightness - default_brightness

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8040 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8040_index, self.feature_8040, _, _ = BrightnessControlTestUtils.HIDppHelper.get_parameters(
            test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Set brightness value = {non_default_brightness}, different from default value")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.set_brightness(self, non_default_brightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check SetBrightnessResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.MessageChecker.check_fields(
            self, response, self.feature_8040.set_brightness_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_OOB_AND_POWER_CYCLE)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check backlight chunk is restored to default in NVS")
        # --------------------------------------------------------------------------------------------------------------
        chunk_data = self.memory_manager.get_active_chunk_by_name(chunk_name='NVS_LED_BRIGHTNESS_ID')
        self.assertEqual(expected=HexList(default_brightness), obtained=HexList(chunk_data),
                         msg='NVS_LED_BRIGHTNESS_ID should be restored to default value in NVS')

        self.testCaseChecked("FUN_1805_0009", _AUTHOR)
    # end def test_led_brightness_on_8040_reset_nvs

    @features("Feature1805")
    @features("Feature8100")
    @features("NvsChunkID", "NVS_PROFILE_ID")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_onboard_profile_config_on_8100_reset_nvs(self):
        """
        Validate all NVS chunks which should be erased/reset are erased/reset: check Profile config is reset

        Use 0x8100 to manage onboard profiles
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8100 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8100_index, self.feature_8100, _, _ = OnboardProfilesTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetOnboardMode SetActiveProfile request with non-default values")
        # --------------------------------------------------------------------------------------------------------------
        set_active_profile_response = OnboardProfilesTestUtils.HIDppHelper.set_active_profile(
            test_case=self, profile_id=OnboardProfiles.SectorId.OOB_PROFILE_START)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetActiveProfileResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        checker.check_fields(self, set_active_profile_response, self.feature_8100.set_onboard_mode_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check profile chunk is deleted in NVS")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        chunk_data = self.memory_manager.get_chunks_by_name("NVS_PROFILE_ID")
        self.assertEqual(expected=0, obtained=len(chunk_data), msg='NVS_PROFILE_ID should be empty in NVS')

        self.testCaseChecked("FUN_1805_0010", _AUTHOR)
    # end def test_onboard_profile_config_on_8100_reset_nvs

    @features("Feature1805")
    @features("Keyboard")
    @features("NoUnifying")
    @features("NoUSB")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    @services("RequiredKeys", (KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_B))
    def test_keyboard_sequence_for_oob_state(self):
        """
        Validate keyboard sequence Esc+O+Esc+O+Esc+B to enter OOB State and check connection is lost and NVS chunks
            erased/reset for BT/BLE Protocol
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press Esc+O+Esc+O+Esc+B")
        # --------------------------------------------------------------------------------------------------------------
        for key in [KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O,
                    KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_B]:
            self.button_stimuli_emulator.keystroke(key_id=key)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _POWER_CYCLE)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_wireless_device_status_broadcast_event=False,
                   verify_connection_reset=False, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DUT is in OOB State (i.e. connection lost and NVS chunks erased/reset)")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_link_not_established_notification(
            test_case=self, expected_pairing_slot=self.current_channel.device_index)

        nvs_list = ['NVS_CONNECT_ID', 'NVS_BTLDR_CONNECT_ID', 'NVS_BLE_LAST_GAP_ADDR_USED']
        self.memory_manager.read_nvs()
        for nvs_chunk in nvs_list:
            chunk_data = self.memory_manager.get_chunks_by_name(chunk_name=nvs_chunk, active_bank_only=True)
            if nvs_chunk == 'NVS_CONNECT_ID':
                if self.f.PRODUCT.DEVICE.F_NbHosts == 3:
                    self.assertEqual(obtained=chunk_data[0].data.pairing_src_1,
                                     expected=HexList(ConnectIdChunkData.PairingSrc.NONE),
                                     msg=f'{nvs_chunk}.data.pairing_src_1 should be None in NVS')
                    self.assertEqual(obtained=chunk_data[0].data.scheme_host_1,
                                     expected=HexList(ConnectIdChunkData.STATUS.OOB),
                                     msg=f'{nvs_chunk}.data.scheme_host_1 Data should be Unpaired in NVS')
                    self.assertEqual(obtained=chunk_data[0].data.pairing_src_2,
                                     expected=HexList(ConnectIdChunkData.PairingSrc.NONE),
                                     msg=f'{nvs_chunk}.data.pairing_src_2 Data should be None in NVS')
                    self.assertEqual(obtained=chunk_data[0].data.scheme_host_2,
                                     expected=HexList(ConnectIdChunkData.STATUS.OOB),
                                     msg=f'{nvs_chunk}.data.scheme_host_2 should be Unpaired in NVS')
                # end if

                self.assertEqual(obtained=chunk_data[0].data.pairing_src_0,
                                 expected=HexList(ConnectIdChunkData.PairingSrc.NONE),
                                 msg=f'{nvs_chunk} Data should be empty in NVS'),
                self.assertEqual(obtained=chunk_data[0].data.scheme_host_0,
                                 expected=HexList(ConnectIdChunkData.STATUS.OOB),
                                 msg=f'{nvs_chunk}.data.scheme_host_0 should be Unpaired in NVS')

            elif nvs_chunk == 'NVS_BTLDR_CONNECT_ID':
                self.assertEqual(obtained=chunk_data[0].host_idx, expected=HexList("00"),
                                 msg=f'{nvs_chunk}.host_idx should be 0 in NVS')
                expected_protocol = HexList(ConnectIdChunkData.Protocol.BLE)
                self.assertEqual(obtained=chunk_data[0].protocol, expected=expected_protocol,
                                 msg=f'{nvs_chunk}.protocol should be {expected_protocol} in NVS')

            elif nvs_chunk == 'NVS_BLE_LAST_GAP_ADDR_USED':
                if self.last_ble_address is not None:
                    min_addr = Numeral(HexList(reversed(self.last_ble_address)))
                    curr_address = Numeral(HexList(reversed(chunk_data[-1].device_bluetooth_address)))
                    self.assertFalse(
                        min_addr <= curr_address <= (min_addr + DiscoveryTestUtils.AUTH_BLE_ADDR_COUNT),
                        f"Bluetooth address {Numeral(HexList(reversed(chunk_data[-1].device_bluetooth_address)))}"
                        f" shall not be in the range {min_addr} - {min_addr + DiscoveryTestUtils.AUTH_BLE_ADDR_COUNT}")
                # end if

            elif chunk_data is not None:
                self.assertEqual(obtained=len(chunk_data),
                                 expected=0,
                                 msg=f'{nvs_chunk} should be empty in NVS')
            # end if
        # end for

        self.testCaseChecked("FUN_1805_0011", _AUTHOR)
    # end def test_keyboard_sequence_for_oob_state

    @features("Feature1805")
    @features("Wireless")
    @level("Functionality")
    @services("Debugger")
    def test_connection_lost_after_receiver_hardware_reset(self):
        """
        Goal: Check connection lost after receiver hardware reset
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        oob_response = OobStateTestUtils.HIDppHelper.set_oob_state(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check valid response")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.MessageChecker.check_fields(
            test_case=self, message=oob_response, expected_cls=self.feature_1805.set_oob_state_response_cls,
            check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify a HID report can be received")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        # Stop Task executor
        ChannelUtils.close_channel(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Do a receiver hardware reset")
        # --------------------------------------------------------------------------------------------------------------
        ReceiverBaseTestUtils.ResetHelper.hardware_reset(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check connection is lost")
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_link_not_established_notification(
            test_case=self, expected_pairing_slot=self.current_channel.device_index)

        self.testCaseChecked("FUN_1805_0012", _AUTHOR)
    # end def test_connection_lost_after_receiver_hardware_reset

    @features("Feature1805")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    @services("LedIndicator")
    def test_connectivity_led_from_oob_state(self):
        """
        When device is set to OOB state, validate all connectivity LEDs blink fast until next power off /on. Then
        validate device is in discoverable mode (fast blinking) on channel 1 with timeout of 3 min.
        """
        self.post_requisite_reload_nvs = True
        connectivity_leds = [LED_ID.CONNECTIVITY_STATUS_LED_1]
        if self.f.PRODUCT.DEVICE.F_NbHosts > 1:
            connectivity_leds.append(LED_ID.CONNECTIVITY_STATUS_LED_2)
        # end if
        if self.f.PRODUCT.DEVICE.F_NbHosts == 3:
            connectivity_leds.append(LED_ID.CONNECTIVITY_STATUS_LED_3)
        # end if

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
        LogHelper.log_step(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        start_time = perf_counter()
        duration = DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT + OobStateFunctionalityTestCase.TWENTY_SECONDS
        end_time = start_time + duration

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait a duration longer than the discoverable period at OOB')
        # --------------------------------------------------------------------------------------------------------------
        sleep(OobStateFunctionalityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            for led_id in connectivity_leds:
                BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                    self, led_id=led_id, state=SchemeType.FAST_BLINKING)
            # end for
            sleep(OobStateFunctionalityTestCase.FIVE_SECONDS)
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Verify all connectivity LEDs are Fast blinking for at least {duration} s')
        # --------------------------------------------------------------------------------------------------------------
        for led_id in connectivity_leds:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
                self, led_id=led_id,
                position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST,
                minimum_duration=duration * OobStateFunctionalityTestCase.SEC_TO_MILLI_SEC)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _POWER_CYCLE)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_wireless_device_status_broadcast_event=False,
                   verify_connection_reset=False, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CONNECTION_LOST)
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_link_not_established_notification(
            test_case=self, expected_pairing_slot=self.current_channel.device_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        start_time = perf_counter()
        duration = DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT - EQuadDeviceConnectionUtils.RESET_DELAY
        end_time = start_time + duration

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for end of the discoverable period')
        # --------------------------------------------------------------------------------------------------------------
        sleep(OobStateFunctionalityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1, state=SchemeType.FAST_BLINKING)
            sleep(OobStateFunctionalityTestCase.FIVE_SECONDS)
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for another 5s where the LED1 shall be off')
        # --------------------------------------------------------------------------------------------------------------
        sleep(OobStateFunctionalityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking for 3min then Off')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST,
            exact_duration=duration * OobStateFunctionalityTestCase.SEC_TO_MILLI_SEC)
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1)

        if self.f.PRODUCT.DEVICE.F_NbHosts > 1:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify Led 2 state is Off')
            # ----------------------------------------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, reset=True,
                minimum_duration=duration * OobStateFunctionalityTestCase.SEC_TO_MILLI_SEC,
                position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        # end if
        if self.f.PRODUCT.DEVICE.F_NbHosts == 3:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify Led 3 state is Off')
            # ----------------------------------------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, reset=True,
                minimum_duration=duration * OobStateFunctionalityTestCase.SEC_TO_MILLI_SEC,
                position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        # end if

        self.testCaseChecked("FUN_1805_0013#1", _AUTHOR)
    # end def test_connectivity_led_from_oob_state

    @features('BLEProConnectionScheme')
    @features("Feature1805")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    @services("LedIndicator")
    def test_connectivity_led_from_oob_state_with_multiple_key_press(self):
        """
        When device is set to OOB state, validate all connectivity LEDs blink fast until next power off /on even if the
        user do a short press or a long press on connectivity button. Then validate device is in discoverable mode
        (fast blinking) on channel 1 with timeout of 3 min.
        """
        self.post_requisite_reload_nvs = True
        connectivity_leds = [LED_ID.CONNECTIVITY_STATUS_LED_1]
        host_indexs = [HOST.CH1]
        if self.f.PRODUCT.DEVICE.F_NbHosts > 1:
            connectivity_leds.append(LED_ID.CONNECTIVITY_STATUS_LED_2)
            host_indexs.append(HOST.CH2)
        # end if
        if self.f.PRODUCT.DEVICE.F_NbHosts == 3:
            connectivity_leds.append(LED_ID.CONNECTIVITY_STATUS_LED_3)
            host_indexs.append(HOST.CH3)
        # end if

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
        LogHelper.log_step(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)
        start_time = perf_counter()
        duration = DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT + OobStateFunctionalityTestCase.TWENTY_SECONDS
        end_time = start_time + duration

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify all connectivity LEDs are Fast blinking')
        # --------------------------------------------------------------------------------------------------------------
        sleep(OobStateFunctionalityTestCase.FIVE_SECONDS)
        for led_id in connectivity_leds:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                self, led_id=led_id, state=SchemeType.FAST_BLINKING)
        # end for

        for host_index in host_indexs:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform a short press on the Connect button')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.change_host(host_index=host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify all connectivity LEDs are still Fast blinking')
            # ----------------------------------------------------------------------------------------------------------
            sleep(OobStateFunctionalityTestCase.FIVE_SECONDS)
            for led_id in connectivity_leds:
                BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                    self, led_id=led_id, state=SchemeType.FAST_BLINKING)
            # end for
        # end for

        for host_index in host_indexs:
            # -----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform a long press on Easy switch button')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.enter_pairing_mode(host_index=host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify all connectivity LEDs are still Fast blinking')
            # ----------------------------------------------------------------------------------------------------------
            sleep(OobStateFunctionalityTestCase.FIVE_SECONDS)
            for led_id in connectivity_leds:
                BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                    self, led_id=led_id, state=SchemeType.FAST_BLINKING)
            # end for
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait a duration longer than the discoverable period at OOB')
        # --------------------------------------------------------------------------------------------------------------
        sleep(OobStateFunctionalityTestCase.ONE_SECOND)
        while perf_counter() < end_time:
            for led_id in connectivity_leds:
                BleProConnectionSchemeTestUtils.LedSpyHelper.check_led_state(
                    self, led_id=led_id, state=SchemeType.FAST_BLINKING)
            # end for
            sleep(OobStateFunctionalityTestCase.FIVE_SECONDS)
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Verify all connectivity LEDs are Fast blinking for at least {duration} s')
        # --------------------------------------------------------------------------------------------------------------
        for led_id in connectivity_leds:
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
                self, led_id=led_id,
                position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST,
                minimum_duration=duration * OobStateFunctionalityTestCase.SEC_TO_MILLI_SEC)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _POWER_CYCLE)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, verify_wireless_device_status_broadcast_event=False,
                   verify_connection_reset=False, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, _CONNECTION_LOST)
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.check_link_not_established_notification(
            test_case=self, expected_pairing_slot=self.current_channel.device_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Start LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.start_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Wait {OobStateFunctionalityTestCase.FIVE_SECONDS}s')
        # --------------------------------------------------------------------------------------------------------------
        sleep(OobStateFunctionalityTestCase.FIVE_SECONDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Stop LEDs monitoring')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.stop_monitoring(self, led_identifiers=CONNECTIVITY_STATUS_LEDS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify Led1State is Fast blinking')
        # --------------------------------------------------------------------------------------------------------------
        BleProConnectionSchemeTestUtils.LedSpyHelper.check_fast_blinking_time(
            self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_1,
            position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST,
            exact_duration=OobStateFunctionalityTestCase.FIVE_SECONDS * OobStateFunctionalityTestCase.SEC_TO_MILLI_SEC)

        if self.f.PRODUCT.DEVICE.F_NbHosts > 1:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify Led 2 state is Off')
            # ----------------------------------------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_2, reset=True,
                minimum_duration=(OobStateFunctionalityTestCase.FIVE_SECONDS *
                                  OobStateFunctionalityTestCase.SEC_TO_MILLI_SEC),
                position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        # end if
        if self.f.PRODUCT.DEVICE.F_NbHosts == 3:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify Led 3 state is Off')
            # ----------------------------------------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.LedSpyHelper.check_off_time(
                self, led_id=LED_ID.CONNECTIVITY_STATUS_LED_3, reset=True,
                minimum_duration=(OobStateFunctionalityTestCase.FIVE_SECONDS *
                                  OobStateFunctionalityTestCase.SEC_TO_MILLI_SEC),
                position=BleProConnectionSchemeTestUtils.LedSpyHelper.POSITION.FIRST)
        # end if

        self.testCaseChecked("FUN_1805_0013#2", _AUTHOR)
    # end def test_connectivity_led_from_oob_state_with_multiple_key_press

    @features("Feature1805")
    @features("Feature0007")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_device_friendly_name_on_0007_reset(self):
        """
        Validate the 'friendly name' parameter linked to the 0x0007 feature restored to the default friendly name
        value.

        Require 0x0007 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0007 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_0007, _, _ = DeviceFriendlyNameTestUtils.HIDppHelper.get_parameters(
            self, DeviceFriendlyName.FEATURE_ID, DeviceFriendlyNameFactory)
        default_friendly_name = DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.HIDppHelper.get_friendly_name(
            self, byte_index=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Delete friendly name chunk from NVS")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.nvs_parser.delete_chunk(chunk_id="NVS_DEVICE_FRIENDLY_NAME_ID")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported Hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Pair device with host {host + 1}")
            # ----------------------------------------------------------------------------------------------------------
            if host + 1 != HOST.CH1:
                OobStateTestUtils.pair_device(self, host=host)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetFriendlyName request with nameChunk different to the default name")
            # ----------------------------------------------------------------------------------------------------------
            # Size of name_chunk to read/write coming from 0x1807 properties if any, else from 0x0007 settings
            friendly_name_len = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(
                self, ConfigurableProperties.PropertyId.BLE_GAP_APP_NAME)
            if friendly_name_len == 0:
                friendly_name_len = self.f.PRODUCT.FEATURES.COMMON.DEVICE_FRIENDLY_NAME.F_NameMaxLength
            # end if

            payload_size = self.feature_0007.set_friendly_name_cls.LEN.NAME_CHUNK // 8
            if friendly_name_len > payload_size:
                warnings.warn("Tests scripts might not cover this case correctly yet. TODO: if this becomes necessary, "
                              "please check scripts and update.")
            # end if

            name_chunk_length = min(payload_size, friendly_name_len)
            test_name_chunk = ''.join(choices(ascii_uppercase + digits, k=name_chunk_length))
            DeviceFriendlyNameTestUtils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(
                self, byte_index=0, name_chunk=test_name_chunk)
            DiscoveryTestUtils.set_ble_device_name(test_case=self, device_name=test_name_chunk)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate new friendly name and friendly name length is set as expected")
            # ----------------------------------------------------------------------------------------------------------
            friendly_name = DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.HIDppHelper.get_friendly_name(
                self, byte_index=0)
            DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.MessageChecker.check_length(
                self, len(friendly_name), len(test_name_chunk))
            DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.MessageChecker.check_name_match(
                self, friendly_name, test_name_chunk)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported Hosts")
        # --------------------------------------------------------------------------------------------------------------
        self.last_ble_address = None
        for host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Pair device with host {host + 1}")
            # ----------------------------------------------------------------------------------------------------------
            OobStateTestUtils.pair_device(self, host=host)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the Friendly name returned to default")
            # ----------------------------------------------------------------------------------------------------------
            friendly_name = DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.HIDppHelper.get_friendly_name(
                self, byte_index=0)
            DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.MessageChecker.check_length(
                self, len(friendly_name), len(default_friendly_name))
            DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.MessageChecker.check_name_match(
                self, friendly_name, default_friendly_name)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_1805_0014", _AUTHOR)
    # end def test_device_friendly_name_on_0007_reset

    @features("Feature0020")
    @features("Feature1805")
    @features("NvsChunkID", "NVS_APPLICATION_CONFIG_CHANGE_ID")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_cookies_on_0020_reset(self):
        """
        Validate the configuration cookie parameter linked to the 0x0020 feature is restored to its default value

        Require 0x0020 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0020")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0020_index = ChannelUtils.update_feature_mapping(self, feature_id=ConfigChange.FEATURE_ID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Delete confguration cookie from NVS")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.nvs_parser.delete_chunk("NVS_APPLICATION_CONFIG_CHANGE_ID")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported Hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            if host + 1 != HOST.CH1:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Pair device with host {host + 1}")
                # ------------------------------------------------------------------------------------------------------
                OobStateTestUtils.pair_device(self, host=host)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetConfigurationCookie request with cookie value greater than 0")
            # ----------------------------------------------------------------------------------------------------------
            set_config_complete = SetConfigurationComplete(deviceIndex=HexList(ChannelUtils.get_device_index(self)),
                                                           featureId=self.feature_0020_index,
                                                           configurationCookie=HexList("0001"))
            set_config_complete_response = ChannelUtils.send(
                self, report=set_config_complete, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=SetConfigurationCompleteResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetConfigurationCookieResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList('0001'),
                             obtained=set_config_complete_response.configurationCookie,
                             msg='The configurationCookie parameter differs from the one expected')
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported Hosts")
        # --------------------------------------------------------------------------------------------------------------
        self.last_ble_address = None
        for host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Pair device with host {host + 1}")
            # ----------------------------------------------------------------------------------------------------------
            OobStateTestUtils.pair_device(self, host=host)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetConfigurationCookie request")
            # ----------------------------------------------------------------------------------------------------------
            get_configuration_cookie = GetConfigurationCookie(deviceIndex=HexList(ChannelUtils.get_device_index(self)),
                                                              featureId=self.feature_0020_index)
            get_configuration_cookie_response = ChannelUtils.send(self, report=get_configuration_cookie,
                                                                  response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                                  response_class_type=GetConfigurationCookieResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the Configuration cookie returned is 0")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=HexList("0000"),
                             obtained=get_configuration_cookie_response.configurationCookie,
                             msg='The configurationCookie parameter differs from the one expected')
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0015", _AUTHOR)
    # end def test_cookies_on_0020_reset

    @features("Feature1805")
    @features("Feature1815")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_host_friendly_name_on_1815_reset(self):
        """
        Validate the 'host friendly name', 'Os type', 'Os version', 'Os revision' and 'Os build' parameters linked to
        the 0x1815 feature restored to the default value for all supported hosts

        Require 0x1815 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        host_info = {}

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1815")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_1815, _, _ = HostsInfoTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported hosts")
        # --------------------------------------------------------------------------------------------------------------
        for host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            if host + 1 != HOST.CH1:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f"Pair device with host {host + 1}")
                # ------------------------------------------------------------------------------------------------------
                OobStateTestUtils.pair_device(self, host=host)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Get default values for OS Type, Version, Revision and build")
            # ----------------------------------------------------------------------------------------------------------
            get_host_os_version_response = HostsInfoTestUtils.HIDppHelper.get_host_os_version(test_case=self,
                                                                                              host_index=host)
            host_info[host] = {
                "default_os_version": get_host_os_version_response.os_version,
                "default_os_type": get_host_os_version_response.os_type,
                "default_os_revision": get_host_os_version_response.os_revision,
                "default_os_build": get_host_os_version_response.os_build
            }

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Set hostFriendlyname, OS Type, Version, Revision and build to values different"
                                     "from default")
            # ----------------------------------------------------------------------------------------------------------
            if self.f.PRODUCT.DEVICE.F_NbHosts == 1:
                host_index = 0
            else:
                host_index = ChangeHostTestUtils.HIDppHelper.get_host_info(self).curr_host
            # end if

            name_chunk_length = self.feature_1815.set_host_friendly_name_cls.LEN.NAME_CHUNK // 8
            test_name_chunk = ''.join(choices(ascii_uppercase + digits, k=name_chunk_length))
            set_host_friendly_name_response = HostsInfoTestUtils.HIDppHelper.set_host_friendly_name(
                self, host_index, name=test_name_chunk)
            set_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.set_host_os_version(self, host_index=host_index,
                                                                                          os_type=0, os_version=0,
                                                                                          os_revision=0, os_build=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate SetHostFriendlyNameResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = HostsInfoTestUtils.SetHostFriendlyNameResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "host_index": (checker.check_host_index, host_index),
                    "name_len": (checker.check_name_len, name_chunk_length)
                }
            )
            checker.check_fields(
                self, set_host_friendly_name_response[0], self.feature_1815.set_host_friendly_name_response_cls,
                check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate SetHostOsVersionResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            HostsInfoTestUtils.SetHostOsVersionResponseChecker.check_fields(
                self, set_host_os_version_resp, self.feature_1815.set_host_os_version_response_cls)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all supported hosts")
        # --------------------------------------------------------------------------------------------------------------
        self.last_ble_address = None
        for host in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Pair device with host {host + 1}")
            # ----------------------------------------------------------------------------------------------------------
            OobStateTestUtils.pair_device(self, host=host)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetHostFriendlyName request")
            # ----------------------------------------------------------------------------------------------------------
            if self.f.PRODUCT.DEVICE.F_NbHosts == 1:
                host_index = 0
            else:
                host_index = ChangeHostTestUtils.HIDppHelper.get_host_info(self).curr_host
            # end if

            get_host_friendly_name_response = HostsInfoTestUtils.HIDppHelper.get_host_friendly_name(
                self, byte_index=0, host_index=host_index)
            get_host_os_version_response = HostsInfoTestUtils.HIDppHelper.get_host_os_version(self, host_index)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Check host configuration restored to default")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate GetHostFriendlyNameResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = HostsInfoTestUtils.GetHostFriendlyNameResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update(
                {
                    "host_index": (checker.check_host_index, host_index)
                }
            )
            checker.check_fields(self, get_host_friendly_name_response,
                                 self.feature_1815.get_host_friendly_name_response_cls, check_map)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate GetHostOsVersionResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = HostsInfoTestUtils.GetHostOsVersionResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "os_type": (checker.check_os_type, host_info[host]["default_os_type"]),
                "os_version": (checker.check_os_version, host_info[host]["default_os_version"]),
                "os_revision": (checker.check_os_revision, host_info[host]["default_os_revision"]),
                "os_build": (checker.check_os_build, host_info[host]["default_os_build"]),
            })
            checker.check_fields(self, get_host_os_version_response, self.feature_1815.get_host_os_version_response_cls,
                                 check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0016", _AUTHOR)
    # end def test_host_friendly_name_on_1815_reset

    @features("Feature1805")
    @features("Feature1982")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_backlight_on_1982_reset(self):
        """
        Validate the Configuration, option & Backlight effect parameters linked to the 0x1982 feature restored to the
        default value

        Require 0x1982 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        backlight_enable = Backlight.Configuration.ENABLE
        backlight_disable = Backlight.Configuration.DISABLE
        default_options = BacklightTestUtils.get_default_options(self)
        backlight_config = self.f.PRODUCT.FEATURES.COMMON.BACKLIGHT

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1982 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_1982, _, _ = BacklightTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Restore default backlight configuration")
        # --------------------------------------------------------------------------------------------------------------
        BacklightTestUtils.HIDppHelper.set_backlight_config(
            self,
            configuration=HexList(backlight_enable),
            options=HexList(default_options),
            backlight_effect=HexList(backlight_config.F_BacklightEffect),
            curr_duration_hands_out=HexList(backlight_config.F_OobDurationHandsOut),
            curr_duration_hands_in=HexList(backlight_config.F_OobDurationHandsIn),
            curr_duration_powered=HexList(backlight_config.F_OobDurationPowered))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetBacklightConfig with a different config from default")
        # --------------------------------------------------------------------------------------------------------------
        set_backlight_config_response = BacklightTestUtils.HIDppHelper.set_backlight_config(
            self, configuration=HexList(backlight_disable), options=default_options)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetBacklightConfigResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        checker.check_fields(self, set_backlight_config_response, self.feature_1982.set_backlight_config_response_cls,
                             {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetBacklightConfig request")
        # --------------------------------------------------------------------------------------------------------------
        get_backlight_config_response = BacklightTestUtils.HIDppHelper.get_backlight_config(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the Backlight config is same as default value.")
        # --------------------------------------------------------------------------------------------------------------
        checker = BacklightTestUtils.GetBacklightConfigResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(
            self, get_backlight_config_response, self.feature_1982.get_backlight_config_response_cls, check_map)

        self.testCaseChecked("FUN_1805_0017", _AUTHOR)
    # end def test_backlight_on_1982_reset

    @features("Feature1805")
    @features("Feature1B04")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_special_keys_on_1b04_reset(self):
        """
        Validate the 'flags' and 'remap' parameters linked to the 0x1B04 feature restored to the default value for
        each CID

        Require 0x1b04 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        cid_info_table = self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.CID_INFO_TABLE

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1b04 index")
        # --------------------------------------------------------------------------------------------------------------
        special_keys_and_mouse_buttons_feature = SpecialKeysMSEButtonsFactory.create(
            self.config_manager.get_feature_version(
                self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS))
        self.feature_1b04_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=SpecialKeysMSEButtons.FEATURE_ID)

        set_cid_reporting_class = special_keys_and_mouse_buttons_feature.set_cid_reporting_cls
        set_cid_reporting_response_class = special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls
        get_cid_info_response_class = special_keys_and_mouse_buttons_feature.get_cid_info_response_cls
        get_cid_reporting_response_class = special_keys_and_mouse_buttons_feature.get_cid_reporting_response_cls

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get Cid count")
        # --------------------------------------------------------------------------------------------------------------
        cid_count = SpecialKeysMseButtonsTestUtils.get_cid_count(self, special_keys_and_mouse_buttons_feature,
                                                                 self.feature_1b04_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over cid count to send SetCidReporting with different remapping than the "
                                 "default value")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(cid_count):
            if self.f.PRODUCT.F_IsPlatform and cid_info_table.F_Cid[index] == '0x50':
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetCidInfo request with index = {index} to get CID value')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1b04_index,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetCidReporting request with non default values')
            # ----------------------------------------------------------------------------------------------------------
            force_raw_xy = True if eval(cid_info_table.F_AdditionalFlagsForceRawXY[index]) else False
            raw_xy = True if eval(cid_info_table.F_AdditionalFlagsRawXY[index]) else False
            persist = True if eval(cid_info_table.F_FlagPersist[index]) else False
            divert = True if eval(
                cid_info_table.F_FlagDivert[index]) and cid_info_table.F_Cid[index] not in ('0x50', '0x51') else False
            raw_wheel = True if eval(cid_info_table.F_AdditionalFlagsRawWheel[index]) else False
            analytics_key_event = True if eval(cid_info_table.F_AdditionalFlagsAnalyticsKeyEvents[index]) else False
            if self.f.PRODUCT.F_IsMice:
                cid_left_click = cid_info_table.F_Cid[cid_info_table.F_FriendlyName.index('Left Click')]
                remap = cid_left_click if cid_info_table.F_Cid[index] != cid_left_click else \
                    cid_info_table.F_Cid[cid_info_table.F_FriendlyName.index('Right Click')]
                remap = HexList(int(remap, 16))
                remap.addPadding(set_cid_reporting_class.LEN.REMAP // 8)
            else:
                remap = 0
            # end if

            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_1b04_index,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        force_raw_xy_valid=True,
                                                        force_raw_xy=force_raw_xy,
                                                        raw_xy_valid=True,
                                                        raw_xy=raw_xy,
                                                        persist_valid=True,
                                                        persist=persist,
                                                        divert_valid=True,
                                                        divert=divert,
                                                        remap=remap,
                                                        raw_wheel_valid=True,
                                                        raw_wheel=raw_wheel,
                                                        analytics_key_event_valid=True,
                                                        analytics_key_event=analytics_key_event)

            set_cid_reporting_response = ChannelUtils.send(test_case=self, report=set_cid_reporting,
                                                           response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                           response_class_type=set_cid_reporting_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate SetCidReporting response format')
            # ----------------------------------------------------------------------------------------------------------
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(test_case=self,
                                                                         message_with_expected_field=set_cid_reporting,
                                                                         response=set_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(cid_count):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetCidInfo request with index = {index} to get CID value')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1b04_index,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetCidReporting request with CID = '
                                     f'{get_cid_info_response.ctrl_id}')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_reporting = special_keys_and_mouse_buttons_feature.get_cid_reporting_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1b04_index,
                ctrl_id=get_cid_info_response.ctrl_id)
            get_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_reporting_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetCidReporting response according to product '
                                      'specification')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_reporting_expected_response = get_cid_reporting_response_class(
                device_index=ChannelUtils.get_device_index(self),
                feature_index=self.feature_1b04_index,
                ctrl_id=get_cid_info_response.ctrl_id)
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, get_cid_reporting_expected_response, get_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B04_0018")
    # end def test_special_keys_on_1b04_reset

    @features("Feature1805")
    @features("Feature1B05")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_full_key_customization_on_1b05_reset(self):
        """
        Validate the poweron_fkc_enable, fkc_enabled, toggle_keys_enabled and sw_configuration_cookie parameters linked
        to the 0x1B05 feature restored to default values after OOB
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1B05 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_1b05, _, _ = FullKeyCustomizationTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Enable FKC and all toggle keys by getSetEnabled request with set_fkc_enabled=1, "
                                 "set_toggle_keys_enabled=1, fkc_enabled=1 and toggle_keys_enabled=0xFF")
        # --------------------------------------------------------------------------------------------------------------
        get_set_enabled_response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.SET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.SET,
            fkc_enabled=FullKeyCustomization.FKCStatus.ENABLE,
            toggle_keys_enabled=0xFF,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check GetSetEnabledResponse fields as expected")
        # --------------------------------------------------------------------------------------------------------------
        fkc_state_checker = FullKeyCustomizationTestUtils.FkcStateChecker
        fkc_state_check_map = fkc_state_checker.get_default_check_map(self)
        fkc_state_check_map['fkc_enabled'] = (fkc_state_checker.check_fkc_enabled,
                                              FullKeyCustomization.FKCStatus.ENABLE)

        toggle_keys_checker = FullKeyCustomizationTestUtils.ToggleKeysStateChecker
        toggle_keys_state_check_map = toggle_keys_checker.get_default_check_map(self)
        toggle_keys_state_check_map['toggle_key_7_enabled'] = (toggle_keys_checker.check_toggle_key_7_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_6_enabled'] = (toggle_keys_checker.check_toggle_key_6_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_5_enabled'] = (toggle_keys_checker.check_toggle_key_5_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_4_enabled'] = (toggle_keys_checker.check_toggle_key_4_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_3_enabled'] = (toggle_keys_checker.check_toggle_key_3_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_2_enabled'] = (toggle_keys_checker.check_toggle_key_2_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_1_enabled'] = (toggle_keys_checker.check_toggle_key_1_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)
        toggle_keys_state_check_map['toggle_key_0_enabled'] = (toggle_keys_checker.check_toggle_key_0_enabled,
                                                               FullKeyCustomization.ToggleKeyStatus.ENABLE)

        get_set_enabled_checker = FullKeyCustomizationTestUtils.GetSetEnabledResponseChecker
        get_set_enabled_check_map = get_set_enabled_checker.get_default_check_map(self)
        get_set_enabled_check_map['fkc_state'] = (get_set_enabled_checker.check_fkc_state, fkc_state_check_map)
        get_set_enabled_check_map['toggle_keys_state'] = (get_set_enabled_checker.check_toggle_keys_state, 
                                                          toggle_keys_state_check_map)
        get_set_enabled_checker.check_fields(self, get_set_enabled_response, 
                                             self.feature_1b05.get_set_enabled_response_cls, get_set_enabled_check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get power-on FKC by getSetPowerOnParams request with set_poweron_fkc_enable=0 and "
                                 "poweron_fkc_enable=0")
        # --------------------------------------------------------------------------------------------------------------
        get_set_power_on_params_response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            self,
            set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.GET,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check PowerOnFKCEnableResponse fields as expected")
        # --------------------------------------------------------------------------------------------------------------
        power_on_fkc_state_checker = FullKeyCustomizationTestUtils.PowerOnFkcStateChecker
        power_on_fkc_state_check_map = power_on_fkc_state_checker.get_default_check_map(self)
        power_on_fkc_state_check_map['power_on_fkc_enable'] = (power_on_fkc_state_checker.check_power_on_fkc_enable,
                                                         FullKeyCustomization.PowerOnFKCStatus.ENABLE)

        power_on_params_checker = FullKeyCustomizationTestUtils.GetSetPowerOnParamsResponseChecker
        power_on_params_check_map = power_on_params_checker.get_default_check_map(self)
        power_on_params_check_map['power_on_fkc_state'] = (power_on_params_checker.check_power_on_fkc_state,
                                                           power_on_fkc_state_check_map)
        power_on_params_checker.check_fields(self, get_set_power_on_params_response,
                                             self.feature_1b05.get_set_power_on_params_response_cls,
                                             power_on_params_check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Update SW cookie by getSetSWConfigurationCookie request with "
                                 "set_sw_configuration_cookie=1 and sw_configuration_cookie=0xFF")
        # --------------------------------------------------------------------------------------------------------------
        set_sw_configuration_cookie_response = (
            FullKeyCustomizationTestUtils.HIDppHelper.get_set_sw_configuration_cookie(
                test_case=self,
                set_sw_configuration_cookie=FullKeyCustomization.SWConfigurationCookieRequest.SET,
                sw_configuration_cookie=0xFF))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetSwConfigurationCookieResponse fields as expected")
        # --------------------------------------------------------------------------------------------------------------
        sw_cookie_checker = FullKeyCustomizationTestUtils.GetSetSWConfigurationCookieResponseChecker
        sw_cookie_check_map = sw_cookie_checker.get_default_check_map(self)
        sw_cookie_check_map['sw_configuration_cookie'] = (sw_cookie_checker.check_sw_configuration_cookie, 0xFF)
        sw_cookie_checker.check_fields(self, set_sw_configuration_cookie_response, 
                                       self.feature_1b05.get_set_sw_configuration_cookie_response_cls,
                                       sw_cookie_check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get FKC and all toggle keys status by getSetEnabled request with set_fkc_enabled=0, "
                                 "set_toggle_keys_enabled=0")
        # --------------------------------------------------------------------------------------------------------------
        get_set_enabled_response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_enabled(
            self,
            set_toggle_keys_enabled=FullKeyCustomization.ToggleKeysRequest.GET,
            set_fkc_enabled=FullKeyCustomization.FKCStateRequest.GET,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check GetSetEnabledResponse fields are restored to default")
        # --------------------------------------------------------------------------------------------------------------
        get_set_enabled_check_map = get_set_enabled_checker.get_default_check_map(self)
        get_set_enabled_checker.check_fields(self, get_set_enabled_response,
                                             self.feature_1b05.get_set_enabled_response_cls, get_set_enabled_check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get power-on FKC by getSetPowerOnParams request with set_poweron_fkc_enable=0")
        # --------------------------------------------------------------------------------------------------------------
        get_set_power_on_params_response = FullKeyCustomizationTestUtils.HIDppHelper.get_set_power_on_params(
            self,
            set_power_on_fkc_enable=FullKeyCustomization.PowerOnFKCRequest.GET,
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check PowerOnFKCEnableResponse fields are restored to default")
        # --------------------------------------------------------------------------------------------------------------
        power_on_params_check_map = power_on_params_checker.get_default_check_map(self)
        power_on_params_checker.check_fields(self, get_set_power_on_params_response,
                                             self.feature_1b05.get_set_power_on_params_response_cls,
                                             power_on_params_check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get SW cookie by getSetSWConfigurationCookie request with "
                                 "set_sw_configuration_cookie=0")
        # --------------------------------------------------------------------------------------------------------------
        set_sw_configuration_cookie_response = (
            FullKeyCustomizationTestUtils.HIDppHelper.get_set_sw_configuration_cookie(
                test_case=self,
                set_sw_configuration_cookie=FullKeyCustomization.SWConfigurationCookieRequest.SET,
                sw_configuration_cookie=0xFF))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetSwConfigurationCookieResponse fields are restored to default")
        # --------------------------------------------------------------------------------------------------------------
        sw_cookie_check_map = sw_cookie_checker.get_default_check_map(self)
        sw_cookie_checker.check_fields(self, set_sw_configuration_cookie_response,
                                       self.feature_1b05.get_set_sw_configuration_cookie_response_cls,
                                       sw_cookie_check_map)
        
        self.testCaseChecked("FUN_1805_0040", _AUTHOR)
    # end def test_full_key_customization_on_1b05_reset

    @features("Feature1805")
    @features("Feature2111")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_wheel_mode_on_2111_reset(self):
        """
        Validate the 'wheelMode' and 'autoDisengage' parameters linked to the 0x2111 feature restored to the default
        value

        Require 0x2111 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        smart_shift_tunable_config = self.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "wheelMode and autoDisengage parameters is set to Default")
        # --------------------------------------------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.set_control_mode_configuration(
            self, smart_shift_tunable_config.F_WheelModeDefault, smart_shift_tunable_config.F_AutoDisengageDefault,
            smart_shift_tunable_config.F_DefaultTunableTorque)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRatchetControlMode request with wheel mode and autodisengage other than the "
                                 "default value")
        # --------------------------------------------------------------------------------------------------------------
        wheel_mode_non_default = SmartShiftTunable.WheelModeConst.RATCHET if \
            smart_shift_tunable_config.F_WheelModeDefault == SmartShiftTunable.WheelModeConst.FREESPIN else \
            SmartShiftTunable.WheelModeConst.FREESPIN

        auto_disengage_non_default = smart_shift_tunable_config.F_AutoDisengageDefault - 1
        tunable_torque_non_default = smart_shift_tunable_config.F_DefaultTunableTorque - 1
        SmartShiftTunableTestUtils.HIDppHelper.set_control_mode_configuration(self, wheel_mode_non_default,
                                                                              auto_disengage_non_default,
                                                                              tunable_torque_non_default)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Send GetRatchetControlMode request to check wheel mode is reflecting correctly")
        # --------------------------------------------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(self, expected=wheel_mode_non_default)
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_auto_disengage(self, auto_disengage_non_default)
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_current_tunable_torque(self, tunable_torque_non_default)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetRatchetControlMode and validate the wheel mode and "
                                 "autodisengage is same as default value")
        # --------------------------------------------------------------------------------------------------------------
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_wheel_mode(
            self, smart_shift_tunable_config.F_WheelModeDefault)
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_auto_disengage(
            self, smart_shift_tunable_config.F_AutoDisengageDefault)
        SmartShiftTunableTestUtils.HIDppHelper.get_and_check_current_tunable_torque(
            self, smart_shift_tunable_config.F_DefaultTunableTorque)

        self.testCaseChecked("FUN_1805_0019", _AUTHOR)
    # end def test_wheel_mode_on_2111_reset

    @features("Feature1805")
    @features("Feature2121")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_analytics_on_2121_reset(self):
        """
        Validate the 'target ', 'resolution',  'invert' and 'analytics' parameters linked to the 0x2121 feature
        restored to the default value

        Require 0x2121 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2121 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_2121_index, self.feature_2121, _, _ = DeviceBaseTestUtils.HIDppHelper.get_parameters(
            test_case=self, feature_id=HiResWheel.FEATURE_ID, factory=HiResWheelFactory,
            device_index=None, port_index=None, skip_not_found=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "target, resolution, invert and analytics parameters is set to Default")
        # --------------------------------------------------------------------------------------------------------------
        set_wheel_mode = self.feature_2121.set_wheel_mode_cls(
            deviceIndex=HexList(ChannelUtils.get_device_index(self)), featureId=self.feature_2121_index,
            reserved=HiResWheel.DEFAULT_RESERVED, analytics=HiResWheel.NON_ANALYTIC, invert=HiResWheel.NOT_INVERT,
            resolution=HiResWheel.LOW_RESOLUTION, target=HiResWheel.HID)

        set_wheel_mode_response = ChannelUtils.send(
            test_case=self, report=set_wheel_mode, response_queue_name=HIDDispatcher.QueueName.MOUSE,
            response_class_type=self.feature_2121.set_wheel_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetWheelMode response")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HiResWheel.HID,
                         obtained=int(set_wheel_mode_response.target),
                         msg='The target parameter differs from the one expected')
        self.assertEqual(expected=HiResWheel.LOW_RESOLUTION,
                         obtained=int(set_wheel_mode_response.resolution),
                         msg='The resolution parameter differs from the one expected')
        self.assertEqual(expected=HiResWheel.NOT_INVERT,
                         obtained=int(set_wheel_mode_response.invert),
                         msg='The invert parameter differs from the one expected')
        if self.f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_Version_1:
            self.assertEqual(expected=HiResWheel.NON_ANALYTIC,
                             obtained=int(set_wheel_mode_response.analytics),
                             msg='The analytics parameter differs from the one expected')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetWheelMode with target, resolution, invert and analytics other than the"
                                 "default value.")
        # --------------------------------------------------------------------------------------------------------------
        set_wheel_mode = self.feature_2121.set_wheel_mode_cls(
            deviceIndex=HexList(ChannelUtils.get_device_index(self)), featureId=self.feature_2121_index,
            reserved=HiResWheel.DEFAULT_RESERVED, analytics=HiResWheel.ANALYTIC, invert=HiResWheel.INVERT,
            resolution=HiResWheel.HIGH_RESOLUTION, target=HiResWheel.HIDPP)

        set_wheel_mode_response = ChannelUtils.send(
            test_case=self, report=set_wheel_mode, response_queue_name=HIDDispatcher.QueueName.MOUSE,
            response_class_type=self.feature_2121.set_wheel_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetWheelMode response")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HiResWheel.HIDPP,
                         obtained=int(set_wheel_mode_response.target),
                         msg='The target parameter differs from the one expected')
        self.assertEqual(expected=HiResWheel.HIGH_RESOLUTION,
                         obtained=int(set_wheel_mode_response.resolution),
                         msg='The resolution parameter differs from the one expected')
        self.assertEqual(expected=HiResWheel.INVERT,
                         obtained=int(set_wheel_mode_response.invert),
                         msg='The invert parameter differs from the one expected')
        if self.f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_Version_1:
            self.assertEqual(expected=HiResWheel.ANALYTIC,
                             obtained=int(set_wheel_mode_response.analytics),
                             msg='The analytics parameter differs from the one expected')
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelMode")
        # --------------------------------------------------------------------------------------------------------------
        get_wheel_mode = self.feature_2121.get_wheel_mode_cls(deviceIndex=HexList(ChannelUtils.get_device_index(self)),
                                                              featureId=self.feature_2121_index, )

        get_wheel_mode_response = ChannelUtils.send(test_case=self, report=get_wheel_mode,
                                                    response_queue_name=HIDDispatcher.QueueName.MOUSE,
                                                    response_class_type=self.feature_2121.get_wheel_mode_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the target, resolution, invert and analytics is same as default value")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=HiResWheel.HID,
                         obtained=int(get_wheel_mode_response.target),
                         msg='The target parameter differs from the one expected')
        self.assertEqual(expected=HiResWheel.LOW_RESOLUTION,
                         obtained=int(get_wheel_mode_response.resolution),
                         msg='The resolution parameter differs from the one expected')
        self.assertEqual(expected=HiResWheel.NOT_INVERT,
                         obtained=int(get_wheel_mode_response.invert),
                         msg='The invert parameter differs from the one expected')

        if self.f.PRODUCT.FEATURES.MOUSE.HI_RES_WHEEL.F_Version_1:
            self.assertEqual(expected=HiResWheel.NON_ANALYTIC,
                             obtained=int(get_wheel_mode_response.analytics),
                             msg='The analytics parameter differs from the one expected')
        # end if

        self.testCaseChecked("FUN_1805_0020", _AUTHOR)
    # end def test_analytics_on_2121_reset

    @features("Feature1805")
    @features("Feature2130")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_ratchet_wheel_on_2130_reset(self):
        """
        Validate the 'divert' parameters linked to the 0x2130 feature restored to the default value

        Require 0x2130 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2130")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_2130, _, _ = RatchetWheelTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send SetModeStatus with Divert set to Default")
        # --------------------------------------------------------------------------------------------------------------
        set_mode_status_response = RatchetWheelTestUtils.HIDppHelper.set_mode_status(self, RatchetWheel.DIVERT.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetModeStatusResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.SetModeStatusResponseChecker
        checker.check_fields(self, set_mode_status_response, self.feature_2130.set_mode_status_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetWheelMode with Divert=HID++(1)")
        # --------------------------------------------------------------------------------------------------------------
        set_mode_status_response = RatchetWheelTestUtils.HIDppHelper.set_mode_status(self, RatchetWheel.DIVERT.HIDPP)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetModeStatusResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.SetModeStatusResponseChecker
        check_map = checker.get_check_map(self, divert=RatchetWheel.DIVERT.HIDPP)
        checker.check_fields(self, set_mode_status_response, self.feature_2130.set_mode_status_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetWheelMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = RatchetWheelTestUtils.HIDppHelper.get_wheel_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the Divert is same as default value.(HID Mode -0)")
        # --------------------------------------------------------------------------------------------------------------
        checker = RatchetWheelTestUtils.GetWheelModeResponseChecker
        check_map = checker.get_check_map(self, RatchetWheel.DIVERT.HID)
        checker.check_fields(self, response, self.feature_2130.get_wheel_mode_response_cls, check_map)

        self.testCaseChecked("FUN_1805_0021", _AUTHOR)
    # end def test_ratchet_wheel_on_2130_reset

    @features("Feature1805")
    @features("Feature2150")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_thumb_wheel_on_2150_reset(self):
        """
        Validate the "reporting_mode" and "invert direction" parameters linked to the 0x2150 feature
        restored to the default value

        Require 0x2150 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2150 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_2150, _, _ = ThumbwheelTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send SetThumbwheelReporting with reporting_mode and invert_direction set to "
                                         "Default")
        # --------------------------------------------------------------------------------------------------------------
        set_thumbwheel_reporting_response = ThumbwheelTestUtils.HIDppHelper.set_thumbwheel_reporting(
            self, Thumbwheel.REPORTING_MODE.HID, ThumbwheelTestUtils.DEFAULT_DIR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetThumbwheelReportingResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        checker.check_fields(self, set_thumbwheel_reporting_response,
                             self.feature_2150.set_thumbwheel_reporting_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetThumbwheelReporting with reporting_mode and invert_direction than the"
                                 "default value")
        # --------------------------------------------------------------------------------------------------------------
        ThumbwheelTestUtils.HIDppHelper.set_thumbwheel_reporting(self, Thumbwheel.REPORTING_MODE.HIDPP,
                                                                 ThumbwheelTestUtils.INVERTED_DIR)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetThumbwheelReportingResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        checker.check_fields(self, set_thumbwheel_reporting_response,
                             self.feature_2150.set_thumbwheel_reporting_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetThumbwheelStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = ThumbwheelTestUtils.HIDppHelper.get_thumbwheel_status(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the reporting_mode and invert_direction is same as default value")
        # --------------------------------------------------------------------------------------------------------------
        checker = ThumbwheelTestUtils.GetThumbwheelStatusResponseChecker
        check_map = checker.get_check_map(self)
        checker.check_fields(self, response, self.feature_2150.get_thumbwheel_status_response_cls, check_map)

        self.testCaseChecked("FUN_1805_0022", _AUTHOR)
    # end def test_thumb_wheel_on_2150_reset

    @features("Feature1805")
    @features("Feature2201")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_dpi_values_on_2201_reset(self):
        """
        Validate the 'dpi' parameters linked to the 0x2201 feature restored to the default value

        Require 0x2201 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        adjustable_dpi_config = self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send SetSensorDPI request with Default value")
        # --------------------------------------------------------------------------------------------------------------
        set_sensor_dpi_response = AdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi(
            self, sensor_idx=0, dpi=int(adjustable_dpi_config.F_DpiDefault), dpi_level=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate SetSensorDpiResponse fields')
        # --------------------------------------------------------------------------------------------------------------
        AdjustableDpiTestUtils.SetSensorDpiResponseChecker.check_fields(
            self, set_sensor_dpi_response, self.feature_2201.set_sensor_dpi_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetSensorDpi with different DPI than the default value")
        # --------------------------------------------------------------------------------------------------------------
        if adjustable_dpi_config.F_DpiDefault != adjustable_dpi_config.F_DpiMax:
            new_dpi_value = adjustable_dpi_config.F_DpiMax
        else:
            new_dpi_value = adjustable_dpi_config.F_DpiMin
        # end if

        set_sensor_dpi_response = AdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi(self, sensor_idx=0,
                                                                                    dpi=int(new_dpi_value), dpi_level=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check SetSensorDpi resposnse fields')
        # --------------------------------------------------------------------------------------------------------------
        checker = AdjustableDpiTestUtils.SetSensorDpiResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "dpi": (checker.check_dpi, new_dpi_value)
            }
        )
        AdjustableDpiTestUtils.SetSensorDpiResponseChecker.check_fields(
            self, set_sensor_dpi_response, self.feature_2201.set_sensor_dpi_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSensorDpi request")
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_dpi_response = AdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the DPI is same as default value")
        # --------------------------------------------------------------------------------------------------------------
        AdjustableDpiTestUtils.GetSensorDpiResponseChecker.check_fields(self, get_sensor_dpi_response,
                                                                        self.feature_2201.get_sensor_dpi_response_cls)

        self.testCaseChecked("FUN_1805_0023", _AUTHOR)
    # end def test_dpi_values_on_2201_reset

    @features("Feature1805")
    @features("Feature2202")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_dpi_values_on_2202_reset(self):
        """
        Validate the 'dpi' parameters linked to the 0x2202 feature restored to the default value

        Require 0x2202 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        extended_adjustable_dpi_config = self.f.PRODUCT.FEATURES.MOUSE.EXTENDED_ADJUSTABLE_DPI

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Switch to Host Mode")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(self, OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2202 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_2202, _, _ = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send SetSensorDPIParameters with DPI and LOD set to Default")
        # --------------------------------------------------------------------------------------------------------------
        set_sensor_dpi_parameters_response = ExtendedAdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi_parameters(
            test_case=self, sensor_idx=0, dpi_x=extended_adjustable_dpi_config.F_DefaultDpiX,
            dpi_y=extended_adjustable_dpi_config.F_DefaultDpiY,
            lod=extended_adjustable_dpi_config.F_DefaultLod)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetSensorDpiParametersResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.SetSensorDpiParametersResponseChecker.check_fields(
            self, set_sensor_dpi_parameters_response, self.feature_2202.set_sensor_dpi_parameters_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetSensorDpiParameters with different DPI and LOD than the default value")
        # --------------------------------------------------------------------------------------------------------------
        dpi_y = 0
        dpi_x = 0
        dpi_lod = 1
        if extended_adjustable_dpi_config.F_DpiYSupported:
            for dpi in extended_adjustable_dpi_config.F_DpiListY:
                if int(dpi) != extended_adjustable_dpi_config.F_DefaultDpiY:
                    dpi_y = int(dpi)
                    break
                # end if
            # end for
        # end if

        if extended_adjustable_dpi_config.F_LodSupported:
            for lod in extended_adjustable_dpi_config.F_DpiLodList:
                if int(lod) != extended_adjustable_dpi_config.F_DefaultLod:
                    dpi_lod = int(lod)
                    break
                # end if
            # end for
        # end if

        for dpi in extended_adjustable_dpi_config.F_DpiListX:
            if int(dpi) != extended_adjustable_dpi_config.F_DefaultDpiX:
                dpi_x = int(dpi)
                break
            # end if
        # end for

        ExtendedAdjustableDpiTestUtils.HIDppHelper.set_sensor_dpi_parameters(test_case=self,
                                                                             sensor_idx=0,
                                                                             dpi_x=dpi_x,
                                                                             dpi_y=dpi_y,
                                                                             lod=dpi_lod)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetSensorDpiParameters request")
        # --------------------------------------------------------------------------------------------------------------
        get_sensor_dpi_parameters_response = ExtendedAdjustableDpiTestUtils.HIDppHelper.get_sensor_dpi_parameters(
            test_case=self, sensor_idx=0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the DPI and IodN is same as default value")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableDpiTestUtils.GetSensorDpiParametersResponseChecker.check_fields(
            self, get_sensor_dpi_parameters_response, self.feature_2202.get_sensor_dpi_parameters_response_cls)

        self.testCaseChecked("FUN_1805_0024", _AUTHOR)
    # end def test_dpi_values_on_2202_reset

    @features("Feature1805")
    @features("Feature2250")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_reporting_mode_on_2250_reset(self):
        """
        Validate the 'mode' parameters linked to the 0x2250 feature restored to the default value

        Require 0x2250 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2250 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_2250_index, self.feature_2250, _, _ = AnalysisModeTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send SetAnalysisMode request with mode set to Default")
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, AnalysisMode.MODE.OFF)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetAnalysisModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.SetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2250.set_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetAnalysisMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetAnalysisModeResponse fields if analysis mode is OFF")
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetAnalysisMode request with different mode than the default value")
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.set_analysis_mode(self, AnalysisMode.MODE.ON)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetAnalysisModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.SetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, AnalysisMode.MODE.ON)
            }
        )
        checker.check_fields(self, response, self.feature_2250.set_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetAnalysisMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetAnalysisModeResponse fields if analysis mode is ON")
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "mode": (checker.check_mode, AnalysisMode.MODE.ON)
            }
        )
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetAnalysisMode request")
        # --------------------------------------------------------------------------------------------------------------
        response = AnalysisModeTestUtils.HIDppHelper.get_analysis_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the mode is same as default value")
        # --------------------------------------------------------------------------------------------------------------
        checker = AnalysisModeTestUtils.GetAnalysisModeResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_2250.get_analysis_mode_response_cls, check_map)

        self.testCaseChecked("FUN_1805_0025", _AUTHOR)
    # end def test_reporting_mode_on_2250_reset

    @features("Feature1805")
    @features("Feature2251")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_reporting_mode_on_2251_reset(self):
        """
        Validate the 'reporting_mode' parameters linked to the 0x2251 feature restored to the default value

        Require 0x2251 feature
        """
        raise NotImplementedError("Feature 0x2251 was not available during 0x1805 test scripts implementation")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x2251 index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "reporting mode is set to Default")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setAnalyticsMode with different reporting mode than the default value.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setOOBState")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getAnalyticsMode")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the reporting mode is same as default value.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0026", _AUTHOR)
    # end def test_reporting_mode_on_2251_reset

    @features("Feature1805")
    @features("Feature40A3")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_fn_inversion_on_40a3_reset(self):
        """
        Validate the 'fnInversionState' parameters linked to the 0x40A3 feature restored to the default value

        Require 0x40a3 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        fn_inversion_config = self.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x40a3 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_40a3, _, _ = FnInversionForMultiHostDevicesTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send SetGlobalFNInversion with Inversion state is to Default")
        # --------------------------------------------------------------------------------------------------------------
        if self.f.PRODUCT.DEVICE.F_NbHosts == 1:
            host_index = 0
        else:
            host_index = ChangeHostTestUtils.HIDppHelper.get_host_info(self).curr_host
        # end if

        set_global_fn_inversion_response = FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(
            self, host_index, fn_inversion_config.F_FnInversionDefaultState)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetGlobalFnInversionResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = FnInversionForMultiHostDevicesTestUtils.SetGlobalFnInversionResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "fn_inversion_state": (checker.check_fn_inversion_state,
                                   fn_inversion_config.F_FnInversionDefaultState),
        })
        checker.check_fields(self, set_global_fn_inversion_response,
                             self.feature_40a3.set_global_fn_inversion_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetGlobalFnInversion with different inversion state than the default value")
        # --------------------------------------------------------------------------------------------------------------
        new_fn_inversion_state = 1 if not fn_inversion_config.F_FnInversionDefaultState else 0
        set_global_fn_inversion_response = FnInversionForMultiHostDevicesTestUtils.HIDppHelper.set_global_fn_inversion(
            self, host_index, new_fn_inversion_state)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetGlobalFnInversionResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = FnInversionForMultiHostDevicesTestUtils.SetGlobalFnInversionResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "host_index": (checker.check_host_index, host_index),
                "fn_inversion_state": (checker.check_fn_inversion_state, new_fn_inversion_state),
            }
        )
        checker.check_fields(self, set_global_fn_inversion_response,
                             self.feature_40a3.set_global_fn_inversion_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetGlobalFnInversion request")
        # --------------------------------------------------------------------------------------------------------------
        if self.f.PRODUCT.DEVICE.F_NbHosts == 1:
            host_index = 0
        else:
            host_index = ChangeHostTestUtils.HIDppHelper.get_host_info(self).curr_host
        # end if

        get_fn_inversion_response = FnInversionForMultiHostDevicesTestUtils.HIDppHelper.get_global_fn_inversion(
            self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the inversion state is same as default value.")
        # --------------------------------------------------------------------------------------------------------------
        checker = FnInversionForMultiHostDevicesTestUtils.GetGlobalFnInversionResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "host_index": (checker.check_host_index, host_index)
            }
        )
        checker.check_fields(self, get_fn_inversion_response,
                             self.feature_40a3.get_global_fn_inversion_response_cls, check_map)

        self.testCaseChecked("FUN_1805_0027", _AUTHOR)
    # end def test_fn_inversion_on_40a3_reset

    @features("Feature1805")
    @features("Feature4521")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_disable_keys_on_4521_reset(self):
        """
        Validate the 'windows', 'Insert', 'ScrollLock', 'NumLock' and 'CapsLock' parameters linked to the 0x4521
        feature restored to the default value

        Require 0x4521 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        disable_keys_config = self.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_KEYS

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x4521 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_4521, _, _ = DisableKeysUtils.HIDppHelper.get_parameters(test_case=self,
                                                                                 feature_id=DisableKeys.FEATURE_ID,
                                                                                 factory=DisableKeysFactory)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send SetDisabledKeys request with windows, insert, scroll lock, num lock and "
                                         "caps lock state is set to default state")
        # --------------------------------------------------------------------------------------------------------------
        self.default_disabled_keys = disable_keys_config.F_DefaultDisabledKeys
        set_disabled_keys_response = DisableKeysUtils.HIDppHelper.set_disabled_keys(
            test_case=self, keys_to_disable=self.default_disabled_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetDisabledKeysResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
            test_case=self, message=set_disabled_keys_response,
            expected_cls=self.feature_4521.set_disabled_keys_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetDisabledKeys with different state other than the default value")
        # --------------------------------------------------------------------------------------------------------------
        keys_to_disable = DisableKeysUtils.convert_all_disableable_keys_to_int(self)
        set_disabled_keys_response = DisableKeysUtils.HIDppHelper.set_disabled_keys(test_case=self,
                                                                                    keys_to_disable=keys_to_disable)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetDisabledKeysResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        check_map = DisableKeysUtils.update_disabled_keys_for_check_map(test_case=self,
                                                                        keys_to_disable=keys_to_disable)
        DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
            test_case=self,
            message=set_disabled_keys_response,
            expected_cls=self.feature_4521.set_disabled_keys_response_cls,
            check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over disabled keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in DisableKeysUtils.convert_disableable_keys_to_key_id(self):
            if key not in self.button_stimuli_emulator.get_fn_keys():
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Key Press the disabled key {key}")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.HID)
                self.button_stimuli_emulator.key_press(key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify HID Report not received for make")
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.check_queue_empty(test_case=self,
                                               timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                               queue_name=HIDDispatcher.QueueName.HID)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Key Release the disabled key")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify HID Report not received for break")
                # ------------------------------------------------------------------------------------------------------
                # Empty hid_message_queue
                # TODO: Temporary workaround to clear the report returned when releasing the Left Win key
                # cf https://jira.logitech.io/browse/NRF52-503
                ChannelUtils.clean_messages(
                    test_case=self, channel=self.current_channel, queue_name=HIDDispatcher.QueueName.HID,
                    class_type=HID_REPORTS)
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetDisabledKeys request")
        # --------------------------------------------------------------------------------------------------------------
        get_disabled_keys_response = DisableKeysUtils.HIDppHelper.get_disabled_keys(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the windows, insert, scroll lock, num lock and caps lock state is same as "
                                  "default value")
        # --------------------------------------------------------------------------------------------------------------
        DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
            test_case=self,
            message=get_disabled_keys_response,
            expected_cls=self.feature_4521.get_disabled_keys_response_cls)

        ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.HID)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over disablable keys")
        # --------------------------------------------------------------------------------------------------------------
        for key in DisableKeysUtils.convert_disableable_keys_to_key_id(self):
            if key not in self.button_stimuli_emulator.get_fn_keys():
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Key Press the key {key}")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_press(key)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify HID Report is received for make")
                # ------------------------------------------------------------------------------------------------------
                if key in HidData.KEY_ID_TO_HID_MAP:
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(key, MAKE))
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Key Release the key")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.key_release(key)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, "Verify HID Report is received for break")
                # ------------------------------------------------------------------------------------------------------
                if key in HidData.KEY_ID_TO_HID_MAP:
                    KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                                  key=KeyMatrixTestUtils.Key(key, BREAK))
                # end if
            # end if
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0028", _AUTHOR)
    # end def test_disable_keys_on_4521_reset

    @features("Feature1805")
    @features("Feature4522")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_disable_keys_on_4522_reset(self):
        """
        Validate the 'windows', 'Insert', 'ScrollLock', 'NumLock' and 'CapsLock' parameters linked to the 0x4522
        feature restored to the default value

        Require 0x4522 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        default_disabled_keys = []

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x4522 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_4522, _, _ = DisableKeysByUsageTestUtils.HIDppHelper.get_parameters(
            test_case=self, factory=DisableKeysByUsageFactory, feature_id=DisableKeysByUsage.FEATURE_ID)

        for key in STANDARD_KEYS:
            if str(key).split('.')[1] in self.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_KEYS_BY_USAGE.F_DefaultDisableKeys:
                default_disabled_keys.append(key)
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send DisableKeys request disabling default disabled keys")
        # --------------------------------------------------------------------------------------------------------------
        disable_keys_response = DisableKeysByUsageTestUtils.HIDppHelper.disable_keys(self, default_disabled_keys)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DisableKeysResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
            test_case=self,
            messages=disable_keys_response,
            expected_cls=self.feature_4522.disable_keys_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Empty the HID message que")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # --------------------------------------------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send disableKeys all of standard keys')
        # --------------------------------------------------------------------------------------------------------------
        standard_keys_id = DisableKeysByUsageTestUtils.get_keyboard_standard_key_id(
            test_case=self,
            keyboard_layout=self.button_stimuli_emulator._keyboard_layout.KEYS.keys())
        disable_keys_resp = DisableKeysByUsageTestUtils.disable_keys_by_key_id(test_case=self,
                                                                               keys=standard_keys_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check disableKeys response fields")
        # --------------------------------------------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.DisableKeysResponseChecker.check_disable_keys_responses(
            test_case=self,
            messages=disable_keys_resp,
            expected_cls=self.feature_4522.disable_keys_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on all of standard keys')
        # --------------------------------------------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=standard_keys_id,
                                                                  collect_hid_report=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate host can not receive key report')
        # --------------------------------------------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Empty the HID message que")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.HID)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable game mode')
        # --------------------------------------------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.enable_game_mode(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate key strokes on default disabled keys')
        # --------------------------------------------------------------------------------------------------------------
        keys_reports = KeyMatrixTestUtils.stroke_keys_in_sequence(test_case=self,
                                                                  keys=default_disabled_keys,
                                                                  collect_hid_report=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate host cannot receive key report')
        # --------------------------------------------------------------------------------------------------------------
        DisableKeysByUsageTestUtils.check_keys_disabled(test_case=self,
                                                        keys_reports=keys_reports)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0029", _AUTHOR)
    # end def test_disable_keys_on_4522_reset

    @features("Feature1805")
    @features("Feature4531")
    @features("SetHostPlatform")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    @bugtracker("Platform_Source")
    def test_multi_platform_on_4531_reset(self):
        """
        Validate the 'platformIndex' parameter linked to the 0x4531 feature restored to the default value

        Require 0x4531 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        marketing_name = self.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
        multi_platform_config = self.f.PRODUCT.FEATURES.KEYBOARD.MULTI_PLATFORM

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x4531 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_4531, _, _ = MultiPlatformTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send SetHostPlatform with platform index set to default")
        # --------------------------------------------------------------------------------------------------------------
        if marketing_name.endswith('for Mac'):
            default_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
                self, MultiPlatform.OsMask.MAC_OS)
        else:
            default_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
                self, MultiPlatform.OsMask.WINDOWS)
        # end if

        if self.f.PRODUCT.DEVICE.F_NbHosts == 1:
            host_index = 0
        else:
            host_index = ChangeHostTestUtils.HIDppHelper.get_host_info(self).curr_host
        # end if

        set_host_platform_response = MultiPlatformTestUtils.HIDppHelper.set_host_platform(
            self, host_index, default_platform_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetHostPlatformResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.SetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "host_index": (checker.check_host_index, host_index),
                "platform_index": (checker.check_platform_index, default_platform_index),
            }
        )
        checker.check_fields(self, set_host_platform_response,
                             self.feature_4531.set_host_platform_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetHostPlatform with platformIndex other than the default value")
        # --------------------------------------------------------------------------------------------------------------
        if not marketing_name.endswith('for Mac'):
            new_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
                self, MultiPlatform.OsMask.MAC_OS)
        else:
            new_platform_index = MultiPlatformTestUtils.get_platform_index_thru_os_mask(
                self, MultiPlatform.OsMask.IOS)
        # end if

        set_host_platform_response = MultiPlatformTestUtils.HIDppHelper.set_host_platform(
            self, host_index, new_platform_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetHostPlatformResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.SetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update(
            {
                "host_index": (checker.check_host_index, host_index),
                "platform_index": (checker.check_platform_index, new_platform_index),
            }
        )
        checker.check_fields(self, set_host_platform_response,
                             self.feature_4531.set_host_platform_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetHostPlatform request")
        # --------------------------------------------------------------------------------------------------------------
        if self.f.PRODUCT.DEVICE.F_NbHosts == 1:
            host_index = 0
        else:
            host_index = ChangeHostTestUtils.HIDppHelper.get_host_info(self).curr_host
        # end if

        response = MultiPlatformTestUtils.HIDppHelper.get_host_platform(self, host_index)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the platformIndex is same as default value")
        # --------------------------------------------------------------------------------------------------------------
        checker = MultiPlatformTestUtils.GetHostPlatformResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "host_index": (checker.check_host_index, host_index),
            "status": (checker.check_status, MultiPlatform.Status.PAIRED),
            "platform_index": (checker.check_platform_index, default_platform_index),
            "platform_source": (checker.check_platform_source, MultiPlatform.PlatformSource.DEFAULT),
            "auto_platform": (checker.check_auto_platform,
                              int(multi_platform_config.F_AutoPlatform[to_int(host_index)])),
            "auto_descriptor": (checker.check_auto_descriptor,
                                int(multi_platform_config.F_AutoDescriptor[to_int(host_index)])),
        })
        checker.check_fields(self, response, self.feature_4531.get_host_platform_response_cls, check_map)

        self.testCaseChecked("FUN_1805_0030", _AUTHOR)
    # end def test_multi_platform_on_4531_reset

    @features("Feature1805")
    @features("Feature8010")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_g_keys_on_8010_reset(self):
        """
        Validate the 'enable' parameters linked to the 0x8010 feature restored to the default value

        Require 0x8010 feature
        """
        raise NotImplementedError("Feature 0x8010 was not available during 0x1805 test scripts implementation")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8010 index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Software control flag is set to False(Default)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send enableSoftwareControl with enable = True")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with G Keys")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: fill this condition
        for _ in []:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Key Press and Release the G Key")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "ButtonReport event received for the selected Key")
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setOOBState")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop with G Keys")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: fill this condition
        for _ in []:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Key Press and Release the G Key")
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "ButtonReport event not received.")
            # ----------------------------------------------------------------------------------------------------------
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("FUN_1805_0031", _AUTHOR)
    # end def test_g_keys_on_8010_reset

    @features("Feature1805")
    @features("Feature8020")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_m_keys_on_8020_reset(self):
        """
        Validate the 'M-Key LED' states linked to the 0x8020 feature restored to the default value

        Require 0x8020 feature
        """
        raise NotImplementedError("Feature 0x8020 was not available during 0x1805 test scripts implementation")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8020 index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "KeyPress M1, Ensure M1 LED is ON and M2 and M3 LED's are OFF")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setMKeyLED to Turn on M2 and turn off M1.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check M2 LED is ON and all other M-Keys are OFF")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setOOBState")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check M1 LED is ON and all other M-Keys are OFF")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0032", _AUTHOR)
    # end def test_m_keys_on_8020_reset

    @features("Feature1805")
    @features("Feature8030")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_mr_key_on_8030_reset(self):
        """
        Validate the 'MR button LED' state linked to the 0x8030 feature restored to the default value

        Require 0x8030 feature
        """
        raise NotImplementedError("Feature 0x8030 was not available during 0x1805 test scripts implementation")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8030 index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "KeyPress MR, Ensure MR LED is ON.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setLED to Turn on MR")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check MR LED is ON.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setOOBState")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check MR LED is OFF.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0033", _AUTHOR)
    # end def test_mr_key_on_8030_reset

    @features("Feature1805")
    @features("Feature8040")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_brightness_on_8040_reset(self):
        """
        Validate the 'brightness' value linked to the 0x8040 feature restored to the default value

        Require 0x8040 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        non_default_brightness = self.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL.F_MaxBrightness - \
            self.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL.F_DefaultBrightness

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8040 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8040_index, self.feature_8040, _, _ = BrightnessControlTestUtils.HIDppHelper.get_parameters(
            test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetBrightness request with max possible brightness value = "
                                 f"{non_default_brightness}")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.set_brightness(self, non_default_brightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Check SetBrightnessResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.MessageChecker.check_fields(
            self, response, self.feature_8040.set_brightness_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _SEND_OOB_AND_POWER_CYCLE)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetBrightness request")
        # --------------------------------------------------------------------------------------------------------------
        response = BrightnessControlTestUtils.HIDppHelper.get_brightness(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the brightness is same as default value.")
        # --------------------------------------------------------------------------------------------------------------
        checker = BrightnessControlTestUtils.GetBrightnessResponseChecker
        check_map = checker.get_default_check_map(self)
        checker.check_fields(self, response, self.feature_8040.get_brightness_response_cls, check_map)

        self.testCaseChecked("FUN_1805_0034", _AUTHOR)
    # end def test_brightness_on_8040_reset

    @features("Feature1805")
    @features("Feature8060")
    @features("Feature8100")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_report_rate_on_8060_reset(self):
        """
        Validate the 'report_rate' parameter linked to the 0x8060 feature restored to the default value

        Require 0x8060 feature

        :raise ``AssertionError``: Can't find a report rate different from the default one
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True

        host_mode = OnboardProfiles.Mode.HOST_MODE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8060 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_8060, _, _ = ReportRateTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {host_mode} (host mode)")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=host_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send SetReportRate request with report rate set to Default value")
        # --------------------------------------------------------------------------------------------------------------
        default_report_rate = int(self.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.OOB_PROFILES.F_ReportRate[0])
        set_report_rate_response = ReportRateTestUtils.HIDppHelper.set_report_rate(self, default_report_rate)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetReportRateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        checker.check_fields(self, set_report_rate_response, self.feature_8060.set_report_rate_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetReportRate with other than the default value")
        # --------------------------------------------------------------------------------------------------------------
        report_rate_list = ReportRateTestUtils.get_default_report_rate_list(self)
        new_report_rate = None
        for report_rate in report_rate_list:
            if report_rate != default_report_rate:
                new_report_rate = report_rate
                break
            # end if
        # end for

        assert new_report_rate is not None
        set_report_rate_response = ReportRateTestUtils.HIDppHelper.set_report_rate(self, new_report_rate)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetReportRateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        checker.check_fields(self, set_report_rate_response, self.feature_8060.set_report_rate_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetReportRate request")
        # --------------------------------------------------------------------------------------------------------------
        response = ReportRateTestUtils.HIDppHelper.get_report_rate(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the report rate is same as default value")
        # --------------------------------------------------------------------------------------------------------------
        checker = ReportRateTestUtils.GetReportRateResponseChecker
        checker.check_fields(self, response, self.feature_8060.get_report_rate_response_cls)

        self.testCaseChecked("FUN_1805_0035", _AUTHOR)
    # end def test_report_rate_on_8060_reset

    @features("Feature1805")
    @features("Feature8061")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_report_rate_on_8061_reset(self):
        """
        Validate the 'reportRate' parameter linked to the 0x8061 feature restored to the default value

        Require 0x8061 feature

        :raise ``AssertionError``: Can't find a report rate different from the default one
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        onboard_mode = OnboardProfiles.Mode.HOST_MODE
        fw_config = self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION
        device_supported_connection_type = {
            ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS: fw_config.F_TransportEQuad,
            ExtendedAdjustableReportRate.ConnectionType.WIRED: fw_config.F_TransportUsb}

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8061")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_8061, _, _ = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over supported connection types.")
        # --------------------------------------------------------------------------------------------------------------
        for connection_type, supported in device_supported_connection_type.items():
            if not supported:
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "DUT is paired with the host using the target connection type.")
            # ----------------------------------------------------------------------------------------------------------
            if connection_type == ExtendedAdjustableReportRate.ConnectionType.WIRED:
                self.post_requisite_unplug_usb_cable = True
                ProtocolManagerUtils.switch_to_usb_channel(self)
                ChannelUtils.update_feature_mapping(test_case=self, feature_id=ExtendedAdjustableReportRate.FEATURE_ID)
            elif connection_type == ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS:
                OobStateTestUtils.pair_device(self)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {onboard_mode} (Host Mode)")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=onboard_mode)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetReportRate request with other than the default value")
            # ----------------------------------------------------------------------------------------------------------
            supported_report_rate_list = ExtendedAdjustableReportRateTestUtils.get_supported_rate_list(test_case=self)
            default_report_rate = ExtendedAdjustableReportRateTestUtils.get_highest_report_rate(self)

            new_report_rate = None
            for report_rate in supported_report_rate_list:
                if report_rate != default_report_rate:
                    new_report_rate = report_rate
                    break
                # end if
            # end for

            assert new_report_rate is not None
            set_report_rate_response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(
                test_case=self, report_rate=new_report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetReportRateResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.SetReportRateResponseChecker
            checker.check_fields(self, set_report_rate_response, self.feature_8061.set_report_rate_response_cls, {})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, _SEND_OOB)
            # ----------------------------------------------------------------------------------------------------------
            OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Pair the device with a new host")
            # ----------------------------------------------------------------------------------------------------------
            if connection_type == ExtendedAdjustableReportRate.ConnectionType.WIRED:
                self.post_requisite_unplug_usb_cable = True
                ProtocolManagerUtils.switch_to_usb_channel(self)
                ChannelUtils.update_feature_mapping(test_case=self, feature_id=ExtendedAdjustableReportRate.FEATURE_ID)
            elif connection_type == ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS:
                OobStateTestUtils.pair_device(self)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send GetReportRate request")
            # ----------------------------------------------------------------------------------------------------------
            connection_type = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(self)
            response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_report_rate(
                self, connection_type=connection_type)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate the report rate is same as default value")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_8061.get_report_rate_response_cls, check_map)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0036", _AUTHOR)
    # end def test_report_rate_on_8061_reset

    @features("Feature1805")
    @features("Feature8071")
    @features("PersistenceSupport")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    @services("LedIndicator")
    def test_rgb_effects_on_8071_reset(self):
        """
        Validate the 'Effects', 'persistence', 'Power mode' & 'swControlFlags'  parameter linked to the 0x8071
        feature restored to the default value

        Require 0x8071 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        oob_profiles_config = self.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.OOB_PROFILES

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8071 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_8071, _, _ = RGBEffectsTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRgbClusterEffect with Persistence to non-volatile")
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.set_fixed_effect(test_case=self,
                                                         cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                                         red=0x00, green=0x00, blue=0x00,
                                                         mode=RGBEffectsTestUtils.FixedRGBEffectMode.DEFAULT,
                                                         persistence=RGBEffectsTestUtils.Persistence.NON_VOLATILE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ManageSwControl request with all swControlFlags to enabled")
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.HIDppHelper.manage_sw_control(
            self,
            get_or_set=1,
            sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS)
        RGBEffectsTestUtils.HIDppHelper.manage_sw_control(
            self,
            get_or_set=1,
            sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_POWER_MODES)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ManageRgbPowerModeConfig with non default values for timeout")
        # --------------------------------------------------------------------------------------------------------------
        power_save_timeout_s = int(oob_profiles_config.PowerSaveTimeout_S[0]) * 2
        power_off_timeout_s = int(oob_profiles_config.PowerOffTimeout_S[0]) * 2
        RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode_config(
            self, get_or_set=1, rgb_power_mode_flags=RGBEffectsTestUtils.PowerMode.FULL_POWER_MODE,
            rgb_no_act_timeout_to_psave=power_save_timeout_s,
            rgb_no_act_timeout_to_off=power_off_timeout_s)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate LED effect is set to bootUpEffect and all other parameters restored to"
                                  "its default value")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Validate LED effect is set to bootUpEffect and all other parameters restored to it's default value
        warnings.warn("Validate LED effect is set to bootUpEffect and all other parameters restored to it's default "
                      "value using led spy")

        self.testCaseChecked("FUN_1805_0037", _AUTHOR)
    # end def test_rgb_effects_on_8071_reset

    @features("Feature1805")
    @features("Feature8081")
    @level("Functionality")
    @services("Debugger")
    @services("LedIndicator")
    @services("HardwareReset")
    def test_per_key_lighting_on_8081_reset(self):
        """
        Validate the 'RGB LEDs' linked to the 0x8081 feature restored to their default states

        Require 0x8081 feature
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True
        supported_zone_list, _ = PerKeyLightingTestUtils.HIDppHelper.get_zone_info(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8081")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_8081, _, _ = PerKeyLightingTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over z in zoneList by step 13")
        # --------------------------------------------------------------------------------------------------------------
        rgb_zone_red = 0xFF
        rgb_zone_blue = 0x00
        rgb_zone_green = 0x00
        for zones in zip_longest(*[iter(supported_zone_list)] * 13, fillvalue='00'):
            rgb_zone_id_0, rgb_zone_id_1, rgb_zone_id_2, rgb_zone_id_3, \
                rgb_zone_id_4, rgb_zone_id_5, rgb_zone_id_6, rgb_zone_id_7, rgb_zone_id_8, rgb_zone_id_9, \
                rgb_zone_id_10, rgb_zone_id_11, rgb_zone_id_12 = zones

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetRGBZonesSingleValue request with all rgb values = 0xFF")
            # ----------------------------------------------------------------------------------------------------------
            response = PerKeyLightingTestUtils.HIDppHelper.set_rgb_zones_single_value(test_case=self,
                                                                                      rgb_zone_red=rgb_zone_red,
                                                                                      rgb_zone_green=rgb_zone_green,
                                                                                      rgb_zone_blue=rgb_zone_blue,
                                                                                      rgb_zone_id_0=rgb_zone_id_0,
                                                                                      rgb_zone_id_1=rgb_zone_id_1,
                                                                                      rgb_zone_id_2=rgb_zone_id_2,
                                                                                      rgb_zone_id_3=rgb_zone_id_3,
                                                                                      rgb_zone_id_4=rgb_zone_id_4,
                                                                                      rgb_zone_id_5=rgb_zone_id_5,
                                                                                      rgb_zone_id_6=rgb_zone_id_6,
                                                                                      rgb_zone_id_7=rgb_zone_id_7,
                                                                                      rgb_zone_id_8=rgb_zone_id_8,
                                                                                      rgb_zone_id_9=rgb_zone_id_9,
                                                                                      rgb_zone_id_10=rgb_zone_id_10,
                                                                                      rgb_zone_id_11=rgb_zone_id_11,
                                                                                      rgb_zone_id_12=rgb_zone_id_12)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetRGBZonesSingleValueResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PerKeyLightingTestUtils.SetRGBZonesSingleValueResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "rgb_zone_red": (checker.check_rgb_zone_red, HexList(rgb_zone_red)),
                "rgb_zone_green": (checker.check_rgb_zone_green, HexList(rgb_zone_green)),
                "rgb_zone_blue": (checker.check_rgb_zone_blue, HexList(rgb_zone_blue)),
                "rgb_zone_id_0": (checker.check_rgb_zone_id_0, HexList(rgb_zone_id_0)),
            })
            checker.check_fields(self, response, self.feature_8081.set_rgb_zones_single_value_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check all RGB LEDs are restored to their default value")
        # --------------------------------------------------------------------------------------------------------------
        # TODO: Check all RGB LEDs are restored to their default value
        warnings.warn("TODO: Check all RGB LEDs are restored to their default value using I2C/led spy")

        self.testCaseChecked("FUN_1805_0038", _AUTHOR)
    # end def test_per_key_lighting_on_8081_reset

    @features("Feature1805")
    @features("Feature8110")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_mouse_button_spy_on_8110_reset(self):
        """
        Validate the 'remappingData' linked to the 0x8110 feature restored to its default value

        Require 0x8110 feature
        """
        raise NotImplementedError("Feature 0x8110 was not available during 0x1805 test scripts implementation")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8110 index")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Buttons are mapped to default configuration (1 to 1)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetRemapping with ButtonX= ButtonX+1 and so on")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getRemapping")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check remappingData matches ButtonX+1 mapping.")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setOOBState")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair the device with a new host")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getRemapping")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate the remap is same as default value.")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1805_0039", _AUTHOR)
    # end def test_mouse_button_spy_on_8110_reset
# end class OobStateFunctionalityTestCase


class OobStateEQuadFunctionalityTestCase(OobStateTestCase):
    """
    Validate ``OobStateEquadFunctionality`` Equad Specific funationality test case
    """

    @features("Feature1805")
    @features("Unifying")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_equad_pairing_data_erased(self):
        """
        Validate all pairing data are erased or loaded with default values, for EQuad protocol

        Perform pairing, then set OOB State and check pairing data in NVS are erased
        """
        self.post_requisite_reload_nvs = True
        self.post_requisite_clean_pairing_data = True

        self.unit_id = DeviceInformationTestUtils.HIDppHelper.get_device_info(test_case=self).unit_id
        nvs_list = ['NVS_CONNECT_ID', 'NVS_BTLDR_CONNECT_ID']

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair DUT with host")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self, pre_pairing=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _SEND_OOB)
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.HIDppHelper.set_oob_state_and_power_cycle(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check pairing data in NVS are erased/reset")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        for nvs_chunk in nvs_list:
            chunk_data = self.memory_manager.get_chunks_by_name(chunk_name=nvs_chunk, active_bank_only=True)
            if nvs_chunk == 'NVS_CONNECT_ID':
                if self.f.PRODUCT.DEVICE.F_NbHosts == 3:
                    self.assertEqual(obtained=chunk_data[-1].data.alt_mode_1,
                                     expected=HexList(0x00),
                                     msg=f'{nvs_chunk}.data.alt_mode_1 should be 0 in NVS')

                    self.assertEqual(obtained=chunk_data[-1].data.conn_flags_1,
                                     expected=HexList(0x00),
                                     msg=f'{nvs_chunk}.data.conn_flags_1 should be 0 in NVS')

                    self.assertEqual(obtained=chunk_data[-1].data.alt_mode_2,
                                     expected=HexList(ConnectIdChunkData.PairingSrc.NONE),
                                     msg=f'{nvs_chunk}.data.alt_mode_2 should be 0 in NVS')

                    self.assertEqual(obtained=chunk_data[-1].data.conn_flags_2,
                                     expected=HexList(0x00),
                                     msg=f'{nvs_chunk}.data.conn_flags_2 should be 0 in NVS')
                # end if

                self.assertEqual(obtained=chunk_data[-1].data.alt_mode_0,
                                 expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.data.alt_mode_0 should be 0 in NVS')

                self.assertEqual(obtained=chunk_data[-1].data.conn_flags_0,
                                 expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.data.conn_flags_0 should be 0 in NVS')

                self.assertEqual(obtained=chunk_data[-1].data.host_index, expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.host_index should be 0 in NVS')

                self.assertEqual(obtained=chunk_data[-1].data.bcast_pending, expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.bcast_pending should be 0 in NVS')

            elif nvs_chunk == 'NVS_BTLDR_CONNECT_ID':
                self.assertEqual(obtained=chunk_data[-1].host_idx, expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.host_idx should be 0 in NVS')

                # gaming devices will switch to usb channel in btldr after OOB
                expected = HexList(ConnectIdChunkData.Protocol.USB)
                self.assertEqual(obtained=chunk_data[-1].protocol, expected=expected,
                                 msg=f'{nvs_chunk}.protocol should be {expected} in NVS')

            elif chunk_data is not None:
                self.assertEqual(obtained=len(chunk_data),
                                 expected=0,
                                 msg=f'{nvs_chunk} should be empty in NVS')
            # end if
        # end for

        self.testCaseChecked("FUN_1805_0002", _AUTHOR)
    # end def test_equad_pairing_data_erased

    @features("Feature1805")
    @features("Keyboard")
    @features("Unifying")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    @services("RequiredKeys", (KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_B))
    def test_keyboard_sequence_for_oob_state(self):
        """
        Validate keyboard sequence Esc+O+Esc+O+Esc+B to enter OOB State and check connection is lost and NVS chunks
            erased/reset for Unifying Protocol
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press Esc+O+Esc+O+Esc+B")
        # --------------------------------------------------------------------------------------------------------------
        for key in [KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O,
                    KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_B]:
            self.button_stimuli_emulator.keystroke(key_id=key)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _POWER_CYCLE)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DUT is in OOB State (i.e. connection lost and NVS chunks erased/reset)")
        # --------------------------------------------------------------------------------------------------------------
        nvs_list = ['NVS_CONNECT_ID', 'NVS_BTLDR_CONNECT_ID']

        self.memory_manager.read_nvs()
        for nvs_chunk in nvs_list:
            chunk_data = self.memory_manager.get_chunks_by_name(chunk_name=nvs_chunk, active_bank_only=True)
            if nvs_chunk == 'NVS_CONNECT_ID':
                if self.f.PRODUCT.DEVICE.F_NbHosts == 3:
                    self.assertEqual(obtained=chunk_data[-1].data.alt_mode_1,
                                     expected=HexList(0x00),
                                     msg=f'{nvs_chunk}.data.alt_mode_1 should be 0 in NVS')

                    self.assertEqual(obtained=chunk_data[-1].data.conn_flags_1,
                                     expected=HexList(0x00),
                                     msg=f'{nvs_chunk}.data.conn_flags_1 should be 0 in NVS')

                    self.assertEqual(obtained=chunk_data[-1].data.alt_mode_2,
                                     expected=HexList(ConnectIdChunkData.PairingSrc.NONE),
                                     msg=f'{nvs_chunk}.data.alt_mode_2 should be 0 in NVS')

                    self.assertEqual(obtained=chunk_data[-1].data.conn_flags_2,
                                     expected=HexList(0x00),
                                     msg=f'{nvs_chunk}.data.conn_flags_2 should be 0 in NVS')
                # end if

                self.assertEqual(obtained=chunk_data[-1].data.alt_mode_0,
                                 expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.data.alt_mode_0 should be 0 in NVS')

                self.assertEqual(obtained=chunk_data[-1].data.conn_flags_0,
                                 expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.data.conn_flags_0 should be 0 in NVS')

                self.assertEqual(obtained=chunk_data[-1].data.host_index, expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.host_index should be 0 in NVS')

                self.assertEqual(obtained=chunk_data[-1].data.bcast_pending, expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.bcast_pending should be 0 in NVS')

            elif nvs_chunk == 'NVS_BTLDR_CONNECT_ID':
                self.assertEqual(obtained=chunk_data[-1].host_idx, expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.host_idx should be 0 in NVS')

                # gaming devices will switch to unifying channel in btldr after OOB and pre-paired to a receiver
                expected = HexList(ConnectIdChunkData.Protocol.UNIFYING)
                self.assertEqual(obtained=chunk_data[-1].protocol, expected=expected,
                                 msg=f'{nvs_chunk}.protocol should be {expected} in NVS')

            elif chunk_data is not None:
                self.assertEqual(obtained=len(chunk_data),
                                 expected=0,
                                 msg=f'{nvs_chunk} should be empty in NVS')
            # end if
        # end for

        self.testCaseChecked("FUN_1805_0011", _AUTHOR)
    # end def test_keyboard_sequence_for_oob_state
# end class OobStateEQuadFunctionalityTestCase


class OobStateUSBFunctionalityTestCase(OobStateTestCase):
    """
    Validate ``OobStateEquadFunctionality`` USB Specific funationality test case
    """

    @features("Feature1805")
    @features("Unifying")
    @features("USB")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    def test_usb_pairing_data_erased(self):
        """
        Validate all pairing data are erased or loaded with default values, for USB protocol

        Perform pairing, then set OOB State and check pairing data in NVS are erased
        """

        self.post_requisite_reload_nvs = True
        self.post_requisite_unplug_usb_cable = True

        nvs_list = ['NVS_CONNECT_ID', 'NVS_BTLDR_CONNECT_ID']

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pair DUT without pre-pairing")
        # --------------------------------------------------------------------------------------------------------------
        OobStateTestUtils.pair_device(self, pre_pairing=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to USB Channel")
        # --------------------------------------------------------------------------------------------------------------
        ProtocolManagerUtils.switch_to_usb_channel(self)

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
        LogHelper.log_step(self, "Turn off USB charging cable")
        # --------------------------------------------------------------------------------------------------------------
        self.device.turn_off_usb_charging_cable()
        ChannelUtils.close_channel(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _POWER_CYCLE)
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check pairing data in NVS are erased/reset")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        for nvs_chunk in nvs_list:
            chunk_data = self.memory_manager.get_chunks_by_name(chunk_name=nvs_chunk, active_bank_only=True)
            if nvs_chunk == 'NVS_CONNECT_ID':
                self.assertEqual(obtained=chunk_data[-1].data.alt_mode_0,
                                 expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.data.alt_mode_0 should be 0 in NVS')

                self.assertEqual(obtained=chunk_data[-1].data.conn_flags_0,
                                 expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.data.conn_flags_0 should be 0 in NVS')

                self.assertEqual(obtained=chunk_data[-1].data.host_index, expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.host_index should be 0 in NVS')

                self.assertEqual(obtained=chunk_data[-1].data.bcast_pending, expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.bcast_pending should be 0 in NVS')

            elif nvs_chunk == 'NVS_BTLDR_CONNECT_ID':
                self.assertEqual(obtained=chunk_data[-1].host_idx, expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.host_index should be 0 in NVS')

                # gaming devices will switch to usb channel in btldr after OOB
                expected = HexList(ConnectIdChunkData.Protocol.USB)
                self.assertEqual(obtained=chunk_data[-1].protocol, expected=expected,
                                 msg=f'{nvs_chunk}.protocol should be {expected} in NVS')

            elif chunk_data is not None:
                self.assertEqual(obtained=len(chunk_data),
                                 expected=0,
                                 msg=f'{nvs_chunk} should be empty in NVS')
            # end if
        # end for
        self.testCaseChecked("FUN_1805_0002", _AUTHOR)
    # end def test_usb_pairing_data_erased

    @features("Feature1805")
    @features("Keyboard")
    @features("Unifying")
    @features("USB")
    @level("Functionality")
    @services("Debugger")
    @services("HardwareReset")
    @services("RequiredKeys", (KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_B))
    def test_keyboard_sequence_for_oob_state(self):
        """
        Validate keyboard sequence Esc+O+Esc+O+Esc+B to enter OOB State and check connection is lost and NVS chunks
            erased/reset for USB Protocol
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Switch to USB Channel")
        # --------------------------------------------------------------------------------------------------------------
        ProtocolManagerUtils.switch_to_usb_channel(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable hidden features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.enable_hidden_features(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Press Esc+O+Esc+O+Esc+B")
        # --------------------------------------------------------------------------------------------------------------
        for key in [KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O, KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_O,
                    KEY_ID.KEYBOARD_ESCAPE, KEY_ID.KEYBOARD_B]:
            self.button_stimuli_emulator.keystroke(key_id=key)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Turn off USB charging cable")
        # --------------------------------------------------------------------------------------------------------------
        ProtocolManagerUtils.exit_usb_channel(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, _POWER_CYCLE)
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DUT is in OOB State (i.e. connection lost and NVS chunks erased/reset)")
        # --------------------------------------------------------------------------------------------------------------
        nvs_list = ['NVS_CONNECT_ID', 'NVS_BTLDR_CONNECT_ID']

        self.memory_manager.read_nvs()
        for nvs_chunk in nvs_list:
            chunk_data = self.memory_manager.get_chunks_by_name(chunk_name=nvs_chunk, active_bank_only=True)
            if nvs_chunk == 'NVS_CONNECT_ID':
                self.assertEqual(obtained=chunk_data[-1].data.alt_mode_0,
                                 expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.data.alt_mode_0 should be 0 in NVS')

                self.assertEqual(obtained=chunk_data[-1].data.conn_flags_0,
                                 expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.data.conn_flags_0 should be 0 in NVS')

                self.assertEqual(obtained=chunk_data[-1].data.host_index, expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.host_index should be 0 in NVS')

                self.assertEqual(obtained=chunk_data[-1].data.bcast_pending, expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.bcast_pending should be 0 in NVS')

            elif nvs_chunk == 'NVS_BTLDR_CONNECT_ID':
                self.assertEqual(obtained=chunk_data[-1].host_idx, expected=HexList(0x00),
                                 msg=f'{nvs_chunk}.host_idx should be 0 in NVS')

                expected = HexList(ConnectIdChunkData.Protocol.UNIFYING)
                self.assertEqual(obtained=chunk_data[-1].protocol, expected=expected,
                                 msg=f'{nvs_chunk}.protocol should be {expected} in NVS')

            elif chunk_data is not None:
                self.assertEqual(obtained=len(chunk_data),
                                 expected=0,
                                 msg=f'{nvs_chunk} should be empty in NVS')
            # end if
        # end for

        self.testCaseChecked("FUN_1805_0011", _AUTHOR)
    # end def test_keyboard_sequence_for_oob_state
# end class OobStateUSBFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
