#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.importutils

@brief Import utilities

@author christophe.roquebert

@date   2018/09/17
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os                           import F_OK
from os                           import R_OK
from os                           import access
from os.path                      import basename
from os.path                      import dirname
from os.path                      import isfile
from os.path                      import join
from os.path                      import normpath
from os.path                      import sep
from os.path                      import splitext
from sys                          import exc_info
from traceback                    import extract_tb
from types                        import ModuleType
import io
from types import FunctionType

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

def importFqn(fqn, exceptOnError=True):
    '''
    Imports the target by its fully qualified name.

    @param fqn [in] (str) The fully qualified name of the target to import
    @param exceptOnError [in] (bool) Whether to raise an exception in case of error, or to return None.
    @return The imported target
    '''
    elements = fqn.split(".")

    rootElements     = elements
    relativeElements = []
    lastException    = None
    locations        = {}

    result = None
    while (     (len(rootElements))
            and (result is None)):
        try:
            imported   = __import__(".".join(rootElements))                     # Do not replace __import__ by importFqn !
            precursors = rootElements[0:1]
            try:
                for element in rootElements[1:]:
                    imported = getattr(imported, element)
                    precursors.append(element)
                # end for

                for element in relativeElements:
                    imported = getattr(imported, element)
                    precursors.append(element)
                # end for

                result = imported
            except AttributeError:
                locations.setdefault(exc_info()[0], []).extend(extract_tb(exc_info()[-1]))
                if (exceptOnError):
                    lines = []
                    for excType, excLocations in sorted(iter(locations.items()), key = lambda x: str(x[0])):
                        lines.append('%s:\n%s' % (excType.__name__,
                                                  '\n'.join(sorted(set((('  File "%s", line %d, in %s' % (location[:3])) for location in excLocations))))))
                    # end for
                    locationsMessage = '\n'.join(lines)
                    raise AttributeError("'%s' has no attribute '%s' (importing: '%s')\nPossible locations:\n%s" % ('.'.join(precursors), element, fqn, locationsMessage))
                # end if
                result = None
                break
            # end try
        except (ImportError, ValueError) as exception:
            locations.setdefault(exc_info()[0], []).extend(extract_tb(exc_info()[-1]))
            lastException = exception
            relativeElements.insert(0, rootElements[-1])
            rootElements = rootElements[:-1]
        # end try
    # end while

    if (result is None) and (exceptOnError):
        if (lastException is not None):
            raise lastException                                                                                         # pylint:disable=E0702
        # end if
        raise ImportError("Unable to import: %s" % (fqn, ))
    # end if

    return result
# end def importFqn

def fqnFromLocation(sourceFilePath, lineNumber=None):                                                                   # pylint:disable=R0912
    '''
    Return the fully qualified name associated with the sourceFilePath and line

    If a lineNumer is specified, the fully qualified name of the innermost
    compound containing that line is obtained

    @param sourceFilePath [in] (str) Path to the source file to load
    @param lineNumber     [in] (int) Line number in the source file.
    @return string containing the fully qualified name to the innermost compound
    '''
    # Build the fully qualified name of the module contained within the file
    baseDir = dirname(sourceFilePath)
    currentName = splitext(basename(sourceFilePath))[0]
    elements = [currentName]
    while (access(join(baseDir, '__init__.py'), F_OK)):
        elements.insert(0, basename(baseDir))
        baseDir = dirname(baseDir)
    # end while

    fqn = '.'.join(elements)
    module = importFqn(fqn)
    if (lineNumber is not None):
        acceptedTypes = (type, ModuleType, FunctionType)

        def fqnFromUnboundMethod(target, name, rootElements):
            '''
            Test if the lineno is within the target's bounds

            @param target       [in] (acceptedTypes) The target node
            @param name         [in] (str) Name of the target node
            @param rootElements [in] (tuple) List of fqn elements
            @return The fqn, or None of the target does not match.
            '''
            result = None
            relFqn = rootElements[:]
            relFqn.append(name if name is not None else target.__name__)

            func = target.__func__
            code = func.__code__

            firstLine = code.co_firstlineno
            lineIncrements = [ord(c) for c in code.co_lnotab[1::2]]
            lineIncrements.append(0)
            lastLine  = firstLine + sum(lineIncrements)

            if (    (firstLine <= lineNumber)
                and (lastLine  >= lineNumber)):
                result = relFqn
            # end if

            return result
        # end def fqnFromUnboundMethod

        def fqnFromElement(target, name, rootElements):
            '''
            Test if the lineno is within the target's bounds

            @param target       [in] (acceptedTypes) The target node
            @param name         [in] (str) Name of the target node
            @param rootElements [in] (tuple) List of fqn elements
            @return The fqn, or None of the target does not match.
            '''
            result = target

            while hasattr(target, 'next'):
                target = target.__next__
            # end while

            if (type(target) not in acceptedTypes):
                return None
            # end if

            relFqn = rootElements[:]
            if (name is not None):
                relFqn.append(name)
            elif (hasattr(target, '__name__')):
                relFqn.append(target.__name__)
            else:
                return result
            # end if

