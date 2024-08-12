"""
:package: method_inner_method_return
:brief: sample file with the edge case of return in an inner function, no errors
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/05/08
"""

def inner_return_method(self):
    """
    Method with return statement to ignore in an inner methode
    """

    def inner_method():
        """
        Inner method

        :return: the code filename
        :rtype: ``str``
        """
        return __file__
    # end def inner_method

    file = inner_method()
    file.strip()
# end def inner_return_method
