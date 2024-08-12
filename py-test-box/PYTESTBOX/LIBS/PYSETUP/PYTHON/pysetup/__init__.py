#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Python Test Harness
# -----------------------------------------------------------------------------
''' @package pysetup

@brief    PySetup Python interface

@author   christophe roquebert

@version  1.7.1.0

@date     2007/10/10
'''
# -----------------------------------------------------------------------------
# imports
# -----------------------------------------------------------------------------
from distutils                          import version
from distutils.versionpredicate         import VersionPredicate as DistUtils_VersionPredicate
from os                                 import F_OK
from os                                 import access
from os                                 import getcwd
from os                                 import listdir
from os                                 import sep
from os.path                            import abspath
from os.path                            import basename
from os.path                            import dirname
from os.path                            import exists
from os.path                            import isdir
from os.path                            import isfile
from os.path                            import join
from os.path                            import normcase
from os.path                            import normpath
from os.path                            import splitdrive
from uuid                               import uuid1
from weakref                            import ref
from zipfile                            import ZipFile
from zipfile                            import is_zipfile
import builtins
import re
import sys
import unicodedata

# -----------------------------------------------------------------------------
# implementation
# -----------------------------------------------------------------------------

# Fix distutil's to a LooseVersion
version.StrictVersion = version.LooseVersion

class VersionPredicate(DistUtils_VersionPredicate):
    '''
    Overrides versonPredicate to keep an egg reference.
    '''
    def __init__(self, versionPredicateStr, egg = None):
        '''
        Constructor

        @param  versionPredicateStr [in] (str) predicate to apply
        @option egg                 [in] (Egg) reference
        '''
        DistUtils_VersionPredicate.__init__(self, versionPredicateStr)
        if (egg is not None):
            egg = ref(egg)
        # end if
        self._egg = egg
    # end def __init__

    def getEgg(self):
        '''
        Obtains the egg.

        @return The egg, or None if no egg is found.
        '''
        egg = self._egg
        if egg is not None:
            egg = egg()
        # end if
        return egg
    # end def getEgg
# end class VersionPredicate

