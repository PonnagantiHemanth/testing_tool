#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.pio
:brief: Kosmos PIO Module Class
:author: Alexandre Lafaye <alafaye@logitech.com>
:date: 2022/10/26
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyraspi.services.kosmos.module.module import ModuleBaseClass
from pyraspi.services.kosmos.module.module import ModuleSettings
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PIO
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_PIO_READ

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
PIO_COUNT = 16


class PioModule(ModuleBaseClass):
    """
    Kosmos PIO module class.
    """

    def __init__(self):
        """
        :raise ``AssertionError``: unexpected argument type
        """

        module_settings = ModuleSettings(
            name=r'PIO',
            instance_id=None,  # Module is a singleton
            optional=False,
            msg_id=MSG_ID_PIO,
        )
        assert isinstance(module_settings, ModuleSettings), module_settings
        super().__init__(module_settings=module_settings)
    # end def __init__

    def read_all(self):
        """
        Read the current PIO pins state

        :return: A list containing all the pio states
        :rtype: ``list[int]``
        """

        # Send datagram and get reply
        payload = self.dt.fpga_transport.send_control_message(MSG_ID_PIO, MSG_ID_PIO_READ)
        pin_list = [int(digit) for digit in bin(payload)[2:]]
        # Reverse the list and pad with 0 to have intuitive list access to pin numbers
        pin_list.reverse()
        pin_list += [0] * (PIO_COUNT - len(pin_list))
        return pin_list
    # end def read_all

    def read_pio(self, pio_number):
        """
        Read a specific PIO pin state

        :param pio_number: Number of the pio to read (from 0 to 15)
        :type pio_number: ``int``

        :return: pio state
        :rtype: ``int``
        """
        return self.read_all()[pio_number]
    # end def read_pio
# end class PioModule

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
