"""
:package: method_raise_deep_in_tree
:brief: Sample code where the return statement in side branch of the tree
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/06/27
"""


def raise_in_else(sample):
    """
    Raises an error in an else block

    :param sample: sample argument
    :type sample: ``bool``

    :raise ``Exception``: test errors
    """
    if sample:
        pass
    else:
        raise Exception()
    # end if
# end def raise_in_else


def raise_in_elif(sample):

    """
    Raises an error in an else block

    :param sample: sample argument
    :type sample: ``bool``

    :raise ``Exception``: test errors
    """

    if sample:
        pass
    elif not sample:
        raise Exception()
    # end if
# end def raise_in_elif


def raise_in_except(sample):
    """
    Raises an error in an except block

    :param sample: sample argument
    :type sample: ``bool``

    :raise ``Exception``: test errors
    """

    try:
        pass
    except Exception as e:
        raise Exception()
    # end try
# end def raise_in_except


def raise_in_case(sample):
    """
    Raises an error in an case block

    :param sample: sample argument
    :type sample: ``bool``

    :raise ``Exception``: test errors
    """
    match sample:
        case True:
            pass
        case _:
            raise Exception()
    # end match
# end def raise_in_case
