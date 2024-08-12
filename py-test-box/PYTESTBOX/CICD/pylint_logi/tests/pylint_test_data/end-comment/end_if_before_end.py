# -*- coding: utf-8 -*-


if __file__ == 'test':
    pass
# end if
elif __file__ == 'toto':
    pass
elif __file__ == 'tata':
    pass
elif __file__ == 'titi':
    pass
# end if

match __file__:
    case "test":
        pass
# end match
    case "toto":
        pass
    case "tata":
        pass
    case "titi":
        pass
# end match

try:
    pass
# end try
except OSError:
    pass
except OverflowError:
    pass
# end try

# standard function to make sure the error isn't reported later
def a():
    pass
# end def a
