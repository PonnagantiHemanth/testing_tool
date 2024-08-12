#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1817.interface
:brief: HID++ 2.0 ``LightspeedPrepairing`` interface test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2022/06/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.lightspeedprepairing import GetPrepairingData
from pyhid.hidpp.features.common.lightspeedprepairing import LightspeedPrepairing
from pyhid.hidpp.features.common.lightspeedprepairing import PrepairingManagement
from pyhid.hidpp.features.common.lightspeedprepairing import SetLTK
from pyhid.hidpp.features.common.lightspeedprepairing import SetPrepairingData
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.lightspeedprepairingutils import LightspeedPrepairingTestUtils
from pytestbox.device.hidpp20.common.feature_1817.lightspeedprepairing import LightspeedPrepairingTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LightspeedPrepairingInterfaceTestCase(LightspeedPrepairingTestCase):
    """
    Validate ``LightspeedPrepairing`` interface test cases
    """

    @features("Feature1817")
    @level("Interface")
    def test_get_capabilities_interface(self):
        """
        Validate ``GetCapabilities`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1817.get_capabilities_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1817.get_capabilities_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LightspeedPrepairingTestUtils.GetCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        })
        checker.check_fields(self, response, self.feature_1817.get_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_1817_0001", _AUTHOR)
    # end def test_get_capabilities_interface

    @features("Feature1817")
    @level("Interface")
    def test_prepairing_management_interface(self):
        """
        Validate ``PrepairingManagement`` interface
        """
        ls2 = False
        crush = False
        ls = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send PrepairingManagement request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1817.prepairing_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            ls2=ls2,
            crush=crush,
            ls=ls,
            prepairing_management_control=PrepairingManagement.Control.START)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1817.prepairing_management_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check PrepairingManagementResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_1817.prepairing_management_response_cls, check_map)

        self.testCaseChecked("INT_1817_0002", _AUTHOR)
    # end def test_prepairing_management_interface

    @features("Feature1817")
    @level("Interface")
    def test_set_ltk_interface(self):
        """
        Validate ``SetLTK`` interface
        """
        self.post_requisite_reload_nvs = True
        ltk = RandHexList(SetLTK.LEN.LTK//8)

        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=False,
            crush=False,
            ls=True,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetLTK request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1817.set_ltk_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            ltk=ltk)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1817.set_ltk_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetLTKResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_1817.set_ltk_response_cls, check_map)

        self.testCaseChecked("INT_1817_0003", _AUTHOR)
    # end def test_set_ltk_interface

    @features("Feature1817")
    @level("Interface")
    def test_set_prepairing_data_interface(self):
        """
        Validate ``SetPrepairingData`` interface
        """
        self.post_requisite_reload_nvs = True
        datatype = HexList(SetPrepairingData.DataType.PAIRING_ADDRESS)

        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=False,
            crush=False,
            ls=True,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetPrepairingData request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1817.set_prepairing_data_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            data_type=datatype,
            pairing_address_base=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1817.set_prepairing_data_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetPrepairingDataResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        }
        checker.check_fields(self, response, self.feature_1817.set_prepairing_data_response_cls, check_map)

        self.testCaseChecked("INT_1817_0004", _AUTHOR)
    # end def test_set_prepairing_data_interface

    @features("Feature1817")
    @level("Interface")
    def test_get_prepairing_data_interface(self):
        """
        Validate ``GetPrepairingData`` interface
        """
        information_type = HexList(GetPrepairingData.InfoType.PAIRING)
        data_type = HexList(GetPrepairingData.DataType.PAIRING_ADDRESS)
        reserved = HexList("00"*(GetPrepairingData.LEN.RESERVED//8))

        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=False,
            crush=False,
            ls=True,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetPrepairingData request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1817.get_prepairing_data_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1817_index,
            information_type=information_type,
            data_type=data_type,
            reserved=reserved)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1817.get_prepairing_data_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetPrepairingDataResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = LightspeedPrepairingTestUtils.GetPrepairingDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "information_type": (checker.check_information_type, information_type),
            "data_type": (checker.check_data_type, data_type),
            "data": None,
        })
        checker.check_fields(self, response, self.feature_1817.get_prepairing_data_response_cls, check_map)

        self.testCaseChecked("INT_1817_0005", _AUTHOR)
    # end def test_get_prepairing_data_interface
# end class LightspeedPrepairingInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
