#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.config

@brief  ConfigParser implementation

@author christophe.roquebert

@date   2018/09/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist            import HexList
import re

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class BaseConfigParser(object):
    '''
    Base implementation of a ConfigParser.

    This reads a config file, and provides access to sections and options.

    The format of a config file is:
    @code
    # A comment
    ; Another comment
    [A_SECTION]
    anoption = theoptionvalue
    @endcode

    Sections must be defined only ONCE in the config file.
    Options must be defined only ONCE in a section.
    Comments are preserved from reading to writing.
    '''

    def __init__(self, strict=False):
        '''
        Constructor.

        Creates an empty configuration.
        Parsing of ini files can be STRICT or not. If strict, the value string
        associated with an option MUST conform with one of the regex.

        A non-match will result in an error.

        @option strict [in] (bool) Whether the parsing is STRICT of not.
        '''
        self.objects = []
        self.strict  = strict
    # end def __init__

    ## @name regular expressions for parsing lines.
    ##@{
    REGEX_COMMENT      = re.compile(r'[#;]\s*(.*)$')
    REGEX_SECTION      = re.compile(r'\[([A-Za-z_0-9/\\]+)\]\s*$')
    REGEX_PROPERTY     = re.compile(r'([a-zA-z_0-9]+)\s*=\s*(.*)\s*$')
    REGEX_BLANK        = re.compile(r'\s*$')
    REGEX_CONTINUATION = re.compile(r'(\s+.*)$')
    ##@}

    ## @name states for the FSM, reading the configuration.
    ##@{
    STATE_LOOKING_FOR_SECTION      = 1
    STATE_LOOKING_FOR_PROPERTY     = 2
    STATE_LOOKING_FOR_CONTINUATION = 3
    ##@}

    ## @name modes for the insertion of comments.
    ##@{
    MODE_BEFORE                = -1
    MODE_INSIDE                =  0
    MODE_AFTER                 =  1
    ##@}

    class _CommentLine(object):
        '''
        A comment line, starting with @c # or @c ;
        '''

        def __init__(self, value):
            '''
            Constructor.

            @param  value [in] (str) The value of the comment line,
                                       without the comment character.
            '''
            self.value = value
        # end def __init__

        def __str__(self):
            '''
            Converts the line to a string.

            The conversion will force the comment character to @c #

            @return (str) The current line, as a string.
            '''
            return "# " + self.value
        # end def __str__

        def __repr__(self):
            '''
            Converts the line to a string.

            @return (str) The string representation of the object.
            '''
            return '%s(value = %r)' % (self.__class__.__name__, self.value)
        # end def __repr__

    # end class _CommentLine

    class _SectionLine(object):
        '''
        A section line, such as @c [SECTION]
        '''
        def __init__(self, value):
            '''
            Creates a new section

            @param  value [in] (str) The name of the section.
            '''
            self.value = value
        # end def __init__

        def __str__(self):
            '''
            Converts the line to a string.

            The section name will be set between brackets: @c [SECTION]

            @return (str) The current line, as a string.
            '''
            return "[%s]" % (self.value,)
        # end def __str__

        def __repr__(self):
            '''
            Converts the line to a string.

            @return (str) The string representation of the object.
            '''
            return '%s(value = %r)' % (self.__class__.__name__, self.value)
        # end def __repr__

    # end class _SectionLine

    class _PropertyLine(object):
        '''
        An option line, such as @c option=value
        '''

        def __init__(self, key, value):
            '''
            Constructor.

            @param  key   [in] (str) The option name to associate the value with
            @param  value [in] (str) The value to set.
            '''
            self.key   = key
            self.value = value
        # end def __init__

        def __str__(self):
            '''
            Converts the line to a string

            The option name and value will be separated by @c = : @c option=value

            @return (str) The current line, as a string.
            '''
            return "%s = %s" % (self.key, self.value)
        # end def __str__

        def __repr__(self):
            '''
            Converts the line to a string.

            @return (str) The string representation of the object.
            '''
            return '%s(key = %r, value = %r)' % (self.__class__.__name__, self.key, self.value)
        # end def __repr__

    # end class _PropertyLine

    class _BlankLine(object):
        '''
        A blank line
        '''

        def __init__(self):
            '''
            Constructor.
            '''
            pass
        # end def __init__

        @staticmethod
        def __str__():
            '''
            Converts the line to a string

            @return An empty line
            '''
            return ""
        # end def __str__

        def __repr__(self):
            '''
            Converts the line to a string.

            @return (str) The string representation of the object.
            '''
            return '%s()' % (self.__class__.__name__)
        # end def __repr__

    # end class _BlankLine

    class _ContinuationLine(object):
        '''
        A continuation line, as set by RFC 822
        '''

        def __init__(self, line):
            '''
            Constructor.

            @param  line [in] (str) The raw, unparsed line
            '''
            self.value = line
        # end def __init__

        def __str__(self):
            '''
            Converts the line to a string

            @return The current line, as a string
            '''
            return self.value
        # end def __str__

        def __repr__(self):
            '''
            Converts the line to a string.

            @return (str) The string representation of the object.
            '''
            return '%s(%r)' % (self.__class__.__name__, self.value)
        # end def __repr__

    # end class _ContinuationLine

    class _DebugLine(object):
        '''
        An unparsed line.
        '''

        def __init__(self, line):
            '''
            Constructor.

            @param  line [in] (str) The raw, unparsed line
            '''
            self.value = line
        # end def __init__

        def __str__(self):
            '''
            Converts the line to a string

            @return (str) The current line, as a string.
            '''
            return "# Syntax error: %s" % (self.value,)
        # end def __str__

        def __repr__(self):
            '''
            Converts the line to a string.

            @return (str) The string representation of the object.
            '''
            return '%s(%r)' % (self.__class__.__name__, self.value)
        # end def __repr__

    # end class _DebugLine

    @staticmethod
    def _readLine(line):
        '''
        Obtains a node matching the line type

        @param  line [in] (str) the line to parse

        @return A wrapper object around the parsed line.

        The line must follow the format:
         - ^\\[([A-Z0-9_]+)\\]\\s*$ : For sections
         - ^([a-zA-z_0-9]+)\\s*=\\s*(.*)\\s*$ : For properties
         - ^[#;]\\s*(.*)$ : For comments
         - ^(\\s+.*)$: For continuations
         _ContinuationLine
         - Otherwise, the line is considered blank
        '''
        re_match = BaseConfigParser.REGEX_COMMENT.match(line)
        if (re_match is not None):
            return BaseConfigParser._CommentLine(re_match.group(1))
        # end if

        re_match = BaseConfigParser.REGEX_SECTION.match(line)
        if (re_match is not None):
            return BaseConfigParser._SectionLine(re_match.group(1))
        # end if

        re_match = BaseConfigParser.REGEX_PROPERTY.match(line)
        if (re_match is not None):
            return BaseConfigParser._PropertyLine(re_match.group(1), re_match.group(2))
        # end if

        re_match = BaseConfigParser.REGEX_BLANK.match(line)
        if (re_match is not None):
            return BaseConfigParser._BlankLine()
        # end if

        re_match = BaseConfigParser.REGEX_CONTINUATION.match(line)
        if (re_match is not None):
            return BaseConfigParser._ContinuationLine(re_match.group(1))
        # end if

        return BaseConfigParser._DebugLine(line)
    # end def _readLine

    def checkConsistency(self):
        '''
        Checks the consistency of the current config.

        The current config:
        - Must not have duplicated sections, such as:
          @code
          [SECTION]
          option1 = value
          [SECTION]
          option2 = value
          @endcode
        - Must not have duplicated options, such as:
          @code
          [SECTION]
          option = value1
          option = value2
          @endcode
        - Must not have unparsed lines, such as:
          @code
          [SECTION]
          This is an unparsable line
          option = value
          @endcode
        '''

        sectionSet = set()
        optionsSet = {}
        currentSection = None
        lineNumber     = 1
        lastLineObject = None
        for lineObject in self.objects:
            if (isinstance(lineObject, self._SectionLine)):
                currentSection = lineObject.value
                if (currentSection in sectionSet):
                    raise ValueError("Duplicated section: %s at line %d" % (currentSection, lineNumber))
                # end if
                sectionSet.add(currentSection)
            elif (isinstance(lineObject, self._PropertyLine)):
                currentOption         = lineObject.key
                currentSectionOptions = optionsSet.setdefault(currentSection, set())
                if (currentOption in currentSectionOptions):
                    raise ValueError("Duplicated option: \"%s\" in section \"%s\" at line %d" % (currentOption, currentSection, lineNumber))
                # end if
                currentSectionOptions.add(currentOption)
            elif (isinstance(lineObject, self._ContinuationLine)):
                if (    (lastLineObject is None)
                    or  (   (not isinstance(lastLineObject, self._PropertyLine))
                        and (not isinstance(lastLineObject, self._CommentLine)))):
                    raise ValueError("Unexpected RFC 822 continuation at line %d: <%s>" % (lineNumber, lineObject))
                # end if
            elif (isinstance(lineObject, self._DebugLine)):
                currentLine = lineObject.value
                raise ValueError("Unable to parse line %d: <%s>" % (lineNumber, currentLine,))
            # end if
            lastLineObject = lineObject
            lineNumber += 1
        # end for
    # end def checkConsistency

    def read(self, filenames):
        '''
        Reads a config from a list of filenames.

        @param  filenames [in] (string, tuple) A single filename, or a list of filenames to read.
        '''

        if (isinstance(filenames, str)):
            self.load(filenames)
        else:
            for filename in filenames:
                self.load(filename)
            # end for
        # end if
    # end def read

    def load(self, filename):
        '''
        Loads a file in the current object.

        @param  filename [in] (str) The file path to load.
        '''
        with open(filename) as configFile:
            self.load_string(configFile.read())
        # end with
    # end def load

    def load_string(self, value):
        '''
        Loads a string in the current object.

        @param  value [in] (str) The file contents to load
        '''
        # Merge sections and options
        if (len(self.objects) == 0):
            lines = value.split('\n')
            self.objects = [self._readLine(line.rstrip(' \b\r\n')) for line in lines]
        else:
            newInstance = self.__class__()
            newInstance.load_string(value)

            for section in newInstance.sections():
                for option in newInstance.options(section):
                    value = newInstance.get(section, option)
                    self.set(section, option, value)
                # end for
            # end for
        # end if

        self.checkConsistency()
    # end def load_string

    def write(self, targetfile):
        '''
        Saves the current config to a file.

        @param  targetfile [in] (string, file) The name of the file to write to, or a file object.
        '''

        if (isinstance(targetfile, str)):
            configFile = open(targetfile, "w+")
        else:
            configFile = targetfile
        # end if

        configFile.write(self.write_string())
        configFile.close()
    # end def write

    def write_string(self):
        '''
        Saves the current config to a string

        @return The current config, as a string
        '''
        lines = [str(subObject) for subObject in self.objects if not (    (isinstance(subObject, self._PropertyLine)
                                                                      and (subObject.value is None)))]

        return "\n".join(lines)
    # end def write_string

    def has_section(self, section):
        '''
        Tests whether the current configuration has the specified section.

        This returns False if the section was not found.

        @param  section [in] (str) The section to lookup
        @return (bool) Whether the section was found.
        '''
        return section in self.sections()
    # end def has_section

    def has_option(self, section, option):
        '''
        Tests whether the current configuration has the specified option.

        This returns False:
        - If no option is found,
        - or the value of the option is None

        @param  section [in] (str) The section where the option is located
        @param  option  [in] (str) The name of the option to locate.

        @return (bool) Whether the option is present.
        '''

        return (self.get(section, option) != None)
    # end def has_option

    def remove_section(self, section):
        '''
        Removes a given section and all its options.

        @param  section [in] (str) The name of the section to remove.
        '''
        newObjects = []
        state = self.STATE_LOOKING_FOR_SECTION
        for subObject in self.objects:
            if (    (state == self.STATE_LOOKING_FOR_SECTION)
                and (subObject.__class__ is BaseConfigParser._SectionLine)
                and (subObject.value == section)):
                state = self.STATE_LOOKING_FOR_PROPERTY
            elif (  (state == self.STATE_LOOKING_FOR_PROPERTY)
                and (subObject.__class__ is BaseConfigParser._SectionLine)):
                state = self.STATE_LOOKING_FOR_SECTION
            # end if

            if (state == self.STATE_LOOKING_FOR_SECTION):
                newObjects.append(subObject)
            # end if
        # end for

        self.objects = newObjects
    # end def remove_section

    def remove_option(self, section, option):
        '''
        Removes a given option from the config.

        @param  section [in] (str) The section where the option is located
        @param  option  [in] (str) The name of the option to locate.
        '''

        self.set(section, option, None)
    # end def remove_option

    def get(self, section,
                  option,
                  default = None):
        '''
        Obtain the option in the given section

        @param  section [in] (str) The section where the option is located.
        @param  option  [in] (str) The name of the option to read
        @param  default [in] (object) The default value if the option is not found.

        @return The value associated with this option
        '''

        result = default
        value = None

        state = self.STATE_LOOKING_FOR_SECTION

        for subObject in self.objects:
            if (    (state == self.STATE_LOOKING_FOR_SECTION)
                and (subObject.__class__ is BaseConfigParser._SectionLine)
                and (subObject.value == section)):
                state = self.STATE_LOOKING_FOR_PROPERTY
            elif (  (state == self.STATE_LOOKING_FOR_PROPERTY)
                and (subObject.__class__ is BaseConfigParser._PropertyLine)
                and (subObject.key == option)):
                value = str(subObject.value)
                state = self.STATE_LOOKING_FOR_CONTINUATION
            elif (  (state == self.STATE_LOOKING_FOR_PROPERTY)
                and (subObject.__class__ is BaseConfigParser._SectionLine)):
                break
            elif (  (state == self.STATE_LOOKING_FOR_CONTINUATION)
                and (subObject.__class__ is BaseConfigParser._ContinuationLine)):
                value += subObject.value
            elif (  (state == self.STATE_LOOKING_FOR_CONTINUATION)
                and (subObject.__class__ is not BaseConfigParser._ContinuationLine)):
                break
            # end if
        # end for

        if (value is not None):
            result = value
        # end if

        return result
    # end def get

    def set(self, section, option, value):                                                                              #@ReservedAssignment
        '''
        Sets a value for the given option in the given section.

        @param  section [in] (str) The section in which the option is located.
        @param  option  [in] (str) The option for which to write the value.
        @param  value   [in] (str) The value to write.
        '''

        lastProperty = 0
        state = self.STATE_LOOKING_FOR_SECTION

        index = 0
        for subObject in self.objects:
            if (    (state == self.STATE_LOOKING_FOR_SECTION)
                and (subObject.__class__ is BaseConfigParser._SectionLine)
                and (subObject.value == section)):
                state = self.STATE_LOOKING_FOR_PROPERTY
                lastProperty = index
            elif (  (state == self.STATE_LOOKING_FOR_PROPERTY)
                and (subObject.__class__ is BaseConfigParser._PropertyLine)):
                if (subObject.key == option):
                    subObject.value = value
                    state = self.STATE_LOOKING_FOR_CONTINUATION
                # end if
                lastProperty = index
            elif (  (state == self.STATE_LOOKING_FOR_PROPERTY)
                and (subObject.__class__ is BaseConfigParser._SectionLine)):
                # Create a new property in the section
                self.objects.insert(lastProperty+1, BaseConfigParser._PropertyLine(option, value))
                return
            elif (  (state == self.STATE_LOOKING_FOR_CONTINUATION)
                and (subObject.__class__ is BaseConfigParser._ContinuationLine)):
                pass
            elif (  (state == self.STATE_LOOKING_FOR_CONTINUATION)
                and (subObject.__class__ is not BaseConfigParser._ContinuationLine)):
                # Delete the continuation lines
                del self.objects[lastProperty+1:index]
                return
            # end if
            index += 1
        # end for

        # This occurs if we are setting an as-yet-unknown property in the last section.
        if (state == self.STATE_LOOKING_FOR_PROPERTY):
            self.objects.insert(lastProperty+1, BaseConfigParser._PropertyLine(option, value))
            return
        # This occurs if the property was found and set, but no continuation
        # line was found
        elif (state == self.STATE_LOOKING_FOR_CONTINUATION):
            return
        # end if

        # Section not found: insert it after all the data
        self.objects.append(BaseConfigParser._SectionLine(section))
        self.objects.append(BaseConfigParser._PropertyLine(option, value))

        self.checkConsistency()
    # end def set

    def add_section(self, section):
        '''
        Adds an empty section to a configuration.

        @param  section [in] (str) The name of the section to add.
        '''
        for subObject in self.objects:
            if (    (subObject.__class__ is BaseConfigParser._SectionLine)
                and (subObject.value == section)):
                return
            # end if
        # end for

        # Section not found: insert it after all the data
        self.objects.append(BaseConfigParser._SectionLine(section))

        self.checkConsistency()
    # end def add_section


    def sections(self):
        '''
        Obtains a list of section names.

        @return a list of section names.
        '''
        return [sectionLine.value for sectionLine in self.objects if isinstance(sectionLine, self._SectionLine)]
    # end def sections

    def options(self, section):
        '''
        Obtains a list of option names for the given section.

        @param  section [in] (str) The section for which to obtain the list of options.

        @return (list) The list of available options for this section.
        '''

        result = []

        inSection = False
        for lineObject in self.objects:
            if (isinstance(lineObject, self._SectionLine)):
                if (inSection):
                    return result
                elif (lineObject.value == section):
                    inSection = True
                # end if
            elif (    (inSection)
                  and (isinstance(lineObject, self._PropertyLine))):
                value = lineObject.key
                result.append(value)
            # end if
        # end for

        return result
    # end def options

    def __str__(self):
        '''
        Writes the current configuration to a string

        @return (str) The current configuration, as a string.
        '''
        lines = [str(subObject) for subObject in self.objects if not (    (isinstance(subObject, self._PropertyLine)
                                                                and (subObject.value is None)))]

        return "\n".join(lines)
    # end def __str__

    def add_comment(self, comment, section=None, option=None, mode=MODE_BEFORE):
        '''
        Adds a comment in the config file.

        The place the comment is added depends
        - on the section/option combination
        - on the mode, which can be BEFORE, INSIDE, AFTER

        Example:
        This adds a comment at the beginning of the file.
        @code
        config.add_comment("my comment")
        @endcode
        and will result in
        @code
        # my comment
        [SECTION]
        option = 1
        @endcode

        This adds a comment at the end of the file
        @code
        config.add_comment("my comment", mode=AFTER)
        @endcode
        and will result in
        @code
        [SECTION]
        option = 1
        # my comment
        @endcode

        This adds a comment before the beginning of section [SECTION]
        @code
        config.add_comment("my comment", "SECTION")
        @endcode
        and will result in
        @code
        [SECTION]
        # my comment
        option = 1
        @endcode

        @param  comment [in] (str) The comment to insert
        @option section [in] (str) The section to insert this comment in.
                                     None if the section is irrelevant
        @option option  [in] (str) The option to insert this comment in.
                                     None if the option is irrelevant
        @option mode    [in] (str) The mode the comment will be inserted in.
        '''
        commentLines = [self._CommentLine(x) for x in comment.strip().split("\n")]

        self._add_lines(commentLines, 'comment', section, option, mode)
    # end def add_comment

    def add_blank(self, section=None, option=None, mode=MODE_BEFORE):
        '''
        Adds a blank line in the config file.

        The place the blank line is added depends
        - on the section/option combination
        - on the mode, which can be BEFORE, INSIDE, AFTER

        Example:
        This adds a blank line at the beginning of the file.
        @code
        config.add_blank()
        @endcode
        and will result in
        @code

        [SECTION]
        option = 1
        @endcode

        This adds a blank line at the end of the file
        @code
        config.add_blank(mode=AFTER)
        @endcode
        and will result in
        @code
        [SECTION]
        option = 1

        @endcode

        This adds a comment before the beginning of section [SECTION]
        @code
        config.add_blank("SECTION")
        @endcode
        and will result in
        @code
        [SECTION]

        option = 1
        @endcode

        @param  section [in] (str) The section to insert this comment in.
                                     None if the section is irrelevant
        @param  option  [in] (str) The option to insert this comment in.
                                     None if the option is irrelevant
        @param  mode    [in] (str) The mode the comment will be inserted in.
        '''
        self._add_lines((self._BlankLine(),), 'blank line', section, option, mode)
    # end def add_blank

    def _add_lines(self, lines,                                                                                         # pylint:disable=R0912
                         linetype,
                         section = None,
                         option  = None,
                         mode    = MODE_BEFORE):
        '''
        Adds a list of lines in the config file.

        The place the lines is added depends
        - on the section/option combination
        - on the mode, which can be BEFORE, INSIDE, AFTER

        Example:
        This adds a line at the beginning of the file.
        @code
        config._add_lines((config._CommentLine('my comment'),))
        @endcode
        and will result in
        @code
        # my comment
        [SECTION]
        option = 1
        @endcode

        This adds a comment at the end of the file
        @code
        config._add_lines((config._CommentLine('my comment'),), mode=AFTER)
        @endcode
        and will result in
        @code
        # my comment
        [SECTION]
        option = 1
        @endcode

        This adds a comment before the beginning of section [SECTION]
        @code
        config._add_lines((config._CommentLine('my comment'),), "SECTION")
        @endcode
        and will result in
        @code
        [SECTION]
        # my comment
        option = 1
        @endcode

        @param  lines    [in] (tuple)  The lines to insert
        @param  linetype [in] (str) The type of the lines to insert.
        @option section  [in] (str) The section to insert this comment in.
                                      None if the section is irrelevant
        @option option   [in] (str) The option to insert this comment in.
                                      None if the option is irrelevant
        @option mode     [in] (str) The mode the comment will be inserted in.
        '''
        # If no section is specified, the file is the reference
        if (section is None):
            if (mode == self.MODE_BEFORE):
                self.objects[0:0] = lines
            elif (mode == self.MODE_AFTER):
                self.objects.extend(lines)
            else:
                raise ValueError("Invalid mode for %s insertion: %s" % (linetype, mode,))
            # end if
        elif (option is None):
            # If no option is specified, the section is the reference
            found    = False
            inserted = False
            index = 0
            while index < len(self.objects):
                objectLine = self.objects[index]
                if (    (isinstance(objectLine, self._SectionLine)
                    and (objectLine.value == section))):
                    found = True
                    # Process the cases where:
                    if (mode == self.MODE_BEFORE):
                        # The comments must be inserted BEFORE the section declaration
                        self.objects[index:index] = lines
                        inserted = True
                        index += len(lines)
                    elif (mode == self.MODE_INSIDE):
                        # The comments must be inserted immediately following the section declaration
                        self.objects[index+1:index+1] = lines
                        inserted = True
                        index += len(lines)
                    # end if
                elif (    (isinstance(objectLine, self._SectionLine)
                      and (objectLine.value != section))):
                    if (found) and (not inserted):
                        # The comments must be inserted before the following section declaration
                        self.objects[index:index] = lines
                        inserted = True
                        index += len(lines)
                    # end if
                # end if
                index += 1
            # end while
            if (found):
                if (not inserted):
                    # No section found, append at the end of the file.
                    self.objects.extend(lines)
                # end if
            else:
                raise ValueError("Section %s not found" % (section,))
            # end if
        else:
            # Both section and option are specified, the option is the reference
            state = self.STATE_LOOKING_FOR_SECTION
            inserted = False
            index = 0
            while (index < len(self.objects)):
                objectLine = self.objects[index]
                if (    (state == self.STATE_LOOKING_FOR_SECTION)
                    and (isinstance(objectLine, self._SectionLine))
                    and (objectLine.value == section)):
                    state = self.STATE_LOOKING_FOR_PROPERTY
                elif (    (state == self.STATE_LOOKING_FOR_PROPERTY)
                    and (isinstance(objectLine, self._PropertyLine))
                    and (objectLine.key == option)
                    and (not inserted)):
                    # A property was found
                    if (mode == self.MODE_BEFORE):
                        self.objects[index:index] = lines
                        inserted = True
                        index += len(lines)
                    elif (mode == self.MODE_AFTER):
                        self.objects[index+1:index+1] = lines
                        inserted = True
                        index += len(lines)
                    else:
                        raise ValueError("Invalid mode for %s insertion: %s" % (linetype, mode,))
                    # end if
                    inserted = True
                # end if
                index += 1
            # end while

            if (not inserted):
                raise ValueError("Unable to insert %s" % (linetype,))
            # end if
        # end if
    # end def _add_lines
