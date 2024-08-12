#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.devicereset

@brief  HID++ 2.0 Device Reset command interface definition

@author christophe.roquebert

@date   2019/03/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceReset(HidppMessage):
    """
    DeviceReset implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0x1802
    MAX_FUNCTION_INDEX = 0

    def __init__(self, deviceIndex, featureIndex):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureIndex           [in] (int)  feature Index
        """
        super(DeviceReset, self).__init__()

        self.deviceIndex = deviceIndex
        self.featureIndex = featureIndex
    # end def __init__
# end class DeviceReset


class ForceDeviceReset(DeviceReset):
    """
    DeviceReset ForceDeviceReset implementation class

    Request the type & description of supported roller.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """
    FUNCTION_INDEX = 0

    class FID(DeviceReset.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(DeviceReset.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = DeviceReset.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=DeviceReset.DEFAULT.PADDING),
    )

    def __init__(self, deviceIndex,
                 featureId):
        """
        Constructor

        @param  deviceIndex            [in] (int)  Device Index
        @param  featureId              [in] (int)  desired feature Id
        """
        super(ForceDeviceReset, self).__init__(deviceIndex, featureId)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class ForceDeviceReset

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
