# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.important.feature_0102.robustness
:brief: VLP IRoot Robustness test cases
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/09/19
"""

# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.vlp.features.important.vlproot import GetPingData, GetProtocolCapabilities, GetFeatureIndex, VLPRoot
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values, compute_inf_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.vlprootutils import VLPRootTestUtils
from pytestbox.device.vlp.important.feature_0102.vlproot import VLPRootTestCase

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"
_LOOP_END = "End Test Loop"
_LOOP_START_RESERVED = "Test loop over reserved range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class VLPRootRobustnessTestCase(VLPRootTestCase):
    """
    Validates VLP Root robustness testcases.
    """
    @features("Feature0102")
    @level("Robustness")
    def test_get_feature_index_software_id(self):
        """
        Validate ``GetFeatureIndex`` software id field is ignored by the firmware

        [0] getFeatureIndex(featureId) -> featureId, featureIndex, featureVersion, featureMaxMemory

        Request: 0x13.DeviceIndex.FeatureIndex.FunctionIndex|SwID

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        feature_id = int(VLPRoot.FEATURE_ID)
        feature_version = self.feature_0102.VERSION
        feature_max_memory = self.config.F_FeatureMaxMemory

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(GetFeatureIndex.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetFeatureIndex request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPRootTestUtils.HIDppHelper.get_feature_index(
                test_case=self,
                feature_id=feature_id,
                software_id=software_id,
                vlp_begin=True,
                vlp_end=True,
                vlp_ack=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetFeatureIndexResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = VLPRootTestUtils.GetFeatureIndexResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "feature_id": (checker.check_feature_id, feature_id),
                "feature_idx": (checker.check_feature_idx, HexList(self.feature_0102_index)),
                "feature_version": (checker.check_feature_version, feature_version),
                "feature_max_memory": (checker.check_feature_max_memory, feature_max_memory)
            })
            checker.check_fields(self, response, self.feature_0102.get_feature_index_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0102_0001#1", _AUTHOR)

    # end def test_get_feature_index_software_id

    @features("Feature0102")
    @level("Robustness")
    def test_get_protocol_capabilities_software_id(self):
        """
        Validate ``GetProtocolCapabilities`` software id field is ignored by the firmware

        [1] getProtocolCapabilities() -> protocolMajor, protocolMinor, availableTotalMemory

        Request: 0x13.DeviceIndex.FeatureIndex.FunctionIndex|SwID

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(GetProtocolCapabilities.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetProtocolCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPRootTestUtils.HIDppHelper.get_protocol_capabilities(
                test_case=self,
                software_id=software_id,
                vlp_begin=True,
                vlp_end=True,
                vlp_ack=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetProtocolCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = VLPRootTestUtils.GetProtocolCapabilitiesResponseChecker
            checker.check_fields(self, response, self.feature_0102.get_protocol_capabilities_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0102_0001#2", _AUTHOR)

    # end def test_get_protocol_capabilities_software_id

    @features("Feature0102")
    @level("Robustness")
    def test_get_ping_data_software_id(self):
        """
        Validate ``GetPingData`` software id field is ignored by the firmware

        [2] getPingData(pingData) -> pingData

        Request: 0x13.DeviceIndex.FeatureIndex.FunctionIndex|SwID

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        test_ping_data = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(GetPingData.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPingData request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPRootTestUtils.HIDppHelper.get_ping_data(
                test_case=self,
                ping_data=test_ping_data,
                software_id=software_id,
                vlp_begin=True,
                vlp_end=True,
                vlp_ack=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPingDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = VLPRootTestUtils.GetPingDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({"ping_data": (checker.check_ping_data, test_ping_data)})
            checker.check_fields(self, response, self.feature_0102.get_ping_data_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0102_0001#3", _AUTHOR)

    # end def test_get_ping_data_software_id

    @features("Feature0102")
    @level("Robustness")
    def test_get_feature_index_reserved(self):
        """
        Validate ``GetFeatureIndex`` reserved bytes are ignored by the firmware

        Request: 0x13.DeviceIndex.FeatureIndex.FunctionIndex|SwID.VLPBegin.VLPEnd.VLPAck.R.VLPSequence

        Reserved (R) boundary values [0..F]
        """
        feature_id = int(VLPRoot.FEATURE_ID)
        feature_version = self.feature_0102.VERSION
        feature_max_memory = self.config.F_FeatureMaxMemory
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        for reserved in compute_sup_values(HexList(
                Numeral(GetFeatureIndex.DEFAULT.RESERVED, GetFeatureIndex.LEN.VLP_RESERVED // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetFeatureIndex request with reserved: {reserved}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPRootTestUtils.HIDppHelper.get_feature_index(
                test_case=self,
                feature_id=feature_id,
                vlp_reserved=reserved,
                vlp_begin=True,
                vlp_end=True,
                vlp_ack=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetFeatureIndexResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = VLPRootTestUtils.GetFeatureIndexResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "feature_id": (checker.check_feature_id, feature_id),
                "feature_idx": (checker.check_feature_idx, HexList(self.feature_0102_index)),
                "feature_version": (checker.check_feature_version, feature_version),
                "feature_max_memory": (checker.check_feature_max_memory, feature_max_memory),
            })
            checker.check_fields(self, response, self.feature_0102.get_feature_index_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0102_0002#1", _AUTHOR)

    # end def test_get_feature_index_reserved

    @features("Feature0102")
    @level("Robustness")
    def test_get_protocol_capabilities_reserved(self):
        """
        Validate ``GetProtocolCapabilities`` reserved bytes are ignored by the firmware

        Request: 0x13.DeviceIndex.FeatureIndex.FunctionIndex|SwID.VLPBegin.VLPEnd.VLPAck.R.VLPSequence

        Reserved (R) boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        for reserved in compute_sup_values(HexList(
                Numeral(GetProtocolCapabilities.DEFAULT.RESERVED, GetProtocolCapabilities.LEN.VLP_RESERVED // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetProtocolCapabilities request with reserved: {reserved}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPRootTestUtils.HIDppHelper.get_protocol_capabilities(
                test_case=self,
                vlp_reserved=reserved,
                vlp_begin=True,
                vlp_end=True,
                vlp_ack=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetProtocolCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = VLPRootTestUtils.GetProtocolCapabilitiesResponseChecker
            checker.check_fields(self, response, self.feature_0102.get_protocol_capabilities_response_cls)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROB_0102_0002#2", _AUTHOR)

    # end def test_get_protocol_capabilities_reserved

    @features("Feature0102")
    @level("Robustness")
    def test_get_ping_data_capabilities_reserved(self):
        """
        Validate ``GetPingData`` reserved bytes are ignored by the firmware

        Request: 0x13.DeviceIndex.FeatureIndex.FunctionIndex|SwID.VLPBegin.VLPEnd.VLPAck.R.VLPSequence

        Reserved (R) boundary values [0..F]
        """
        test_ping_data = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        for reserved in compute_sup_values(HexList(
                Numeral(GetPingData.DEFAULT.RESERVED, GetPingData.LEN.VLP_RESERVED // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPingData request with reserved: {reserved}")
            # ----------------------------------------------------------------------------------------------------------
            response = VLPRootTestUtils.HIDppHelper.get_ping_data(
                test_case=self,
                ping_data=test_ping_data,
                vlp_reserved=reserved,
                vlp_begin=True,
                vlp_end=True,
                vlp_ack=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPingDataResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = VLPRootTestUtils.GetPingDataResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({"ping_data": (checker.check_ping_data, test_ping_data)})
            checker.check_fields(self, response, self.feature_0102.get_ping_data_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROB_0102_0002#3", _AUTHOR)
    # end def test_get_ping_data_capabilities_reserved

    @features("Feature0102")
    @level("Robustness")
    def test_zero_ping_data(self):
        """
        Validate Ping Data value zero can be sent. Specification mentions that this value should not be used by
        software but if it is, firmware respond normally.
        """
        test_ping_data = 0
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Send GetPingData request")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPRootTestUtils.HIDppHelper.get_ping_data(
            test_case=self,
            ping_data=test_ping_data,
            vlp_begin=True,
            vlp_end=True,
            vlp_ack=True)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetPingDataResponse fields")
        # ----------------------------------------------------------------------------------------------------------
        checker = VLPRootTestUtils.GetPingDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({"ping_data": (checker.check_ping_data, test_ping_data)})
        checker.check_fields(self, response, self.feature_0102.get_ping_data_response_cls, check_map)

        self.testCaseChecked("ROB_0102_0005", _AUTHOR)
    # end def test_zero_ping_data
# end class VLPRootRobustnessTestCase