class Egg(object):
    '''
    An object representing an egg.

    It contains the location of the egg, its path, and utility methods to access its contents.
    '''

    def __init__(self, location):
        '''
        Initializes the egg information.

        @param  location [in] (str) The location of the egg.
        '''
        self._location = location

        self._eggInfoRead  = False

        self._name         = None
        self._version      = None
        self._requirements = None
    # end def __init__

    def __str__(self):
        '''
        Convert the current object to a string

        @return (str) A readable name for the object
        '''
        return '%s %s at %s' % (self._name, self._version, self._location)
    # end def __str__

    _RE_COMPARISON = re.compile(r'(\S)(<=|>=|<|>|!=|==)')

    def _readEggInfo(self):
        '''
        Extracts relevant information from an PKG-INFO file, and updates the
        internal cache.
        '''
        eggInfo = self.readFile('EGG-INFO/PKG-INFO')
        if isinstance(eggInfo, bytes):
            eggInfo = eggInfo.decode('utf-8')
        # end if

        # Extract relevant information from the contents
        eggName = None
        eggVersion = None
        eggRequires = []
        for line in [x.rstrip() for x in eggInfo.split('\n')]:
            if not line.startswith(' '):
                if (line.startswith('Name:')):
                    eggName = line[len('Name:'):].replace('-', '.').strip()
                elif (line.startswith('Version:')):
                    eggVersion = line[len('Version:'):].strip()
                elif (line.startswith('Requires:')):
                    eggRequires.append(line[len('Requires:'):].strip())
                # end if
            # end if
        # end for

        # Also check for requires.txt file
        requiresTxtPath = 'EGG-INFO/requires.txt'
        if (self.hasFile(requiresTxtPath)):
            requiresFile = self.readFile(requiresTxtPath)
            if isinstance(requiresFile, bytes):
                requiresFile = requiresFile.decode('utf-8')
            # end if
            for line in requiresFile.split('\n'):
                if (line and '[' not in line):
                    # package>=x.y.z
                    line = self._RE_COMPARISON.sub(r'\1 \2', line)
                    # package >=x.y.z
                    elements = line.split(' ', 1)
                    if (len(elements) > 1):
                        line = '%s (%s)' % (elements[0], elements[1].strip())
                        # package (>=x.y.z)
                    # end if
                    eggRequires.append(line.replace('-', '.').strip())
                # end if
            # end for
        # end if

        self._name         = eggName
        self._version      = eggVersion
        self._requirements = [VersionPredicate(x, self) for x in eggRequires]

        self._eggInfoRead = True
    # end def _readEggInfo

    def listPaths(self):
        '''
        Obtains a list of the eggs contents, relative to the egg location.

        @return (tuple) Tuple of egg contents paths.
        '''
        raise NotImplementedError
    # end def listPaths

    def readFile(self, path):
        '''
        Obtains the contents of the target file within the egg.

        @param  path [in] (str) Relative path to the file within the egg

        @return (str) String containing the file contents.
        '''
        raise NotImplementedError
    # end def readFile

    def hasFile(self, path):
        '''
        Tests if the contents of the target are available.

        @param  path [in] (str) Relative path to the file within the egg

        @return (bool) Whether the file exists within the egg.
        '''
        raise NotImplementedError
    # end def hasFile

    def getLocation(self):
        '''
        Obtains the egg location.

        @return (str) The egg location
        '''
        return self._location
    # end def getLocation

    def getName(self):
        '''
        Obtains the egg name

        @return (str) The egg name
        '''
        if (not self._eggInfoRead):
            self._readEggInfo()
        # end if

        return self._name
    # end def getName
    name = property(getName)

    def getVersion(self):
        '''
        Obtains the egg version

        @return (str) The egg version
        '''
        if (not self._eggInfoRead):
            self._readEggInfo()
        # end if

        return self._version
    # end def getVersion

    def getRequirements(self):
        '''
        Obtains the egg requirements

        @return (str) The egg requirements
        '''
        if (not self._eggInfoRead):
            self._readEggInfo()
        # end if

        return self._requirements
    # end def getRequirements

    @classmethod
    def createOrNone(cls, location):
        '''
        Creates a new instance of an egg if the given location is acceptable,
        or returns None

        @param  location [in] (str) The location to create the egg from.

        @return (object) A new egg instance, or None if unacceptable.
        '''
        raise NotImplementedError
    # end def createOrNone

    def getTestSuiteFqn(self):
        '''
        Extracts the test suite fully qualified name from the setup.py file.

        This is NOT a clean implementation, but distutils does not (yet) support
        the extraction of such a property in egg-info

        @return None if no test suite has been found, a string with the test
                suite's fully qualified name otherwise.
        '''
        result = None
        if (self.hasFile('setup.py')):
            contents = self.readFile('setup.py')
            lines = [line.strip() for line in contents.split('\n')]
            lines = [line for line in lines if line.startswith('test_suite')]

            test_suite_regex = re.compile('test_suite\\s*=\\s*["\']([^"\']+)["\'].*')
            for line in lines:
                re_match = test_suite_regex.match(line)
                if re_match:
                    result = re_match.group(1)
                    break
                # end if
            # end for
        # end if

        return result
    # end def getTestSuiteFqn
# end class Egg

