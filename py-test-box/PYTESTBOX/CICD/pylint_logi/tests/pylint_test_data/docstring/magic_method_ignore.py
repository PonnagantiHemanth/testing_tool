"""
:package: magic_method_ignore
:brief: sample file with magic methods without values
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/06/24
"""

class TestClass:
    """
    Test class with magic methods without docstrings
    """

    def __repr__(self):
        return "TestClass"
    # end def __repr__

    def __set_name__(self, owner, name):
        pass
    # end def __set_name__
# end class TestClass
