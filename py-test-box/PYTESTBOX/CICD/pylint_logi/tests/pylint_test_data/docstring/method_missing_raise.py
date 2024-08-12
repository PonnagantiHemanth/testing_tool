"""
:package: method_missing_raise
:brief: sample file with raise missing in docstring
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/05/08
"""


def raise_function(on):
    """
    function that raises an exception

    :param on: an example parameter
    :type on: ``bool``
    """
    if on:
        raise ValueError('on is True')
    # end if
    pass
# end def raise_function
