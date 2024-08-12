#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.forcepairingutils
:brief:  Helpers for Force Pairing feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.common.forcepairing import ForcePairing
from pyhid.hidpp.features.common.forcepairing import ForcePairingFactory
from pyhid.hidpp.features.common.forcepairing import GetCapabilitiesResponse
from pyhid.hidpp.features.common.forcepairing import SetForcePairingResponse
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ForcePairingTestUtils(DeviceBaseTestUtils):
    """
    Test utils for Force Pairing feature
    """

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=ForcePairing.FEATURE_ID,
                           factory=ForcePairingFactory, device_index=None, port_index=None,
                           update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)

        # end def get_parameters

        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None):
            """
            Return the force pairing information.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: get power modes response
            :rtype: ``GetCapabilitiesResponse``
            """
            # Add feature class and index as test attributes
            feature_1500_index, feature_1500, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(test_case, 'Send GetCapabilities request')
            # ----------------------------------------------------------------------------------------------------------
            get_capabilities = feature_1500.get_capabilities_cls(
                device_index=device_index, feature_index=feature_1500_index)
            get_capabilities_response = test_case.send_report_wait_response(
                report=get_capabilities,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature_1500.get_capabilities_response_cls)

            return get_capabilities_response
        # end def get_capabilities

        @classmethod
        def set_force_pairing(cls, test_case, pairing_address, device_index=None, port_index=None):
            """
            Force the device entering to the pairing mode.

            :param test_case: The current test case
            :type test_case: ``Class inheriting CommonBaseTestCase``
            :param pairing_address: Pairing address of the destination receiver (4 bytes)
            :type pairing_address: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: set force pairing response
            :rtype: ``SetForcePairingResponse``
            """
            # Add feature class and index as test attributes
            feature_1500_index, feature_1500, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(test_case, 'Send SetForcePairing request')
            # ----------------------------------------------------------------------------------------------------------
            set_force_pairing = feature_1500.set_force_pairing_cls(device_index=device_index,
                                                                   feature_index=feature_1500_index,
                                                                   pairing_address=pairing_address)
            set_force_pairing_response = test_case.send_report_wait_response(
                report=set_force_pairing,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=feature_1500.set_force_pairing_response_cls)

            return set_force_pairing_response
        # end def set_force_pairing
    # end class HIDppHelper
# end class ForcePairingTestUtils
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
