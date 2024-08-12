# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.vlp.important.feature_0102.interface
:brief: VLP IRoot Interface test cases
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/09/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.vlp.features.important.vlproot import VLPRoot
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.vlprootutils import VLPRootTestUtils
from pytestbox.device.vlp.important.feature_0102.vlproot import VLPRootTestCase


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
_AUTHOR = "Vinodh Selvaraj"

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class VLPRootInterfaceTestCase(VLPRootTestCase):
    """
    Validates VLP Root interface testcases.
    """
    @features("Feature0102")
    @level("Interface")
    def test_get_feature_index(self):
        """
        Validate ``GetFeatureIndex`` normal processing

        [0] getFeatureIndex(featureId) -> featureId, featureIndex, featureVersion, featureMaxMemory
        """
        feature_id = int(VLPRoot.FEATURE_ID)
        feature_version = self.feature_0102.VERSION
        feature_max_memory = self.config.F_FeatureMaxMemory

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetFeatureIndex request")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPRootTestUtils.HIDppHelper.get_feature_index(
            test_case=self,
            feature_id=feature_id,
            vlp_begin=True,
            vlp_end=True,
            vlp_ack=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetFeatureIndexResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPRootTestUtils.GetFeatureIndexResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_0102_index)),
            "feature_id": (checker.check_feature_id, feature_id),
            "feature_idx": (checker.check_feature_idx, HexList(self.feature_0102_index)),
            "feature_version": (checker.check_feature_version, feature_version),
            "feature_max_memory": (checker.check_feature_max_memory, feature_max_memory)
        })
        checker.check_fields(test_case=self, message=response,
                             expected_cls=self.feature_0102.get_feature_index_response_cls,
                             check_map=check_map)

        self.testCaseChecked("INT_0102_0001", _AUTHOR)
    # end def test_get_feature_index

    @features("Feature0102")
    @level("Interface")
    def test_get_protocol_capabilities(self):
        """
        Validate ``GetProtocolCapabilities`` normal processing

        [1] getProtocolCapabilities() -> protocolMajor, protocolMinor, availableTotalMemory
        """
        protocol_major = self.config.F_ProtocolNumMajor
        protocol_minor = self.config.F_ProtocolNumMinor
        available_total_memory = self.config.F_TotalMemory
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetProtocolCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPRootTestUtils.HIDppHelper.get_protocol_capabilities(
            test_case=self,
            vlp_begin=True,
            vlp_end=True,
            vlp_ack=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetProtocolCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPRootTestUtils.GetProtocolCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_0102_index)),
            "protocol_major": (checker.check_protocol_major, protocol_major),
            "protocol_minor": (checker.check_protocol_minor, protocol_minor),
            "available_total_memory": (checker.check_available_total_memory, available_total_memory)
        })
        checker.check_fields(self, response, self.feature_0102.get_protocol_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_0102_0002", _AUTHOR)
    # end def test_get_protocol_capabilities

    @features("Feature0102")
    @level("Interface")
    def test_get_ping_data(self):
        """
        Validate ``GetPingData`` normal processing

        [2] getPingData(pingData) -> pingData
        """
        test_ping_data = 1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetPingData request")
        # --------------------------------------------------------------------------------------------------------------
        response = VLPRootTestUtils.HIDppHelper.get_ping_data(
            test_case=self,
            ping_data=test_ping_data,
            vlp_begin=True,
            vlp_end=True,
            vlp_ack=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetPingDataResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = VLPRootTestUtils.GetPingDataResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "device_index": (checker.check_device_index, HexList(self.original_device_index)),
            "feature_index": (checker.check_feature_index, HexList(self.feature_0102_index)),
            "ping_data": (checker.check_ping_data, test_ping_data)
        })
        checker.check_fields(self, response, self.feature_0102.get_ping_data_response_cls, check_map)

        self.testCaseChecked("INT_0102_0003", _AUTHOR)
    # end def test_get_ping_data