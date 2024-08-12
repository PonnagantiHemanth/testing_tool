
#ifndef LTYPES_H
#define LTYPES_H

#include "compiler.h"
#include "arch.h"

/* For TDD RAKE: enable test framework */
#undef STATIC
#ifdef TDD_TEST
#define STATIC
#else
#define STATIC static
#endif

/* Boolean definitions */
#ifndef TRUE
#ifdef __bool_true_false_are_defined
#define TRUE    true
#else
#define TRUE    1
#endif
#endif
#ifndef FALSE
#ifdef __bool_true_false_are_defined
#define FALSE   false
#else
#define FALSE   0
#endif
#endif
#ifndef NULL
#define NULL    ((void*)0)
#endif

typedef uint8_t status_t;

#undef E_OK
#undef E_NOT_OK
#undef STD_HIGH
#undef STD_LOW
#undef STD_ACTIVE
#undef STD_IDLE
#undef STD_ON
#undef STD_OFF
#undef STD_ENABLE
#undef STD_DISABLE

#define E_OK        0x00
#define E_NOT_OK    0x01

#define STD_HIGH    0x01
#define STD_LOW     0x00

#define STD_ACTIVE  0x01
#define STD_IDLE    0x00

#define STD_ON      0x01
#define STD_OFF     0x00

#define STD_ENABLE  0x01
#define STD_DISABLE 0x00

/* Possible values for CPU_TYPE */
#undef CPU_TYPE_8
#undef CPU_TYPE_16
#undef CPU_TYPE_32
#undef CPU_TYPE_64

#define CPU_TYPE_8  8
#define CPU_TYPE_16 16
#define CPU_TYPE_32 32
#define CPU_TYPE_64 64

/* Possible values for CPU_BIT_ORDER (register bit ordering) */
#undef MSB_FIRST
#undef LSB_FIRST

#define MSB_FIRST   0x01            /* The most significant bit is the first bit of the bit field */
#define LSB_FIRST   0x00            /* The least significant bit is the first bit of the bit field */

/* Possible values for CPU_BYTE_ORDER (memory byte ordering) */
#undef HIGH_BYTE_FIRST
#undef LOW_BYTE_FIRST

#define HIGH_BYTE_FIRST 0x00        /* High order byte of a multi-byte value is located at the lowest address (Big Endian) */
#define LOW_BYTE_FIRST  0x01        /* Low order byte of a multi-byte value is located at the lowest address (Little Endian) */

/* Store to array and load from array. First parameter is destination, second is source.
 * p must be of pointer type (pointing in RAM) and val of integer type.
 */

#undef STORE_TO_BE16
#undef STORE_TO_LE16
#undef LOAD_FROM_BE16
#undef LOAD_FROM_LE16
#undef READ_BE16
#undef READ_LE16
#undef STORE_TO_BE32
#undef STORE_TO_LE32
#undef LOAD_FROM_BE32
#undef LOAD_FROM_LE32
#undef READ_BE32
#undef READ_LE32

#define STORE_TO_BE16(p, val) do {                               \
        ((uint8_t STDRAM_PTR) (p))[0] = (uint8_t) ((uint16_t) (val) >> 8);   \
        ((uint8_t STDRAM_PTR) (p))[1] = (uint8_t) ((uint16_t) (val));        \
    } while (0)

#define STORE_TO_LE16(p, val) do {                               \
        ((uint8_t STDRAM_PTR) (p))[0] = (uint8_t) ((uint16_t) (val));        \
        ((uint8_t STDRAM_PTR) (p))[1] = (uint8_t) ((uint16_t) (val) >> 8);   \
    } while (0)

#define LOAD_FROM_BE16(val, p) do {                              \
    (val) =   ((uint16_t) ((uint8_t STDRAM_PTR) (p))[0] << 8)    \
            | ((uint16_t) ((uint8_t STDRAM_PTR) (p))[1]);        \
    } while (0)

#define LOAD_FROM_LE16(val, p) do {                              \
    (val) =   ((uint16_t) ((uint8_t STDRAM_PTR) (p))[0])         \
            | ((uint16_t) ((uint8_t STDRAM_PTR) (p))[1] << 8);   \
    } while (0)

