"""
:package: init_with_return
:brief: sample file where inits have returns
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/05/08
"""
from PYTESTBOX.LIBS.PYLIBRARY.pylibrary.tools.util import NotImplementedAbstractMethodError


class TestClassBase:
    """
    Doc string sample test class
    """

    def __init__(self):
        """
        :return: erroneous return
        :rtype: ``object``
        """
        pass
    # end def __init__
# end class TestClassBase


class TestOverrideRepeatDocs(TestClassBase):
    """
    Doc string sample test class repeating the docstring
    """

    def __init__(self):
        """
        :return: erroneous return
        :rtype: ``object``
        """
        super().__init__()
    # end def __init__
# end class TestOverrideRepeatDocs


class TestOverrideReferenceDocs(TestClassBase):
    # See ``TestClassBase``

    def __init__(self):
        """
        :return: erroneous return
        :rtype: ``object``
        """
        super().__init__()
    # end def __init__
# end class TestOverrideReferenceDocs

class TestInitWithParam:
    """
    Doc string sample class where the init method has parameters
    """

    def __init__(self, a, b=0, c=None):
        """
        :param a: first parameter
        :type a: ``object``
        :param b: second parameter - OPTIONAL
        :type b: ``int``
        :param c: third parameter - OPTIONAL
        :type c: ``int``


        :return: erroneous return
        :rtype: ``object``
        """
        self.a = a
        self.b = b
        self.c = c
    # end def __init__
# end class TestInitWithParam
