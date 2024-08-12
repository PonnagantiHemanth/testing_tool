"""
:package: method_no_param_type
:brief: sample file without errors
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/05/08
"""
from PYTESTBOX.LIBS.PYLIBRARY.pylibrary.tools.util import NotImplementedAbstractMethodError


class TestClassBase:
    """
    Doc string sample test class
    """
    def param_method(self, a, b=1, c=None):
        """
        Method with parameters
        """
        raise NotImplementedAbstractMethodError()
    # end def param_method

    def return_param_method(self, a, b=1, c=None):
        """
        Method with parameters

        :return: a value
        :rtype: ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def return_param_method
# end class TestClassBase


class TestOverrideRepeatDocs(TestClassBase):
    """
    Doc string sample test class repeating the docstring
    """
    def param_method(self, a, b=1, c=None):
        """
        Method with parameters
        """
        pass

    # end def param_method

    def return_param_method(self, a, b=1, c=None):
        """
        Method with parameters

        :return: a value
        :rtype: ``int``
        """

        temp = c if c else 0

        return id(self) + id(a) + b + temp
    # end def return_param_method
# end class TestOverrideRepeatDocs

class TestInitWithParam:
    """
    Doc string sample class where the init method has parameters
    """

    def __init__(self, a, b=0, c=None):
        """
        """
        self.a = a
        self.b = b
        self.c = c
    # end def __init__
# end class TestInitWithParam

def note_with_link_to_ignore(sample):
    """
    this is a brief with a note, no special processing should happen

    Note: see confluence: https://spaces.logitech.com/display/ptb/Python+docstring+format+and+best+practices
    """
    pass
# end def note_with_link_to_ignore