#define READ_BE16(p)                                             \
     ( ((uint16_t) ((uint8_t STDRAM_PTR) (p))[0] << 8)           \
     | ((uint16_t) ((uint8_t STDRAM_PTR) (p))[1]))

#define READ_LE16(p)                                             \
     ( ((uint16_t) ((uint8_t STDRAM_PTR) (p))[0])                \
     | ((uint16_t) ((uint8_t STDRAM_PTR) (p))[1] << 8))

#define STORE_TO_BE32(p, val) do {                               \
        ((uint8_t STDRAM_PTR) (p))[0] = (uint8_t) ((uint32_t) (val) >> 24);  \
        ((uint8_t STDRAM_PTR) (p))[1] = (uint8_t) ((uint32_t) (val) >> 16);  \
        ((uint8_t STDRAM_PTR) (p))[2] = (uint8_t) ((uint32_t) (val) >>  8);  \
        ((uint8_t STDRAM_PTR) (p))[3] = (uint8_t) ((uint32_t) (val));        \
    } while (0)

#define STORE_TO_LE32(p, val) do {                               \
        ((uint8_t STDRAM_PTR) (p))[0] = (uint8_t) ((uint32_t) (val));        \
        ((uint8_t STDRAM_PTR) (p))[1] = (uint8_t) ((uint32_t) (val) >>  8);  \
        ((uint8_t STDRAM_PTR) (p))[2] = (uint8_t) ((uint32_t) (val) >> 16);  \
        ((uint8_t STDRAM_PTR) (p))[3] = (uint8_t) ((uint32_t) (val) >> 24);  \
    } while (0)

#define LOAD_FROM_BE32(val, p) do {                              \
    (val) =   ((uint32_t) ((uint8_t STDRAM_PTR) (p))[0] << 24)   \
            | ((uint32_t) ((uint8_t STDRAM_PTR) (p))[1] << 16)   \
            | ((uint32_t) ((uint8_t STDRAM_PTR) (p))[2] <<  8)   \
            | ((uint32_t) ((uint8_t STDRAM_PTR) (p))[3]);        \
    } while (0)

#define LOAD_FROM_LE32(val, p) do {                              \
    (val) =   ((uint32_t) ((uint8_t STDRAM_PTR) (p))[0])         \
            | ((uint32_t) ((uint8_t STDRAM_PTR) (p))[1] <<  8)   \
            | ((uint32_t) ((uint8_t STDRAM_PTR) (p))[2] << 16)   \
            | ((uint32_t) ((uint8_t STDRAM_PTR) (p))[3] << 24);  \
    } while (0)

#define READ_BE32(p)                                             \
     ( ((uint32_t) ((uint8_t STDRAM_PTR) (p))[0] << 24)          \
     | ((uint32_t) ((uint8_t STDRAM_PTR) (p))[1] << 16)          \
     | ((uint32_t) ((uint8_t STDRAM_PTR) (p))[2] << 8)           \
     | ((uint32_t) ((uint8_t STDRAM_PTR) (p))[3]))

#define READ_LE32(p)                                             \
     ( ((uint32_t) ((uint8_t STDRAM_PTR) (p))[0])                \
     | ((uint32_t) ((uint8_t STDRAM_PTR) (p))[1] << 8)           \
     | ((uint32_t) ((uint8_t STDRAM_PTR) (p))[2] << 16)          \
     | ((uint32_t) ((uint8_t STDRAM_PTR) (p))[3] << 24))

/* generic macros for accesing/managing partial word segments */
/* Note: this replaces struct & unions for byte, word16, word32 access */
#undef LOBYTE
#undef HIBYTE

#define LOBYTE(x)                   ((uint8_t)(x))
#define HIBYTE(x)                   ((uint8_t)((x) >> 8))

/* Build a 16 bit word from two bytes */
#undef BUILD_WORD16
#define BUILD_WORD16(msb,lsb)         (((uint16_t)(msb) << 8) | ((uint16_t)(lsb) & 0x00FF))

/* DEPRECATED:Build a 16 bit word from two bytes, please use BUILD_WORD16() */
#undef BUILD_WORD
#define BUILD_WORD(msb, lsb) BUILD_WORD16(msb, lsb)

/* Obtain the least significant 16 bits on a 32 bits word */
#undef LOWORD16
#define LOWORD16(x)                 ((uint16_t)(x))