class EggAsZip(Egg):
    '''
    An egg, stored in a zip file.
    '''
    def __init__(self, location):
        '''
        @copydoc pysetup.Egg.__init__
        '''
        super(EggAsZip, self).__init__(location)
        self.__zipFile = None
    # end def __init__

    def __getZipFile(self):
        '''
        Obtains or create the zipfile associated with the egg

        @return (file) zipfile The zip file for the egg
        '''
        if (self.__zipFile is None):
            self.__zipFile = ZipFile(self._location, 'r')
        # end if

        return self.__zipFile
    # end def __getZipFile

    def listPaths(self):
        '''
        @copydoc pysetup.Egg.listPaths
        '''
        zipFile = self.__getZipFile()

        return tuple(zipFile.namelist())
    # end def listPaths

    def readFile(self, path):
        '''
        @copydoc pysetup.Egg.readFile
        '''
        zipFile = self.__getZipFile()
        return zipFile.read(path)
    # end def readFile

    def hasFile(self, path):
        '''
        @copydoc pysetup.Egg.hasFile
        '''
        zipFile = self.__getZipFile()
        return path in zipFile.namelist()
    # end def hasFile

    @classmethod
    def createOrNone(cls, location):
        '''
        @copydoc pysetup.Egg.createOrNone
        '''
        result = None
        if (    (location.endswith('.egg'))
            and (isfile(location))
            and (is_zipfile(location))):
            result = EggAsZip(location)
        # end if

        return result
    # end def createOrNone
# end class EggAsZip

class EggAsDir(Egg):
    '''
    An egg, stored in a directory structure.
    '''

    IGNORE_DIRS = ('.svn', 'CVS')

    def listPaths(self):
        '''
        @copydoc pysetup.Egg.listPaths
        '''
        from os                         import walk
        collector = set()
        location = normpath(self._location)
        for rootPath, dirs, files in walk(location):
            for d in self.IGNORE_DIRS:
                while d in dirs:
                    dirs.remove(d)
                # end while
            # end for

            for fileName in files:
                collector.add(join(rootPath, fileName)[len(location)+1:])
            # end for
        # end for

        return tuple(collector)
    # end def listPaths

    def readFile(self, path):
        '''
        @copydoc pysetup.Egg.readFile
        '''
        try:
            # Text I/O expects and produces str objects.
            with open(join(self._location, path), 'r') as inputFile:
                result = inputFile.read()
            # end with
        except:
            try:
                # Binary I/O (also called buffered I/O) expects bytes-like objects and produces bytes objects.
                with open(join(self._location, path), 'rb') as inputFile:
                    result = inputFile.read()
                    result = result.decode('utf-8')
                # end with
            except Exception as exp:
                raise BaseException('readFile error in %s (%s)' % (str(inputFile), str(exp)))
        # end with

        return result
    # end def readFile

    def hasFile(self, path):
        '''
        @copydoc pysetup.Egg.hasFile
        '''
        return exists(join(self._location, path))
    # end def hasFile

    @classmethod
    def createOrNone(cls, location):
        '''
        @copydoc pysetup.Egg.createOrNone
        '''
        result = None
        if (    (isdir(location))
            and (exists(join(location, 'EGG-INFO', 'PKG-INFO')))):
            result = EggAsDir(location)
        # end if

        return result
    # end def createOrNone
# end class EggAsDir

class EggFactory(object):
    '''
    Creates an egg from a path
    '''

    @classmethod
    def create(cls, fromPath):
        '''
        Creates an egg from a path.

        @param  fromPath [in] (str) The path to create the egg from.

        @return (object) An egg, or None if not applicable.
        '''
        result = None
        for eggClass in (EggAsZip, EggAsDir):
            result = eggClass.createOrNone(fromPath)
            if (result is not None):
                break
            # end if
        # end for

        return result
    # end def create
# end class EggFactory


# A list of all eggs found in the path.
# This contains a dict, where the key is the identifier of the egg,
# The value is itself a dict, where the key is the version of the egg
# The value of this inner dict is a tuple(location, egg_config)
# New: The value of this inner dict is the egg instance
ALL_EGGS = {}

# A set of all locations where eggs can be found (nests...)
# This guarantees that a nest is scanned once, and only once
EGG_NESTS = set()

