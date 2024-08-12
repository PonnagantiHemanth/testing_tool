#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.securitychunks
:brief: Security oriented NVS chunks definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/07/23
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pylibrary.tools.docutils import DocUtils
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class DfuCtrlChunk(BitFieldContainerMixin):
    """
    Define the format of the NVS_DFU_ID chunk

    {
        bool enable;
        uint8_t param; /* project-specific */
    } dctrl_dfuCtrl_ts;
    """

    class LEN:
        """
        Field Lengths in bits
        """
        ENABLE = 0x08
        PARAM = 0x08
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        ENABLE = 0xFF
        PARAM = 0xFE
    # end class FID

    class STATE:
        """
        enable bit 0 interpretation
        """
        DFU_DISABLED = 0
        DFU_ENABLED = 1
    # end class STATE

    FIELDS = (
        BitField(
            fid=FID.ENABLE,
            length=LEN.ENABLE,
            title='Enable',
            name='enable',
            checks=(CheckHexList(LEN.ENABLE // 8), CheckByte(),), ),
        BitField(
            fid=FID.PARAM,
            length=LEN.PARAM,
            title='Param',
            name='param',
            checks=(CheckHexList(LEN.PARAM // 8), CheckByte(),), ),
    )

    def __init__(self, enable, param, ref=None, **kwargs):
        """
        :param enable: Flag enabling the enter into dfu mechanism
        :type enable: ``int or HexList``
        :param param: project-specific parameter
        :type param: ``int or HexList``
        :param ref: Chunk object provided by the NvsParser
        :type ref: ``NvsChunk``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.ref = ref
        self.enable = enable
        self.param = param
    # end def __init__
# end class DfuCtrlChunk


class DfuCheckFwInfoChunk(BitFieldContainerMixin):
    """
    Define the format of the NVS_DFU_CHECK_ID chunk

    {
        uint16_t fwBuild; /* Used to store fwn_BUILD */
        uint16_t reserved;
    } dfuchk_fwInfo_ts
    """

    class LEN:
        """
        Field Lengths in bits
        """
        FW_BUILD = 0x10
        RESERVED = 0x10
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        FW_BUILD = 0xFF
        RESERVED = FW_BUILD - 1
    # end class FID

    class DEFAULT(object):
        """
        Fields Default values
        """
        RESERVED = HexList('0000')
    # end class DEFAULT

    FIELDS = (
        BitField(
            fid=FID.FW_BUILD,
            length=LEN.FW_BUILD,
            title='FW Build (little endian)',
            name='little_endian_fw_build',
            checks=(CheckHexList(LEN.FW_BUILD // 8), ), ),
        BitField(
            fid=FID.RESERVED,
            length=LEN.RESERVED,
            title='Reserved',
            name='reserved',
            checks=(CheckHexList(LEN.RESERVED // 8), ),
            default_value=DEFAULT.RESERVED),
    )

    def __init__(self, fw_build, ref=None, **kwargs):
        """
        :param fw_build: FW build number of the application that stored this chunk (stored in little endian)
        :type fw_build: ``HexList``
        :param ref: Chunk object provided by the NvsParser
        :type ref: ``NvsChunk``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.ref = ref
        self.fw_build = fw_build
    # end def __init__

    @property
    def fw_build(self):
        """
        Convert to big endian

        :return: FW Build value in big endian
        :rtype: ``HexList``
        """
        return self.little_endian_fw_build[::-1]
    # end getter def fw_build

    @fw_build.setter
    def fw_build(self, value):
        """
        Convert value to little endian

        :param value: FW Build value in big endian
        :type value: ``HexList``
        """
        self.little_endian_fw_build = value[::-1]
    # end setter def fw_build

# end class DfuCheckFwInfoChunk


class TdeDeactivationChunk(BitFieldContainerMixin):
    """
    Define the format of the Device Tde Deactivation chunk
    """
    class LEN:
        """
        Field Lengths in bits
        """
        # version 1 is 3 bytes long
        TDE_DEACTIVATION_DATA_V1 = 0x18
        # version 2 is 1 byte long
        TDE_DEACTIVATION_DATA_V2 = 0x08
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        TDE_DEACTIVATION_DATA = 0xFF
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.TDE_DEACTIVATION_DATA,
            length=LEN.TDE_DEACTIVATION_DATA_V1,
            title='Data',
            name='data',
            checks=(CheckHexList(max_length=(LEN.TDE_DEACTIVATION_DATA_V1 // 8),
                                 min_length=(LEN.TDE_DEACTIVATION_DATA_V2 // 8), ),)),
    )

    @classmethod
    @DocUtils.copy_doc(BitFieldContainerMixin.fromHexList)
    def fromHexList(cls, *args, **kwargs):
        """
        See ``BitFieldContainerMixin.fromHexList``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        if len(inner_field_container_mixin.data) == (cls.LEN.TDE_DEACTIVATION_DATA_V1 // 8):
            return TdeDeactivationChunkV1.fromHexList(inner_field_container_mixin.data)
        elif len(inner_field_container_mixin.data) == (cls.LEN.TDE_DEACTIVATION_DATA_V2 // 8):
            return TdeDeactivationChunkV2.fromHexList(inner_field_container_mixin.data)
        else:
            raise ValueError("Unknown Device TDE Deactivation chunk structure")
        # end if
    # end def fromHexList
# end class TdeDeactivationChunk


class TdeDeactivationChunkV1(BitFieldContainerMixin):
    """
    Define the format of the NVS_XEE_DEACT_CNTR_ID  chunk

    {
        uint8_t ; /* Disable manufacturing registers counter*/
        uint8_t ; /* Disable compliance registers counter */
        uint8_t ; /* Disable Gothard counter */
    } ;
    """

    class LEN:
        """
        Field Lengths in bits
        """
        DISABLE_MANUFACTURING_REGISTERS_COUNTER = 0x08
        DISABLE_COMPLIANCE_REGISTERS_COUNTER = 0x08
        DISABLE_GOTHARD_COUNTER = 0x08
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        DISABLE_MANUFACTURING_REGISTERS_COUNTER = 0xFF
        DISABLE_COMPLIANCE_REGISTERS_COUNTER = 0xFE
        DISABLE_GOTHARD_COUNTER = 0xFD
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.DISABLE_MANUFACTURING_REGISTERS_COUNTER,
            length=LEN.DISABLE_MANUFACTURING_REGISTERS_COUNTER,
            title='DisableManufacturingRegistersCounter',
            name='disable_manufacturing_registers_counter',
            checks=(CheckHexList(LEN.DISABLE_MANUFACTURING_REGISTERS_COUNTER // 8), CheckByte(),), ),
        BitField(
            fid=FID.DISABLE_COMPLIANCE_REGISTERS_COUNTER,
            length=LEN.DISABLE_COMPLIANCE_REGISTERS_COUNTER,
            title='DisableComplianceRegistersCounter',
            name='disable_compliance_registers_counter',
            checks=(CheckHexList(LEN.DISABLE_COMPLIANCE_REGISTERS_COUNTER // 8), CheckByte(),), ),
        BitField(
            fid=FID.DISABLE_GOTHARD_COUNTER,
            length=LEN.DISABLE_GOTHARD_COUNTER,
            title='DisableGothardCounter',
            name='disable_gothard_counter',
            checks=(CheckHexList(LEN.DISABLE_GOTHARD_COUNTER // 8), CheckByte(),), ),
    )

    def __init__(self, disable_manufacturing_registers_counter=0, disable_compliance_registers_counter=0,
                 disable_gothard_counter=0, ref=None, **kwargs):
        """
        :param disable_manufacturing_registers_counter: When the counter reaches 0, manufacturing registers are
                                                        disabled on the device
        :type disable_manufacturing_registers_counter: ``int or HexList``
        :param disable_compliance_registers_counter: When the counter reaches 0, compliance registers are disabled
                                                     on the device.
        :type disable_compliance_registers_counter: ``int or HexList``
        :param disable_gothard_counter: Not used
        :type disable_gothard_counter: ``int or HexList``
        :param ref: Chunk object provided by the NvsParser
        :type ref: ``NvsChunk``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.ref = ref
        self.disable_manufacturing_registers_counter = disable_manufacturing_registers_counter
        self.disable_compliance_registers_counter = disable_compliance_registers_counter
        self.disable_gothard_counter = disable_gothard_counter
    # end def __init__
# end class DfuCtrlChunk


class TdeDeactivationChunkV2(BitFieldContainerMixin):
    """
    Define the format of the NVS_X1E02_STATE_ID chunk

    {
        uint8_t stateBitMap;
    }
    """
    class LEN:
        """
        Field Lengths in bits
        """
        STATE_BIT_MAP = 0x08

    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        STATE_BIT_MAP = 0xFF
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.STATE_BIT_MAP,
            length=LEN.STATE_BIT_MAP,
            title='StateBitMap',
            name='state_bit_map',
            checks=(CheckHexList(LEN.STATE_BIT_MAP // 8), CheckByte(),), ),
    )
# end class TdeDeactivationChunkV2


class DfuRecoveryChunk(BitFieldContainerMixin):
    """
    Define the format of the NVS_DFU_OUT_OF_RECOVERY_ID chunk

    {
        uint8_t version;
    } nvsChunkVersion0_ts;
    """

    class LEN:
        """
        Field Lengths in bits
        """
        VERSION = 0x08
    # end class LEN

    class FID:
        """
        Field Identifiers
        """
        VERSION = 0xFF
    # end class FID

    FIELDS = (
        BitField(
            fid=FID.VERSION,
            length=LEN.VERSION,
            title='Version',
            name='version',
            checks=(CheckHexList(LEN.VERSION // 8), CheckByte(),), ),
    )

    def __init__(self, version, ref=None, **kwargs):
        """
        The chunk is written in NVS when a DFU starts in recovery mode.

        :param version: unused (for future extension/reuse of this chunk ID)
        :type version: ``int or HexList``
        :param ref: Chunk object provided by the NvsParser
        :type ref: ``NvsChunk``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        # Parameters initialization
        self.ref = ref
        self.version = version
    # end def __init__
# end class DfuRecoveryChunk


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
