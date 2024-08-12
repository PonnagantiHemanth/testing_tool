#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1815.functionality
:brief: HID++ 2.0 Hosts Info functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/03/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.changehost import ChangeHost
from pyhid.hidpp.features.common.hostsinfo import HostsInfo
from pyhid.hidpp.features.common.hostsinfo import SetHostFriendlyNameV1ToV2
from pyhid.hidpp.features.common.hostsinfo import SetHostOsVersionV1ToV2
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.hostsinfoutils import HostsInfoTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hidpp20.common.feature_1815.hostsinfo import HostsInfoTestCase
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class HostsInfoFunctionalityTestCase(HostsInfoTestCase):
    """
    Validate Hosts Info Functionality TestCases
    """

    @features('Feature1815')
    @features('BLEDevicePairing')
    @level('Functionality')
    def test_get_host_info_current_host(self):
        """
        Validate getHostInfo request when matching the current host (i.e. host index. 0xFF)
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getHostInfo request with host index = 0xFF')
        # ----------------------------------------------------------------------------
        get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_info(self, host_index=0xFF)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check getHostInfo response fields')
        # ----------------------------------------------------------------------------
        HostsInfoTestUtils.GetHostInfoResponseChecker.check_fields(
            self, get_host_info_resp, self.feature_1815.get_host_info_response_cls)

        self.testCaseChecked("FUN_1815_0020")
    # end def test_get_host_info_current_host

    @features('Feature1815')
    @features('BLEDevicePairing')
    @level('Functionality')
    def test_get_ble_descriptor(self):
        """
        Validate host descriptor pages returned by getHostDescriptor
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getHostDescriptor request for every host')
        # ----------------------------------------------------------------------------
        f = self.getFeatures()
        for index in range(f.PRODUCT.DEVICE.F_NbHosts):
            (ble_address, ble_descriptor) = HostsInfoTestUtils.get_ble_descriptor(self, index)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostDescriptor host descriptor page')
            # ----------------------------------------------------------------------------
            if ble_descriptor is not None:
                HostsInfoTestUtils.check_ble_descriptor(self, ble_descriptor, self.receiver_serial_numbers[index])
            # end if
        # end for

        self.testCaseChecked("FUN_1815_0021")
    # end def test_get_ble_descriptor

    @features('Feature1815')
    @features('BLEDevicePairing')
    @level('Functionality')
    def test_get_ble_descriptor_current_host(self):
        """
        Validate host descriptor pages returned by getHostDescriptor for the current host (i.e. host index. 0xFF)
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getHostDescriptor request with host index = 0xFF')
        # ----------------------------------------------------------------------------
        (ble_address, ble_descriptor) = HostsInfoTestUtils.get_ble_descriptor(self, 0xFF)
        if ble_descriptor is not None:
            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostDescriptor host descriptor page')
            # ----------------------------------------------------------------------------
            HostsInfoTestUtils.check_ble_descriptor(self, ble_descriptor, self.receiver_serial_numbers[0])
        # end if

        self.testCaseChecked("FUN_1815_0022")
    # end def test_get_ble_descriptor

    @features('Feature1815')
    @level('Functionality')
    def test_get_host_friendly_name(self):
        """
        Validate getHostFriendlyName response with byte index in range [0..name_len-1]
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getHostInfo request')
        # ----------------------------------------------------------------------------
        get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_info(self, host_index=0)

        host_friendly_name_check_map = HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.get_default_check_map(self)
        for index in range(int(Numeral(get_host_info_resp.name_len))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostFriendlyName request')
            # ----------------------------------------------------------------------------
            get_host_friendly_name_resp = HostsInfoTestUtils.HIDppHelper.get_host_friendly_name(
                self, host_index=0, byte_index=index)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostFriendlyName response fields')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            host_friendly_name_check_map["byte_index"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_byte_index, index)
            host_friendly_name_check_map["name_chunk"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_name_chunk,
                (HostsInfoTestUtils.NAME.BLE_FRIENDLY_NAME, index))
            HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_fields(
                self, get_host_friendly_name_resp, self.feature_1815.get_host_friendly_name_response_cls,
                check_map=host_friendly_name_check_map)
        # end for

        self.testCaseChecked("FUN_1815_0023")
    # end def test_get_host_friendly_name

    @features('Feature1815')
    @level('Functionality')
    def test_set_host_friendly_name(self):
        """
        Validate setHostFriendlyName usage to set name to 'Logitech Bolt receiver'
        """
        default_name = HostsInfoTestUtils.NAME.BLE_FRIENDLY_NAME
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setHostFriendlyName request to set the name by chunk')
        # ----------------------------------------------------------------------------
        set_host_friendly_name_resp_list = HostsInfoTestUtils.HIDppHelper.set_host_friendly_name(
            self, host_index=0, name=default_name)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check setHostFriendlyName responses fields')
        # ----------------------------------------------------------------------------
        response_index = 0
        for chunk_index in range(1 + len(default_name) * 8 // SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK):
            max_offset = min(len(default_name), (chunk_index + 1) * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)
            host_friendly_name_check_map = HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.get_default_check_map(
                self)
            # Fix name length expected value in check map
            host_friendly_name_check_map["name_len"] = (
                HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_name_len, max_offset)
            HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_fields(
                self, set_host_friendly_name_resp_list[response_index],
                self.feature_1815.set_host_friendly_name_response_cls, check_map=host_friendly_name_check_map)
            response_index += 1
        # end for

        self.testCaseChecked("FUN_1815_0024")
    # end def test_set_host_friendly_name

    @features('Feature1815')
    @level('Functionality')
    def test_set_host_friendly_name_incremented_to_max(self):
        """
        Validate setHostFriendlyName with name length incremented by 1 in the test loop
        """
        max_len_name = 'Very long name to test max length'
        self.post_requisite_reload_nvs = True

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getHostInfo request to retrieve the name_max_len value')
        # ----------------------------------------------------------------------------
        get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_info(self, host_index=0)

        for name_size in range(int(Numeral(get_host_info_resp.name_max_len))+1):
            new_name = max_len_name[:name_size]
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setHostFriendlyName request with byte_index from 0 to name_max_len')
            # ----------------------------------------------------------------------------
            set_host_friendly_name_resp_list = HostsInfoTestUtils.HIDppHelper.set_host_friendly_name(
                self, host_index=0, name=new_name)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check setHostFriendlyName response fields')
            # ----------------------------------------------------------------------------
            host_friendly_name_check_map = HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.get_default_check_map(
                self)
            # Fix name length expected value in check map
            host_friendly_name_check_map["name_len"] = (
                HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_name_len, len(new_name))
            HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_fields(
                self, set_host_friendly_name_resp_list[-1], self.feature_1815.set_host_friendly_name_response_cls,
                check_map=host_friendly_name_check_map)

        self.testCaseChecked("FUN_1815_0025")
    # end def test_set_host_friendly_name_incremented_to_max

    @features('Feature1815')
    @level('Functionality')
    def test_set_host_friendly_name_decremented_to_max(self):
        """
        Validate setHostFriendlyName with name length decremented by 1 in the test loop
        """
        max_len_name = 'Very long name to test max length'
        self.post_requisite_reload_nvs = True

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getHostInfo request to retrieve the name_max_len value')
        # ----------------------------------------------------------------------------
        get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_info(self, host_index=0)

        for name_size in reversed(range(int(Numeral(get_host_info_resp.name_max_len))+1)):
            new_name = max_len_name[:name_size]
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setHostFriendlyName request with byte_index from name_max_len to 0')
            # ----------------------------------------------------------------------------
            set_host_friendly_name_resp_list = HostsInfoTestUtils.HIDppHelper.set_host_friendly_name(
                self, host_index=0, name=new_name)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check setHostFriendlyName response fields')
            # ----------------------------------------------------------------------------
            host_friendly_name_check_map = HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.get_default_check_map(
                self)
            # Fix name length expected value in check map
            host_friendly_name_check_map["name_len"] = (
                HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_name_len, len(new_name))
            HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_fields(
                self, set_host_friendly_name_resp_list[-1], self.feature_1815.set_host_friendly_name_response_cls,
                check_map=host_friendly_name_check_map)

        self.testCaseChecked("FUN_1815_0026")
    # end def test_set_host_friendly_name_decremented_to_max

    @features('Feature1815')
    @level('Functionality')
    def test_set_get_host_os_type(self):
        """
        Validate SetHostOsVersion OS type parameter valid range [0..7]
        """
        self.post_requisite_reload_nvs = True

        get_host_os_version_check_map = HostsInfoTestUtils.GetHostOsVersionResponseChecker.get_default_check_map(self)
        for os_type in reversed(range(SetHostOsVersionV1ToV2.TYPE.RESERVED)):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetHostOsVersion request with os_type in range [0..7]')
            # ----------------------------------------------------------------------------
            set_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.set_host_os_version(
                self, host_index=0, os_type=os_type, os_version=0, os_revision=0, os_build=0)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check SetHostOsVersion response fields')
            # ----------------------------------------------------------------------------
            HostsInfoTestUtils.SetHostOsVersionResponseChecker.check_fields(
                self, set_host_os_version_resp, self.feature_1815.set_host_os_version_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetHostOsVersion request')
            # ----------------------------------------------------------------------------
            get_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.get_host_os_version(self, host_index=0)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check GetHostOsVersion OS type response field matches the input')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            get_host_os_version_check_map["os_type"] = (
                HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_os_type, os_type)
            HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_fields(
                self, get_host_os_version_resp, self.feature_1815.get_host_os_version_response_cls,
                check_map=get_host_os_version_check_map)
        # end for
        self.post_requisite_reload_nvs = False

        self.testCaseChecked("FUN_1815_0027")
    # end def test_set_get_host_os_type

    @features('Feature1815')
    @level('Functionality')
    def test_set_get_host_os_version(self):
        """
        Validate SetHostOsVersion version parameter valid range [0..0xFF]
        """
        self.post_requisite_reload_nvs = True

        get_host_os_version_check_map = HostsInfoTestUtils.GetHostOsVersionResponseChecker.get_default_check_map(self)
        for os_version in reversed(compute_sup_values(HexList(Numeral(0)), is_equal=True)):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetHostOsVersion request with os_version in range [0..0xFF]')
            # ----------------------------------------------------------------------------
            set_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.set_host_os_version(
                self, host_index=0, os_type=0, os_version=os_version, os_revision=0, os_build=0)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check SetHostOsVersion response fields')
            # ----------------------------------------------------------------------------
            HostsInfoTestUtils.SetHostOsVersionResponseChecker.check_fields(
                self, set_host_os_version_resp, self.feature_1815.set_host_os_version_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetHostOsVersion request')
            # ----------------------------------------------------------------------------
            get_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.get_host_os_version(self, host_index=0)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check GetHostOsVersion version response field matches the input')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            get_host_os_version_check_map["os_version"] = (
                HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_os_version, os_version)
            HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_fields(
                self, get_host_os_version_resp, self.feature_1815.get_host_os_version_response_cls,
                check_map=get_host_os_version_check_map)
        # end for
        self.post_requisite_reload_nvs = False

        self.testCaseChecked("FUN_1815_0028")
    # end def test_set_get_host_os_version

    @features('Feature1815')
    @level('Functionality')
    def test_set_get_host_os_revision(self):
        """
        Validate SetHostOsVersion revision parameter valid range [0..0xFFFF]
        """
        self.post_requisite_reload_nvs = True

        get_host_os_version_check_map = HostsInfoTestUtils.GetHostOsVersionResponseChecker.get_default_check_map(self)
        for os_revision in reversed(compute_sup_values(HexList(
                Numeral(0, self.feature_1815.set_host_os_version_cls.LEN.OS_REVISION // 8)), is_equal=True)):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetHostOsVersion request with os_revision in range [0..0xFFFF]')
            # ----------------------------------------------------------------------------
            set_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.set_host_os_version(
                self, host_index=0, os_type=0, os_version=0, os_revision=os_revision, os_build=0)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check SetHostOsVersion response fields')
            # ----------------------------------------------------------------------------
            HostsInfoTestUtils.SetHostOsVersionResponseChecker.check_fields(
                self, set_host_os_version_resp, self.feature_1815.set_host_os_version_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetHostOsVersion request')
            # ----------------------------------------------------------------------------
            get_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.get_host_os_version(self, host_index=0)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check GetHostOsVersion revision response field matches the input')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            get_host_os_version_check_map["os_revision"] = (
                HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_os_revision, os_revision)
            HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_fields(
                self, get_host_os_version_resp, self.feature_1815.get_host_os_version_response_cls,
                check_map=get_host_os_version_check_map)
        # end for
        self.post_requisite_reload_nvs = False

        self.testCaseChecked("FUN_1815_0029")
    # end def test_set_get_host_os_revision

    @features('Feature1815')
    @level('Functionality')
    def test_set_get_host_os_build(self):
        """
        Validate SetHostOsVersion build parameter valid range [0..0xFFFF]
        """
        get_host_os_version_check_map = HostsInfoTestUtils.GetHostOsVersionResponseChecker.get_default_check_map(self)
        for os_build in reversed(compute_sup_values(HexList(
                Numeral(0, self.feature_1815.set_host_os_version_cls.LEN.OS_BUILD // 8)), is_equal=True)):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send SetHostOsVersion request with os_build in range [0..0xFFFF]')
            # ----------------------------------------------------------------------------
            set_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.set_host_os_version(
                self, host_index=0, os_type=0, os_version=0, os_revision=0, os_build=os_build)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check SetHostOsVersion response fields')
            # ----------------------------------------------------------------------------
            HostsInfoTestUtils.SetHostOsVersionResponseChecker.check_fields(
                self, set_host_os_version_resp, self.feature_1815.set_host_os_version_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetHostOsVersion request')
            # ----------------------------------------------------------------------------
            get_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.get_host_os_version(self, host_index=0)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check GetHostOsVersion OS build response field matches the input')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            get_host_os_version_check_map["os_build"] = (
                HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_os_build, os_build)
            HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_fields(
                self, get_host_os_version_resp, self.feature_1815.get_host_os_version_response_cls,
                check_map=get_host_os_version_check_map)
        # end for

        self.testCaseChecked("FUN_1815_0030")
    # end def test_set_get_host_os_build

    @features('Feature1815')
    @level('Functionality')
    @services('HardwareReset')
    @bugtracker('Device_HostName_ResetAtReconnection')
    def test_set_host_friendly_name_reset(self):
        """
        Validate the new friendly name is kept after a reset

        Related to Jira ticket: https://jira.logitech.io/browse/NRF52-261
        Fixed in Quark platform code in patchset #7899
        https://goldenpass.logitech.com:8443/c/ccp_fw/quark/+/7899
        """
        new_name = 'friendly name reset'
        self.post_requisite_reload_nvs = True

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setHostFriendlyName request to set the name by chunk')
        # ----------------------------------------------------------------------------
        set_host_friendly_name_resp_list = HostsInfoTestUtils.HIDppHelper.set_host_friendly_name(
            self, host_index=0, name=new_name)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check setHostFriendlyName responses fields')
        # ----------------------------------------------------------------------------
        response_index = 0
        for chunk_index in range(1 + len(new_name) * 8 // SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK):
            max_offset = min(len(new_name), (chunk_index + 1) * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)
            host_friendly_name_check_map = HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.get_default_check_map(
                self)
            # Fix name length expected value in check map
            host_friendly_name_check_map["name_len"] = (
                HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_name_len, max_offset)
            HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_fields(
                self, set_host_friendly_name_resp_list[response_index],
                self.feature_1815.set_host_friendly_name_response_cls, check_map=host_friendly_name_check_map)
            response_index += 1
        # end for

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on DUT')
        # ---------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        host_friendly_name_check_map = HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.get_default_check_map(self)
        for index in range(len(set_host_friendly_name_resp_list)):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getHostFriendlyName request immediately with index = {index}')
            # ----------------------------------------------------------------------------
            get_host_friendly_name_resp = HostsInfoTestUtils.HIDppHelper.get_host_friendly_name(
                self, host_index=0, byte_index=index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostFriendlyName response fields')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            host_friendly_name_check_map["byte_index"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_byte_index,
                index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)
            host_friendly_name_check_map["name_chunk"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_name_chunk,
                (new_name, index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8))
            HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_fields(
                self, get_host_friendly_name_resp, self.feature_1815.get_host_friendly_name_response_cls,
                check_map=host_friendly_name_check_map)
        # end for

        # Wait a few hundred milliseconds
        sleep(.3)

        for index in range(len(set_host_friendly_name_resp_list)):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostFriendlyName request after a delay')
            # ----------------------------------------------------------------------------
            get_host_friendly_name_resp = HostsInfoTestUtils.HIDppHelper.get_host_friendly_name(
                self, host_index=0, byte_index=index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostFriendlyName response fields')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            host_friendly_name_check_map["byte_index"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_byte_index,
                index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)
            host_friendly_name_check_map["name_chunk"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_name_chunk,
                (new_name, index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8))
            HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_fields(
                self, get_host_friendly_name_resp, self.feature_1815.get_host_friendly_name_response_cls,
                check_map=host_friendly_name_check_map)
        # end for

        self.testCaseChecked("FUN_1815_0031")
    # end def test_set_host_friendly_name_reset

    @features('Feature1815')
    @level('Functionality')
    def test_set_host_os_parameters_reset(self):
        """
        Validate OS parameters are kept after a reset
        """
        self.post_requisite_reload_nvs = True

        get_host_os_version_check_map = HostsInfoTestUtils.GetHostOsVersionResponseChecker.get_default_check_map(self)
        os_type = SetHostOsVersionV1ToV2.TYPE.ANDROID
        os_version = 0xFF
        os_revision = HexList('01FF')
        os_build = HexList('02FF')
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send SetHostOsVersion request with os_type = {os_type}, os_version = {os_version},'
                                 f' os_revision = {os_revision} and os_build = {os_build}')
        # ----------------------------------------------------------------------------
        set_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.set_host_os_version(
            self, host_index=0, os_type=os_type, os_version=os_version, os_revision=os_revision, os_build=os_build)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check SetHostOsVersion response fields')
        # ----------------------------------------------------------------------------
        HostsInfoTestUtils.SetHostOsVersionResponseChecker.check_fields(
            self, set_host_os_version_resp, self.feature_1815.set_host_os_version_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Power off / on DUT')
        # ---------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        sleep(.1)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetHostOsVersion request')
        # ----------------------------------------------------------------------------
        get_host_os_version_resp = HostsInfoTestUtils.HIDppHelper.get_host_os_version(self, host_index=0)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check GetHostOsVersion OS type response fields match the provided values')
        # ----------------------------------------------------------------------------
        # Fix host index expected value in check map
        get_host_os_version_check_map["os_type"] = (
            HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_os_type, os_type)
        get_host_os_version_check_map["os_version"] = (
            HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_os_version, os_version)
        get_host_os_version_check_map["os_revision"] = (
            HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_os_revision, os_revision)
        get_host_os_version_check_map["os_build"] = (
            HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_os_build, os_build)
        HostsInfoTestUtils.GetHostOsVersionResponseChecker.check_fields(
            self, get_host_os_version_resp, self.feature_1815.get_host_os_version_response_cls,
            check_map=get_host_os_version_check_map)
        # end for

        self.testCaseChecked("FUN_1815_0032")
    # end def test_set_host_os_parameters_reset

    @features('Feature1815')
    @features('Feature1830')
    @level('Functionality')
    @bugtracker('Device_HostName_ResetAtReconnection')
    def test_set_host_friendly_name_deep_sleep(self):
        """
        Validate the new friendly name is kept after waking up from deep sleep

        Related to Jira ticket: https://jira.logitech.io/browse/NRF52-261
        Fixed in Quark platform code in patchset #7899
        https://goldenpass.logitech.com:8443/c/ccp_fw/quark/+/7899
        """
        new_name = 'friendly name deep_sleep'
        self.post_requisite_reload_nvs = True

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setHostFriendlyName request to set the name by chunk')
        # ----------------------------------------------------------------------------
        set_host_friendly_name_resp_list = HostsInfoTestUtils.HIDppHelper.set_host_friendly_name(
            self, host_index=0, name=new_name)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check setHostFriendlyName responses fields')
        # ----------------------------------------------------------------------------
        response_index = 0
        for chunk_index in range(1 + len(new_name) * 8 // SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK):
            max_offset = min(len(new_name), (chunk_index + 1) * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)
            host_friendly_name_check_map = HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.get_default_check_map(
                self)
            # Fix name length expected value in check map
            host_friendly_name_check_map["name_len"] = (
                HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_name_len, max_offset)
            HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_fields(
                self, set_host_friendly_name_resp_list[response_index],
                self.feature_1815.set_host_friendly_name_response_cls, check_map=host_friendly_name_check_map)
            response_index += 1
        # end for

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetPowerMode with powerModeNumber = 3')
        # ---------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wake up DUT by button clicking')
        # ---------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()
        sleep(0.3)

        host_friendly_name_check_map = HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.get_default_check_map(self)
        for index in range(len(set_host_friendly_name_resp_list)):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostFriendlyName request after the device wake-up')
            # ----------------------------------------------------------------------------
            get_host_friendly_name_resp = HostsInfoTestUtils.HIDppHelper.get_host_friendly_name(
                self, host_index=0, byte_index=index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostFriendlyName response fields')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            host_friendly_name_check_map["byte_index"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_byte_index,
                index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)
            host_friendly_name_check_map["name_chunk"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_name_chunk,
                (new_name, index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8))
            HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_fields(
                self, get_host_friendly_name_resp, self.feature_1815.get_host_friendly_name_response_cls,
                check_map=host_friendly_name_check_map)
        # end for

        self.testCaseChecked("FUN_1815_0033")
    # end def test_set_host_friendly_name_deep_sleep

    @features('Feature1815')
    @features('Feature1814')
    @level('Functionality')
    @services('AtLeastOneKey', (KEY_ID.HOST_1, KEY_ID.CONNECT_BUTTON))
    @bugtracker('Device_HostName_ResetAtReconnection')
    def test_set_host_friendly_name_reconnection(self):
        """
        Validate the new friendly name is kept after a missed channel change and a reconnection

        Related to Jira ticket: https://jira.logitech.io/browse/NRF52-261
        Fixed in Quark platform code in patchset #7899
        https://goldenpass.logitech.com:8443/c/ccp_fw/quark/+/7899
        """
        new_name = 'host name reconnection'
        self.post_requisite_reload_nvs = True

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setHostFriendlyName request to set the name by chunk')
        # ----------------------------------------------------------------------------
        set_host_friendly_name_resp_list = HostsInfoTestUtils.HIDppHelper.set_host_friendly_name(
            self, host_index=0, name=new_name)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check setHostFriendlyName responses fields')
        # ----------------------------------------------------------------------------
        host_friendly_name_check_map = HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.get_default_check_map(self)
        response_index = 0
        for chunk_index in range(1 + len(new_name) * 8 // SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK):
            max_offset = min(len(new_name), (chunk_index + 1) * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)
            # Fix name length expected value in check map
            host_friendly_name_check_map["name_len"] = (
                HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_name_len, max_offset)
            HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_fields(
                self, set_host_friendly_name_resp_list[response_index],
                self.feature_1815.set_host_friendly_name_response_cls, check_map=host_friendly_name_check_map)
            response_index += 1
        # end for

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force a disconnection then reconnection using the easy switch button')
        # ----------------------------------------------------------------------------
        DevicePairingTestUtils.change_host_by_link_state(self, DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
        DevicePairingTestUtils.change_host_by_link_state(self, DeviceConnection.LinkStatus.LINK_ESTABLISHED)

        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)

        for index in range(len(set_host_friendly_name_resp_list)):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostFriendlyName request after the reconnection')
            # ----------------------------------------------------------------------------
            get_host_friendly_name_resp = HostsInfoTestUtils.HIDppHelper.get_host_friendly_name(
                self, host_index=0, byte_index=index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostFriendlyName response fields')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            host_friendly_name_check_map["byte_index"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_byte_index,
                index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)
            host_friendly_name_check_map["name_chunk"] = (
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_name_chunk,
                (new_name, index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8))
            HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_fields(
                self, get_host_friendly_name_resp, self.feature_1815.get_host_friendly_name_response_cls,
                check_map=host_friendly_name_check_map)
        # end for

        self.testCaseChecked("FUN_1815_0034")
    # end def test_set_host_friendly_name_reconnection
# end class HostsInfoFunctionalityTestCase


class HostsInfoFunctionalityMultiReceiverTestCase(HostsInfoTestCase):
    """
    Validate Hosts Info with Multi Receivers TestCases
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.post_requisite_switch_back_receiver = False

        super().setUp()

        if self.f.SHARED.PAIRING.F_BLEDevicePairing:
            self.post_requisite_reload_nvs = True
            # Cleanup all pairing slots except the first one
            CommonBaseTestUtils.NvsHelper.clean_pairing_data(self)

            # ---------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Pair device to [nbHost] dongles')
            # ---------------------------------------------------------------------------
            # Initialize the authentication method parameter
            DevicePairingTestUtils.set_authentication_method(self, self.config_manager)

            ble_pro_receiver_port_indexes = ReceiverTestUtils.get_receiver_port_indexes(
                self,
                ReceiverTestUtils.USB_PID_MEZZY_BLE_PRO,
                skip=[ChannelUtils.get_port_index(test_case=self)])
            assert(len(ble_pro_receiver_port_indexes) > 0)

            self.post_requisite_switch_back_receiver = True
            device_slot = 1
            dispatcher_to_dump = self.current_channel.hid_dispatcher
            for index in ble_pro_receiver_port_indexes:
                if device_slot >= self.f.PRODUCT.DEVICE.F_NbHosts:
                    break
                else:
                    DevicePairingTestUtils.pair_device_slot_to_other_receiver(
                        test_case=self,
                        device_slot=device_slot,
                        other_receiver_port_index=index,
                        hid_dispatcher_to_dump=dispatcher_to_dump)
                    device_slot += 1
                    # Note that if we do not close the channel here, we got 3 receiver * 4 interfaces opened at the
                    # same time and we do not receive the HID event when emulating a user action
                    # FIXME : To be removed when the HID device layer is available
                    self.current_channel.close()
                # end if
            # end for

            # Reconnect with the first receiver
            ReceiverTestUtils.switch_to_receiver(
                self, receiver_port_index=ChannelUtils.get_port_index(test_case=self, channel=self.backup_dut_channel))

            # Change host on Device
            DevicePairingTestUtils.change_host_by_link_state(
                self, link_state=DeviceConnection.LinkStatus.LINK_ESTABLISHED)

            DeviceManagerUtils.set_channel(test_case=self, new_channel=self.backup_dut_channel)
        # end if
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # noinspection PyBroadException
        try:
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
            if self.post_requisite_switch_back_receiver:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(
                    self, "Switch communication channel to receiver on port 0")
                # ------------------------------------------------------
                status = self.channel_switch(
                    device_uid=ChannelIdentifier(port_index=self.host_number_to_port_index(0), device_index=1))
                self.assertTrue(status, msg='The device do not connect on host 0')
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try

        super().tearDown()
    # end def tearDown

    @features('Feature1815')
    @features('BLEDevicePairing')
    @level('Functionality')
    @services('MultiHost')
    def test_get_ble_descriptors_multi_hosts(self):
        """
        Validate get_host_descriptor data when the device is paired with different receiver on each channel
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send get_host_descriptor request on all available host indexes')
        # ----------------------------------------------------------------------------
        for index in range(self.f.PRODUCT.DEVICE.F_NbHosts):
            (ble_address, ble_descriptor) = HostsInfoTestUtils.get_ble_descriptor(self, index)
            if ble_descriptor is not None:
                # ----------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check getHostDescriptor host descriptor page')
                # ----------------------------------------------------------------------------
                HostsInfoTestUtils.check_ble_descriptor(self, ble_descriptor, self.receiver_serial_numbers[index])
            # end if
        # end for
        self.testCaseChecked("FUN_1815_0035")
    # end def test_get_ble_descriptors_multi_hosts

    @features('Feature1815')
    @features('BLEDevicePairing')
    @features('Feature1814')
    @level('Functionality')
    @services('MultiHost')
    def test_get_host_info_current_host_multi_host(self):
        """
        Validate getHostInfo with host index = 0xFF on all possible host by using 0x1814 change host feature to
        switch from one host to another
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1814) index')
        # ---------------------------------------------------------------------------
        self.feature_1814_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=ChangeHost.FEATURE_ID)

        host_info_check_map = HostsInfoTestUtils.GetHostInfoResponseChecker.get_default_check_map(self)
        for host_index in reversed(range(self.f.PRODUCT.DEVICE.F_NbHosts)):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send ChangeHost SetCurrentHost with hostIndex={host_index}')
            # ---------------------------------------------------------------------------
            self.set_back_current_host = True
            ChangeHostTestUtils.HIDppHelper.set_current_host(self,
                                                             device_index=ChannelUtils.get_device_index(test_case=self),
                                                             host_index=host_index)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Switch communication channel to receiver on port {host_index}')
            # ---------------------------------------------------------------------------
            status = self.channel_switch(
                device_uid=ChannelIdentifier(port_index=self.host_number_to_port_index(host_index), device_index=1))
            self.assertTrue(status, msg=f'The device do not connect on host {host_index}')

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Verify an HID report can be received')
            # ---------------------------------------------------------------------------
            DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getHostInfo request with host index = 0xFF')
            # ----------------------------------------------------------------------------
            get_host_info_resp = HostsInfoTestUtils.HIDppHelper.get_host_info(self, host_index=0xFF)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check getHostInfo response fields')
            # ----------------------------------------------------------------------------
            # Fix host index expected value in check map
            host_info_check_map["host_index"] = (
                HostsInfoTestUtils.GetHostInfoResponseChecker.check_host_index, host_index)
            HostsInfoTestUtils.GetHostInfoResponseChecker.check_fields(
                self, get_host_info_resp, self.feature_1815.get_host_info_response_cls, check_map=host_info_check_map)
        # end for
        self.testCaseChecked("FUN_1815_0036")
    # end def test_get_host_info_current_host_multi_host

    @features('Feature1815')
    @features('Feature1814')
    @level('Functionality')
    @services('MultiHost')
    def test_set_host_friendly_name_multi_host(self):
        """
        Validate the new friendly name is kept after multiple successful channel changes
        """
        new_name = 'name on multi host'
        self.post_requisite_reload_nvs = True

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1814)')
        # ---------------------------------------------------------------------------
        self.feature_1814_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=ChangeHost.FEATURE_ID)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send setHostFriendlyName request to set the name by chunk for Host index 0')
        # ----------------------------------------------------------------------------
        set_host_friendly_name_resp_list = HostsInfoTestUtils.HIDppHelper.set_host_friendly_name(
            self, host_index=HostsInfo.HostIndex.HOST_0, name=new_name)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check setHostFriendlyName responses fields')
        # ----------------------------------------------------------------------------
        response_index = 0
        for chunk_index in range(1 + len(new_name) * 8 // SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK):
            max_offset = min(len(new_name), (chunk_index + 1) * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)
            host_friendly_name_check_map = HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.get_default_check_map(
                self)
            # Fix name length expected value in check map
            host_friendly_name_check_map["name_len"] = (
                HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_name_len, max_offset)
            HostsInfoTestUtils.SetHostFriendlyNameResponseChecker.check_fields(
                self, set_host_friendly_name_resp_list[response_index],
                self.feature_1815.set_host_friendly_name_response_cls, check_map=host_friendly_name_check_map)
            response_index += 1
        # end for

        for host_index in range(1, self.f.PRODUCT.DEVICE.F_NbHosts):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send ChangeHost.SetCurrentHost with hostIndex = {host_index}')
            # ---------------------------------------------------------------------------
            ChangeHostTestUtils.HIDppHelper.set_current_host(
                self, device_index=ChannelUtils.get_device_index(test_case=self), host_index=host_index)

            # Switch communication channel to receiver on port = host_index
            status = self.channel_switch(
                device_uid=ChannelIdentifier(port_index=self.host_number_to_port_index(host_index), device_index=1))
            self.assertTrue(status, msg='The device do not connect on host %d' % host_index)
            # Empty queue
            ChannelUtils.empty_queue(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send ChangeHost.GetHostInfo request')
            # ---------------------------------------------------------------------------
            get_host_info_response = HostsInfoTestUtils.HIDppHelper.get_host_info(self, host_index=0xFF)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetHostInfo current Host value')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=host_index,
                             obtained=to_int(get_host_info_response.host_index),
                             msg='The currHost parameter differs from the one expected')

            host_friendly_name_check_map = HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.\
                get_default_check_map(self)
            for index in range(len(set_host_friendly_name_resp_list)):
                # ----------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send getHostFriendlyName request on the initial Host index 0')
                # ----------------------------------------------------------------------------
                get_host_friendly_name_resp = HostsInfoTestUtils.HIDppHelper.get_host_friendly_name(
                    self, host_index=HostsInfo.HostIndex.HOST_0,
                    byte_index=index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)

                # ----------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check getHostFriendlyName response fields')
                # ----------------------------------------------------------------------------
                # Fix host index expected value in check map
                host_friendly_name_check_map["byte_index"] = (
                    HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_byte_index,
                    index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8)
                host_friendly_name_check_map["name_chunk"] = (
                    HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_name_chunk,
                    (new_name, index * SetHostFriendlyNameV1ToV2.LEN.NAME_CHUNK // 8))
                HostsInfoTestUtils.GetHostFriendlyNameResponseChecker.check_fields(
                    self, get_host_friendly_name_resp, self.feature_1815.get_host_friendly_name_response_cls,
                    check_map=host_friendly_name_check_map)
            # end for
        # end for
        self.testCaseChecked("FUN_1815_0037")
    # end def test_set_host_friendly_name_multi_host
# end class HostsInfoFunctionalityMultiReceiverTestCase
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