def _enumerateEggNest(fromPath):
    '''
    Enumerates all eggs found in a path.

    @param  fromPath [in] (str) Path to enumerate

    @return a dict similar to ALL_EGGS
    '''
    result = {}
    if (    (fromPath not in EGG_NESTS)
        and (exists(fromPath))):

        eggs = []

        # check if the path is itself an egg.
        egg = EggFactory.create(fromPath)
        if (egg is not None):
            eggs.append(egg)
        elif isdir(fromPath):
            # The path is not an egg: check its children
            for fileName in listdir(fromPath):
                filePath = join(fromPath, fileName)
                egg = EggFactory.create(filePath)
                if (egg is not None):
                    eggs.append(egg)
                # end if
            # end for
        # end if

        for egg in eggs:
            eggName = egg.getName()
            eggSiblings = result.setdefault(eggName, {})
            eggSiblings.setdefault(egg.getVersion(), egg)
        # end for
    # end if
    return result
# end def _enumerateEggNest

def _enumerateAllEggs(fromPath=None):
    '''
    Updates the egg list in the python path.

    @param  fromPath [in] (str) Path to lookup from
    '''

    if (fromPath is None):
        pathList = sys.path
    else:
        pathList = [fromPath]
    # end if

    for fromPath in pathList:
        if (fromPath not in EGG_NESTS):
            nests = _enumerateEggNest(fromPath)
            for eggName, eggSiblings in nests.items():
                allEggSiblings = ALL_EGGS.setdefault(eggName, {})
                allEggSiblings.update(eggSiblings)
            # end for
            EGG_NESTS.add(fromPath)
        # end if
    # end for
# end def _enumerateAllEggs

def _getBestEgg(eggName, versionPredicates):
    '''
    Find the best egg, given the current requirements

    @param  eggName           [in] (str) Name of the egg to lookup
    @param  versionPredicates [in] (str) List of version predicates to apply

    @return (tuple) A tuple (version, updatedRequirements), with the best version,
            and the associated (possibly cascaded) requirements.
    '''

    # An egg must have been found.
    if (eggName not in ALL_EGGS):
        raise ImportError('Unable to find egg for: %s' % (eggName,))
    # end if

    eggSiblings = ALL_EGGS[eggName]
    dropThisEggVersion = True
    eggVersion = None
    innerVersionPredicates = versionPredicates

    # Lookup siblings, using the highest version first
    for eggVersion, egg in sorted(iter(list(eggSiblings.items())),
                                  key     = lambda x: x[-1].getVersion(),
                                  reverse = True):
        eggRequirements = egg.getRequirements()

        dropThisEggVersion = False
        # Match the egg version against the current requirements
        for versionPredicate in [vp for vp in versionPredicates if vp.name == eggName]:
            if (not versionPredicate.satisfied_by(eggVersion)):
                dropThisEggVersion = True
                break
            # end if
        # end for

        # If the egg Version matches, lookup the dependencies
        # will possibly need to backtrack...
        if (not dropThisEggVersion):
            innerVersionPredicates = versionPredicates[:]
            innerVersionPredicates.extend(eggRequirements)

            # Iterate on the egg dependencies
            for innerEggName in iter(set([e.name for e in eggRequirements])):
                innerEggVersion, innerVersionPredicates = _getBestEgg(innerEggName, innerVersionPredicates)

                # If the dependency cannot be found, drop this egg version.
                if (innerEggVersion is None):
                    dropThisEggVersion = True
                    break
                # end if
            # end for

            # The egg matches the requirements, and all its dependencies match
            # the requirements. As the higher version was looked up first,
            # we can stop searching
            if (not dropThisEggVersion):
                # Add one requirement, that freezes this egg version
                innerVersionPredicates.insert(0, VersionPredicate('%s (==%s)' % (eggName, eggVersion), egg))
                break
            # end if
        # end if
    else:
        if (dropThisEggVersion):
            eggVersion = None
            innerVersionPredicates = versionPredicates
        # end if
    # end for

    # eggVersion now contains the relevant egg version
    # innerVersionPredicates now contains the updated predicates
    return (eggVersion, innerVersionPredicates)                                                                         # pylint:disable=W0631
