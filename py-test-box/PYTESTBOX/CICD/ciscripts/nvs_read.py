# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylink.jlink import JLink
from pylink.library import Library
from pylink.errors import JLinkException
from intelhex import IntelHex
from sys import argv
from sys import platform
import subprocess


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
# SEGGER Identifier
SEGGER_VENDOR_ID = 0x1366

# name of the file where the raw nvs data is to be placed
output_filename = 'nvs_raspberry_PI_x.hex'
nvs_uicr_filename = 'nvs_uicr_raspberry_PI_x.hex'


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
def get_platform_configuration(target_platform):
    """
    Platform configuration extracted from mem_map_cfg.h

    :param target_platform: Target platform name
    :type target_platform: ``str``
    """
    # chip to which the adapter is connected
    chip_name = ''
    # total flash size of the chip
    device_flash_size = 0
    # size of the nvs section of the chip
    nvs_size = 0
    # flash base address
    device_flash_base = 0

    if target_platform == 'QUARK256':
        chip_name = 'NRF52832_XXAB'
        device_flash_size = 256 * 1024
        nvs_size = 8 * 1024
    elif target_platform == 'QUARK':
        chip_name = 'NRF52832_XXAA'
        device_flash_size = 512 * 1024
        nvs_size = 8 * 1024
    elif target_platform == 'QUARK_GAMING':
        chip_name = 'NRF52832_XXAA'
        device_flash_size = 512 * 1024
        nvs_size = 40 * 1024
    elif target_platform == 'GLUON':
        chip_name = 'NRF52810_XXAA'
        device_flash_size = 192 * 1024
        nvs_size = 8 * 1024
    elif target_platform == 'GRAVITON':
        chip_name = 'NRF52840_XXAA'
        device_flash_size = 1024 * 1024
        nvs_size = 24 * 1024
    elif target_platform == 'HADRON':
        chip_name = 'NRF52833_XXAA'
        device_flash_size = 512 * 1024
        nvs_size = 24 * 1024
    elif target_platform == 'HADRON_GAMING':
        chip_name = 'NRF52833_XXAA'
        device_flash_size = 512 * 1024
        nvs_size = 40 * 1024
    elif target_platform == 'HADRON_GAMING_64K':
        chip_name = 'NRF52833_XXAA'
        device_flash_size = 512 * 1024
        nvs_size = 64 * 1024
    elif target_platform == 'MESON':
        chip_name = 'NRF52820_XXAA'
        device_flash_size = 256 * 1024
        nvs_size = 16 * 1024
    elif target_platform == 'STM32H7B0IB':
        chip_name = 'STM32H7B0IB'
        device_flash_size = 128 * 1024
        nvs_size = 16 * 1024
        device_flash_base = 0x08000000
    else:
        raise ValueError(f"Unknown target platform {target_platform}")
    # end if

    return chip_name, device_flash_size, nvs_size, device_flash_base
# end def get_platform_configuration


def get_serial_no():
    """
    Try to guess a possible J-Link match using SEGGER Vendor Id
    """
    if platform == 'linux':
        segger_vid = '%x' % SEGGER_VENDOR_ID
        # lsusb -v -d 1366: | grep -oP 'iSerial +[0-9] \K[0-9]+'
        # run() returns a CompletedProcess object if it was successful
        # errors in the created process are raised here too
        completed_process = subprocess.run(f'lsusb -v -d {segger_vid}: | grep -oP "iSerial +[0-9] \K[0-9]+"',
                                           shell=True, check=True, stdout=subprocess.PIPE,
                                           universal_newlines=True)
        assert (completed_process.returncode == 0)
        number_list = completed_process.stdout.rstrip().split('\n')
        if len(number_list) == 1:
            serial_no = int(number_list[0])
        else:
            raise ValueError('Unable to determine the J-Link serial number, got: %s' % str(completed_process.stdout))
        # end if
    else:
        serial_no = None
    # end if
    return serial_no
# end def get_serial_no


dllpath = '/opt/SEGGER/JLink/libjlinkarm.so'
lib = Library(dllpath=dllpath)
jlink = JLink(lib)
assert (jlink.version >= '7.88')
# j-link adapter serial number
serial_number = None
if len(argv) >= 3:
    serial_number = argv[2]
else:
    serial_number = get_serial_no()
if serial_number is not None:
    jlink.open(serial_number)
else:
    jlink.open()
    serial_number = jlink.serial_number
print(jlink.product_name)
print('Open J-Link DLL: %r' % jlink.opened())
print('Open J-Link connection: %r' % jlink.connected())
# noinspection PyProtectedMember
res = jlink._dll.JLINKARM_TIF_Select(1)
assert(res == 0)
jlink._tif = 1

if len(argv) >= 2:
    platform_name = argv[1]
else:
    platform_name = 'QUARK256'
    print('usage: python nvs_read.py <platform_name>/n supported platform_name are GLUON or QUARK256')
# end if
# Retrieve platform constants
platform_config = get_platform_configuration(platform_name)
(platform_chip_name, platform_device_flash_size, platform_nvs_size, platform_device_flash_base) = platform_config
try:
    jlink.connect(platform_chip_name)
except JLinkException:
    print("device is secured, can't read the nvs data, aborting... ")
    exit(1)
# end try

print(f"Connection to JLink with serial {serial_number} {'successful' if jlink.target_connected() else 'failed'}")

nvs_address_base = platform_device_flash_base + platform_device_flash_size - platform_nvs_size
nvs_data = jlink.memory_read(nvs_address_base, platform_nvs_size)
nvs_addresses = range(nvs_address_base, nvs_address_base + platform_nvs_size)
hexdata = dict(zip(nvs_addresses, nvs_data))
outhex = IntelHex(hexdata)
outhex.tofile(output_filename, 'hex')

if platform_chip_name.startswith("NRF52"):
    uicr_aes_key_address_base = 0x100010A0
    uicr_aes_key_size = 0x10
    uicr_data = jlink.memory_read(uicr_aes_key_address_base, uicr_aes_key_size)
    uicr_addresses = range(uicr_aes_key_address_base, uicr_aes_key_address_base + uicr_aes_key_size)
    hex_uicr_data = dict(zip(uicr_addresses, uicr_data))
    outhex.fromdict(hex_uicr_data)
    outhex.tofile(nvs_uicr_filename, 'hex')
# end if
