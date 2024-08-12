# -*- coding: utf-8 -*-


if __file__ == 'test':
    pass
# a comment is allowed here to mark the elif as a whole
elif __file__ == 'toto':
    #comment here should give no issues
    pass
elif __file__ == 'tata':
    pass
# a comment is allowed here too
elif __file__ == 'titi':
    pass
# end if

match __file__:
    case "test":
        pass
    # by extension a comment is allowed here too
    case "toto":
        # of course a comment is allowed here
        pass
    case "tata":
        pass
    # and here too
    case "titi":
        pass
# end match

try:
    pass
# and you can also put it here
except OSError:
    # and here it should be no issues either
    pass
    # and here too
except OverflowError:
    pass
# end try

# standard function to make sure the error isn't reported later
def a():
    pass
# end def a