# end def _getBestEgg

def _lookupEggs(eggDict, eggRequirements):
    '''
    Filters eggDict keeping only the eggs that are valid for the given _starting_
    requirement set, resolving dependencies on the fly.

    @param  eggDict [in] (dict) Similar to ALL_EGGS, containing valid eggs
    @param  eggRequirements [in] (set) egg requirements to apply to the dict

    @return (list) A list of (name, version, egg)
    '''
    matchingEggs = {}

    # Iterate on egg names
    versionPredicates = []
    newVersionPredicates = eggRequirements[:]

    while (newVersionPredicates != versionPredicates):

        versionPredicates = newVersionPredicates
        eggNames = set([e.name for e in versionPredicates])

        for eggName in iter(eggNames - set(matchingEggs.keys())):
            eggVersion, newVersionPredicates = _getBestEgg(eggName, versionPredicates)
            if (eggVersion is None):

                # Attempt to generate a map of the egg dependencies
                try:
                    from pysetup        import LIBS_LOCAL_TMP_PATH                                                            # pylint:disable=E0611
                except ImportError:
                    LIBS_LOCAL_TMP_PATH = '.'                                                                          # pylint:disable=C0103
                # end try

                try:
                    from pysetup        import DOT                                                                             # pylint:disable=E0611
                except ImportError:
                    DOT = None                                                                                          # pylint:disable=C0103
                # end try

                eggDependencyPath = abspath(join(LIBS_LOCAL_TMP_PATH, 'egg-dependencies.dot'))
                generateDependencyGraph(eggDependencyPath)

                if (exists(eggDependencyPath) and DOT is not None):

                    from subprocess     import Popen                                                                        # pylint:disable=W0404,W0621
                    from subprocess     import PIPE
                    process = Popen((DOT, '-Tpng', '-O', eggDependencyPath),
                                    stdin  = PIPE,
                                    stdout = PIPE,
                                    stderr = PIPE,
                                    cwd    = dirname(eggDependencyPath))
                    process.communicate()
                    eggDependencyPath = eggDependencyPath + '.png'
                # end if

                raise ImportError("Unable to find suitable <%s> egg or library.\nConstraints: \n  %s\nAvailable eggs:\n  %s\nAn egg dependency graph has been generated at:\n  " % \
                                  (eggName,
                                   '\n  '.join(["%s  [from %s]" % (str(x), str(x.getEgg())) for x in versionPredicates
                                                                                 if x.name == eggName]),
                                   '\n  '.join([str(x) for x in list(ALL_EGGS.get(eggName, {}).values())
                                                 if x.name == eggName])),
                                   eggDependencyPath)
            # end if

            eggNames.remove(eggName)
            matchingEggs[eggName] = (eggName, eggVersion, eggDict[eggName][eggVersion])
        # end for
    # end while

    return list(matchingEggs.values())
# end def _lookupEggs

def _extractEggInfo(eggInfo):
    '''
    Extracts relevant information from an PKG-INFO file

    @param  eggInfo [in] (str) The contents of a PKG-INFO file
    @return tuple(requires, name, version)
    '''

    # Extract relevant information from the contents
    eggName = None
    eggVersion = None
    eggRequires = []
    for line in [x.rstrip() for x in eggInfo.split('\n')]:
        if not line.startswith(' '):
            if (line.startswith('Name:')):
                eggName = line[len('Name:'):].strip()
            elif (line.startswith('Version:')):
                eggVersion = line[len('Version:'):].strip()
            elif (line.startswith('Requires:')):
                eggRequires.append(line[len('Requires:'):].strip())
            # end if
        # end if
    # end for

    return eggRequires, eggName, eggVersion
# end def _extractEggInfo