/* Obtain the most significant 16 bits on a 32 bits word */
#undef HIWORD16
#define HIWORD16(x)                 ((uint16_t)((x) >> 16))

/* byte swapping functions */
#undef SWAP_BYTES_UINT16_C
#undef SWAP_BYTES_UINT32_C
#undef SWAP_BYTES_UINT16
#undef SWAP_BYTES_UINT32

#define SWAP_BYTES_UINT16_C(value)  ((uint16_t)(((uint16_t)(value) >> 8) | ((uint16_t)(value) << 8)))
#define SWAP_BYTES_UINT32_C(value)  ((uint32_t)(((uint32_t)(value) >> 24) |               \
                                                (((uint32_t)(value) << 8) & 0x00FF0000) | \
                                                (((uint32_t)(value) >> 8) & 0x0000FF00) | \
                                                ((uint32_t)(value) << 24)))

#ifdef SWAP_BYTES_UINT16_ARCH
#define SWAP_BYTES_UINT16(value)    SWAP_BYTES_UINT16_ARCH(value)
#else
#define SWAP_BYTES_UINT16(value)    SWAP_BYTES_UINT16_C(value)
#endif
#ifdef SWAP_BYTES_UINT32_ARCH
#define SWAP_BYTES_UINT32(value)    SWAP_BYTES_UINT32_ARCH(value)
#else
#define SWAP_BYTES_UINT32(value)    SWAP_BYTES_UINT32_C(value)
#endif

/* deprecated macro name */
#undef INVERT_16BITS_ORDER
#define INVERT_16BITS_ORDER(value)  SWAP_BYTES_UINT16(value)

/* generic macros bit management */
#undef BIT_CLR
#undef BIT_SET
#undef IS_BIT_SET
#undef IS_BIT_CLR

#define BIT_CLR(var,bit)    ((var)&=~(1<<(bit)))
#define BIT_SET(var,bit)    ((var)|=(1<<(bit)))
#define IS_BIT_SET(var,bit) ((var) & (1<<(bit)))
#define IS_BIT_CLR(var,bit) (!((var) & (1<<(bit))))

/* generic macros for mathematical comparisons */

/* if we use an external framework, MAX etc... might be aleady defined */
#undef MAX
#undef MIN
#undef ABS
#undef NABS
#undef SIGN

#define MAX(x,y)    ((x) > (y) ? (x) : (y))
#define MIN(x,y)    ((x) < (y) ? (x) : (y))
#define ABS(x)      (((x) < 0) ? -(x) : (x))
/* negative ABS is well defined for typical signed integers (aka, it won't fail for the most negative number of the range */
#define NABS(x)     (((x) > 0) ? -(x) : (x))
#define SIGN(x)     (((x) < 0) ? -1 : +1)

/*
 * Helper macro whose result is 'low' if (val <= low)
 * 'high' if (val >= high)
 * 'val' if (low < val < high)
 */
#undef CLIP
#define CLIP(low, val, high)  MAX(low, MIN(val, high))

/* Division and rounding macros for unsigned integers. Warning, macros might overflow */
#undef FLOOR_UDIV
#undef CEIL_UDIV
#undef RND_UDIV

#define FLOOR_UDIV(x, y)   ((x) / (y))
#define CEIL_UDIV(x, y)    (((x) + (y) - 1) / (y))
#define RND_UDIV(x, y)     (((x) + (y) / 2) / (y))

/* Division and rounding macros for signed integers */
#undef FLOOR_SDIV
#undef CEIL_SDIV
#undef RND_SDIV

#define FLOOR_SDIV(x, y)   (((x) - (SIGN(x) != SIGN(y) ? (y) - SIGN(y) : 0)) / (y))
#define CEIL_SDIV(x, y)    (((x) + (SIGN(x) == SIGN(y) ? (y) - SIGN(y) : 0)) / (y))
#define RND_SDIV(x, y)     (((x) + (SIGN(x) * ABS(y)) / 2) / (y))

