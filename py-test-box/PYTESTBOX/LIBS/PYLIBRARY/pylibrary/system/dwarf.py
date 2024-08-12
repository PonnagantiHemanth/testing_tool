#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.system.dwarf

@brief  DWARF debug info parser implementation

@author christophe.roquebert

This follows DWARF's standard V2.0.0, but only implements a limited subset of

@date   2018/09/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.numeral            import Numeral
from pylibrary.tools.strutils          import StrAbleMixin

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

def _read_block(buffer, offset, count):                                                                                 #@ReservedAssignment pylint:disable=W0622
    '''
    Reads a block of data

    @param  buffer [in] (HexList) The buffer to read from.
    @param  offset [in] (int) The offset at which to start reading
    @param  count  [in] (int) The number of bytes the value is encoded on

    @return (value, newOffset)
    '''
    return buffer[offset:offset+count], offset+count
# end def _read_block

def _read_un(buffer, offset, count):                                                                                    #@ReservedAssignment pylint:disable=W0622
    '''
    Reads an unsigned integer encoded on a fixed number of bytes

    @param  buffer [in] (HexList) The buffer to read from.
    @param  offset [in] (int) The offset at which to start reading
    @param  count  [in] (int) The number of bytes the value is encoded on

    @return (value, newOffset)
    '''
    if (len(buffer) < (offset+count)):
        raise IndexError('Index out of bounds: %d' % (max(min(len(buffer), offset+count), offset)))
    # end if

    return int(Numeral(buffer[offset:offset+count], littleEndian = True)), offset + count
# end def _read_un

def _read_sn(buffer, offset, count):                                                                                    #@ReservedAssignment pylint:disable=W0622
    '''
    Reads an unsigned integer encoded on a fixed number of bytes

    @param  buffer [in] (HexList) The buffer to read from.
    @param  offset [in] (int) The offset at which to start reading
    @param  count  [in] (int) The number of bytes the value is encoded on

    @return (value, newOffset)
    '''
    if (len(buffer) < (offset+count)):
        raise IndexError('Index out of bounds: %d' % (max(min(len(buffer), offset+count), offset)))
    # end if

    value, offset = _read_un(buffer, offset, count)
    return (value if value < (1 << ((count * 8) - 1)) else value - (1 << (count * 8))), offset
# end def _read_sn

def _read_uword(buffer, offset):                                                                                        #@ReservedAssignment pylint:disable=W0622
    '''
    Reads an unsigned integer encoded on 4 bytes

    @param  buffer [in] (HexList) The buffer to read from.
    @param  offset [in] (int) The offset at which to start reading

    @return (value, newOffset)
    '''
    return _read_un(buffer, offset, 4)
# end def _read_uword

def _read_sword(buffer, offset):                                                                                        #@ReservedAssignment pylint:disable=W0622
    '''
    Reads a signed integer encoded on 4 bytes

    @param  buffer [in] (HexList) The buffer to read from.
    @param  offset [in] (int) The offset at which to start reading

    @return (value, newOffset)
    '''
    return _read_sn(buffer, offset, 4)
# end def _read_sword

def _read_uhalf(buffer, offset):                                                                                        #@ReservedAssignment pylint:disable=W0622
    '''
    Reads an unsigned integer encoded on 2 bytes

    @param  buffer [in] (HexList) The buffer to read from.
    @param  offset [in] (int) The offset at which to start reading

    @return (value, newOffset)
    '''
    return _read_un(buffer, offset, 2)
# end def _read_uhalf

def _read_shalf(buffer, offset):                                                                                        #@ReservedAssignment pylint:disable=W0622
    '''
    Reads a signed integer encoded on 2 bytes

    @param  buffer [in] (HexList) The buffer to read from.
    @param  offset [in] (int) The offset at which to start reading

    @return (value, newOffset)
    '''
    return _read_sn(buffer, offset, 2)
# end def _read_shalf

def _read_ubyte(buffer, offset):                                                                                        #@ReservedAssignment pylint:disable=W0622
    '''
    Reads an unsigned integer encoded on 1 byte

    @param  buffer [in] (HexList) The buffer to read from.
    @param  offset [in] (int) The offset at which to start reading

    @return (value, newOffset)
    '''
    return _read_un(buffer, offset, 1)
# end def _read_ubyte

def _read_sbyte(buffer, offset):                                                                                        #@ReservedAssignment pylint:disable=W0622
    '''
    Reads a signed integer encoded on 1 byte

    @param  buffer [in] (HexList) The buffer to read from.
    @param  offset [in] (int) The offset at which to start reading

    @return (value, newOffset)
    '''
    return _read_sn(buffer, offset, 1)
# end def _read_sbyte

def _read_string(buffer, offset):                                                                                       #@ReservedAssignment pylint:disable=W0622
    '''
    Reads null-terminated string

    @param  buffer [in] (HexList) The buffer to read from.
    @param  offset [in] (int) The offset at which to start reading

    @return (value, newOffset)
    '''
    count = 0
    while (buffer[offset+count] != 0):
        count += 1
    # end while

    return buffer[offset:offset+count].toString(), offset+count+1
# end def _read_string

def _read_uleb128(buffer, offset):                                                                                      #@ReservedAssignment pylint:disable=W0622
    '''
    Reads a variable-length-encoded unsigned integer

    @param  buffer [in] (HexList) The buffer to read from.
    @param  offset [in] (int) The offset at which to start reading

    @return (value, newOffset)
    '''
    result = 0
    loop = True
    shift = 0
    while (loop):
        value, offset = _read_ubyte(buffer, offset)
        loop = (value & 0x80) != 0
        value = value & 0x7F

        result = result | (value << shift)
        shift += 7
    # end while

    return result, offset
# end def _read_uleb128

def _read_sleb128(buffer, offset):                                                                                      #@ReservedAssignment pylint:disable=W0622
    '''
    Reads a variable-length-encoded signed integer

    @param  buffer [in] (HexList) The buffer to read from.
    @param  offset [in] (int) The offset at which to start reading

    @return (value, newOffset)
    '''
    result = 0
    loop = True
    shift = 0
    while (loop):
        value, offset = _read_ubyte(buffer, offset)
        loop = (value & 0x80) != 0
        value = value & 0x7F

        result = result | (value << shift)
        shift += 7
    # end while

    result = result if (result < (1 << (shift - 1))) else (result - (1 << shift))

    return result, offset
# end def _read_sleb128

