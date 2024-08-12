#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
@package pyhid.hidparser.usagepages.mediacenter

@brief  HID parser usage pages media center class
        Built from https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf

@author christophe Roquebert

@date   2019/01/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidparser.UsagePage import Usage, UsageType, UsagePage

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class MediaCenter(UsagePage):
    @classmethod
    def _get_usage_page_index(cls):
        return 0xffbc
    # end def _get_usage_page_index

    # media center category usages
    RESERVED_01 = Usage(0x01, UsageType.DATA_SELECTOR)
    RESERVED_02 = Usage(0x02, UsageType.DATA_SELECTOR)
    RESERVED_03 = Usage(0x03, UsageType.DATA_SELECTOR)
    RESERVED_04 = Usage(0x04, UsageType.DATA_SELECTOR)
    RESERVED_05 = Usage(0x05, UsageType.DATA_SELECTOR)
    RESERVED_06 = Usage(0x06, UsageType.DATA_SELECTOR)
    RESERVED_07 = Usage(0x07, UsageType.DATA_SELECTOR)
    RESERVED_08 = Usage(0x08, UsageType.DATA_SELECTOR)
    RESERVED_09 = Usage(0x09, UsageType.DATA_SELECTOR)
    RESERVED_0A = Usage(0x0A, UsageType.DATA_SELECTOR)
    RESERVED_0B = Usage(0x0B, UsageType.DATA_SELECTOR)
    RESERVED_0C = Usage(0x0C, UsageType.DATA_SELECTOR)
    RESERVED_0D = Usage(0x0D, UsageType.DATA_SELECTOR)
    RESERVED_0E = Usage(0x0E, UsageType.DATA_SELECTOR)
    RESERVED_0F = Usage(0x0F, UsageType.DATA_SELECTOR)
    RESERVED_10 = Usage(0x10, UsageType.DATA_SELECTOR)
    RESERVED_11 = Usage(0x11, UsageType.DATA_SELECTOR)
    RESERVED_12 = Usage(0x12, UsageType.DATA_SELECTOR)
    RESERVED_13 = Usage(0x13, UsageType.DATA_SELECTOR)
    RESERVED_14 = Usage(0x14, UsageType.DATA_SELECTOR)
    RESERVED_15 = Usage(0x15, UsageType.DATA_SELECTOR)
    RESERVED_16 = Usage(0x16, UsageType.DATA_SELECTOR)
    RESERVED_17 = Usage(0x17, UsageType.DATA_SELECTOR)
    RESERVED_18 = Usage(0x18, UsageType.DATA_SELECTOR)
    RESERVED_19 = Usage(0x19, UsageType.DATA_SELECTOR)
    RESERVED_1A = Usage(0x1A, UsageType.DATA_SELECTOR)
    RESERVED_1B = Usage(0x1B, UsageType.DATA_SELECTOR)
    RESERVED_1C = Usage(0x1C, UsageType.DATA_SELECTOR)
    RESERVED_1D = Usage(0x1D, UsageType.DATA_SELECTOR)
    RESERVED_1E = Usage(0x1E, UsageType.DATA_SELECTOR)
    RESERVED_1F = Usage(0x1F, UsageType.DATA_SELECTOR)
    RESERVED_20 = Usage(0x20, UsageType.DATA_SELECTOR)
    RESERVED_21 = Usage(0x21, UsageType.DATA_SELECTOR)
    RESERVED_22 = Usage(0x22, UsageType.DATA_SELECTOR)
    RESERVED_23 = Usage(0x23, UsageType.DATA_SELECTOR)
    DVD_MENU = Usage(0x24, UsageType.DATA_SELECTOR)
    TV_JUMP = Usage(0x25, UsageType.DATA_SELECTOR)
    RESERVED_26 = Usage(0x26, UsageType.DATA_SELECTOR)
    RESERVED_27 = Usage(0x27, UsageType.DATA_SELECTOR)
    RESERVED_28 = Usage(0x28, UsageType.DATA_SELECTOR)
    RESERVED_29 = Usage(0x29, UsageType.DATA_SELECTOR)
    RESERVED_2A = Usage(0x2A, UsageType.DATA_SELECTOR)
    RESERVED_2B = Usage(0x2B, UsageType.DATA_SELECTOR)
    RESERVED_2C = Usage(0x2C, UsageType.DATA_SELECTOR)
    RESERVED_2D = Usage(0x2D, UsageType.DATA_SELECTOR)
    RESERVED_2E = Usage(0x2E, UsageType.DATA_SELECTOR)
    RESERVED_2F = Usage(0x2F, UsageType.DATA_SELECTOR)
    RESERVED_30 = Usage(0x30, UsageType.DATA_SELECTOR)
    RESERVED_31 = Usage(0x31, UsageType.DATA_SELECTOR)
    RESERVED_32 = Usage(0x32, UsageType.DATA_SELECTOR)
    RESERVED_33 = Usage(0x33, UsageType.DATA_SELECTOR)
    RESERVED_34 = Usage(0x34, UsageType.DATA_SELECTOR)
    RESERVED_35 = Usage(0x35, UsageType.DATA_SELECTOR)
    RESERVED_36 = Usage(0x36, UsageType.DATA_SELECTOR)
    RESERVED_37 = Usage(0x37, UsageType.DATA_SELECTOR)
    RESERVED_38 = Usage(0x38, UsageType.DATA_SELECTOR)
    RESERVED_39 = Usage(0x39, UsageType.DATA_SELECTOR)
    RESERVED_3A = Usage(0x3A, UsageType.DATA_SELECTOR)
    RESERVED_3B = Usage(0x3B, UsageType.DATA_SELECTOR)
    RESERVED_3C = Usage(0x3C, UsageType.DATA_SELECTOR)
    RESERVED_3D = Usage(0x3D, UsageType.DATA_SELECTOR)
    RESERVED_3E = Usage(0x3E, UsageType.DATA_SELECTOR)
    RESERVED_3F = Usage(0x3F, UsageType.DATA_SELECTOR)
    RESERVED_40 = Usage(0x40, UsageType.DATA_SELECTOR)
    RESERVED_41 = Usage(0x41, UsageType.DATA_SELECTOR)
    RESERVED_42 = Usage(0x42, UsageType.DATA_SELECTOR)
    RESERVED_43 = Usage(0x43, UsageType.DATA_SELECTOR)
    RESERVED_44 = Usage(0x44, UsageType.DATA_SELECTOR)
    RESERVED_45 = Usage(0x45, UsageType.DATA_SELECTOR)
    RESERVED_46 = Usage(0x46, UsageType.DATA_SELECTOR)
    RESERVED_47 = Usage(0x47, UsageType.DATA_SELECTOR)
    RESERVED_48 = Usage(0x48, UsageType.DATA_SELECTOR)
    RESERVED_49 = Usage(0x49, UsageType.DATA_SELECTOR)
    RESERVED_4A = Usage(0x4A, UsageType.DATA_SELECTOR)
    RESERVED_4B = Usage(0x4B, UsageType.DATA_SELECTOR)
    RESERVED_4C = Usage(0x4C, UsageType.DATA_SELECTOR)
    RESERVED_4D = Usage(0x4D, UsageType.DATA_SELECTOR)
    RESERVED_4E = Usage(0x4E, UsageType.DATA_SELECTOR)
    RESERVED_4F = Usage(0x4F, UsageType.DATA_SELECTOR)
    RESERVED_50 = Usage(0x50, UsageType.DATA_SELECTOR)
    RESERVED_51 = Usage(0x51, UsageType.DATA_SELECTOR)
    RESERVED_52 = Usage(0x52, UsageType.DATA_SELECTOR)
    RESERVED_53 = Usage(0x53, UsageType.DATA_SELECTOR)
    RESERVED_54 = Usage(0x54, UsageType.DATA_SELECTOR)
    RESERVED_55 = Usage(0x55, UsageType.DATA_SELECTOR)
    RESERVED_56 = Usage(0x56, UsageType.DATA_SELECTOR)
    RESERVED_57 = Usage(0x57, UsageType.DATA_SELECTOR)
    RESERVED_58 = Usage(0x58, UsageType.DATA_SELECTOR)
    RESERVED_59 = Usage(0x59, UsageType.DATA_SELECTOR)
    RESERVED_5A = Usage(0x5A, UsageType.DATA_SELECTOR)
    RESERVED_5B = Usage(0x5B, UsageType.DATA_SELECTOR)
    RESERVED_5C = Usage(0x5C, UsageType.DATA_SELECTOR)
    RESERVED_5D = Usage(0x5D, UsageType.DATA_SELECTOR)
    RESERVED_5E = Usage(0x5E, UsageType.DATA_SELECTOR)
    RESERVED_5F = Usage(0x5F, UsageType.DATA_SELECTOR)
    RESERVED_60 = Usage(0x60, UsageType.DATA_SELECTOR)
    RESERVED_61 = Usage(0x61, UsageType.DATA_SELECTOR)
    RESERVED_62 = Usage(0x62, UsageType.DATA_SELECTOR)
    RESERVED_63 = Usage(0x63, UsageType.DATA_SELECTOR)
    RESERVED_64 = Usage(0x64, UsageType.DATA_SELECTOR)
    RESERVED_65 = Usage(0x65, UsageType.DATA_SELECTOR)
    RESERVED_66 = Usage(0x66, UsageType.DATA_SELECTOR)
    RESERVED_67 = Usage(0x67, UsageType.DATA_SELECTOR)
    RESERVED_68 = Usage(0x68, UsageType.DATA_SELECTOR)
    RESERVED_69 = Usage(0x69, UsageType.DATA_SELECTOR)
    RESERVED_6A = Usage(0x6A, UsageType.DATA_SELECTOR)
    RESERVED_6B = Usage(0x6B, UsageType.DATA_SELECTOR)
    RESERVED_6C = Usage(0x6C, UsageType.DATA_SELECTOR)
    RESERVED_6D = Usage(0x6D, UsageType.DATA_SELECTOR)
    RESERVED_6E = Usage(0x6E, UsageType.DATA_SELECTOR)
    RESERVED_6F = Usage(0x6F, UsageType.DATA_SELECTOR)
    RESERVED_70 = Usage(0x70, UsageType.DATA_SELECTOR)
    RESERVED_71 = Usage(0x71, UsageType.DATA_SELECTOR)
    RESERVED_72 = Usage(0x72, UsageType.DATA_SELECTOR)
    RESERVED_73 = Usage(0x73, UsageType.DATA_SELECTOR)
    RESERVED_74 = Usage(0x74, UsageType.DATA_SELECTOR)
    RESERVED_75 = Usage(0x75, UsageType.DATA_SELECTOR)
    RESERVED_76 = Usage(0x76, UsageType.DATA_SELECTOR)
    RESERVED_77 = Usage(0x77, UsageType.DATA_SELECTOR)
    RESERVED_78 = Usage(0x78, UsageType.DATA_SELECTOR)
    RESERVED_79 = Usage(0x79, UsageType.DATA_SELECTOR)
    RESERVED_7A = Usage(0x7A, UsageType.DATA_SELECTOR)
    RESERVED_7B = Usage(0x7B, UsageType.DATA_SELECTOR)
    RESERVED_7C = Usage(0x7C, UsageType.DATA_SELECTOR)
    RESERVED_7D = Usage(0x7D, UsageType.DATA_SELECTOR)
    RESERVED_7E = Usage(0x7E, UsageType.DATA_SELECTOR)
    RESERVED_7F = Usage(0x7F, UsageType.DATA_SELECTOR)
    RESERVED_80 = Usage(0x80, UsageType.DATA_SELECTOR)
    RESERVED_81 = Usage(0x81, UsageType.DATA_SELECTOR)
    RESERVED_82 = Usage(0x82, UsageType.DATA_SELECTOR)
    RESERVED_83 = Usage(0x83, UsageType.DATA_SELECTOR)
    RESERVED_84 = Usage(0x84, UsageType.DATA_SELECTOR)
    RESERVED_85 = Usage(0x85, UsageType.DATA_SELECTOR)
    RESERVED_86 = Usage(0x86, UsageType.DATA_SELECTOR)
    RESERVED_87 = Usage(0x87, UsageType.DATA_SELECTOR)
    RESERVED_88 = Usage(0x88, UsageType.DATA_SELECTOR)
    RESERVED_89 = Usage(0x89, UsageType.DATA_SELECTOR)
    RESERVED_8A = Usage(0x8A, UsageType.DATA_SELECTOR)
    RESERVED_8B = Usage(0x8B, UsageType.DATA_SELECTOR)
    RESERVED_8C = Usage(0x8C, UsageType.DATA_SELECTOR)
    RESERVED_8D = Usage(0x8D, UsageType.DATA_SELECTOR)
    RESERVED_8E = Usage(0x8E, UsageType.DATA_SELECTOR)
    RESERVED_8F = Usage(0x8F, UsageType.DATA_SELECTOR)
    RESERVED_90 = Usage(0x90, UsageType.DATA_SELECTOR)
    RESERVED_91 = Usage(0x91, UsageType.DATA_SELECTOR)
    RESERVED_92 = Usage(0x92, UsageType.DATA_SELECTOR)
    RESERVED_93 = Usage(0x93, UsageType.DATA_SELECTOR)
    RESERVED_94 = Usage(0x94, UsageType.DATA_SELECTOR)
    RESERVED_95 = Usage(0x95, UsageType.DATA_SELECTOR)
    RESERVED_96 = Usage(0x96, UsageType.DATA_SELECTOR)
    RESERVED_97 = Usage(0x97, UsageType.DATA_SELECTOR)
    RESERVED_98 = Usage(0x98, UsageType.DATA_SELECTOR)
    RESERVED_99 = Usage(0x99, UsageType.DATA_SELECTOR)
    RESERVED_9A = Usage(0x9A, UsageType.DATA_SELECTOR)
    RESERVED_9B = Usage(0x9B, UsageType.DATA_SELECTOR)
    RESERVED_9C = Usage(0x9C, UsageType.DATA_SELECTOR)
    RESERVED_9D = Usage(0x9D, UsageType.DATA_SELECTOR)
    RESERVED_9E = Usage(0x9E, UsageType.DATA_SELECTOR)
    RESERVED_9F = Usage(0x9F, UsageType.DATA_SELECTOR)
    RESERVED_A0 = Usage(0xA0, UsageType.DATA_SELECTOR)
    RESERVED_A1 = Usage(0xA1, UsageType.DATA_SELECTOR)
    RESERVED_A2 = Usage(0xA2, UsageType.DATA_SELECTOR)
    RESERVED_A3 = Usage(0xA3, UsageType.DATA_SELECTOR)
    RESERVED_A4 = Usage(0xA4, UsageType.DATA_SELECTOR)
    RESERVED_A5 = Usage(0xA5, UsageType.DATA_SELECTOR)
    RESERVED_A6 = Usage(0xA6, UsageType.DATA_SELECTOR)
    RESERVED_A7 = Usage(0xA7, UsageType.DATA_SELECTOR)
    RESERVED_A8 = Usage(0xA8, UsageType.DATA_SELECTOR)
    RESERVED_A9 = Usage(0xA9, UsageType.DATA_SELECTOR)
    RESERVED_AA = Usage(0xAA, UsageType.DATA_SELECTOR)
    RESERVED_AB = Usage(0xAB, UsageType.DATA_SELECTOR)
    RESERVED_AC = Usage(0xAC, UsageType.DATA_SELECTOR)
    RESERVED_AD = Usage(0xAD, UsageType.DATA_SELECTOR)
    RESERVED_AE = Usage(0xAE, UsageType.DATA_SELECTOR)
    RESERVED_AF = Usage(0xAF, UsageType.DATA_SELECTOR)
    RESERVED_B0 = Usage(0xB0, UsageType.DATA_SELECTOR)
    RESERVED_B1 = Usage(0xB1, UsageType.DATA_SELECTOR)
    RESERVED_B2 = Usage(0xB2, UsageType.DATA_SELECTOR)
    RESERVED_B3 = Usage(0xB3, UsageType.DATA_SELECTOR)
    RESERVED_B4 = Usage(0xB4, UsageType.DATA_SELECTOR)
    RESERVED_B5 = Usage(0xB5, UsageType.DATA_SELECTOR)
    RESERVED_B6 = Usage(0xB6, UsageType.DATA_SELECTOR)
    RESERVED_B7 = Usage(0xB7, UsageType.DATA_SELECTOR)
    RESERVED_B8 = Usage(0xB8, UsageType.DATA_SELECTOR)
    RESERVED_B9 = Usage(0xB9, UsageType.DATA_SELECTOR)
    RESERVED_BA = Usage(0xBA, UsageType.DATA_SELECTOR)
    RESERVED_BB = Usage(0xBB, UsageType.DATA_SELECTOR)
    RESERVED_BC = Usage(0xBC, UsageType.DATA_SELECTOR)
    RESERVED_BD = Usage(0xBD, UsageType.DATA_SELECTOR)
    RESERVED_BE = Usage(0xBE, UsageType.DATA_SELECTOR)
    RESERVED_BF = Usage(0xBF, UsageType.DATA_SELECTOR)
    RESERVED_C0 = Usage(0xC0, UsageType.DATA_SELECTOR)
    RESERVED_C1 = Usage(0xC1, UsageType.DATA_SELECTOR)
    RESERVED_C2 = Usage(0xC2, UsageType.DATA_SELECTOR)
    RESERVED_C3 = Usage(0xC3, UsageType.DATA_SELECTOR)
    RESERVED_C4 = Usage(0xC4, UsageType.DATA_SELECTOR)
    RESERVED_C5 = Usage(0xC5, UsageType.DATA_SELECTOR)
    RESERVED_C6 = Usage(0xC6, UsageType.DATA_SELECTOR)
    RESERVED_C7 = Usage(0xC7, UsageType.DATA_SELECTOR)
    RESERVED_C8 = Usage(0xC8, UsageType.DATA_SELECTOR)
    RESERVED_C9 = Usage(0xC9, UsageType.DATA_SELECTOR)
    RESERVED_CA = Usage(0xCA, UsageType.DATA_SELECTOR)
    RESERVED_CB = Usage(0xCB, UsageType.DATA_SELECTOR)
    RESERVED_CC = Usage(0xCC, UsageType.DATA_SELECTOR)
    RESERVED_CD = Usage(0xCD, UsageType.DATA_SELECTOR)
    RESERVED_CE = Usage(0xCE, UsageType.DATA_SELECTOR)
    RESERVED_CF = Usage(0xCF, UsageType.DATA_SELECTOR)
    RESERVED_D0 = Usage(0xD0, UsageType.DATA_SELECTOR)
    RESERVED_D1 = Usage(0xD1, UsageType.DATA_SELECTOR)
    RESERVED_D2 = Usage(0xD2, UsageType.DATA_SELECTOR)
    RESERVED_D3 = Usage(0xD3, UsageType.DATA_SELECTOR)
    RESERVED_D4 = Usage(0xD4, UsageType.DATA_SELECTOR)
    RESERVED_D5 = Usage(0xD5, UsageType.DATA_SELECTOR)
    RESERVED_D6 = Usage(0xD6, UsageType.DATA_SELECTOR)
    RESERVED_D7 = Usage(0xD7, UsageType.DATA_SELECTOR)
    RESERVED_D8 = Usage(0xD8, UsageType.DATA_SELECTOR)
    RESERVED_D9 = Usage(0xD9, UsageType.DATA_SELECTOR)
    RESERVED_DA = Usage(0xDA, UsageType.DATA_SELECTOR)
    RESERVED_DB = Usage(0xDB, UsageType.DATA_SELECTOR)
    RESERVED_DC = Usage(0xDC, UsageType.DATA_SELECTOR)
    RESERVED_DD = Usage(0xDD, UsageType.DATA_SELECTOR)
    RESERVED_DE = Usage(0xDE, UsageType.DATA_SELECTOR)
    RESERVED_DF = Usage(0xDF, UsageType.DATA_SELECTOR)
    RESERVED_E0 = Usage(0xE0, UsageType.DATA_SELECTOR)
    RESERVED_E1 = Usage(0xE1, UsageType.DATA_SELECTOR)
    RESERVED_E2 = Usage(0xE2, UsageType.DATA_SELECTOR)
    RESERVED_E3 = Usage(0xE3, UsageType.DATA_SELECTOR)
    RESERVED_E4 = Usage(0xE4, UsageType.DATA_SELECTOR)
    RESERVED_E5 = Usage(0xE5, UsageType.DATA_SELECTOR)
    RESERVED_E6 = Usage(0xE6, UsageType.DATA_SELECTOR)
    RESERVED_E7 = Usage(0xE7, UsageType.DATA_SELECTOR)
    RESERVED_E8 = Usage(0xE8, UsageType.DATA_SELECTOR)
    RESERVED_E9 = Usage(0xE9, UsageType.DATA_SELECTOR)
    RESERVED_EA = Usage(0xEA, UsageType.DATA_SELECTOR)
    RESERVED_EB = Usage(0xEB, UsageType.DATA_SELECTOR)
    RESERVED_EC = Usage(0xEC, UsageType.DATA_SELECTOR)
    RESERVED_ED = Usage(0xED, UsageType.DATA_SELECTOR)
    RESERVED_EE = Usage(0xEE, UsageType.DATA_SELECTOR)
    RESERVED_EF = Usage(0xEF, UsageType.DATA_SELECTOR)
    RESERVED_F0 = Usage(0xF0, UsageType.DATA_SELECTOR)
    RESERVED_F1 = Usage(0xF1, UsageType.DATA_SELECTOR)
    RESERVED_F2 = Usage(0xF2, UsageType.DATA_SELECTOR)
    RESERVED_F3 = Usage(0xF3, UsageType.DATA_SELECTOR)
    RESERVED_F4 = Usage(0xF4, UsageType.DATA_SELECTOR)
    RESERVED_F5 = Usage(0xF5, UsageType.DATA_SELECTOR)
    RESERVED_F6 = Usage(0xF6, UsageType.DATA_SELECTOR)
    RESERVED_F7 = Usage(0xF7, UsageType.DATA_SELECTOR)
    RESERVED_F8 = Usage(0xF8, UsageType.DATA_SELECTOR)
    RESERVED_F9 = Usage(0xF9, UsageType.DATA_SELECTOR)
    RESERVED_FA = Usage(0xFA, UsageType.DATA_SELECTOR)
    RESERVED_FB = Usage(0xFB, UsageType.DATA_SELECTOR)
    RESERVED_FC = Usage(0xFC, UsageType.DATA_SELECTOR)
    RESERVED_FD = Usage(0xFD, UsageType.DATA_SELECTOR)
    RESERVED_FE = Usage(0xFE, UsageType.DATA_SELECTOR)
    RESERVED_FF = Usage(0xFF, UsageType.DATA_SELECTOR)
# end class MediaCenter
