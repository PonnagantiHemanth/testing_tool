
#ifndef ARCH_H
#define ARCH_H


/* Architecture (CPU) word length (in bits) */
#define CPU_TYPE        CPU_TYPE_32


/* Memory byte ordering:
 * HIGH_BYTE_FIRST:   High order byte of a multi-byte value is located at the lowest address (Big Endian)
 * LOW_BYTE_FIRST:    Low order byte of a multi-byte value is located at the lowest address (Little Endian)
 *
 * The macro "ASSERT_ENDIANNESS" is defined for compatibility with CPUs whose endianness is configurable.
 */
#define CPU_BYTE_ORDER  LOW_BYTE_FIRST

#define ASSERT_ENDIANNESS() ((void)0)

/* Byte swapping macros:
 * The macros "SWAP_BYTES_UINT16_ARCH" and/or "SWAP_BYTES_UINT32_ARCH" may be deined if the architecture
 * provides a fast way of swapping bytes.  It is safe to leave these macros undefined.
 *
 * Example:
 * #define SWAP_BYTES_UINT16_ARCH(value)    ((uint16_t) SWAP16((uint16_t) (value)))
 * #define SWAP_BYTES_UINT32_ARCH(value)    ((uint32_t) SWAP32((uint32_t) (value)))
 */

#endif /* !defined(ARCH_H) */
