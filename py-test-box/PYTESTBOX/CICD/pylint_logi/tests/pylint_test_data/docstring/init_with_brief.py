"""
:package: init_with_brief
:brief: sample file where init methods have briefs
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/05/21
"""


class TestClassBase:
    """
    Doc string sample test class
    """

    def __init__(self):
        """
        Erroneous brief in the init
        """
        pass
    # end def __init__
# end class TestClassBase

class TestInitWithParam:
    """
    Doc string sample class where the init method has parameters
    """

    def __init__(self, a, b=0, c=None):
        """
        Erroneous brief in init

        :param a: first parameter
        :type a: ``object``
        :param b: second parameter - OPTIONAL
        :type b: ``int``
        :param c: third parameter - OPTIONAL
        :type c: ``int``
        """
        self.a = a
        self.b = b
        self.c = c
    # end def __init__
# end class TestInitWithParam
