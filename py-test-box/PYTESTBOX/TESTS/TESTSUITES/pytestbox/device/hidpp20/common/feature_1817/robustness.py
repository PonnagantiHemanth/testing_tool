#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1817.robustness
:brief: HID++ 2.0 ``LightspeedPrepairing`` robustness test suite
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
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.lightspeedprepairingutils import LightspeedPrepairingTestUtils
from pytestbox.device.hidpp20.common.feature_1817.lightspeedprepairing import LightspeedPrepairingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_RESERVED = "Test loop over reserved range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LightspeedPrepairingRobustnessTestCase(LightspeedPrepairingTestCase):
    """
    Validate ``LightspeedPrepairing`` robustness test cases
    """

    @features("Feature1817")
    @level("Robustness")
    def test_get_capabilities_software_id(self):
        """
        Validate ``GetCapabilities`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LightspeedPrepairing.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1817.get_capabilities_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1817_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1817.get_capabilities_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LightspeedPrepairingTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            })
            checker.check_fields(self, response, self.feature_1817.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1817_0001", _AUTHOR)
    # end def test_get_capabilities_software_id

    @features("Feature1817")
    @level("Robustness")
    def test_prepairing_management_software_id(self):
        """
        Validate ``PrepairingManagement`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.LS2.Crush.LS.prepairing_management_control

        SwID boundary values [0..F]
        """
        slot = self._test_get_the_first_available_slot()
        prepairing_management_control = PrepairingManagement.Control.START
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LightspeedPrepairing.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send PrepairingManagement request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1817.prepairing_management_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1817_index,
                ls2=slot == PrepairingManagement.PairingSlot.LS2,
                crush=slot == PrepairingManagement.PairingSlot.CRUSH,
                ls=slot == PrepairingManagement.PairingSlot.LS,
                prepairing_management_control=prepairing_management_control)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1817.prepairing_management_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check PrepairingManagementResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1817.prepairing_management_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1817_0002", _AUTHOR)
    # end def test_prepairing_management_software_id

    @features("Feature1817")
    @level("Robustness")
    def test_set_ltk_software_id(self):
        """
        Validate ``SetLTK`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ltk

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True
        ltk = RandHexList(SetLTK.LEN.LTK//8)
        slot = self._test_get_the_first_available_slot()

        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LightspeedPrepairing.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetLTK request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1817.set_ltk_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1817_index,
                ltk=ltk)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1817.set_ltk_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetLTKResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1817.set_ltk_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1817_0003", _AUTHOR)
    # end def test_set_ltk_software_id

    @features("Feature1817")
    @level("Robustness")
    def test_set_prepairing_data_software_id(self):
        """
        Validate ``SetPrepairingData`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.dataType.data

        SwID boundary values [0..F]
        """
        self.post_requisite_reload_nvs = True
        slot = self._test_get_the_first_available_slot()

        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        datatype = SetPrepairingData.DataType.PAIRING_ADDRESS

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LightspeedPrepairing.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetPrepairingData request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1817.set_prepairing_data_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1817_index,
                data_type=datatype,
                pairing_address_base=RandHexList(
                    LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
                address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1817.set_prepairing_data_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetPrepairingDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1817.set_prepairing_data_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1817_0004", _AUTHOR)
    # end def test_set_prepairing_data_software_id

    @features("Feature1817")
    @level("Robustness")
    def test_get_prepairing_data_software_id(self):
        """
        Validate ``GetPrepairingData`` software id field is ignored by the firmware

        Request: 0x11.DeviceIndex.FeatureIndex.FunctionIndex|SwID.information_type.data_type.Reserved

        SwID boundary values [0..F]
        """
        slot = self._test_get_the_first_available_slot()
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=slot,
            base_address=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        )

        information_type = GetPrepairingData.InfoType.PRE_PAIRING
        data_type = GetPrepairingData.DataType.EQUAD_ATTRIBUTES
        reserved = HexList("00" * (GetPrepairingData.LEN.RESERVED // 8))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(LightspeedPrepairing.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPrepairingData request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
                test_case=self,
                ls2=slot == PrepairingManagement.PairingSlot.LS2,
                crush=slot == PrepairingManagement.PairingSlot.CRUSH,
                ls=slot == PrepairingManagement.PairingSlot.LS,
                prepairing_management_control=PrepairingManagement.Control.START
            )

            report = self.feature_1817.get_prepairing_data_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1817_index,
                information_type=information_type,
                data_type=data_type,
                reserved=reserved)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1817.get_prepairing_data_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPrepairingDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LightspeedPrepairingTestUtils.GetPrepairingDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "information_type": (checker.check_information_type, information_type),
                "data_type": (checker.check_data_type, data_type),
                "data": None,
            })
            checker.check_fields(self, response, self.feature_1817.get_prepairing_data_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1817_0005", _AUTHOR)
    # end def test_get_prepairing_data_software_id

    @features("Feature1817")
    @level("Robustness")
    def test_get_capabilities_padding(self):
        """
        Validate ``GetCapabilities`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1817.get_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1817_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1817.get_capabilities_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LightspeedPrepairingTestUtils.GetCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "deviceIndex": (checker.check_device_index, report.deviceIndex),
                "featureIndex": (checker.check_feature_index, report.featureIndex),
            })
            checker.check_fields(self, response, self.feature_1817.get_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1817_0006", _AUTHOR)
    # end def test_get_capabilities_padding

    @features("Feature1817")
    @level("Robustness")
    def test_prepairing_management_reserved_slot_bits(self):
        """
        Validate ``PrepairingManagement`` reserved slot bits shall get errors from the firmware
        for the values other than 0
        """
        ls2 = True
        crush = False
        ls = False
        prepairing_management_control = PrepairingManagement.Control.START
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1817.prepairing_management_cls
        for wrong_reserved in compute_wrong_range(0, max_value=(1 << request_cls.LEN.RESERVED_SLOT) - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send PrepairingManagement request with reserved: {wrong_reserved}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1817_index,
                ls2=ls2,
                crush=crush,
                ls=ls,
                prepairing_management_control=prepairing_management_control)
            report.reserved_slot = wrong_reserved

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check PrepairingManagementResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            LightspeedPrepairingTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.NOT_ALLOWED])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1817_0007", _AUTHOR)
    # end def test_prepairing_management_reserved_slot_bits

    @features("Feature1817")
    @level("Robustness")
    def test_prepairing_management_padding(self):
        """
        Validate ``PrepairingManagement`` padding bytes are ignored by the firmware
        """
        slot = self._test_get_the_first_available_slot()
        prepairing_management_control = PrepairingManagement.Control.START
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1817.prepairing_management_cls
        for wrong_reserved in compute_wrong_range(0, max_value=(1 << request_cls.LEN.PADDING) - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send PrepairingManagement request with reserved: {wrong_reserved}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1817_index,
                ls2=slot == PrepairingManagement.PairingSlot.LS2,
                crush=slot == PrepairingManagement.PairingSlot.CRUSH,
                ls=slot == PrepairingManagement.PairingSlot.LS,
                prepairing_management_control=prepairing_management_control)
            report.reserved2 = wrong_reserved
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1817.prepairing_management_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check PrepairingManagementResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1817.prepairing_management_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1817_0008", _AUTHOR)
    # end def test_prepairing_management_padding

    @features("Feature1817")
    @level("Robustness")
    def test_set_prepairing_data_reserved(self):
        """
        Validate ``SetPrepairingData`` reserved bytes are ignored by the firmware
        """
        self.post_requisite_reload_nvs = True
        slot = self._test_get_the_first_available_slot()

        LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
            test_case=self,
            ls2=slot == PrepairingManagement.PairingSlot.LS2,
            crush=slot == PrepairingManagement.PairingSlot.CRUSH,
            ls=slot == PrepairingManagement.PairingSlot.LS,
            prepairing_management_control=PrepairingManagement.Control.START
        )

        datatype = SetPrepairingData.DataType.PAIRING_ADDRESS

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1817.set_prepairing_data_cls
        for wrong_reserved in compute_wrong_range(0, max_value=(1 << request_cls.LEN.RESERVED) - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetPrepairingData request with reserved: {wrong_reserved}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1817_index,
                data_type=datatype,
                pairing_address_base=RandHexList(
                    LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
                address_dest=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST)
            report.reserved = wrong_reserved
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1817.set_prepairing_data_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetPrepairingDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1817.set_prepairing_data_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1817_0009", _AUTHOR)
    # end def test_set_prepairing_data_reserved

    @features("Feature1817")
    @level("Robustness")
    def test_get_prepairing_data_reserved(self):
        """
        Validate ``GetPrepairingData`` reserved bytes are ignored by the firmware
        """
        slot = self._test_get_the_first_available_slot()
        LightspeedPrepairingTestUtils.pre_pairing_sequence(
            test_case=self,
            slot_index=slot,
            base_address=RandHexList(LightspeedPrepairing.DataDetailsPairingAddress.LEN.PAIRING_ADDRESS_BASE//8),
            last_dest_id=LightspeedPrepairing.DataDetailsPairingAddress.DEFAULT.ADDRESS_DEST,
            equad_attributes=RandHexList(LightspeedPrepairing.DataDetailsEquadAttributes.LEN.EQUAD_ATTRIBUTES//8)
        )

        information_type = GetPrepairingData.InfoType.PRE_PAIRING
        data_type = GetPrepairingData.DataType.EQUAD_ATTRIBUTES
        reserved = HexList("00" * (GetPrepairingData.LEN.RESERVED // 8))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1817.get_prepairing_data_cls
        for wrong_reserved in compute_wrong_range(0, max_value=(1 << request_cls.LEN.RESERVED) - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPrepairingData request with reserved: {wrong_reserved}")
            # ----------------------------------------------------------------------------------------------------------
            LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
                test_case=self,
                ls2=slot == PrepairingManagement.PairingSlot.LS2,
                crush=slot == PrepairingManagement.PairingSlot.CRUSH,
                ls=slot == PrepairingManagement.PairingSlot.LS,
                prepairing_management_control=PrepairingManagement.Control.START
            )

            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1817_index,
                information_type=information_type,
                data_type=data_type,
                reserved=reserved)
            report.reserved = wrong_reserved
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1817.get_prepairing_data_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPrepairingDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = LightspeedPrepairingTestUtils.GetPrepairingDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "information_type": (checker.check_information_type, information_type),
                "data_type": (checker.check_data_type, data_type),
                "data": None,
            })
            checker.check_fields(self, response, self.feature_1817.get_prepairing_data_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1817_0010", _AUTHOR)
    # end def test_get_prepairing_data_reserved
# end class LightspeedPrepairingRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