def listEggsAndPaths(eggRequirements, fromPath=None):
    '''
    Adds all eggs necessary for the given requirements

    @param  eggRequirements [in] (set) egg requirements to apply to the dict
    @option fromPath [in] (str) Path containing the libraries

    @return (list) A list of egg locations
    '''
    _enumerateAllEggs(fromPath)

    if (isinstance(eggRequirements, str)):
        eggRequirements = [eggRequirements]
    # end if
    eggRequirements = [isinstance(e, str) and VersionPredicate(e) or e for e in eggRequirements]

    return [(egg.getLocation(), egg) for (unused_eggName, unused_eggVersion, egg) in _lookupEggs(ALL_EGGS, eggRequirements)]
# end def listEggsAndPaths

# Maps an egg path to an egg instance.
LOADED_EGG_PATHS = {}

# initialize loadedEggsAndPaths with the eggs already present in the path
def _initializeLoadedEggPathsFromSysPath():
    '''
    Initializes LOADED_EGG_PATHS from the sys path.
    '''
    for path in sys.path:
        egg = EggFactory.create(path)
        if (egg is not None):
            LOADED_EGG_PATHS[path] = egg
        # end if
    # end for
# end def _initializeLoadedEggPathsFromSysPath
_initializeLoadedEggPathsFromSysPath()

def addEggsToSysPath(eggRequirements, fromPath=None):
    '''
    Adds all eggs necessary for the given requirements to the sys.path

    @param  eggRequirements [in] (set) egg requirements to apply to the dict
    @option fromPath        [in] (str) Path containing the libraries
    '''
    _enumerateAllEggs(fromPath)

    eggsAndPaths = listEggsAndPaths(eggRequirements, fromPath)

    loadedEggsAndPaths = {}
    for path, egg in eggsAndPaths:
        loadedEggsAndPaths[path] = egg
    # end for

    sys.path[0:0] = list(loadedEggsAndPaths.keys())

    LOADED_EGG_PATHS.update(loadedEggsAndPaths)
# end def addEggsToSysPath

def addEggDependenciesToSysPath(sourcePath, fromPath = None):
    '''
    Adds the detected dependencies to the path

    @param  sourcePath [in] (str) Source library path
    @option fromPath   [in] (str) Path containing the libraries
    '''
    egg = None
    for eggClass in (EggAsZip, EggAsDir):
        egg = eggClass.createOrNone(sourcePath)
        if (egg is not None):
            break
        # end if
    # end for

    if (egg is not None):
        eggRequirements = egg.getRequirements()

        addEggsToSysPath(eggRequirements, fromPath)
    # end if
# end def addEggDependenciesToSysPath

def generateDependencyGraph(filePath):
    '''
    Generates a DOT dependency graph for all known eggs

    @param  filePath [in] (string) Path to the dot file to generate
    '''
    _enumerateAllEggs()
    with open(filePath, 'w+') as outputFile:
        outputFile.write('\n'.join(('digraph G',
                                    '{',
                                    '    graph   [bgcolor=transparent]'
                                    '    node    [fontname=Arial, fontsize = 10, align=center, shape=box, width=1.0, style=filled bgcolor="#CC0000"];',
                                    '    edge    [fontname=Arial, fontsize = 8, len=0.5];',
                                    '',
                                    )))
        doneLinks = set()
        for name, eggSiblings in list(ALL_EGGS.items()):
            for eggVersion, egg in list(eggSiblings.items()):
                key = ('EGG_%s_%s' % (name, eggVersion)).replace('.', '____').replace('-', '_')
                outputFile.write('    %s [label="%s\\n%s", shape=box, fillcolor=seashell];\n' % (key, name, eggVersion))
                for versionPredicate in egg.getRequirements():
                    predicateName = str(versionPredicate)
                    predicateKey = 'PRED_%s' % predicateName
                    reserved = '<=>!( ).-'
                    for x in reserved:
                        predicateKey = predicateKey.replace(x, '_x%02X' % ord(x))
                    # end for
                    outputFile.write('    %s [label="%s", shape=ellipse, fillcolor=mintcream];\n' % (predicateKey, predicateName,))
                    outputFile.write('    %s -> %s' % (key, predicateKey))
                    for (targetName, targetEggSiblings) in list(ALL_EGGS.items()):
                        if (targetName == versionPredicate.name):
                            for targetEggVersion, _ in list(targetEggSiblings.items()):
                                if versionPredicate.satisfied_by(targetEggVersion):
                                    targetKey = ('EGG_%s_%s' % (targetName, targetEggVersion)).replace('.', '____').replace('-', '_')
                                    linkKey = (predicateKey, targetKey)
                                    if (linkKey not in doneLinks):
                                        outputFile.write('    %s -> %s;\n' % (predicateKey, targetKey))
                                        doneLinks.add(linkKey)
                                    # end if
                                # end if
                            # end for
                        # end if
                    # end for
                # end for
            # end for
        # end for
        outputFile.write('}')
    # end with