#             if (isinstance(target, UnboundMethodType)):
#                 return fqnFromUnboundMethod(target, name, rootElements)
#             else:
            children = [(n, getattr(target, n)) for n in dir(target)
                                                if not (    (n.startswith('__'))
                                                        or  (n.endswith('__')))]
                                                # end if
#                if (hasattr(target, '__base__')):
#                    pass
#                # end if
            if len(children) > 0:
                for name, attr in children:
                    result = fqnFromElement(attr, name, relFqn)
                    if result is not None:
                        break
                    # end if
                # end for
            else:
                result = relFqn
            return result
        # end def fqnFromElement

        elements = fqnFromElement(module, currentName, elements[:-1])
    # end if

    if (elements is not None):
        return '.'.join(elements)
    # end if
    return None
# end def fqnFromLocation

def getResourceStream(targetPath, byteFormat=False):
    '''
    Obtains a stream from a path.

    The path may include an egg as one of its elements.
    If such is the case, the egg is opened, and the resource extracted

    @param targetPath [in] (str) Path to the resource to load.
    @option byteFormat [in] (bool) return BytesIO object if True
                                          StringIO otherwise.
    @return A stream on the target resource
    '''

    rootElements = normpath(targetPath).split(sep)
    relativeElements = []

    while (len(rootElements)):
        rootPath = sep.join(rootElements)
        if (access(rootPath, R_OK)):
            break
        # end if
        relativeElements.insert(0, rootElements[-1])
        del rootElements[-1]
    # end while

    # rootElement cannot be accessed: NOT FOUND
    if (len(rootElements) == 0):
        return None
    # end if

    # The leaf can be accessed
    if (len(relativeElements) == 0):
        with open(targetPath, "rb") as inputFile:
            data = inputFile.readline()
            line = data
            while(len(line) > 0):
                line = inputFile.readline()
                data += line
        # end with
        if not byteFormat:
            return io.StringIO(data.decode('utf8'))
        else:
            return io.BytesIO(data)
        # end try
        
    # end if

    # This is an intermediate
    # If the root is a zip, extract the data
    rootPath = sep.join(rootElements)

    import zipfile
    if (    (isfile(rootPath))
        and (zipfile.is_zipfile(rootPath))):

        zipFile = zipfile.ZipFile(rootPath)
        relativePath = '/'.join(relativeElements)
        for replacement in ['\\', '/', '.']:
            relativePathReplaced = relativePath.replace('/', replacement)
            if (relativePathReplaced in zipFile.namelist()):
                data = zipFile.read(relativePathReplaced)
                zipFile.close()
                return io.StringIO(data.decode('utf8'))
            # end if
        # end for
        zipFile.close()
    # end if

    return None
# end def getResourceStream

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
