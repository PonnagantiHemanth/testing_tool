#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: codegenerator.validator.engine
:brief: Validator engine
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2021/07/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# import
# ----------------------------------------------------------------------------------------------------------------------
import sys


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SizeValidator(object):
    """
    Validate the size of the generated field
    """

    @classmethod
    def validate_negative_padding_size(cls, size, name):
        """
        Validate if the size is negative

        :param size: Size
        :type size: ``int``
        :param name: Message
        :type name: ``str``

        :raise ``ValueError``: Check and raise if the size is negative
        """
        if size < 0:
            raise ValueError(f"Invalid structure for ({name}). The total size exceeds by ({abs(size)} bits)")
        # end if
    # end def validate_negative_padding_size
# end class SizeValidator


class FileValidator(object):
    """
    Validate the file operation
    """

    @staticmethod
    def write_file(file_name, data):
        """
        Write operation on a file

        :param file_name: Name of the file
        :type file_name: ``str``
        :param data: Data to write
        :type data: ``list[str]``

        :return: Flag indicating if the write operation is successful
        :rtype: ``bool``
        """
        with open(file_name, "w", encoding='utf-8') as writer:
            for line in data:
                try:
                    writer.write(line)
                except Exception as e:
                    sys.stdout.write(f"\nFile write failed with error: {type(e).__name__}: {e}")
                    msg = "\tOption 1: Re-run the program by skip test case (-t or --testcase)" \
                          "\n\tOption 2: Fix the line which contains some unicode chars:"
                    if "UnicodeEncodeError" in type(e).__name__:
                        msg += "\n\t\t- Example 1: Find and replace (→ symbol) with (-> text)."
                    elif "SyntaxError: (unicode error)" in type(e).__name__:
                        # SyntaxError: (unicode error) 'utf-8' codec can't decode byte 0x92
                        # SyntaxError: (unicode error) 'utf-8' codec can't decode byte 0xa6
                        msg += "\n\t\t- Example 1: Find and replace (right single quotation mark) with (' text)." \
                               "\n\t\t- Example 2: Find and replace (¦ symbol) with (|)."
                    # end if
                    sys.stdout.write(f"\n{msg}\n{line}\n")
                    return False
                # end try
            # end for
        # end with
        return True
    # end def write_file
# end class FileValidator
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
