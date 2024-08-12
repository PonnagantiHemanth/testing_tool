""" @package pylibrary.tools.checkmustoverridebaseclass

@brief Class and decorator for must override method

@author Stanislas Cottard

@date   2019/10/17
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
def must_override(method):
    """
    Decorator for methods that must be overridden in child class.

    @param method: Method decorated
    @return: Method decorated with the attribute 'must_override_in_child' to true
    """
    method.must_override_in_child = True
    return method
# end def must_override


class CheckMustOverrideBaseClass(object):
    """
    Class to use as a parent for classes with method that must be overridden if inherited
    """

    def __init__(self):
        """
        Constructor
        """
        if self.__class__.__name__ == CheckMustOverrideBaseClass.__name__:
            return
        # end if

        parent_classes = self.__class__.__bases__
        current_class_method_name_list = [func for func in self.__class__.__dict__.keys()
                                          if callable(getattr(self.__class__, func))]

        # Check if all method that should be overridden are override
        method_not_overridden_that_should_be = []
        for parent_class in parent_classes:
            parent_method_name_list = [func for func in parent_class.__dict__.keys()
                                       if callable(getattr(parent_class, func))]

            for method_name in parent_method_name_list:
                method = getattr(parent_class, method_name)
                # Check that the 'must_override_in_child' attribute exists, that it has been enabled in the parent
                # class and that the method does not appear in the child class.
                if hasattr(method, 'must_override_in_child') and \
                        method.must_override_in_child and \
                        method_name not in current_class_method_name_list:
                    method_not_overridden_that_should_be.append(parent_class.__name__ + '.' + method_name)
                # end if
            # end for
        # end for

        if len(method_not_overridden_that_should_be) != 0:
            raise NotImplementedError(f"Can't instantiate {self.__class__.__name__} without overriding the methods: "
                                      f"{method_not_overridden_that_should_be}")
        # end if
    # end def __init__
# end class CheckMustOverrideBaseClass