class DebugLineSection(StrAbleMixin):
    '''
    Interpretation of the debug_line section of a DWARF file.

    The debug_line section is actually a script, that unfolds the contents of
    the debug line information to memory.

    Usage:
    1. Read the section in a HexList
    2. Create a DebugLineSection on this buffer
    3. Use decode(offset) to start decoding at the given offset.
    @c decode returns a matrix, mapping addresses to informations in the prologue
    '''

    _STRABLE_FIELDS = ('entry_sets',)

    class EntrySet(StrAbleMixin):
        '''
        An entry set in the .debug_line section

        It consists in a prologue, and statements.
        '''
        _STRABLE_FIELDS = ('prologue', 'statements')

        class Registers(object):
            '''
            The FSM registers
            '''

            def __init__(self, address      = 0,
                               file         = 1,                                                                        #@ReservedAssignment pylint:disable=W0622
                               line         = 1,
                               column       = 0,
                               is_stmt      = False,
                               basic_block  = False,
                               end_sequence = False,
                               prologue     = None):
                '''
                Constructor

                @option address      [in] (int) The starting address
                @option file         [in] (int) Index in the prologue's file_names list
                @option line         [in] (int) Index of the line in the current file
                @option column       [in] (int) Index of the column in the current file
                @option is_stmt      [in] (bool) Whether the current address is a statement
                @option basic_block  [in] (bool) Whether the current address starts a block
                @option end_sequence [in] (bool) Whether the sequence has ended
                @option prologue     [in] (Prologue) The prologue to initialize the registers with
                '''
                self._address      = address
                self.file         = file
                self.line         = line
                self.column       = column
                self.is_stmt      = is_stmt
                self.basic_block  = basic_block
                self.end_sequence = end_sequence

                if (prologue is not None):
                    self.reset(prologue)
                # end if

                self.last_address = None
            # end def __init__

            def getAddress(self):
                '''
                Obtain the current address

                @return (int) The current address
                '''
                return self._address
            # end def getAddress

            def setAddress(self, address):
                '''
                Sets the current address, saving the last_address

                @param  address [in] (int) The address to set
                '''
                self.last_address, self._address = self._address, address
            # end def setAddress

            address = property(getAddress, setAddress)

            def reset(self, prologue):
                '''
                Resets the current registers, using the defaults from the prologue.

                @param  prologue [in] (Prologue) The prologue to initialize with.
                '''
                self.address      = 0
                self.file         = 1
                self.line         = 1
                self.column       = 0
                self.is_stmt      = prologue.default_is_stmt
                self.basic_block  = False
                self.end_sequence = False

                self.last_address = None
            # end def reset
        # end class Registers

        class Prologue(StrAbleMixin):
            '''
            Wrapper/decoder for a .debug_line prologue.
            '''

            _STRABLE_FIELDS = ('total_length',
                               'version',
                               'prologue_length',
                               'minimum_instruction_length',
                               'default_is_stmt',
                               'line_base',
                               'line_range',
                               'opcode_base',
                               'standard_opcode_lengths',
                               'include_directories',
                               'file_names')

            def __init__(self, total_length,
                               version,
                               prologue_length,
                               minimum_instruction_length,
                               default_is_stmt,
                               line_base,
                               line_range,
                               opcode_base,
                               standard_opcode_lengths,
                               include_directories,
                               file_names):
                '''
                Constructor.

                @param  total_length               [in] (int)  The size in bytes of the statement information for
                                                              this compilation unit (not including the
                                                              total_length field itself).
                @param  version                    [in] (int)  Version identifier for the statement information format.
                @param  prologue_length            [in] (int)  The number of bytes following the prologue_length
                                                              field to the beginning of the first byte of
                                                              the statement program itself
                @param  minimum_instruction_length [in] (int)  The size in bytes of the smallest target
                                                              machine instruction.  Statement program opcodes
                                                              that alter the address register first multiply
                                                              their operands by this value.
                @param  default_is_stmt            [in] (bool)  The initial value of the is_stmt register.
                @param  line_base                  [in] (int)  This parameter affects the meaning of the special opcodes.
                @param  line_range                 [in] (int)  This parameter affects the meaning of the special opcodes.
                @param  opcode_base                [in] (int)  The number assigned to the first special opcode.
                @param  standard_opcode_lengths    [in] (list) Number of LEB128 opcodes for standard opcodes
                @param  include_directories        [in] (list) list of path names
                @param  file_names                 [in] (list) list of (name, drectory_index, time, size)
                '''
                super(DebugLineSection.EntrySet.Prologue, self).__init__()

                self.total_length               = total_length
                self.version                    = version
                self.prologue_length            = prologue_length
                self.minimum_instruction_length = minimum_instruction_length
                self.default_is_stmt            = default_is_stmt
                self.line_base                  = line_base
                self.line_range                 = line_range
                self.opcode_base                = opcode_base
                self.standard_opcode_lengths    = standard_opcode_lengths
                self.include_directories        = include_directories
                self.file_names                 = file_names
            # end def __init__

            @classmethod
            def fromHexList(cls, buffer, offset):                                                                        #@ReservedAssignment pylint:disable=W0622
                '''
                Build a new object from buffer

                @param  buffer [in] (HexList) The buffer to build the object from.
                @param  offset [in] (int) The offset at which to start reading.

                @return (Prologue) A new Prologue instance
                '''

                total_length, offset               = _read_uword(buffer, offset)
                version, offset                    = _read_uhalf(buffer, offset)
                prologue_length, offset            = _read_uword(buffer, offset)
                minimum_instruction_length, offset = _read_ubyte(buffer, offset)
                default_is_stmt, offset            = _read_ubyte(buffer, offset)
                line_base, offset                  = _read_sbyte(buffer, offset)
                line_range, offset                 = _read_ubyte(buffer, offset)
                opcode_base, offset                = _read_ubyte(buffer, offset)

                standard_opcode_lengths = {}
                for opcode in range(1, opcode_base):
                    opcode_length, offset = _read_ubyte(buffer, offset)
                    standard_opcode_lengths[opcode] = opcode_length
                # end for

                include_directories = ['.']
                loop = True
                while (loop):
                    include_directory, offset = _read_string(buffer, offset)
                    if (len(include_directory)):
                        include_directories.append(include_directory)
                    else:
                        loop = False
                    # end if
                # end while

                file_names = [None]
                loop = True
                while (loop):
                    file_name, offset = _read_string(buffer, offset)
                    if (len(file_name)):
                        directory_index, offset = _read_uleb128(buffer, offset)
                        last_modification_time, offset = _read_uleb128(buffer, offset)
                        byte_length, offset = _read_uleb128(buffer, offset)

                        file_names.append((file_name, directory_index, last_modification_time, byte_length))
                    else:
                        loop = False
                    # end if
                # end while

                return cls(total_length,
                           version,
                           prologue_length,
                           minimum_instruction_length,
                           default_is_stmt,
                           line_base,
                           line_range,
                           opcode_base,
                           standard_opcode_lengths,
                           include_directories,
                           file_names)
            # end def fromHexList
        # end class Prologue

        class Opcode(object):
            '''
            Base class for opcodes

            This defines the interface for opcode statement processors

            Usage:
            1. Use accept to find it the opcode matches the given position
            2. Create an instance
            3. Call it
            '''

            def getLength(self):
                '''
                Obtains the length of the opcode and operands.

                @return The length of the opcode and its operands
                '''
                raise NotImplementedError
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                Whether the opcode is acceptable for the given position.

                @param  prologue [in] (Prologue) The prologue used for decoding the opcode
                @param  buffer   [in] (HexList)   The buffer from which to read the opcode
                @param  offset   [in] (int)      The offset at which to read the opcode.

                @return (bool) True if the opcode can decode the given position
                '''
                raise NotImplementedError
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                Working method.

                @param  prologue  [in] (Prologue)  The prologue used to execute the opcode
                @param  registers [in] (Registers) The registers context
                @param  matrix    [in] (list)      The matrix collector
                '''
                raise NotImplementedError
            # end def __call__

            def __str__(self):
                '''
                Converts the current object to a string

                @return (str) The current object, as a string.
                '''
                raise NotImplementedError
            # end def __str__

            @staticmethod
            def _appendRow(registers, matrix):
                '''
                Append a row to the matrix, using the current registers

                @param  registers [in] (Registers) The current registers state.
                @param  matrix    [in] (dict) The current matrix collector
                '''
                last_entry = matrix.get(registers.last_address, None)
                if (last_entry is not None):
                    for address in range(registers.last_address, registers.address):
                        matrix[address] = last_entry
                    # end for
                # end if

                matrix[registers.address] = ((registers.address,
                                              registers.file,
                                              registers.line,
                                              registers.column,
                                              registers.is_stmt,
                                              registers.basic_block))
            # end def _appendRow
        # end class Opcode

        class SpecialOpcode(Opcode):
            '''
            SPECIAL opcode.
            '''
            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.SpecialOpcode, self).__init__()
                adjusted_opcode = buffer[offset] - prologue.opcode_base

                self._add_address = adjusted_opcode / prologue.line_range
                self._add_line    = prologue.line_base + (adjusted_opcode % prologue.line_range)
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'SPECIAL (%d, %s)' % (self._add_address, self._add_line)
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return 1
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                return (buffer[offset] >= prologue.opcode_base)
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''
                registers.address += self._add_address
                registers.line    += self._add_line

                self._appendRow(registers, matrix)

                registers.basic_block = False
            # end def __call__
        # end class SpecialOpcode

        # The matrix: address, sourceFileName, sourceLineNumber, sourceColumnNumber, beginSourceStatement, beginBasicBlock
        MATRIX = []

        class CopyStandardOpcode(Opcode):
            '''
            COPY opcode
            '''

            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0613,W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.CopyStandardOpcode, self).__init__()
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'DW_LNS_copy'
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return 1
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                return (buffer[offset] == 1)
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''

                self._appendRow(registers, matrix)
            # end def __call__
        # end class CopyStandardOpcode

        class AdvancePcStandardOpcode(Opcode):
            '''
            ADVANCE PC opcode
            '''

            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.AdvancePcStandardOpcode, self).__init__()

                leb128, finalOffset = _read_uleb128(buffer, offset+1)
                self._add_address = prologue.minimum_instruction_length * leb128
                self._length = finalOffset - offset
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'DW_LNS_advance_pc += %d' % self._add_address
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return self._length
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                return (buffer[offset] == 2)
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''
                registers.address += self._add_address
            # end def __call__
        # end class AdvancePcStandardOpcode

        class AdvanceLineStandardOpcode(Opcode):
            '''
            ADVANCE LINE opcode
            '''

            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0613,W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.AdvanceLineStandardOpcode, self).__init__()

                self._leb128, finalOffset = _read_uleb128(buffer, offset+1)
                self._length = finalOffset - offset
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'DW_LNS_advance_line += %d' % self._leb128
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return self._length
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                return buffer[offset] == 3
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''
                registers.line += self._leb128
            # end def __call__
        # end class AdvanceLineStandardOpcode

        class SetFileStandardOpcode(Opcode):
            '''
            SET FILE opcode
            '''

            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0613,W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.SetFileStandardOpcode, self).__init__()

                self._leb128, finalOffset = _read_uleb128(buffer, offset+1)
                self._length = finalOffset - offset
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'DW_LNS_set_file = %d' % self._leb128
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return self._length
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                return buffer[offset] == 4
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''
                registers.file = self._leb128
            # end def __call__
        # end class SetFileStandardOpcode

        class SetColumnStandardOpcode(Opcode):
            '''
            SET COLUMN opcode
            '''

            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0613,W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.SetColumnStandardOpcode, self).__init__()

                self._leb128, finalOffset = _read_uleb128(buffer, offset+1)
                self._length = finalOffset - offset
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'DW_LNS_set_column = %d' % self._leb128
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return self._length
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                return (buffer[offset] == 5)
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''
                registers.column = self._leb128
            # end def __call__
        # end class SetColumnStandardOpcode

        class NegateStmtStandardOpcode(Opcode):
            '''
            NEGATE STMT opcode
            '''

            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0613,W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.NegateStmtStandardOpcode, self).__init__()
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'DW_LNS_negate_stmt'
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return 1
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                return (buffer[offset] == 6)
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''
                registers.is_stmt = not registers.is_stmt
            # end def __call__
        # end class NegateStmtStandardOpcode

        class SetBasicBlockStandardOpcode(Opcode):
            '''
            SET BASIC BLOCK opcode
            '''

            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0613,W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.SetBasicBlockStandardOpcode, self).__init__()
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'DW_LNS_set_basic_block'
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return 1
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                return (buffer[offset] == 7)
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''
                registers.basic_block = True
            # end def __call__
        # end class SetBasicBlockStandardOpcode

        class ConstAddPcStandardOpcode(Opcode):
            '''
            ADD PC opcode
            '''

            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0613,W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.ConstAddPcStandardOpcode, self).__init__()

                adjusted_opcode = 255 - prologue.opcode_base
                self._add_address = adjusted_opcode / prologue.line_range
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'DW_LNS_add_pc += %d' % self._add_address
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return 1
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                return (buffer[offset] == 8)
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''
                registers.address += self._add_address
            # end def __call__
        # end class ConstAddPcStandardOpcode

        class FixedAdvancePcStandardOpcode(Opcode):
            '''
            FIXED ADVANCE PC opcode
            '''

            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0613,W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.FixedAdvancePcStandardOpcode, self).__init__()
                self._uhalf = _read_uhalf(buffer, offset+1)
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'DW_LNS_fixed_advance_pc += %d' % self._uhalf
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return 1+2
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                return (buffer[offset] == 9)
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''
                registers.address += self._uhalf
            # end def __call__
        # end class FixedAdvancePcStandardOpcode

        class EndSequenceExtendedOpcode(Opcode):
            '''
            END SEQUENCE opcode
            '''

            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0613,W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.EndSequenceExtendedOpcode, self).__init__()

                _, finalOffset = _read_uleb128(buffer, offset+1)
                self._length = finalOffset + 1 - offset
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'DW_LNE_end_sequence'
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return self._length
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                if (buffer[offset] == 0):
                    _, offset = _read_uleb128(buffer, offset+1)
                    return (buffer[offset] == 1)
                # end if

                return False
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''
                self._appendRow(registers, matrix)

                registers.reset(prologue)
                registers.end_sequence = True
            # end def __call__
        # end class EndSequenceExtendedOpcode

        class SetAddressExtendedOpcode(Opcode):
            '''
            SET ADDRESS opcode
            '''

            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0613,W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.SetAddressExtendedOpcode, self).__init__()

                _, finalOffset = _read_uleb128(buffer, offset+1)

                # FIXME This assumes a 32-bit address
                self._address, finalOffset = _read_uword(buffer, finalOffset+1)
                self._length = finalOffset - offset
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'DW_LNE_set_address = 0x%08x' % self._address
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return self._length
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                if (buffer[offset] == 0):
                    _, offset = _read_uleb128(buffer, offset+1)
                    return (buffer[offset] == 2)
                # end if

                return False
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''
                registers.address = self._address
            # end def __call__
        # end class SetAddressExtendedOpcode

        class DefineFileExtendedOpcode(Opcode):
            '''
            DEFINE FILE opcode
            '''

            def __init__(self, buffer, offset, prologue):                                                               #@ReservedAssignment pylint:disable=W0613,W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__init__
                @param  buffer   [in] (list) The buffer to read from
                @param  offset   [in] (int) The offset at which to start reading
                @param  prologue [in] (Prologue) The prologue to initialize the registers with
                '''
                super(DebugLineSection.EntrySet.DefineFileExtendedOpcode, self).__init__()

                _, finalOffset = _read_uleb128(buffer, offset+1)

                self._source_file_name, finalOffset = _read_string(buffer, finalOffset)
                self._directory_index, finalOffset  = _read_uleb128(buffer, finalOffset)
                self._last_modification_time, finalOffset = _read_uleb128(buffer, finalOffset)
                self._byte_length, finalOffset = _read_uleb128(buffer, finalOffset)

                self._length = finalOffset + 1 - offset
            # end def __init__

            def __str__(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__str__
                '''
                return 'DW_LNE_DEFINE_FILE(\'%s\', %d, %d, %d)' % (self._source_file_name,
                                                                   self._directory_index,
                                                                   self._last_modification_time,
                                                                   self._byte_length)
            # end def __str__

            def getLength(self):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.getLength
                '''
                return self._length
            # end def getLength

            @classmethod
            def accept(cls, prologue, buffer, offset):                                                                  #@ReservedAssignment pylint:disable=W0622
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.accept
                '''
                if (buffer[offset] == 0):
                    _, offset = _read_uleb128(buffer, offset+1)
                    return (buffer[offset] == 3)
                # end if

                return False
            # end def accept

            def __call__(self, prologue, registers, matrix):
                '''
                @copydoc pylibrary.system.dwarf.DebugLineSection.EntrySet.Opcode.__call__
                '''
                prologue.file_names.append((self._source_file_name,
                                            self._directory_index,
                                            self._last_modification_time,
                                            self._byte_length))
                registers.end_sequence = True
            # end def __call__
        # end class DefineFileExtendedOpcode

        OPCODES = (CopyStandardOpcode,
                   AdvancePcStandardOpcode,
                   AdvanceLineStandardOpcode,
                   SetFileStandardOpcode,
                   SetColumnStandardOpcode,
                   NegateStmtStandardOpcode,
                   SetBasicBlockStandardOpcode,
                   ConstAddPcStandardOpcode,
                   FixedAdvancePcStandardOpcode,
                   SpecialOpcode,
                   EndSequenceExtendedOpcode,
                   SetAddressExtendedOpcode,
                   DefineFileExtendedOpcode,
                   )

        def __init__(self, prologue, statements):
            '''
            Constructor

            @param  prologue   [in] (Prologue) The prologue for this entry
            @param  statements [in] (list) List of opcodes for this entry
            '''
            super(DebugLineSection.EntrySet, self).__init__()

            self.prologue   = prologue
            self.statements = statements

            self._matrix = None
        # end def __init__

        @classmethod
        def fromHexList(cls, buffer, offset):                                                                            #@ReservedAssignment pylint:disable=W0622
            '''
            Decodes an entry set from a HexList

            @param  buffer [in] (HexList) The buffer to build the object from.
            @param  offset [in] (int) The offset at which to start reading.

            @return (EntrySet) A new EntrySet instance
            '''
            prologue = cls.Prologue.fromHexList(buffer, offset)
            statements = []

            finalOffset = offset + 4 + prologue.total_length
            offset += prologue.prologue_length + 10

            while (offset < finalOffset):
                opcodeClass = None
                for opcodeClass in cls.OPCODES:
                    if (opcodeClass.accept(prologue, buffer, offset)):
                        opcode = opcodeClass(buffer, offset, prologue)
                        break
                    # end if
                else:
                    raise ValueError('Unknown opcode at offset %d: %s' % (offset, buffer[offset: offset+16]))
                # end for

                statements.append(opcode)

                offset += opcode.getLength()
            # end while

            return cls(prologue,
                       statements)
        # end def fromHexList

        def getMatrix(self, cached = False):
            '''
            Builds the address matrix, and cache it if requested.

            @option cached [in] (bool) Whether to cache this matrix or not.

            @return (dict) The built matrix
            '''
            if (self._matrix is None):
                matrix = {}
                prologue = self.prologue
                registers = self.Registers(prologue = prologue)
                for statement in self.statements:
                    statement(prologue, registers, matrix)
                # end for

                if (cached):
                    self._matrix = matrix
                # end if
            else:
                matrix = self._matrix
            # end if

            return matrix
        # end def getMatrix
    # end class EntrySet

    def __init__(self, entry_sets):
        '''
        Constructor

        @param  entry_sets [in] (dict) The entry sets for this section.

        The contents are identified by offset, and contain EntrySet instances.
        Each EntrySet instance can build the address matrix, which is can be cached for later access
        '''
        super(DebugLineSection, self).__init__()

        self.entry_sets = entry_sets
    # end def __init__

    @classmethod
    def fromHexList(cls, buffer, offset, length):                                                                        #@ReservedAssignment pylint:disable=W0622
        '''
        Parses a .debug_aranges DWARF section

        @param  buffer [in] (HexList) The buffer to read from.
        @param  offset [in] (int)    The offset at which to read
        @param  length [in] (int)    The length for which to read.

        @return New instance of an DebugArangesSection
        '''
        entry_sets = {}
        startOffset = offset
        finalOffset = offset + length
        while (offset < finalOffset):
            entry_set = cls.EntrySet.fromHexList(buffer, offset)
            entry_sets[offset-startOffset] = entry_set
            length, offset = _read_uword(buffer, offset)
            offset += length
        # end while

        return cls(entry_sets)
    # end def fromHexList