# end class BaseConfigParser

class ConfigParser(BaseConfigParser):
    '''
    Utility class for config parsing, providing a default value, and advanced parsing
    '''

    def __init__(self, strict=False):
        '''
        constructor

        @option strict [in] (bool) Whether the parsing is STRICT of not.
        '''
        super(ConfigParser, self).__init__(strict)
    # end def __init__

    INT_REGEX    = re.compile("[0-9]+")
    STRING_REGEX = re.compile("[\"'].*[\"']")
    HEX_REGEX    = re.compile("0x[0-9A-Fa-f]+")
    HEXBUF_REGEX = re.compile("\\[(?:[0-9A-Fa-f]{2}\\s*)+\\]")
    LIST_REGEX   = re.compile("\\(.+.*\\)")
    BOOL_REGEX   = re.compile("(True)|(False)")

    def __parseValue(self, section,
                           option,
                           readValue,
                           default = None):
        '''
        Extracts the contents of a read value.

        @param  section   [in] (str) indicative section
        @param  option    [in] (str) indicative option
        @param  readValue [in] (str) the value read from the file
        @option default   [in] (object) Default value

        @return (object) The parsed value
        '''
        if (    (readValue is not None)
            and (isinstance(readValue, str))
            and (readValue is not default)):

            if (self.HEX_REGEX.match(readValue)):
                value = int(readValue[2:], 16)
            elif (self.INT_REGEX.match(readValue)):
                value = int(readValue)
            elif (self.STRING_REGEX.match(readValue)):
                value = readValue[1:-1]
            elif (self.HEXBUF_REGEX.match(readValue)):
                value = HexList(readValue[1:-1])
            elif (self.BOOL_REGEX.match(readValue)):
                value = True
                if (readValue == "False"):
                    value = False
                # end if
            elif (self.LIST_REGEX.match(readValue)):
                values = (v for v in readValue[1:-1].split(',')
                             if (len(v) > 0))
                value = tuple((self.__parseValue(section, option, v) for v in values))
            elif (readValue == "None"):
                value = None
            elif (not self.strict):
                value = readValue.strip()
            else:
                # The value does not match a strict interpretation
                # This is an error
                raise ValueError("In section %s, option %s, unable to parse: %s" % \
                    (section, option, readValue))
            # end if
            return value
        # end if

        return readValue
    # end def __parseValue

    def get(self, section, option, default=None):
        '''
        @copydoc pylibrary.tools.config.BaseConfigParser.get
        '''
        readValue = super(ConfigParser, self).get(section, option, default)

        return self.__parseValue(section, option, readValue, default)
    # end def get

    def __unparseValue(self, value):
        '''
        Formats the value for writing

        @param  value [in] (object) the value to be written to a file

        @return The un-parsed value
        '''
        itemType = value.__class__

        writtenValue = value
        if (itemType is int):
            writtenValue = str(value)
        elif (issubclass(itemType, str)):
            writtenValue = "\"%s\"" % value
        elif (itemType is HexList):
            writtenValue = "[%s]" % (" ".join(["%02.2X" % x for x in value]))
        elif (value is None):
            writtenValue = "None"
        elif (value in (True, False)):
            writtenValue = str(value)
        elif (  (itemType is list)
            or  (itemType is tuple)):
            writtenValue = "(" + ",".join([self.__unparseValue(v) for v in value]) + ")"
        elif not self.strict:
            writtenValue = value
        else:
            # The value does not match a strict interpretation
            # This is an error
            raise ValueError("The value %s cannot be written" % (str(value),))
        # end if

        return writtenValue
    # end def __unparseValue

    def set(self, section, option, value):                                                                              #@ReservedAssignment
        '''
        @copydoc pylibrary.tools.config.BaseConfigParser.set
        '''

        # Translate typed parameters to string format
        writtenValue = self.__unparseValue(value)

        super(ConfigParser, self).set(section, option, writtenValue)
    # end def set
