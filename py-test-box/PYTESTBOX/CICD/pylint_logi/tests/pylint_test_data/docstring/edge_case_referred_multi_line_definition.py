#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: edge_case_referred_multi_line_definition
:brief: Sample file with refered multi line definition
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/07/09
"""


class BaseClass:
    """
    Stub reference base class to fulfill the parent need of the following class
    Note if the presence of the method is required, it would need to be more than a stub
    """
    pass
# end class BaseClass


class TestReferencedClass(BaseClass):
    """
    Class referencing docstring with multi line definition
    """
    def two_lines(self,
                  and_a_very_long_character_that_requires_a_new_line):
        # See ``BaseClass.two_lines``

        # and this comment need to be ignored
        pass
    # end def two_lines

    def three_lines(self,
                     and_a_very_long_character_that_requires_a_new_line,
                     and_another_very_long_character_that_requires_a_new_line):
        # See ``BaseClass.three_lines``

        # and this comment need to be ignored
        pass
    # end def three_lines
# end class TestReferencedClass
