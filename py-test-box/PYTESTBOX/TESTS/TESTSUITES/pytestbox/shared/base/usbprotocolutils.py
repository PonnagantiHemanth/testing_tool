#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.usbprotocolutils
:brief:  Helpers for USB Protocol (applicable to device and receiver targets)
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/06/29
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from contextlib import contextmanager

from pylibrary.system.tracelogger import TraceLevel
from pylibrary.system.tracelogger import TraceLogger
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
TRACE_LOGGER = TraceLogger.get_instance()


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class UsbProtocolTestUtils(DeviceBaseTestUtils):
    """
    Test utils for USB Protocol (applicable to device and receiver targets)
    """
    @classmethod
    @contextmanager
    def manage_verbosity_usb_context(cls, test_case, trace_level):
        """
        Change the trace level of the USB context for a given section. If the level is the same as the current one,
        nothing is done.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param trace_level: The wanted trace level requested for the USB context
        :type trace_level: ``TraceLevel``
        """
        usb_context = cls.get_usb_context(test_case=test_case)
        current_trace_level = TRACE_LOGGER.get_trace_level(subscription_owner=usb_context)
        assert current_trace_level is not None, "The USB context is not subscribed to the trace logger"

        if current_trace_level == trace_level:
            yield
            return
        # end if

        TRACE_LOGGER.update_trace_level(subscription_owner=usb_context, trace_level=trace_level)
        try:
            yield
        finally:
            TRACE_LOGGER.update_trace_level(subscription_owner=usb_context, trace_level=current_trace_level)
        # end try
    # end def manage_verbosity_usb_context

    @staticmethod
    def get_usb_context(test_case, perform_sanity_check=True):
        """
        Get the USB context. If requested (by default it is), a sanity check of it being not ``None`` and open is
        performed.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param perform_sanity_check:  Flag indicating to perform the sanity check - OPTIONAL
        :type perform_sanity_check: ``bool``

        :return: The USB context or ``None`` if it is not present and the sanity check is not requested
        :rtype: ``UsbContext`` or ``None``

        :raise ``AssertionError``: if the sanity check fails
        """
        if perform_sanity_check:
            assert test_case.device.USB_CONTEXT is not None and test_case.device.USB_CONTEXT.is_open, \
                "Test case should have an open USB context to use this method"
        # end if

        return test_case.device.USB_CONTEXT
    # end def get_usb_context
# end class UsbProtocolTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
