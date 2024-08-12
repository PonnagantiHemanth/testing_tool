#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pylibrary.tools.docutils
    :brief: Doc utils
    :author: Martin Cryonnet
    :date: 2020/10/23
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DocUtils:
    @staticmethod
    def copy_doc(original):
        """
        Decorator to copy docstring from one function to an other

        :param original: function with reference docstring
        :type original: ``function or any``
        """
        def wrapper(target):
            target.__doc__ = original.__doc__
            return target
        # end def wrapper
        return wrapper
    # end def copy_doc
# end class DocUtils


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