# end class DebugLineSection

class DebugArangesSection(StrAbleMixin):
    '''
    Interpretation of the .aranges section of a DWARF file.
    '''

    _STRABLE_FIELDS = ('entry_sets', )

    class EntrySet(StrAbleMixin):
        '''
        An entry set in the .aranges section
        '''

        _STRABLE_FIELDS = ('length',
                           'version',
                           'debug_info_offset',
                           'address_size',
                           'segment_size',
                           'addresses_and_lengths',
                           )

        def __init__(self, length,
                           version,
                           debug_info_offset,
                           address_size,
                           segment_size,
                           addresses_and_lengths):
            '''
            Constructor

            @param  length                [in] (int) length of the set of entries for this compilation unit
            @param  version               [in] (int) version identifier
            @param  debug_info_offset     [in] (int) offset in the .debug_info section.
            @param  address_size          [in] (int) size in bytes of an address (or the offset portion of an address for segmented addressing)
            @param  segment_size          [in] (int) size in bytes of a segment descriptor on the target system.
            @param  addresses_and_lengths [in] (tuple) Series of pairs (address, length)
            '''
            super(DebugArangesSection.EntrySet, self).__init__()

            self.length                = length
            self.version               = version
            self.debug_info_offset     = debug_info_offset
            self.address_size          = address_size
            self.segment_size          = segment_size
            self.addresses_and_lengths = addresses_and_lengths
        # end def __init__

        @classmethod
        def fromHexList(cls, buffer, offset):                                                                            #@ReservedAssignment pylint:disable=W0622
            '''
            Read an entry from a HexList

            @param  buffer [in] (HexList) The buffer to read from.
            @param  offset [in] (int)    The offset at which to read

            @return (EntrySet) New instance of an EntrySet
            '''
            startOffset = offset

            length, offset = _read_uword(buffer, offset)
            finalOffset = offset + length

            version, offset           = _read_uhalf(buffer, offset)
            debug_info_offset, offset = _read_uword(buffer, offset)
            address_size, offset      = _read_ubyte(buffer, offset)
            segment_size, offset      = _read_ubyte(buffer, offset)

            full_address_size = address_size + segment_size

            # Adjust the offset to the padded value
            while (((offset - startOffset) % full_address_size) != 0):
                offset += 1
            # end while

            addresses_and_lengths = []

            element = (None, None)
            while (offset < finalOffset) and (element != (0, 0)):
                tuple_address, offset = _read_un(buffer, offset, full_address_size)
                tuple_length, offset  = _read_un(buffer, offset, full_address_size)

                element = (tuple_address, tuple_length)

                if (element != (0, 0)):
                    addresses_and_lengths.append(element)
                # end if
            # end while

            return cls(length,
                       version,
                       debug_info_offset,
                       address_size,
                       segment_size,
                       addresses_and_lengths)
        # end def fromHexList
    # end class EntrySet

    def __init__(self, entry_sets):
        '''
        Constructor

        @param  entry_sets [in] (tuple) List of entry sets
        '''
        super(DebugArangesSection, self).__init__()

        self.entry_sets = entry_sets
    # end def __init__

    @classmethod
    def fromHexList(cls, buffer, offset, length):                                                                        #@ReservedAssignment pylint:disable=W0622
        '''
        Parses a .debug_aranges DWARF section

        @param  buffer [in] (HexList) The buffer to read from.
        @param  offset [in] (int)    The offset at which to read
        @param  length [in] (int)    The length for which to read.

        @return (DebugArangesSection) New instance of an DebugArangesSection
        '''
        entry_sets = {}
        startOffset = offset
        finalOffset = offset + length
        while (offset < finalOffset):
            entry_set = cls.EntrySet.fromHexList(buffer, offset)
            entry_sets[offset - startOffset] = entry_set
            length, offset = _read_uword(buffer, offset)
            offset += length
        # end while

        return cls(entry_sets)
    # end def fromHexList
