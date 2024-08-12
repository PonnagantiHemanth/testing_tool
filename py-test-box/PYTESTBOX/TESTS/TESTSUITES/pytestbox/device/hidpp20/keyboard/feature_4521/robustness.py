#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4521.robustness
:brief: HID++ 2.0 DisableKeys robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2021/12/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features, services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.disablekeys import DisableKeys
from pyhid.hidpp.features.keyboard.disablekeys import DisableKeysFactory
from pyhid.hidpp.features.keyboard.disablekeys import GetCapabilities
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values, compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablekeysutils import DisableKeysUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4521.disablekeys import DisableKeysBaseTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysRobustnessTestCase(DisableKeysBaseTestCase):
    """
    0x4521 DisableKeys robustness test case
    """
    @features('Feature4521')
    @level('Robustness')
    @services('KeyMatrix')
    def test_disabled_same_keys(self):
        """
        Validate same keys can be disabled twice and work with no error

        disabledKeys [2]SetDisabledKeys
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over i in the range 2')
        # ---------------------------------------------------------------------------
        for i in range(2):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send SetDisabledKeys with keysToDisable = {self.all_disableable_keys}')
            # ---------------------------------------------------------------------------
            set_disabled_keys_response = DisableKeysUtils.set_disabled_keys_by_key_id(test_case=self,
                                                                                      key_ids=self.all_disableable_keys)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(
                self, f'Validate SetDisabledKeys.disabledKeys value is equal to {self.all_disableable_keys}')
            # ---------------------------------------------------------------------------
            check_map = DisableKeysUtils.update_disabled_keys_for_check_map(test_case=self,
                                                                            keys_to_disable=self.all_disableable_keys)
            DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
                                                          test_case=self,
                                                          message=set_disabled_keys_response,
                                                          expected_cls=self.feature_4521.set_disabled_keys_response_cls,
                                                          check_map=check_map)
            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, f'Test Loop over key ids in {self.all_disableable_keys}')
            # ---------------------------------------------------------------------------
            for key_id_to_stroke in self.all_disableable_keys:
                # ---------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate keystroke on {key_id_to_stroke}')
                # ---------------------------------------------------------------------------
                KeyMatrixTestUtils.stroke_key_with_fn(test_case=self, key_id=key_id_to_stroke)

                # ---------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate host cannot receive keystroke reports from the DUT')
                # ---------------------------------------------------------------------------
                self.check_key_disabled(key_id=key_id_to_stroke)
            # end for
            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, 'End Test Loop')
            # ---------------------------------------------------------------------------
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked('ROB_4521_0001')
    # end def test_disabled_sam_keys

    @features('Feature4521')
    @level('Robustness')
    def test_get_capabilities_after_set_disabled_keys(self):
        """
        Validate disabled disableable keys will not change the capability of disableable keys

        disableableKeys [0]GetCapabilities
        disabledKeys    [2]SetDisabledKeys
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over key in {self.all_disableable_keys}')
        # ---------------------------------------------------------------------------
        for key in self.all_disableable_keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send SetDisabledKeys with keysToDisable = {key}')
            # ---------------------------------------------------------------------------
            set_disabled_keys_response = DisableKeysUtils.set_disabled_keys_by_key_id(test_case=self,
                                                                                      key_ids=[key])

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate SetDisabledKeys.disabledKeys value is equal to {key}')
            # ---------------------------------------------------------------------------
            check_map = DisableKeysUtils.update_disabled_keys_for_check_map(test_case=self,
                                                                            keys_to_disable=[key])
            DisableKeysUtils.DisabledKeysResponseChecker.check_fields(
                                                          test_case=self,
                                                          message=set_disabled_keys_response,
                                                          expected_cls=self.feature_4521.set_disabled_keys_response_cls,
                                                          check_map=check_map)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetCapabilities request')
            # ---------------------------------------------------------------------------
            get_capabilities_response = DisableKeysUtils.HIDppHelper.get_capabilities(test_case=self)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetCapabilities.disableableKeys value')
            # ---------------------------------------------------------------------------
            DisableKeysUtils.GetCapabilitiesResponseChecker.check_fields(
                                                           test_case=self,
                                                           message=get_capabilities_response,
                                                           expected_cls=self.feature_4521.get_capabilities_response_cls)
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked('ROB_4521_0002')
    # end def test_get_capabilities_after_set_disabled_keys

    @features('Feature4521')
    @level('Robustness')
    def test_ignore_software_id(self):
        """
        Inputs.softwareId input is ignored by the firmware
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, f'Test Loop over softwareId range (several interesting values)')
        # ----------------------------------------------------------------------------
        for software_id in compute_wrong_range(value=DisableKeys.DEFAULT.SOFTWARE_ID,
                                               max_value=0xF):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetCapabilities with softwareId = {software_id}')
            # ----------------------------------------------------------------------------
            response = self.get_capabilities_with_specific_software_id(software_id=software_id)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(
                            self, 'Validate GetCapabilities.disableableKeys value is equal to product default settings')
            # ----------------------------------------------------------------------------
            DisableKeysUtils.GetCapabilitiesResponseChecker.check_fields(
                                                        test_case=self,
                                                        message=response,
                                                        expected_cls=self.feature_4521.get_capabilities_response_cls)
        # end for
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, f'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked('ROB_4521_0003')
    # end test_ignore_software_id

    @features('Feature4521')
    @level('Robustness')
    def test_ignore_padding(self):
        """
        Padding bytes shall be ignored by the firmware

        disableableKeys [0]GetCapabilites
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over getCapabilities padding range (several interesting values)')
        # ---------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(GetCapabilities.DEFAULT.PADDING,
                                                               GetCapabilities.LEN.PADDING // 8))):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetCapabilities with several value for padding')
            # ---------------------------------------------------------------------------
            response = self.get_capabilities_with_specific_padding(padding_byte=HexList(padding_byte))

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetCapabilities.disableableKeys value')
            # ---------------------------------------------------------------------------
            DisableKeysUtils.GetCapabilitiesResponseChecker.check_fields(
                self, response, self.feature_4521.get_capabilities_response_cls)
        # end for
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked('ROB_4521_0004')
    # end test_ignore_padding

    def get_capabilities_with_specific_padding(self, padding_byte, device_index=None, port_index=None):
        """
        Get capabilities with several value for padding. This could be used for padding byte test.

        :param padding_byte: specific value for padding
        :type padding_byte: ``HexList``
        :param device_index: Device index - OPTIONAL
        :type device_index: ``int``
        :param port_index: Port index - OPTIONAL
        :type port_index: ``int``

        :return: The message retrieved from the queue
        :rtype: ``GetCapabilitiesResponse``
        """
        feature_4521_index, feature_4521, device_index, port_index = DisableKeysUtils.HIDppHelper.get_parameters(
            self, DisableKeys.FEATURE_ID, DisableKeysFactory, device_index, port_index)

        get_capabilities_request = feature_4521.get_capabilities_cls(device_index=device_index,
                                                                     feature_index=feature_4521_index)
        get_capabilities_request.padding = padding_byte

        return ChannelUtils.send(test_case=self,
                                 report=get_capabilities_request,
                                 response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                                 response_class_type=self.feature_4521.get_capabilities_response_cls)
    # end def get_capabilities_with_specific_padding

    def get_capabilities_with_specific_software_id(self, software_id, device_index=None, port_index=None):
        """
        Get capabilities with several value for software ID. This could be used for software id test.

        :param software_id: specific value for software id
        :type software_id: ``int``
        :param device_index: Device index - OPTIONAL
        :type device_index: ``int``
        :param port_index: Port index - OPTIONAL
        :type port_index: ``int``

        :return: The message retrieved from the queue
        :rtype: ``GetCapabilitiesResponse``
        """
        feature_4521_index, feature_4521, device_index, port_index = DisableKeysUtils.HIDppHelper.get_parameters(
            self, DisableKeys.FEATURE_ID, DisableKeysFactory, device_index, port_index)

        get_capabilities = feature_4521.get_capabilities_cls(device_index=device_index,
                                                             feature_index=feature_4521_index)

        get_capabilities.softwareId = software_id

        return ChannelUtils.send(test_case=self,
                                 report=get_capabilities,
                                 response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                                 response_class_type=self.feature_4521.get_capabilities_response_cls)
    # end def get_capabilities_with_specific_software_id
# end class DisableKeysRobustnessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
