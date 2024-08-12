#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_0011.robustness
:brief: HID++ 2.0 ``PropertyAccess`` robustness test suite
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/06/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.configurableproperties import WriteProperty
from pyhid.hidpp.features.common.propertyaccess import PropertyAccess
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.propertyaccessutils import PropertyAccessTestUtils
from pytestbox.device.hidpp20.common.feature_0011.propertyaccess import PropertyAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Kevin Dayet"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class PropertyAccessRobustnessTestCase(PropertyAccessTestCase):
    """
    Validate ``PropertyAccess`` robustness test cases
    """

    @features("Feature0011")
    @level("Robustness")
    def test_get_property_info_software_id(self):
        """
        Validate ``GetPropertyInfo`` software id field is ignored by the firmware

        [0] getPropertyInfo(propertyId) -> flags, size

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PropertyId.0xPP.0xPP

        SwID boundary values [0..F]
        """
        property_id = PropertyAccess.PropertyId.MIN
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PropertyAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPropertyInfo request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = PropertyAccessTestUtils.HIDppHelper.get_property_info(
                test_case=self,
                property_id=property_id,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check GetPropertyInfoResponse fields with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            checker = PropertyAccessTestUtils.GetPropertyInfoResponseChecker
            check_map = checker.get_check_map_by_property(
                self, property_id=property_id)
            checker.check_fields(self, response, self.feature_0011.get_property_info_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0011_0002#1", _AUTHOR)
    # end def test_get_property_info_software_id

    @features("Feature0011")
    @level("Robustness")
    def test_select_property_software_id(self):
        """
        Validate ``SelectProperty`` software id field is ignored by the firmware

        [1] selectProperty(propertyId, rdOffset) -> None

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PropertyId.RdOffset

        SwID boundary values [0..F]
        """
        property_id, _ = PropertyAccessTestUtils.ConfigurationHelper.get_first_supported_property(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PropertyAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SelectProperty request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = PropertyAccessTestUtils.HIDppHelper.select_property(
                test_case=self,
                property_id=property_id,
                software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check SelectPropertyResponse fields with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            PropertyAccessTestUtils.MessageChecker.check_fields(
                self, response, self.feature_0011.select_property_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0011_0002#2", _AUTHOR)
    # end def test_select_property_software_id

    @features("Feature0011")
    @level("Robustness")
    def test_read_property_software_id(self):
        """
        Validate ``ReadProperty`` software id field is ignored by the firmware

        [2] readProperty() -> data

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        SwID boundary values [0..F]
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select first present property")
        # --------------------------------------------------------------------------------------------------------------
        property_id, _ = PropertyAccessTestUtils.HIDppHelper.get_first_property_present(
            self, write_data_if_none=0xAA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(PropertyAccess.DEFAULT.SOFTWARE_ID):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SelectProperty with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id=property_id, software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadProperty request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            response = PropertyAccessTestUtils.HIDppHelper.read_property(test_case=self, software_id=software_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check ReadPropertyResponse fields with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            checker = PropertyAccessTestUtils.ReadPropertyResponseChecker
            check_map = checker.get_default_check_map(self)
            # Skip check of field data
            check_map["data"] = None
            checker.check_fields(self, response, self.feature_0011.read_property_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0011_0002#3", _AUTHOR)
    # end def test_read_property_software_id

    @features("Feature0011")
    @level("Robustness")
    def test_get_property_info_padding(self):
        """
        Validate ``GetPropertyInfo`` padding bytes are ignored by the firmware

        [0] getPropertyInfo(propertyId) -> flags, size

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.PropertyId.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        property_id = PropertyAccess.PropertyId.MIN
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_0011.get_property_info_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPropertyInfo request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = PropertyAccessTestUtils.HIDppHelper.get_property_info(
                test_case=self,
                property_id=property_id,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPropertyInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PropertyAccessTestUtils.GetPropertyInfoResponseChecker
            check_map = checker.get_check_map_by_property(self, property_id=property_id)
            checker.check_fields(self, response, self.feature_0011.get_property_info_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0011_0003#1", _AUTHOR)
    # end def test_get_property_info_padding

    @features("Feature0011")
    @level("Robustness")
    def test_read_property_padding(self):
        """
        Validate ``ReadProperty`` padding bytes are ignored by the firmware

        [2] readProperty() -> data

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.0xPP.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        property_id, _ = PropertyAccessTestUtils.HIDppHelper.get_first_property_present(
            self, write_data_if_none=0xAA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_0011.read_property_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Select first supported property")
            # ----------------------------------------------------------------------------------------------------------
            PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id=property_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send ReadProperty request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            response = PropertyAccessTestUtils.HIDppHelper.read_property(
                test_case=self,
                padding=padding)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReadPropertyResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = PropertyAccessTestUtils.ReadPropertyResponseChecker
            check_map = checker.get_default_check_map(self)
            # Skip check of field data
            check_map["data"] = None
            checker.check_fields(self, response, self.feature_0011.read_property_response_cls, check_map=check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_0011_0003#2", _AUTHOR)
    # end def test_read_property_padding

    @features("Feature0011")
    @features("Feature1807")
    @level("Robustness")
    @services('Debugger')
    def test_select_property_with_feature_1807_select_other_property(self):
        """
        Validate 0x1807 ConfigurableProperties.SelectProperties.propertyId has no effect on 0x0011
        SelectProperty.propertyId
        """
        data_property_1 = 0xAA
        data_property_2 = 0xBB
        property_id_1, property_size_1 = PropertyAccessTestUtils.HIDppHelper.\
            get_first_property_present(self, write_data_if_none=data_property_1)
        property_id_2, property_size_2 = PropertyAccessTestUtils.HIDppHelper.\
            get_first_property_present(self, skip_properties=[property_id_1], write_data_if_none=data_property_2)
        data_property_1 = HexList(data_property_1) * property_size_1
        data_property_2 = HexList(data_property_2) * property_size_2
        data_property_1.addPadding(WriteProperty.LEN.DATA // 8, fromLeft=False)
        data_property_2.addPadding(WriteProperty.LEN.DATA // 8, fromLeft=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select first property with 0x0011 SelectProperty")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id=property_id_1)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select an other property with 0x1807 ConfigurableProperties.SelectProperties")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property with 0x0011 ReadProperty")
        # --------------------------------------------------------------------------------------------------------------
        response = PropertyAccessTestUtils.HIDppHelper.read_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check first property is read")
        # --------------------------------------------------------------------------------------------------------------
        checker = PropertyAccessTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_property_1),
        })
        checker.check_fields(self, response, self.feature_0011.read_property_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property with 0x1807 ConfigurableProperties.ReadProperty")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurablePropertiesTestUtils.HIDppHelper.read_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the other property is read with 0x1807")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_property_2),
        })
        checker.check_fields(self, response, self.feature_1807.read_property_response_cls, check_map=check_map)

        self.testCaseChecked("ROB_0011_0004", _AUTHOR)
    # end def test_select_property_with_feature_1807_select_other_property

    @features("Feature0011")
    @features("Feature1807")
    @level("Robustness")
    @services('Debugger')
    def test_select_property_with_feature_1807_rd_offset(self):
        """
        Validate 0x1807 ``ConfigurableProperties.SelectProperties.rdOffset`` has no effect on 0x0011
        ``SelectProperty.propertyId``
        """
        property_id, property_size = PropertyAccessTestUtils.\
            HIDppHelper.get_first_property_present(self, min_size=3,
                                                   skip_properties=[PropertyAccess.PropertyId.SERIAL_NUMBER])
        data_property = HexList("AA" + "BB" + "CC" + ("DD" * (property_size - 3)))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Write data property with nvs parser")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        PropertyAccessTestUtils.NvsHelper.write_property_id(self, property_id, data_property)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select property with SelectProperty with a first offset")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id=property_id, rd_offset=1)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select same property property with ConfigurableProperties.SelectProperties, "
                                         "but with a different rdOffset")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id, rd_offset=2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property with ReadProperty")
        # --------------------------------------------------------------------------------------------------------------
        response = PropertyAccessTestUtils.HIDppHelper.read_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check first property is read from first offset")
        # --------------------------------------------------------------------------------------------------------------
        data_field_len = self.feature_0011.read_property_response_cls.LEN.DATA // 8
        if data_field_len < property_size:
            data_expected = data_property[1:data_field_len + 1]
        else:
            data_expected = HexList(data_property[1::])
            data_expected.addPadding(size=data_field_len, fromLeft=False)
        # end if
        checker = PropertyAccessTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_expected),
        })
        checker.check_fields(self, response, self.feature_0011.read_property_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property with ConfigurableProperties.ReadProperty")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurablePropertiesTestUtils.HIDppHelper.read_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the other property is read from other offset")
        # --------------------------------------------------------------------------------------------------------------
        data_field_len = self.feature_1807.read_property_response_cls.LEN.DATA // 8
        if data_field_len < property_size:
            data_expected = data_property[2:data_field_len + 2]
        else:
            data_expected = HexList(data_property[2::])
            data_expected.addPadding(size=data_field_len, fromLeft=False)
        # end if
        checker = ConfigurablePropertiesTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_expected),
        })
        checker.check_fields(self, response, self.feature_1807.read_property_response_cls, check_map=check_map)

        self.testCaseChecked("ROB_0011_0005", _AUTHOR)
    # end def test_select_property_with_feature_1807_rd_offset

    @features("Feature0011")
    @features("Feature1807")
    @level("Robustness")
    @services('Debugger')
    def test_select_property_with_feature_1807_select_same_property(self):
        """
        Validate 0x1807 ``ConfigurableProperties.SelectProperties`` has no effect on 0x0011
        ``SelectProperty.property``
        """
        property_id, property_size = PropertyAccessTestUtils. \
            HIDppHelper.get_first_property_present(self, min_size=2,
                                                   skip_properties=[PropertyAccess.PropertyId.SERIAL_NUMBER])
        data_property = HexList("AA" + "BB" + ("CC" * (property_size - 2)))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Write data property with nvs parser")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        PropertyAccessTestUtils.NvsHelper.write_property_id(self, property_id, data_property)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select first property with SelectProperty")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id=property_id, rd_offset=1)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select same property with ConfigurableProperties.SelectProperties and same "
                                         "rdOffset")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id, rd_offset=1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property with ReadProperty")
        # --------------------------------------------------------------------------------------------------------------
        response = PropertyAccessTestUtils.HIDppHelper.read_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check first property is read")
        # --------------------------------------------------------------------------------------------------------------
        data_field_len = self.feature_0011.read_property_response_cls.LEN.DATA // 8
        if data_field_len < property_size:
            data_expected = data_property[1:data_field_len + 1]
        else:
            data_expected = HexList(data_property[1::])
            data_expected.addPadding(size=data_field_len, fromLeft=False)
        # end if
        checker = PropertyAccessTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_expected),
        })
        checker.check_fields(self, response, self.feature_0011.read_property_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property with ConfigurableProperties.ReadProperty")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurablePropertiesTestUtils.HIDppHelper.read_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, " Check same property is read, from original offset")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_expected),
        })
        checker.check_fields(self, response, self.feature_1807.read_property_response_cls, check_map=check_map)

        self.testCaseChecked("ROB_0011_0006", _AUTHOR)
    # end def test_select_property_with_feature_1807_select_same_property

    @features("Feature0011")
    @features("Feature1807")
    @level("Robustness")
    @services('Debugger')
    def test_select_property_other_on_feature_1807_select_property(self):
        """
        Validate 0x0011 ``SelectProperties`` has no effect on 0x1807 ``ConfigurableProperties.SelectProperties`` for
        reading
        """
        data_property_1 = 0xAA
        data_property_2 = 0xBB
        property_id_1, property_size_1 = PropertyAccessTestUtils.HIDppHelper. \
            get_first_property_present(self, write_data_if_none=data_property_1)
        property_id_2, property_size_2 = PropertyAccessTestUtils.HIDppHelper. \
            get_first_property_present(self, skip_properties=[property_id_1], write_data_if_none=data_property_2)
        data_property_1 = HexList(data_property_1) * property_size_1
        data_property_2 = HexList(data_property_2) * property_size_2
        data_property_1.addPadding(WriteProperty.LEN.DATA // 8, fromLeft=False)
        data_property_2.addPadding(WriteProperty.LEN.DATA // 8, fromLeft=False)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select first property with ConfigurableProperties.SelectProperties")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select an other property with SelectProperty")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id=property_id_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property with ConfigurableProperties.ReadProperty")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurablePropertiesTestUtils.HIDppHelper.read_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check first property is read")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_property_1),
        })
        checker.check_fields(self, response, self.feature_1807.read_property_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property with ReadProperty")
        # --------------------------------------------------------------------------------------------------------------
        response = PropertyAccessTestUtils.HIDppHelper.read_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the other property is read")
        # --------------------------------------------------------------------------------------------------------------
        checker = PropertyAccessTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_property_2),
        })
        checker.check_fields(self, response, self.feature_0011.read_property_response_cls, check_map=check_map)

        self.testCaseChecked("ROB_0011_0007", _AUTHOR)
    # end def test_select_property_other_on_feature_1807_select_property

    @features("Feature0011")
    @features("Feature1807")
    @level("Robustness")
    @services('Debugger')
    def test_select_property_on_feature_1807_write_other_property(self):
        """
        Validate 0x0011 ``SelectProperties`` has no effect on 0x1807 ``ConfigurableProperties.SelectProperties`` for
        writing
        """
        data_property_1 = 0xAA
        data_property_2 = 0xBB
        property_id_1, property_size_1 = PropertyAccessTestUtils.HIDppHelper.get_first_property_present(self)
        property_id_2, property_size_2 = PropertyAccessTestUtils.HIDppHelper. \
            get_first_property_present(self, skip_properties=[property_id_1], write_data_if_none=data_property_2)
        data_property_1 = HexList(data_property_1) * property_size_1
        data_property_2 = HexList(data_property_2) * property_size_2
        data_property_1.addPadding(WriteProperty.LEN.DATA // 8, fromLeft=False)
        data_property_2.addPadding(WriteProperty.LEN.DATA // 8, fromLeft=False)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select first property with ConfigurableProperties.SelectProperties")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select an other property with SelectProperty")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id=property_id_2)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write property with ConfigurableProperties.WriteProperty")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.write_property(self, data_property_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property with ReadProperty")
        # --------------------------------------------------------------------------------------------------------------
        response = PropertyAccessTestUtils.HIDppHelper.read_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the other property is read")
        # --------------------------------------------------------------------------------------------------------------
        checker = PropertyAccessTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_property_2),
        })
        checker.check_fields(self, response, self.feature_0011.read_property_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Select first property again with ConfigurableProperties.SelectProperties")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property with ConfigurableProperties.ReadProperty")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurablePropertiesTestUtils.HIDppHelper.read_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check first property is read")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_property_1),
        })
        checker.check_fields(self, response, self.feature_1807.read_property_response_cls, check_map=check_map)

        self.testCaseChecked("ROB_0011_0008", _AUTHOR)
    # end def test_select_property_on_feature_1807_write_other_property

    @features("Feature0011")
    @features("Feature1807")
    @level("Robustness")
    @services('Debugger')
    def test_select_property_padding_on_feature_1807_write_same_property(self):
        """
        Validate 0x0011 ``SelectProperties`` has no effect on 0x1807 ``ConfigurableProperties.SelectProperties`` for
        writing
        """
        property_id, property_size = PropertyAccessTestUtils. \
            HIDppHelper.get_first_property_present(self,
                                                   present=False,
                                                   min_size=3,
                                                   skip_properties=[PropertyAccess.PropertyId.SERIAL_NUMBER])
        data_field_len = self.feature_1807.write_property_cls.LEN.DATA // 8
        data_property = HexList("AA" + "BB" + ("CC" * (min(property_size, data_field_len) - 2)))

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select first property with ConfigurableProperties.SelectProperties")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Select same property with SelectProperty with SelectProperty.padding = 1 and "
                                         "rd_offset = 2")
        # --------------------------------------------------------------------------------------------------------------
        padding = HexList("01")
        PropertyAccessTestUtils.HIDppHelper.select_property(
            test_case=self,
            property_id=HexList(property_id),
            rd_offset=2,
            padding=padding)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Write property with ConfigurableProperties.WriteProperty")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.write_property(self, data_property)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property with ReadProperty")
        # --------------------------------------------------------------------------------------------------------------
        response = PropertyAccessTestUtils.HIDppHelper.read_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check property is read, from SelectProperty.rdOffset "
                                  "(and SelectProperty.padding is ignored)")
        # --------------------------------------------------------------------------------------------------------------
        data_response = HexList(data_property[2::])
        data_field_len = self.feature_0011.read_property_response_cls.LEN.DATA // 8
        data_response.addPadding(size=data_field_len, fromLeft=False)
        checker = PropertyAccessTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_response),
        })
        checker.check_fields(self, response, self.feature_0011.read_property_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Select first property again with ConfigurableProperties.SelectProperties")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property with ConfigurableProperties.ReadProperty")
        # --------------------------------------------------------------------------------------------------------------
        response = ConfigurablePropertiesTestUtils.HIDppHelper.read_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check first property is read and has been written from correct offset")
        # --------------------------------------------------------------------------------------------------------------
        checker = ConfigurablePropertiesTestUtils.ReadPropertyResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "data": (checker.check_data, data_property),
        })
        checker.check_fields(self, response, self.feature_1807.read_property_response_cls, check_map=check_map)

        self.testCaseChecked("ROB_0011_0009", _AUTHOR)
    # end def test_select_property_padding_on_feature_1807_write_same_property
# end class PropertyAccessRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