# end def generateDependencyGraph

# ------------------------------------------------------------------------------
# LOCAL configuration
# ------------------------------------------------------------------------------
def absNormPath(path):
    '''
    @copydoc os.path.abspath
    @copydoc os.path.normpath

    It also converts drive to uppercase
    '''
    (drive, tail) = splitdrive(abspath(path))
    return drive.upper() + normpath(tail)
# end def absNormPath

try:
    _referencePath = absNormPath(__file__)
except NameError:
    _referencePath = absNormPath(sys.argv[0])
# end try

# Import all constants defined in local.py
PROJECT_PATH = _referencePath[:_referencePath.index(normpath('/LIBS/'))]

try:
    from imp                            import load_source

    # Import all constants defined in local.py
    _local   = join(PROJECT_PATH, 'LIBS', 'LOCAL', 'local.py')
    globals().update(load_source('local', _local).__dict__)

except IOError:
    # Check the current environment
    from subprocess                     import Popen
    Popen([sys.executable, 'pyEnvChecker.py'],                                                                              # pylint:disable=E1101
          cwd = join(PROJECT_PATH, 'LIBS', 'PYENVCHECKER')).wait()

    # Import again all constants defined in local.py
    try:
        globals().update(load_source('local', _local).__dict__)
    except ImportError:
        exit('Please check your environment first!')
    # end try
# end try

sys.path.extend((p for p in LOCAL_PYTHON_PATH if p not in sys.path))                                                    # @UndefinedVariable pylint:disable=E0602

def getVersion(name):
    '''
    Retrieve version from Local.txt

    @param  name [in] (str) NAME

    @return (str) version or None
    '''
    name  = 'name    : %s' % (name,)
    local = open(join(LIBS_LOCAL_PATH, 'Local.txt'), 'r')                                                              # @UndefinedVariable pylint:disable=E0602
    lines = local.readlines()
    local.close()

    for i, line in enumerate(lines):
        if (line.rstrip() == name):
            return lines[i+2].split(':')[-1].strip()
        # end if
    # end for
# end def getVersion

# ------------------------------------------------------------------------------
# APP
# ------------------------------------------------------------------------------
START_PATH = absNormPath(getcwd())

if (sys.argv[0] and (sys.argv[0] != '-c')):
    APP_PATH      = absNormPath(dirname(sys.argv[0]))
    APP_TMP_PATH  = join(LIBS_LOCAL_TMP_PATH, basename(sys.argv[0]).upper())                                           # @UndefinedVariable pylint:disable=E0602
else:
    APP_PATH      = START_PATH
    APP_TMP_PATH  = join(LIBS_LOCAL_TMP_PATH, str(uuid1()))                                                            # @UndefinedVariable pylint:disable=E0602
# end if

