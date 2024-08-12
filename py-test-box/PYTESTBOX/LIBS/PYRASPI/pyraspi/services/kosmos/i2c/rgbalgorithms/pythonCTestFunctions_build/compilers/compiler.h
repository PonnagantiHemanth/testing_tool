
#ifndef COMPILER_H
#define COMPILER_H


#include <stdint.h>
#include <stdbool.h>
#include <string.h>

/* Definition of memory storage classes:
   The ARMv6-M/ARMv7-M architecture of the Cortex-M series (M0, M3, M4) support a single, unified address space.
   All memory access instructions can be used to address items in all regions of memory.  This is much more
   flexible, allowing code and data to be essentially freely allocated across all available memory regions.
   The compiler and linker automatically handle run-time initialization of volatile regions from the contents
   of ROM following reset. */
#define FASTRAM
#define STDRAM
#define DATAROM
#define PGMROM

/* Definition of memory specific pointers:
   There is no need for any such distinction when coding for Cortex-M. Since all pointers are 32 bits in size
   and are held in 32-bit registers, the address of any location in memory can be held within a single register
   and all pointers are treated identically. */
#define FASTRAM_PTR *
#define STDRAM_PTR  *
#define DATAROM_PTR *
#define PGMROM_PTR  *

/* Program space data access macros for basic built in data types */
#define READ_DATAROM_UINT8(var)      ((uint8_t)(var))
#define READ_DATAROM_UINT16(var)     ((uint16_t)(var))
#define READ_DATAROM_UINT32(var)     ((uint32_t)(var))
#define READ_DATAROM_PTR(var)        ((void *)(var))

/* Program space data access macros for custom defined data sizetypes
 * MEMCPY_DATAROM(ramdest, romsource, size);
 * ramdest and romsource are object pointer, size is an integer
 */
#define MEMCPY_DATAROM(ramdest, romsource, size)  do {                                   \
        if ((size) == sizeof(uint8_t)) {                                                 \
            ((uint8_t STDRAM_PTR)(ramdest))[0] = ((uint8_t DATAROM_PTR)(romsource))[0];  \
        } else if ((size) == sizeof(uint16_t)) {                                         \
            ((uint8_t STDRAM_PTR)(ramdest))[0] = ((uint8_t DATAROM_PTR)(romsource))[0];  \
            ((uint8_t STDRAM_PTR)(ramdest))[1] = ((uint8_t DATAROM_PTR)(romsource))[1];  \
        } else if ((size) == sizeof(uint32_t)) {                                         \
            ((uint8_t STDRAM_PTR)(ramdest))[0] = ((uint8_t DATAROM_PTR)(romsource))[0];  \
            ((uint8_t STDRAM_PTR)(ramdest))[1] = ((uint8_t DATAROM_PTR)(romsource))[1];  \
            ((uint8_t STDRAM_PTR)(ramdest))[2] = ((uint8_t DATAROM_PTR)(romsource))[2];  \
            ((uint8_t STDRAM_PTR)(ramdest))[3] = ((uint8_t DATAROM_PTR)(romsource))[3];  \
         } else {                                                                        \
            memcpy(ramdest, romsource, size);                                            \
        }                                                                                \
    } while (0)

/* fastbool_t should be preferred when using local (automatic) boolean
 * variables and as function return values, also in any file scope global
 * boolean type.
 */
typedef bool fastbool_t;
typedef bool bool_t;

/* A struct bitfield is always treated as unsigned integer value.
 * Only char, unsigned char, int, and unsigned int are supported
 * as storage unit for bitfields. Bitfields are allocated within
 * the storage unit from the least-significant to the most-significant
 * bit (LSB_FIRST) and a bitfield cannot straddle across a storage unit
 * boundaries */
#define CPU_BIT_ORDER   LSB_FIRST

/* Inhibit compiler warning for unused argument in function */
#if defined(UNUSED)
#undef UNUSED
#endif
#define UNUSED(arg)  ((void) (arg))

#endif /* !defined(COMPILER_H) */
