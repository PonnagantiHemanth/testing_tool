Table of content
================

 * RGB Test module content

RGB Test module content
=======================

The module includes the functionality to create hybrid Python/C objects from the
rgb_algorithms functions (Gamma calculation, Basic Effects generation , Drift corrections (effects sync),
RGB <-> HSV Conversions) , callable from any python script. It is used for the validation
of the rgb effect through the interface rgbalgoc.py

Configuration File:
The configuration file needed for rgb_algorithms module is rgb_algorithms_cfg.h. It depends on the DUT.
If this file is different from the original rgb_algorithms_cfg.h file presents in the directory, the
pythonCTestFunctions.so must be rebuild using the Makefile in the directory.

Note : Need to install python3-dev on the raspberry Pi to build the library