/*
 * Number of bits set to 1 in an unsigned integer not larger than 32 bits or
 * 64 bits, respectively (signed integers shall be type-cast to an unsigned
 * integer of the same size).
 *
 * Implementation note
 *
 * An alternate implementation is to replace the multiplication, shift, and
 * mask operations by a modulo operation:
 *
 * #define NB_BIT_1_32(x) \
 *     (((NB_BIT_1_32_NIBBLE(x) + (NB_BIT_1_32_NIBBLE(x) >> 4)) & \
 *       0x0F0F0F0F) % 255)
 *
 * #define NB_BIT_1_64(x) \
 *     (((NB_BIT_1_64_NIBBLE(x) + (NB_BIT_1_64_NIBBLE(x) >> 4)) & \
 *       0x0F0F0F0F0F0F0F0F) % 255)
 *
 * However, when these macros are computed in real-time (variables) rather
 * than at compile-time (constants), the multiplicative version is faster
 * that the one based on a division (modulo).  With an nRF52840, the it is
 * 43% faster (190 ns vs. 332 ns) for 32 bits and faster by a factor of 7.5
 * (424 ns vs. 3.21 us) for 64 bits.
 */
#undef NB_BIT_1_32_PAIR
#undef NB_BIT_1_32_NIBBLE
#undef NB_BIT_1_32

#define NB_BIT_1_32_PAIR(x) \
    ((x) - (((x) >> 1) & 0x55555555))
#define NB_BIT_1_32_NIBBLE(x) \
    ((NB_BIT_1_32_PAIR(x) & 0x33333333) + \
     ((NB_BIT_1_32_PAIR(x) >> 2) & 0x33333333))
#define NB_BIT_1_32(x) \
    (((((NB_BIT_1_32_NIBBLE(x) + (NB_BIT_1_32_NIBBLE(x) >> 4)) & \
        0x0F0F0F0F) * 0x01010101) >> 24) & 0xFF)

#undef NB_BIT_1_64_PAIR
#undef NB_BIT_1_64_NIBBLE
#undef NB_BIT_1_64

#define NB_BIT_1_64_PAIR(x) \
    ((x) - (((x) >> 1) & 0x5555555555555555))
#define NB_BIT_1_64_NIBBLE(x) \
    ((NB_BIT_1_64_PAIR(x) & 0x3333333333333333) + \
     ((NB_BIT_1_64_PAIR(x) >> 2) & 0x3333333333333333))
#define NB_BIT_1_64(x) \
    (((((NB_BIT_1_64_NIBBLE(x) + (NB_BIT_1_64_NIBBLE(x) >> 4)) & \
        0x0F0F0F0F0F0F0F0F) * 0x0101010101010101) >> 56) & 0xFF)

/* Back-ward compatibility (deprecated) */
#define NB_BIT_1(x)        NB_BIT_1_32(x)

/*
 * Helper macros to apply the token pasting operator and still expand adjacent
 * macros, the preprocessor would not expand a macro that is next to the ## operator
 * this construct allows this.
 */
#undef TOKENPASTE_INTERNAL
#undef TOKENPASTE
#undef TOKENPASTE3_INTERNAL
#undef TOKENPASTE3
#undef TOKENPASTE4_INTERNAL
#undef TOKENPASTE4
#undef TOKENPASTE5_INTERNAL
#undef TOKENPASTE5

#define TOKENPASTE_INTERNAL(a, b) a ## b
#define TOKENPASTE(a, b) TOKENPASTE_INTERNAL(a, b)

#define TOKENPASTE3_INTERNAL(a, b, c) a ## b ## c
#define TOKENPASTE3(a, b, c) TOKENPASTE3_INTERNAL(a, b, c)

#define TOKENPASTE4_INTERNAL(a, b, c, d) a ## b ## c ## d
#define TOKENPASTE4(a, b, c, d) TOKENPASTE4_INTERNAL(a, b, c, d)

#define TOKENPASTE5_INTERNAL(a, b, c, d, e) a ## b ## c ## d ## e
#define TOKENPASTE5(a, b, c, d, e) TOKENPASTE5_INTERNAL(a, b, c, d, e)

/*
 * Helper macros to apply the stringizing operator and still expand adjacent
 * macros, the preprocessor would not expand a macro that is next to the # operator
 * this construct allows this.
 */
#undef STRINGIFY_INTERNAL
#undef STRINGIFY
#undef WSTRINGIFY_INTERNAL
#undef WSTRINGIFY

