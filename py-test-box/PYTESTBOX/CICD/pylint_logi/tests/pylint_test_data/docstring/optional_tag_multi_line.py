#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: optional_tag_multi_line
:brief: sample file where the optional tag is at multiple position on the param brief
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/07/04
"""


def first_line(param=False):
    """
    test function

    :param param: first line of the docstring - OPTIONAL
                  and some more text
                  and a final line
    :type param: ``bool``
    """
    pass
# end def first_line


def second_line(param=False):
    """
    test function

    :param param: first line of the docstring
                  and some more text - OPTIONAL
                  and a final line
    :type param: ``bool``
    """
    pass
# end def second_line

def third_line(param=False):
    """
    test function

    :param param: first line of the docstring
                  and some more text
                  and a final line - OPTIONAL
    :type param: ``bool``
    """
    pass
# end def third_line
