#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.bas_test
:brief: Kosmos BAS Module Test Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyraspi.services.kosmos.module.bas import BasModule
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.test.module_test import AbstractTestClass
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
@require_kosmos_device(DeviceName.BAS)
class BasModuleTestCase(AbstractTestClass.UploadModuleInterfaceTestCase):
    """
    Kosmos BAS Module Test Class
    """

    @classmethod
    def _get_module_under_test(cls):
        """
        Return the module instance to be tested.
        Override `AbstractTestClass.ModuleInterfaceTestCase._get_module_under_test()`.

        :return: The module instance to be tested.
        :rtype: ``BasModule``
        """
        return cls.kosmos.dt.bas
    # end def _get_module_under_test
# end class BasModuleTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
