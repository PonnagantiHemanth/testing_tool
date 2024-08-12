#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.utils
:brief: define the usage of the hub ports
:author: Zane Lu
:date: 2021/2/3
"""


class PortConfiguration:
    """
    The configuration of the usb hub ports
    """
    USB_PID_CRUSH = 0xC53A
    USB_PID_MOLDUCK = 0xC547
    USB_PID_SAVITAK = 0xC54D

    PRE_PAIRED_RECEIVER_PORT = 1
    CRUSH_RECEIVER_PORT = 2
    LS2_RECEIVER_PORT = 3
    LS2_RECEIVER2_PORT = 4
    CRUSH_RECEIVER2_PORT = 7
    NUM_OF_RECEIVERS = 5
    PORT_ARRANGEMENT = [
        PRE_PAIRED_RECEIVER_PORT, CRUSH_RECEIVER_PORT, LS2_RECEIVER_PORT, LS2_RECEIVER2_PORT, CRUSH_RECEIVER2_PORT]

    CABLE_CONNECTED_PORT = 5
# end class PortConfiguration


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