# end class DebugArangesSection

class DebugAbbrevSection(StrAbleMixin):
    '''
    Interpretation of the debug_abbrev section of a DWARF file.
    '''
    class AbbrevTable(StrAbleMixin):
        '''
        An abbrev section tables
        '''

        class EntrySet(StrAbleMixin):
            '''
            An entry set in the .debug_abbrev section's table
            '''

            _STRABLE_FIELDS = ('abbreviation_code',
                               'entry_tag',
                               'has_children',
                               'attributes')

            def __init__(self, abbreviation_code,
                               entry_tag,
                               has_children,
                               attributes,
                               length = None):
                '''
                Constructor

                @param  abbreviation_code [in] (int) The abbreviation code for this entry
                @param  entry_tag         [in] (int) The actual tag for this entry
                @param  has_children      [in] (int) Whether the debug information has children
                @param  attributes        [in] (int) List of attribute definitions for the debug information
                @option length            [in] (int) Length of the encoded version of this entry set.
                                                    Useful when reading from HexList
                '''
                super(DebugAbbrevSection.AbbrevTable.EntrySet, self).__init__()

                self.abbreviation_code = abbreviation_code
                self.entry_tag         = entry_tag
                self.has_children      = has_children
                self.attributes        = attributes

                self.length            = length
            # end def __init__

            @classmethod
            def fromHexList(cls, buffer, offset):                                                                        #@ReservedAssignment pylint:disable=W0622
                '''
                Build a new object from buffer

                @param  buffer [in] (HexList) The buffer to build the object from.
                @param  offset [in] (int) The offset at which to start reading.

                @return (EntrySet) A new EntrySet instance
                '''
                startOffset = offset

                abbreviation_code, offset = _read_uleb128(buffer, offset)
                entry_tag, offset         = _read_uleb128(buffer, offset)
                has_children, offset      = _read_ubyte(buffer, offset)

                attributes = []
                attribute = (None, None)
                while (attribute != (0, 0)):
                    attribute_name, offset = _read_uleb128(buffer, offset)
                    attribute_form, offset = _read_uleb128(buffer, offset)

                    attribute = (attribute_name, attribute_form)
                    if (attribute != (0, 0)):
                        attributes.append(attribute)
                    # end if
                # end while

                return cls(abbreviation_code,
                           entry_tag,
                           has_children,
                           attributes,
                           offset - startOffset)
            # end def fromHexList
        # end class EntrySet

        _STRABLE_FIELDS = ('entry_sets',)

        def __init__(self, entry_sets,
                           length = None):
            '''
            Constructor

            @param  entry_sets [in] (dict) The entry sets for this section.
            @param  length     [in] (int)  The length of the table in HexList form.
                                          Useful for deserialization

            The contents are identified by abbreviation name, and contain EntrySet instances.
            '''
            super(DebugAbbrevSection.AbbrevTable, self).__init__()

            self.entry_sets = entry_sets
            self.length     = length
        # end def __init__

        @classmethod
        def fromHexList(cls, buffer, offset):                                                                            #@ReservedAssignment pylint:disable=W0622
            '''
            Parses a .debug_abbrev DWARF section

            @param  buffer [in] (HexList) The buffer to read from.
            @param  offset [in] (int)    The offset at which to read

            @return (AbbrevTable) New instance of an DebugAbbrev
            '''
            entry_sets = { 0: cls.EntrySet(abbreviation_code = 0,
                                           entry_tag         = 0,
                                           has_children      = False,
                                           attributes        = tuple(),
                                           length            = None),
                                           }
            startOffset = offset
            abbreviation_code = None
            while (abbreviation_code != 0):
                abbreviation_code, _ = _read_uleb128(buffer, offset)

                if (abbreviation_code != 0):
                    entry_set = cls.EntrySet.fromHexList(buffer, offset)
                    entry_sets[abbreviation_code] = entry_set
                    offset += entry_set.length
                else:
                    offset += 1
                # end if
            # end while

            length = offset - startOffset
            return cls(entry_sets,
                       length)
        # end def fromHexList
    # end class AbbrevTable

    _STRABLE_FIELDS = ('tables',)

    def __init__(self, tables):
        '''
        Constructor

        @param  tables [in] (dict) The entry sets for this section.

        The contents are identified by abbreviation name, and contain EntrySet instances.
        '''
        super(DebugAbbrevSection, self).__init__()

        self.tables = tables
    # end def __init__

    @classmethod
    def fromHexList(cls, buffer, offset, length):                                                                        #@ReservedAssignment pylint:disable=W0622
        '''
        Parses a .debug_abbrev DWARF section

        @param  buffer [in] (HexList) The buffer to read from.
        @param  offset [in] (int)    The offset at which to read
        @param  length [in] (int)    The length for which to read.

        @return New instance of an DebugAbbrev
        '''
        tables = {}
        startOffset = offset
        finalOffset = offset + length
        while (offset < finalOffset):
            table = cls.AbbrevTable.fromHexList(buffer, offset)
            tables[offset - startOffset] = table

            offset += table.length
        # end while

        return cls(tables)
    # end def fromHexList