# ------------------------------------------------------------------------------
# TOOL | PRODUCT/VARIANT/TARGET
# ------------------------------------------------------------------------------
_aName = (   (START_PATH.startswith(PROJECT_PATH) and START_PATH)
          or APP_PATH).replace(PROJECT_PATH, '').split(sep)
_cName = len(_aName)

if (_cName > 1):

    _aName[0] = PROJECT_PATH

    if (_aName[1] == 'LIBS'):

        TOOL_NAME = None

        # 0 - PROJECT
        # 1   +- LIBS
        # 2      +- PYSETUP|PROJECT
        # 3      +- <TOOL>
        if (_cName > 3):
            TOOL_NAME = _aName[3]
            TOOL_PATH = join(PROJECT_PATH, 'LIBS', TOOL_NAME)

            # 4     +- <TOOL>
            # 5        +- LOCAL
            if (_cName > 4):
                TOOL_VARIANT_NAME       = _aName[4]
                TOOL_VARIANT_PATH       = join(TOOL_PATH, TOOL_VARIANT_NAME)
                TOOL_VARIANT_LOCAL_PATH = join(TOOL_VARIANT_PATH, 'LOCAL')
            # end if
        # end if

    else:
        PRODUCT_NAME = None
        VARIANT_NAME = None
        TARGET_NAME  = None

        if (_aName[1] in ('RELEASE', 'WORKING')):

            # 0 - PROJECT
            # 1   +- RELEASE|WORKING
            # 2      + <PRODUCT>
            if (_cName > 2):
                PRODUCT_NAME = _aName[2]

                # 3    +- <VARIANT>
                # x       +- [SUB_VARIANT]
                # y          +- <TARGET>

            # end if

        elif (_aName[1] not in ('ABOUT', 'TEST', 'TESTS')):

            # 0 - PROJECT
            # 1   +- <PRODUCT>
            PRODUCT_NAME = _aName[1]

            # 2      +- VARIANT
            # 3         +- <VARIANT>
            # x            +- [SUB_VARIANT]
            if ((_cName > 3) and (_aName[2] == 'VARIANT')):

                # _iName      +- LOCAL
                # _iName+1       +- <TARGET>
                # _cName
                if ('LOCAL' in _aName):
                    _iName = _aName.index('LOCAL')

                    if (_cName > (_iName+1)):
                        TARGET_NAME = _aName[_iName+1]
                    # end if
                else:
                    _iName = _cName
                # end if
                VARIANT_NAME = '_'.join(_aName[3:_iName])
                VARIANT_PATH = sep.join(_aName[3:_iName])
            # end if
        # end if

        if (PRODUCT_NAME):
            PRODUCT_WORKING_PATH = join(WORKING_PATH, PRODUCT_NAME)                                                     # @UndefinedVariable pylint:disable=E0602
            PRODUCT_RELEASE_PATH = join(RELEASE_PATH, PRODUCT_NAME)                                                     # @UndefinedVariable pylint:disable=E0602
            PRODUCT_PATH         = join(PROJECT_PATH, PRODUCT_NAME)

            if (VARIANT_NAME):
                VARIANT_WORKING_PATH = join(PRODUCT_WORKING_PATH, VARIANT_PATH)
                VARIANT_RELEASE_PATH = join(PRODUCT_RELEASE_PATH, VARIANT_PATH)
                VARIANT_PATH         = join(PRODUCT_PATH, 'VARIANT', VARIANT_PATH)
                VARIANT_LOCAL_PATH   = join(VARIANT_PATH, 'LOCAL')

                if (TARGET_NAME):
                    TARGET_WORKING_PATH = join(VARIANT_WORKING_PATH, TARGET_NAME)
                    TARGET_RELEASE_PATH = join(VARIANT_RELEASE_PATH, TARGET_NAME)
                    TARGET_PATH         = join(VARIANT_LOCAL_PATH, TARGET_NAME)
                # end if
            # end if
        # end if
    # end if
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