#define STRINGIFY_INTERNAL(x)    #x
#define STRINGIFY(x)             STRINGIFY_INTERNAL(x)
#define WSTRINGIFY_INTERNAL(x)   L ## #x
#define WSTRINGIFY(x)            WSTRINGIFY_INTERNAL(x)

/* returns the number of elements in a static array */
#undef ARRAY_SIZE
#define ARRAY_SIZE(x)     (sizeof(x) / sizeof((x)[0]))

/* returns the size of a structure/union member */
#undef MEMBER_SIZE
#define MEMBER_SIZE(type, member) (sizeof(((type *) 0)->member))

/* returns the number of elements in an array which is a structure/union member */
#undef MEMBER_ARRAY_SIZE
#define MEMBER_ARRAY_SIZE(type, member) (ARRAY_SIZE(((type *) 0)->member))

/* bit definitions */

#undef BIT_0
#undef BIT_1
#undef BIT_2
#undef BIT_3
#undef BIT_4
#undef BIT_5
#undef BIT_6
#undef BIT_7
#undef BIT_8
#undef BIT_9
#undef BIT_10
#undef BIT_11
#undef BIT_12
#undef BIT_13
#undef BIT_14
#undef BIT_15
#undef BIT_16
#undef BIT_17
#undef BIT_18
#undef BIT_19
#undef BIT_20
#undef BIT_21
#undef BIT_22
#undef BIT_23
#undef BIT_24
#undef BIT_25
#undef BIT_26
#undef BIT_27
#undef BIT_28
#undef BIT_29
#undef BIT_30
#undef BIT_31

#if (CPU_BIT_ORDER == LSB_FIRST)

#define BIT_00   (0x00000001)
#define BIT_01   (0x00000002)
#define BIT_02   (0x00000004)
#define BIT_03   (0x00000008)
#define BIT_04   (0x00000010)
#define BIT_05   (0x00000020)
#define BIT_06   (0x00000040)
#define BIT_07   (0x00000080)
#define BIT_08   (0x00000100)
#define BIT_09   (0x00000200)
#define BIT_10   (0x00000400)
#define BIT_11   (0x00000800)
#define BIT_12   (0x00001000)
#define BIT_13   (0x00002000)
#define BIT_14   (0x00004000)
#define BIT_15   (0x00008000)
#define BIT_16   (0x00010000)
#define BIT_17   (0x00020000)
#define BIT_18   (0x00040000)
#define BIT_19   (0x00080000)
#define BIT_20   (0x00100000)
#define BIT_21   (0x00200000)
#define BIT_22   (0x00400000)
#define BIT_23   (0x00800000)
#define BIT_24   (0x01000000)
#define BIT_25   (0x02000000)
#define BIT_26   (0x04000000)
#define BIT_27   (0x08000000)
#define BIT_28   (0x10000000)
#define BIT_29   (0x20000000)
#define BIT_30   (0x40000000)
#define BIT_31   (0x80000000)

#elif (CPU_BIT_ORDER == MSB_FIRST)

#define BIT_00   (0x10000000)
#define BIT_01   (0x20000000)
#define BIT_02   (0x40000000)
#define BIT_03   (0x80000000)
#define BIT_04   (0x01000000)
#define BIT_05   (0x02000000)
#define BIT_06   (0x04000000)
#define BIT_07   (0x08000000)
#define BIT_08   (0x00100000)
#define BIT_09   (0x00200000)
#define BIT_10   (0x00400000)
#define BIT_11   (0x00800000)
#define BIT_12   (0x00010000)
#define BIT_13   (0x00020000)
#define BIT_14   (0x00040000)
#define BIT_15   (0x00080000)
#define BIT_16   (0x00001000)
#define BIT_17   (0x00002000)
#define BIT_18   (0x00004000)
#define BIT_19   (0x00008000)
#define BIT_20   (0x00000100)
#define BIT_21   (0x00000200)
#define BIT_22   (0x00000400)
#define BIT_23   (0x00000800)
#define BIT_24   (0x00000010)
#define BIT_25   (0x00000020)
#define BIT_26   (0x00000040)
#define BIT_27   (0x00000080)
#define BIT_28   (0x00000001)
#define BIT_29   (0x00000002)
#define BIT_30   (0x00000004)
#define BIT_31   (0x00000008)

#endif  /* CPU_BIT_ORDER */

#endif /* !defined(LTYPES_H) */