# end class DebugAbbrevSection

class DebugInfoSection(StrAbleMixin):
    '''
    Interpretation of the debug_info section of a DWARF file.
    '''

    class EntrySet(StrAbleMixin):
        '''
        An entry set in the .debug_info section
        '''

        _STRABLE_FIELDS = ('length',
                           'version',
                           'debug_abbrev_offset',
                           'address_size',
                           'debugging_informations',
                           )

        def __init__(self, length,
                           version,
                           debug_abbrev_offset,
                           address_size,
                           debugging_informations):
            '''
            Constructor

            @param  length                 [in] (int) length of the set of entries for this compilation unit
            @param  version                [in] (int) version identifier
            @param  debug_abbrev_offset    [in] (int) offset in the .debug_abbrev section.
            @param  address_size           [in] (int) size in bytes of an address (or the offset portion of an address for segmented addressing)
            @param  debugging_informations [in] (tuple) Series of DebugginInformationEntry
            '''
            super(DebugInfoSection.EntrySet, self).__init__()

            self.length                 = length
            self.version                = version
            self.debug_abbrev_offset    = debug_abbrev_offset
            self.address_size           = address_size
            self.debugging_informations = debugging_informations
        # end def __init__

        class DebuggingInformationEntry(StrAbleMixin):
            '''
            Wrapper around a DIE
            '''

            DW_AT_sibling          = 0x01 # reference
            DW_AT_location         = 0x02 # block, constant
            DW_AT_name             = 0x03 # string
            DW_AT_ordering         = 0x09 # constant
            DW_AT_byte_size        = 0x0b # constant
            DW_AT_bit_offset       = 0x0c # constant
            DW_AT_bit_size         = 0x0d # constant
            DW_AT_stmt_list        = 0x10 # constant
            DW_AT_low_pc           = 0x11 # address
            DW_AT_high_pc          = 0x12 # address
            DW_AT_language         = 0x13 # constant
            DW_AT_discr            = 0x15 # reference
            DW_AT_discr_value      = 0x16 # constant
            DW_AT_visibility       = 0x17 # constant
            DW_AT_import           = 0x18 # reference
            DW_AT_string_length    = 0x19 # block, constant
            DW_AT_common_reference = 0x1a # reference
            DW_AT_comp_dir         = 0x1b # string
            DW_AT_const_value      = 0x1c # string, constant, block
            DW_AT_containing_type  = 0x1d # reference
            DW_AT_default_value    = 0x1e # reference
            DW_AT_inline           = 0x20 # constant
            DW_AT_is_optional      = 0x21 # flag
            DW_AT_lower_bound      = 0x22 # constant, reference
            DW_AT_producer         = 0x25 # string
            DW_AT_prototyped       = 0x27 # flag
            DW_AT_return_addr      = 0x2a # block, constant
            DW_AT_start_scope      = 0x2c # constant
            DW_AT_stride_size      = 0x2e # constant
            DW_AT_upper_bound      = 0x2f # constant, reference

            DW_AT_abstract_origin      = 0x31 # reference
            DW_AT_accessibility        = 0x32 # constant
            DW_AT_address_class        = 0x33 # constant
            DW_AT_artificial           = 0x34 # flag
            DW_AT_base_types           = 0x35 # reference
            DW_AT_calling_convention   = 0x36 # constant
            DW_AT_count                = 0x37 # constant, reference
            DW_AT_data_member_location = 0x38 # block, reference
            DW_AT_decl_column          = 0x39 # constant
            DW_AT_decl_file            = 0x3a # constant
            DW_AT_decl_line            = 0x3b # constant
            DW_AT_declaration          = 0x3c # flag
            DW_AT_discr_list           = 0x3d # block
            DW_AT_encoding             = 0x3e # constant
            DW_AT_external             = 0x3f # flag
            DW_AT_frame_base           = 0x40 # block, constant
            DW_AT_friend               = 0x41 # reference
            DW_AT_identifier_case      = 0x42 # constant
            DW_AT_macro_info           = 0x43 # constant
            DW_AT_namelist_item        = 0x44 # block
            DW_AT_priority             = 0x45 # reference
            DW_AT_segment              = 0x46 # block, constant
            DW_AT_specification        = 0x47 # reference
            DW_AT_static_link          = 0x48 # block, constant
            DW_AT_type                 = 0x49 # reference
            DW_AT_use_location         = 0x4a # block, constant
            DW_AT_variable_parameter   = 0x4b # flag
            DW_AT_virtuality           = 0x4c # constant
            DW_AT_vtable_elem_location = 0x4d # block, reference
            DW_AT_lo_user              = 0x2000
            DW_AT_hi_user              = 0x3fff

            ATTRIBUTE_NAMES = {DW_AT_sibling:          'sibling',
                               DW_AT_location:         'location',
                               DW_AT_name:             'name',
                               DW_AT_ordering:         'ordering',
                               DW_AT_byte_size:        'byte_size',
                               DW_AT_bit_offset:       'bit_offset',
                               DW_AT_bit_size:         'bit_size',
                               DW_AT_stmt_list:        'stmt_list',
                               DW_AT_low_pc:           'low_pc',
                               DW_AT_high_pc:          'high_pc',
                               DW_AT_language:         'language',
                               DW_AT_discr:            'discr',
                               DW_AT_discr_value:      'discr_value',
                               DW_AT_visibility:       'visibility',
                               DW_AT_import:           'import',
                               DW_AT_string_length:    'string_length',
                               DW_AT_common_reference: 'common_reference',
                               DW_AT_comp_dir:         'comp_dir',
                               DW_AT_const_value:      'const_value',
                               DW_AT_containing_type:  'containing_type',
                               DW_AT_default_value:    'default_value',
                               DW_AT_inline:           'inline',
                               DW_AT_is_optional:      'is_optional',
                               DW_AT_lower_bound:      'lower_bound',
                               DW_AT_producer:         'producer',
                               DW_AT_prototyped:       'prototyped',
                               DW_AT_return_addr:      'return_addr',
                               DW_AT_start_scope:      'start_scope',
                               DW_AT_stride_size:      'stride_size',
                               DW_AT_upper_bound:      'upper_bound',
                               DW_AT_abstract_origin:      'abstract_origin',
                               DW_AT_accessibility:        'accessibility',
                               DW_AT_address_class:        'address_class',
                               DW_AT_artificial:           'artificial',
                               DW_AT_base_types:           'base_types',
                               DW_AT_calling_convention:   'calling_convention',
                               DW_AT_count:                'count',
                               DW_AT_data_member_location: 'data_member_location',
                               DW_AT_decl_column:          'decl_column',
                               DW_AT_decl_file:            'decl_file',
                               DW_AT_decl_line:            'decl_line',
                               DW_AT_declaration:          'declaration',
                               DW_AT_discr_list:           'discr_list',
                               DW_AT_encoding:             'encoding',
                               DW_AT_external:             'external',
                               DW_AT_frame_base:           'frame_base',
                               DW_AT_friend:               'friend',
                               DW_AT_identifier_case:      'identifier_case',
                               DW_AT_macro_info:           'macro_info',
                               DW_AT_namelist_item:        'namelist_item',
                               DW_AT_priority:             'priority',
                               DW_AT_segment:              'segment',
                               DW_AT_specification:        'specification',
                               DW_AT_static_link:          'static_link',
                               DW_AT_type:                 'type',
                               DW_AT_use_location:         'use_location',
                               DW_AT_variable_parameter:   'variable_parameter',
                               DW_AT_virtuality:           'virtuality',
                               DW_AT_vtable_elem_location: 'vtable_elem_location',
                               DW_AT_lo_user:              'lo_user',
                               DW_AT_hi_user:              'hi_user',
                               }

            DW_TAG_array_type             = 0x01
            DW_TAG_class_type             = 0x02
            DW_TAG_entry_point            = 0x03
            DW_TAG_enumeration_type       = 0x04
            DW_TAG_formal_parameter       = 0x05
            DW_TAG_imported_declaration   = 0x08
            DW_TAG_label                  = 0x0a
            DW_TAG_lexical_block          = 0x0b
            DW_TAG_member                 = 0x0d
            DW_TAG_pointer_type           = 0x0f
            DW_TAG_reference_type         = 0x10
            DW_TAG_compile_unit           = 0x11
            DW_TAG_string_type            = 0x12
            DW_TAG_structure_type         = 0x13
            DW_TAG_subroutine_type        = 0x15
            DW_TAG_typedef                = 0x16
            DW_TAG_union_type             = 0x17
            DW_TAG_unspecified_parameters = 0x18
            DW_TAG_variant                = 0x19
            DW_TAG_common_block           = 0x1a
            DW_TAG_common_inclusion       = 0x1b
            DW_TAG_inheritance            = 0x1c
            DW_TAG_inlined_subroutine     = 0x1d
            DW_TAG_module                 = 0x1e
            DW_TAG_ptr_to_member_type     = 0x1f
            DW_TAG_set_type               = 0x20
            DW_TAG_subrange_type          = 0x21
            DW_TAG_with_stmt              = 0x22
            DW_TAG_access_declaration     = 0x23
            DW_TAG_base_type              = 0x24
            DW_TAG_catch_block            = 0x25
            DW_TAG_const_type             = 0x26
            DW_TAG_constant               = 0x27
            DW_TAG_enumerator             = 0x28
            DW_TAG_file_type              = 0x29

            TAG_NAMES = {DW_TAG_array_type:             'array_type',
                         DW_TAG_class_type:             'class_type',
                         DW_TAG_entry_point:            'entry_point',
                         DW_TAG_enumeration_type:       'enumeration_type',
                         DW_TAG_formal_parameter:       'formal_parameter',
                         DW_TAG_imported_declaration:   'imported_declaration',
                         DW_TAG_label:                  'label',
                         DW_TAG_lexical_block:          'lexical_block',
                         DW_TAG_member:                 'member',
                         DW_TAG_pointer_type:           'pointer_type',
                         DW_TAG_reference_type:         'reference_type',
                         DW_TAG_compile_unit:           'compile_unit',
                         DW_TAG_string_type:            'string_type',
                         DW_TAG_structure_type:         'structure_type',
                         DW_TAG_subroutine_type:        'subroutine_type',
                         DW_TAG_typedef:                'typedef',
                         DW_TAG_union_type:             'union_type',
                         DW_TAG_unspecified_parameters: 'unspecified_parameters',
                         DW_TAG_variant:                'variant',
                         DW_TAG_common_block:           'common_block',
                         DW_TAG_common_inclusion:       'common_inclusion',
                         DW_TAG_inheritance:            'inheritance',
                         DW_TAG_inlined_subroutine:     'inlined_subroutine',
                         DW_TAG_module:                 'module',
                         DW_TAG_ptr_to_member_type:     'ptr_to_member_type',
                         DW_TAG_set_type:               'set_type',
                         DW_TAG_subrange_type:          'subrange_type',
                         DW_TAG_with_stmt:              'with_stmt',
                         DW_TAG_access_declaration:     'access_declaration',
                         DW_TAG_base_type:              'base_type',
                         DW_TAG_catch_block:            'catch_block',
                         DW_TAG_const_type:             'const_type',
                         DW_TAG_constant:               'constant',
                         DW_TAG_enumerator:             'enumerator',
                         DW_TAG_file_type:              'file_type',
                         }

            DW_FORM_addr      = 0x01 # address
            DW_FORM_block2    = 0x03 # block
            DW_FORM_block4    = 0x04 # block
            DW_FORM_data2     = 0x05 # constant
            DW_FORM_data4     = 0x06 # constant
            DW_FORM_data8     = 0x07 # constant
            DW_FORM_string    = 0x08 # string
            DW_FORM_block     = 0x09 # block
            DW_FORM_block1    = 0x0a # block
            DW_FORM_data1     = 0x0b # constant
            DW_FORM_flag      = 0x0c # flag
            DW_FORM_sdata     = 0x0d # constant
            DW_FORM_strp      = 0x0e # string
            DW_FORM_udata     = 0x0f # constant
            DW_FORM_ref_addr  = 0x10 # reference
            DW_FORM_ref1      = 0x11 # reference
            DW_FORM_ref2      = 0x12 # reference
            DW_FORM_ref4      = 0x13 # reference
            DW_FORM_ref8      = 0x14 # reference
            DW_FORM_ref_udata = 0x15 # reference

            def __init__(self, abbreviation_code,
                               children,
                               attributes,
                               length = None):
                '''
                Constructor

                @param  abbreviation_code [in] (int) Abbreviation code for his DIE
                @param  children          [in] (list) List of child DIE
                @param  attributes        [in] (dict) Dictionary of attributes for this DIE
                @option length            [in] (list) Length of the serialized DIE
                                                    Useful when reading from HexList
                '''
                super(DebugInfoSection.EntrySet.DebuggingInformationEntry, self).__init__()

                self.abbreviation_code = abbreviation_code
                self.children          = children

                for key, value in attributes.items():
                    setattr(self, key, value)
                # end for

                self._STRABLE_FIELDS = ['abbreviation_code', ]
                self._STRABLE_FIELDS.extend(list(attributes.keys()))
                if (len(children)):
                    self._STRABLE_FIELDS.append('children')
                # end if

                self.length = length
            # end def __init__

            @classmethod
            def fromHexList(cls, buffer, offset, abbrev_table, address_size):                                            #@ReservedAssignment pylint:disable=W0622,R0912
                '''
                Read a DIE from a HexList

                @param  buffer       [in] (HexList) The buffer to read from.
                @param  offset       [in] (int)    The offset at which to read
                @param  abbrev_table [in] (DebugAbbrevSection.AbbrevTable) The abbreviation table
                @param  address_size [in] (int) Size of an address, in bytes

                @return (DebuggingInformationEntry) New instance of a DebuggingInformationEntry
                '''
                startOffset = offset

                abbreviation_code, offset = _read_uleb128(buffer, offset)
                abbrev_entry_set = abbrev_table.entry_sets.get(abbreviation_code)

                attributes = {}
                for attribute_name, attribute_form in abbrev_entry_set.attributes:

                    if (attribute_form == cls.DW_FORM_addr):
                        value, offset = _read_un(buffer, offset, address_size)
                    elif (attribute_form == cls.DW_FORM_block1):
                        block_length, offset = _read_ubyte(buffer, offset)
                        value, offset = _read_block(buffer, offset, block_length)
                    elif (attribute_form == cls.DW_FORM_block2):
                        block_length, offset = _read_uhalf(buffer, offset)
                        value, offset = _read_block(buffer, offset, block_length)
                    elif (attribute_form == cls.DW_FORM_block4):
                        block_length, offset = _read_uword(buffer, offset)
                        value, offset = _read_block(buffer, offset, block_length)
                    elif (attribute_form == cls.DW_FORM_block):
                        block_length, offset = _read_uleb128(buffer, offset)
                        value, offset = _read_block(buffer, offset, block_length)
                    elif (attribute_form == cls.DW_FORM_data1):
                        value, offset = _read_un(buffer, offset, 1)
                    elif (attribute_form == cls.DW_FORM_data2):
                        value, offset = _read_un(buffer, offset, 2)
                    elif (attribute_form == cls.DW_FORM_data4):
                        value, offset = _read_un(buffer, offset, 4)
                    elif (attribute_form == cls.DW_FORM_data8):
                        value, offset = _read_un(buffer, offset, 8)
                    elif (attribute_form == cls.DW_FORM_sdata):
                        value, offset = _read_uleb128(buffer, offset)
                    elif (attribute_form == cls.DW_FORM_udata):
                        value, offset = _read_sleb128(buffer, offset)
                    elif (attribute_form == cls.DW_FORM_flag):
                        value, offset = _read_ubyte(buffer, offset)
                    elif (attribute_form == cls.DW_FORM_ref1):
                        value, offset = _read_sn(buffer, offset, 1)
                    elif (attribute_form == cls.DW_FORM_ref2):
                        value, offset = _read_sn(buffer, offset, 2)
                    elif (attribute_form == cls.DW_FORM_ref4):
                        value, offset = _read_sn(buffer, offset, 4)
                    elif (attribute_form == cls.DW_FORM_ref8):
                        value, offset = _read_sn(buffer, offset, 8)
                    elif (attribute_form == cls.DW_FORM_ref_udata):
                        value, offset = _read_uleb128(buffer, offset)
                    elif (attribute_form == cls.DW_FORM_string):
                        value, offset = _read_string(buffer, offset)
                    elif (attribute_form == cls.DW_FORM_strp):
                        value, offset = _read_uword(buffer, offset)
                    else:
                        raise ValueError('Unknown form: %d (0x%02x)'
                                         % (attribute_form, attribute_form))
                    # end if

                    attributes[cls.ATTRIBUTE_NAMES[attribute_name]] = value
                # end for

                children = []
                # Read children
                if (abbrev_entry_set.has_children):
                    loop = True
                    while (loop):
                        child = cls.fromHexList(buffer, offset, abbrev_table, address_size)
                        children.append(child)
                        offset += child.length

                        loop = (child.abbreviation_code != 0)
                    # end while
                # end if


                length = offset - startOffset

                return cls(abbreviation_code,
                           children,
                           attributes,
                           length = length)
            # end def fromHexList
        # end class DebuggingInformationEntry

        @classmethod
        def fromHexList(cls, buffer, offset, debug_abbrev):                                                              #@ReservedAssignment pylint:disable=W0622
            '''
            Read an entry from a HexList

            @param  buffer       [in] (HexList) The buffer to read from.
            @param  offset       [in] (int)    The offset at which to read
            @param  debug_abbrev [in] (DebugAbbrevSection) The parsed contents of the .debug_abbrev section

            @return (EntrySet) New instance of an EntrySet
            '''
            # Read header
            length, offset = _read_uword(buffer, offset)
            finalOffset = offset + length

            version, offset             = _read_uhalf(buffer, offset)
            debug_abbrev_offset, offset = _read_uword(buffer, offset)
            address_size, offset        = _read_ubyte(buffer, offset)

            abbrev_table = debug_abbrev.tables[debug_abbrev_offset]
            debugging_informations = []
            # Read debug information entries
            while (offset < finalOffset):
                debuggingInformationEntry = cls.DebuggingInformationEntry.fromHexList(buffer, offset, abbrev_table, address_size)
                debugging_informations.append(debuggingInformationEntry)

                offset += debuggingInformationEntry.length
            # end while

            return cls(length,
                       version,
                       debug_abbrev_offset,
                       address_size,
                       debugging_informations)
        # end def fromHexList
    # end class EntrySet

    _STRABLE_FIELDS = ('entry_sets',)

    def __init__(self, entry_sets):
        '''
        Constructor

        @param  entry_sets [in] (dict) The entry sets for this section.

        The contents are identified by offset, and contain EntrySet instances.
        '''
        super(DebugInfoSection, self).__init__()

        self.entry_sets = entry_sets
    # end def __init__

    @classmethod
    def fromHexList(cls, buffer, offset, length, debug_abbrev):                                                          #@ReservedAssignment pylint:disable=W0622
        '''
        Parses a .debug_info DWARF section

        @param  buffer       [in] (HexList) The buffer to read from.
        @param  offset       [in] (int)    The offset at which to read
        @param  length       [in] (int)    The length for which to read.
        @param  debug_abbrev [in] (DebugAbbrevSection) The parsed contents of the .debug_abbrev section

        @return New instance of an DebugAbbrev
        '''
        startOffset = offset
        entry_sets = {}
        finalOffset = offset + length
        while (offset < finalOffset):
            entry_set = cls.EntrySet.fromHexList(buffer, offset, debug_abbrev)
            entry_sets[offset - startOffset] = entry_set

            offset += 4 + entry_set.length
        # end while

        return cls(entry_sets)
    # end def fromHexList
# end class DebugInfoSection

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
