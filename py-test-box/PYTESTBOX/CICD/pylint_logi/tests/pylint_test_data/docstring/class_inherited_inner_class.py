#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: class_inherited_inner_class
:brief: sample file where inner class refer a parent class
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/06/17
"""


class TestClassBase:
    """
    Doc string sample test class
    """

    class InnerClass:
        """
        Inner class
        """
        pass
    # end class InnerClass

    pass
# end class TestClassBase


class InheritedClass(TestClassBase):
    # See ``TestClassBase``

    class InnerClass:
        # See ``TestClassBase.InnerClass``
        pass
    # end class InnerClass

    pass
# end class InheritedClass
