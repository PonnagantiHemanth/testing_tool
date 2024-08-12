#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.propertyaccessutils
:brief: Helpers for ``PropertyAccess`` feature
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/06/17
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.propertyaccess import PropertyAccess
from pyhid.hidpp.features.common.propertyaccess import PropertyAccessFactory
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PropertyAccessTestUtils(ConfigurablePropertiesTestUtils):
    """
    Provide helpers for common checks on ``PropertyAccess`` feature
    """

    class ConfigurationHelper(ConfigurablePropertiesTestUtils.ConfigurationHelper):
        # See ``ConfigurablePropertiesTestUtils.ConfigurationHelper``

        # Override these properties from 0x1807 ConfigurablePropertiesUtils
        SUPPORTED_PROPERTIES = ConfigurationManager.ID.SW_ACCESSIBLE_PROPERTIES
        SUPPORTED_PROPERTIES_SIZES = ConfigurationManager.ID.SW_ACCESSIBLE_PROPERTIES_SIZES
        LIBRARY = PropertyAccess
    # end class ConfigurationHelper

    class GetPropertyInfoResponseChecker(ConfigurablePropertiesTestUtils.GetPropertyInfoResponseChecker):
        # See ``ConfigurablePropertiesTestUtils.GetPropertyInfoResponseChecker``

        @classmethod
        def get_check_map_by_property(cls, test_case, property_id):
            """
            Get the default check methods and expected values for the ``GetPropertyInfoResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier
            :type property_id: ``PropertyAccess.PropertyId | int | HexList``

            :return: Check map for given property identifier
            :rtype: ``dict``
            """
            supported = PropertyAccessTestUtils.ConfigurationHelper.is_supported(test_case, property_id)
            size = PropertyAccessTestUtils.ConfigurationHelper.get_size(test_case, property_id)

            checker = PropertyAccessTestUtils.FlagsMaskBitMapChecker
            flags = checker.get_default_check_map(test_case)
            flags.update({
                "supported": (checker.check_supported, supported)
            })
            check_map = cls.get_default_check_map(test_case)
            check_map.update({
                "flags": (cls.check_flags, flags),
                "size": (cls.check_size, size)
            })
            return check_map
        # end def get_check_map_by_property
    # end class GetPropertyInfoResponseChecker

    class NvsHelper(ConfigurablePropertiesTestUtils.CommonNvsHelper):
        # See ``ConfigurablePropertiesTestUtils.CommonNvsHelper``
        pass
    # end class NvsHelper

    class HIDppHelper(ConfigurablePropertiesTestUtils.CommonHIDppHelper):
        # See ``ConfigurablePropertiesTestUtils.CommonHIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=PropertyAccess.FEATURE_ID, factory=PropertyAccessFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def select_property(cls, test_case, property_id, rd_offset=0, device_index=None,
                            port_index=None, software_id=None, padding=None):
            """
            Process ``SelectProperty``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier [1 to 255] or 0 to deselect all properties
            :type property_id: ``PropertyAccess.PropertyId | int | HexList``
            :param rd_offset: Property read offset in bytes - OPTIONAL
            :type rd_offset: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | HexList | None``

            :return: SelectPropertyResponse
            :rtype: ``pyhid.hidpp.features.common.propertyaccess.SelectPropertyResponse``
            """
            feature_0011_index, feature_0011, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0011.select_property_cls(
                device_index=device_index,
                feature_index=feature_0011_index,
                property_id=HexList(property_id),
                rd_offset=rd_offset)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_0011.select_property_response_cls)
        # end def select_property

        @classmethod
        def select_property_and_check_error(
                cls, test_case, error_codes, property_id, rd_offset=0, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``SelectProperty``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param property_id: Property identifier [1 to 255] or 0 to deselect all properties
            :type property_id: ``PropertyAccess.PropertyId | int | HexList``
            :param rd_offset: Property read offset in bytes - OPTIONAL
            :type rd_offset: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``

            :return: SelectPropertyResponse
            :rtype: ``pyhid.hidpp.features.common.propertyaccess.SelectPropertyResponse``
            """
            feature_0011_index, feature_0011, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0011.select_property_cls(
                device_index=device_index,
                feature_index=feature_0011_index,
                property_id=HexList(property_id),
                rd_offset=rd_offset)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def select_property_and_check_error

        @classmethod
        def search_present(cls, test_case, present=True, min_size=0, skip_properties=None, device_index=None,
                           port_index=None):
            """
            Search the first property matching the presence and size requirements

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param present: Flag to indicate whether property should be present - OPTIONAL
            :type present: ``bool``
            :param min_size: Minimum property size required - OPTIONAL
            :type min_size: ``int``
            :param skip_properties: Properties not wanted for selection - OPTIONAL
            :type skip_properties: ``list | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``

            :return: Property id or None if no match
            :rtype: ``PropertyAccess.PropertyId | None``
            """
            skip_properties = [] if skip_properties is None else skip_properties
            properties = [prop for prop in
                          test_case.config_manager.get_feature(ConfigurationManager.ID.SW_ACCESSIBLE_PROPERTIES)
                          if prop not in skip_properties]

            for property_id in properties:
                # Check property size first because it's faster, no need to send requests if size doesn't match
                property_size = PropertyAccessTestUtils.ConfigurationHelper.get_size(test_case, property_id)
                if property_size >= min_size:
                    is_present = cls.is_present(test_case, property_id, device_index, port_index)
                    if (is_present and present) or (not is_present and not present):
                        return property_id
                    # end if
                # end if
            # end for
        # end def search_present

        @classmethod
        def is_present(cls, test_case, property_id, device_index=None, port_index=None):
            """
            Check if a property is present

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier
            :type property_id: ``PropertyAccess.PropertyId | int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``

            :return: True if property is present
            :rtype: ``bool``
            """
            property_info = cls.get_property_info(test_case, property_id, device_index, port_index)
            return PropertyAccess.FlagsMaskBitMap(property_info.flags).present
        # end def is_present

        @classmethod
        def get_first_property_present(cls, test_case, present=True, min_size=0, skip_properties=None,
                                       write_data_if_none=None, device_index=None, port_index=None):
            """
            Get the first property matching the presence and size requirements. If no property is found at first
            search, write the first supported one.

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param present: Flag to indicate whether property should be present - OPTIONAL
            :type present: ``bool``
            :param min_size: Minimum property size required - OPTIONAL
            :type min_size: ``int``
            :param skip_properties: Properties not wanted for selection - OPTIONAL
            :type skip_properties: ``list | None``
            :param write_data_if_none: Data to write if a property has to be written - OPTIONAL
            :type write_data_if_none: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``

            :return: Property id
            :rtype: ``ConfigurableProperties.PropertyId``
            """
            property_id = cls.search_present(test_case, present, min_size, skip_properties, device_index, port_index)
            if property_id is not None:
                property_size = PropertyAccessTestUtils.ConfigurationHelper.get_size(test_case, property_id=property_id)
                return property_id, property_size
            # end if

            property_id, property_size = PropertyAccessTestUtils.ConfigurationHelper.get_first_supported_property(
                test_case, min_size, skip_properties)
            test_case.post_requisite_reload_nvs = True
            if write_data_if_none is None:
                write_data_if_none = HexList("00")
            else:
                write_data_if_none = HexList(write_data_if_none)
            # end if
            if property_size > 0:
                d, m = divmod(len(write_data_if_none), property_size)
                if d == 0:
                    assert m == 1, f'Provided data {write_data_if_none} is uneven to match size ({property_size})'
                    write_data_if_none *= property_size
                # end if
            # end if
            if present:
                PropertyAccessTestUtils.NvsHelper.write_property_id(test_case, property_id, write_data_if_none)
            else:
                PropertyAccessTestUtils.NvsHelper.invalidate_chunk(test_case, property_id)
            # end if
            return property_id, property_size
        # end def get_first_property_present
    # end class HIDppHelper
# end class PropertyAccessTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