# end class ConfigParser

class CachingConfigParser(object):
    '''
    A ConfigParser-like object, that provides an in-memory cache of values
    '''

    IMMUTABLE_APIS = ('get', 'has_option', 'has_section', 'options', 'sections')
    MUTABLE_APIS   = ('add_blank', 'add_comment', 'add_section', 'load', 'load_string', 'read', 'remove_option', 'remove_section', 'set')

    def __init__(self, configParser):
        '''
        Constructor

        @param  configParser [in] (BaseConfigParser) ConfigParser to cache.
        '''
        self.__configParser = configParser

        for mutableApiName in self.MUTABLE_APIS:
            self.__createMutableApi(mutableApiName)
        # end for

        self.__reInitCache()
    # end def __init__

    def __createImmutableApi(self, immutableApiName):
        '''
        Creates a mutable proxy.

        @param  immutableApiName [in] (str) Name of the API to decorate.
        '''
        immutableApiTarget = getattr(self.__configParser, immutableApiName)
        immutableApiCache  = {}
        def immutableApi(*args, **kwArgs):
            '''
            Actual proxy

            @param  args [in] (tuple) Arguments
            @param  kwArgs [in] (dict) Keyword arguments

            @return API result
            '''
            key = (args, str(kwArgs) if (len(kwArgs)) else None)
            if (key not in immutableApiCache):
                immutableApiCache[key] = immutableApiTarget(*args, **kwArgs)
            # end if

            return immutableApiCache[key]
        # end def immutableApi

        setattr(self, immutableApiName, immutableApi)
    # end def __createImmutableApi

    def __createMutableApi(self, mutableApiName):
        '''
        Creates a mutable proxy.

        @param  mutableApiName [in] (str) Name of the API to decorate.
        '''
        mutableApiTarget = getattr(self.__configParser, mutableApiName)
        def mutableApi(*args, **kwArgs):
            '''
            Actual proxy

            @option args   [in] (tuple) Arguments
            @option kwArgs [in] (dict)  Keyword arguments

            @return API result
            '''
            self.__reInitCache()
            return mutableApiTarget(*args, **kwArgs)
        # end def mutableApi

        setattr(self, mutableApiName, mutableApi)
    # end def __createMutableApi

    def __reInitCache(self):
        '''
        Clears the mutable cache
        '''
        for immutableApiName in self.IMMUTABLE_APIS:
            self.__createImmutableApi(immutableApiName)
        # end for
    # end def __reInitCache

    def __getattr__(self, name):
        '''
        When attempting to use another attribute, assume a transparent API, with no caching.

        @param  name [in] (str) name of the attribute to obtain.

        @return (object) attribute value
        '''
        return getattr(self.__configParser, name)
    # end def __getattr__
# end class CachingConfigParser

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
