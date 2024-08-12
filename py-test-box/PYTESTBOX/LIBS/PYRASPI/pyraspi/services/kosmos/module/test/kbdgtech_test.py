#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.kbdgtech_test
:brief: Kosmos KBD_GTECH Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2024/04/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod

from pylibrary.emulator.keyid import KEY_ID
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.kbdgtech import KbdGtechModule
from pyraspi.services.kosmos.module.test.module_test import AbstractTestClass
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.test.usbhubutils import UsbHubTestCaseUtils
from pytransport.usb.usbhub.usbhubconstants import UsbHubAction

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

GALVATRON_KBD_FW_ID = 'U170'
GALVATRON_BOOT_UP_DURATION_S = 2.5  # time required for the firmware to boot (from power on to USB discovered)
GALVATRON_USB_HUB_PORT_INDEX = 1    # Phidget USH hub port 1 (rightmost port)

# Those keys do not generate any HID report, as there are purely handled by the DUT firmware
GALVATRON_NO_HID_REPORTING_KEYS = {
    KEY_ID.DIMMING_KEY,
    KEY_ID.GAME_MODE_KEY
}

VERBOSE = False  # Toggle verbose mode for this Unit Test file


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KbdGtechModuleAbstractTestCase:
    """
    This class is used to wrap Abstract TestCase classes, so that they cannot be automatically discovered
    and executed by test executors (unittest, pytest...).

    Refer to ``pyraspi.services.kosmos.module.test.module_test.AbstractTestClass``
    """

    @require_kosmos_device(DeviceName.KBD_GTECH)
    class BaseTestCase(AbstractTestClass.UploadModuleInterfaceTestCase, UsbHubTestCaseUtils, metaclass=ABCMeta):
        """
        Kosmos KBD_GTECH Module Test Class.

        """
        # Update type hint
        module: KbdGtechModule

        @classmethod
        def setUpClass(cls):
            """
            Setup KosmosGtechKeyMatrixEmulator class
            """
            super().setUpClass()

            cls.VERBOSE = VERBOSE  # Set KosmosCommonTestCase.VERBOSE mode
        # end def setUpClass

        @classmethod
        def _get_module_under_test(cls):
            """
            Return the module instance to be tested.
            Override `AbstractTestClass.ModuleInterfaceTestCase._get_module_under_test()`.

            :return: The module instance to be tested.
            :rtype: ``KbdGtechModule``
            """
            return cls.kosmos.dt.kbd_gtech
        # end def _get_module_under_test

        def setUp(self):
            """
            Setup test
            """
            super().setUp()
            self.power_on()
        # end def setUp

        def tearDown(self):
            """
            TearDown test
            """
            self.power_off()
            super().tearDown()
        # end def tearDown

        @classmethod
        def power_on(cls):
            """
            Power ON the keyboard.
            """
            cls.set_usb_port(port_index=GALVATRON_USB_HUB_PORT_INDEX, status=UsbHubAction.ON,
                             delay=GALVATRON_BOOT_UP_DURATION_S)
        # end def power_on

        @classmethod
        def power_off(cls):
            """
            Power OFF the keyboard.
            """
            cls.set_usb_port(port_index=GALVATRON_USB_HUB_PORT_INDEX, status=UsbHubAction.OFF)
        # end def power_off
    # end class BaseTestCase
# end class KbdGtechModuleAbstractTestCase


class LegacyKbdGtechModuleTestCase(KbdGtechModuleAbstractTestCase.BaseTestCase):
    """
    Kosmos KBD Gtech Module Test Class related to KBD functional mode: Legacy
    (Key Press & Key Release ony).
    """
    pass
# end class LegacyKbdGtechModuleTestCase


class AnalogKbdGtechModuleTestCase(KbdGtechModuleAbstractTestCase.BaseTestCase):
    """
    Kosmos KBD Gtech Module Test Class related to KBD functional mode: Analog
    (Key Release: displacement level 0 / Key Press displacement level 40)
    """

    def setUp(self):
        """
        Setup test
        """
        super().setUp()

        # Change KBD Functional Mode from Legacy to Analog
        self.module.func_mode_analog()
    # end def setUp

# end class AnalogKbdGtechModuleTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
