#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.1'
:package: pytestbox.device.hidpp20.common.feature_0011.propertyaccess
:brief: Validate HID++ 2.0 ``PropertyAccess`` feature
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/06/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.propertyaccessutils import PropertyAccessTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class PropertyAccessTestCase(DeviceBaseTestCase):
    """
    Validate ``PropertyAccess`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Post requisite flags definition
        self.post_requisite_restart_in_main_application = False
        self.post_requisite_reset_receiver = False
        self.post_requisite_reload_nvs = False
        self.post_requisite_new_equad_connection = False

        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0011 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0011_index, self.feature_0011, _, _ = PropertyAccessTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1807 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1807_index, self.feature_1807, _, _ = ConfigurablePropertiesTestUtils.HIDppHelper.get_parameters(
            self)

        self.config = self.f.PRODUCT.FEATURES.COMMON.PROPERTY_ACCESS
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_post_requisite():
            if self.post_requisite_restart_in_main_application:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text="Restart in Main Application mode")
                # ------------------------------------------------------------------------------------------------------
                DfuTestUtils.force_target_on_application(test_case=self)
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_reset_receiver:
                ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
                ReceiverTestUtils.reset_receiver(self)
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_new_equad_connection:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Redo the equad pairing with the default values")
                # ------------------------------------------------------------------------------------------------------
                # noinspection PyUnresolvedReferences
                # unit_id should be read in test pre-requisite if this post-requisite is required
                EQuadDeviceConnectionUtils.new_device_connection_and_pre_pairing(
                    test_case=self, unit_ids=[self.unit_id], disconnect=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Get device name in pairing info')
                # ------------------------------------------------------------------------------------------------------
                device_name_req = GetEQuadDeviceNameRequest(
                    NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN +
                    ChannelUtils.get_device_index(self) - 1)
                device_name_resp = ChannelUtils.send(
                    test_case=self,
                    channel=self.current_channel.receiver_channel,
                    report=device_name_req,
                    response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                    response_class_type=GetEQuadDeviceNameResponse
                )
                equad_device_name = device_name_resp.name_string.toString()
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'New connection with device {equad_device_name}')
                # ------------------------------------------------------------------------------------------------------
            # end if
        # end with
        super().tearDown()
    # end def tearDown

    def _write_check_supported_property(self, property_id, test_data):
        """
        Perform steps to check a supported property:
            - Check property supported but not present
            - Write it with nvs pars
            - Check property supported and present
            - Select property, Read it and Check Property in HID++ read response and in NVS

        :param property_id: Property identifier
        :type property_id: ``PropertyAccess.PropertyId | int | HexList``
        :param test_data: Data to use for the test
        :type test_data: ``int | HexList``

        :return: Read response data
        :rtype: ``HexList``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get property {repr(property_id)} info")
        # --------------------------------------------------------------------------------------------------------------
        response = PropertyAccessTestUtils.HIDppHelper.get_property_info(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)} is supported but not present")
        # --------------------------------------------------------------------------------------------------------------
        checker = PropertyAccessTestUtils.FlagsMaskBitMapChecker
        flags = checker.get_default_check_map(self)
        flags.update({
            "present": (checker.check_present, False),
            "supported": (checker.check_supported, True)
        })
        checker = PropertyAccessTestUtils.GetPropertyInfoResponseChecker
        check_map = checker.get_check_map_by_property(test_case=self, property_id=property_id)
        check_map["flags"] = (checker.check_flags, flags)
        checker.check_fields(
            self, response, self.feature_0011.get_property_info_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(property_id)} with nvs parser")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        PropertyAccessTestUtils.NvsHelper.write_property_id(self, property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get property {repr(property_id)} info after writing")
        # --------------------------------------------------------------------------------------------------------------
        response = PropertyAccessTestUtils.HIDppHelper.get_property_info(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)} is supported and present after writing")
        # --------------------------------------------------------------------------------------------------------------
        checker = PropertyAccessTestUtils.FlagsMaskBitMapChecker
        flags = checker.get_default_check_map(self)
        flags.update({
            "present": (checker.check_present, True),
            "supported": (checker.check_supported, True)
        })
        checker = PropertyAccessTestUtils.GetPropertyInfoResponseChecker
        check_map = checker.get_check_map_by_property(self, property_id)
        check_map["flags"] = (checker.check_flags, flags)
        checker.check_fields(self, response, self.feature_0011.get_property_info_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)} data in HID++ read response and in NVS")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.check_property(self, property_id, test_data, hidpp_check=True, nvs_check=True)
    # end def _write_check_supported_property

    def _activate_features(self):
        """
        Activate features
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
    # end def _activate_features
# end class PropertyAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
