#ifndef LFIXEDPOINT_H
#define LFIXEDPOINT_H

#include "ltypes.h"

/* Signed 64 bits Fixed Point types */
typedef int64_t sfp63_0_t;
typedef int64_t sfp62_1_t;
typedef int64_t sfp61_2_t;
typedef int64_t sfp60_3_t;
typedef int64_t sfp59_4_t;
typedef int64_t sfp58_5_t;
typedef int64_t sfp57_6_t;
typedef int64_t sfp56_7_t;
typedef int64_t sfp55_8_t;
typedef int64_t sfp54_9_t;
typedef int64_t sfp53_10_t;
typedef int64_t sfp52_11_t;
typedef int64_t sfp51_12_t;
typedef int64_t sfp50_13_t;
typedef int64_t sfp49_14_t;
typedef int64_t sfp48_15_t;
typedef int64_t sfp47_16_t;
typedef int64_t sfp46_17_t;
typedef int64_t sfp45_18_t;
typedef int64_t sfp44_19_t;
typedef int64_t sfp43_20_t;
typedef int64_t sfp42_21_t;
typedef int64_t sfp41_22_t;
typedef int64_t sfp40_23_t;
typedef int64_t sfp39_24_t;
typedef int64_t sfp38_25_t;
typedef int64_t sfp37_26_t;
typedef int64_t sfp36_27_t;
typedef int64_t sfp35_28_t;
typedef int64_t sfp34_29_t;
typedef int64_t sfp33_30_t;
typedef int64_t sfp32_31_t;
typedef int64_t sfp31_32_t;
typedef int64_t sfp30_33_t;
typedef int64_t sfp29_34_t;
typedef int64_t sfp28_35_t;
typedef int64_t sfp27_36_t;
typedef int64_t sfp26_37_t;
typedef int64_t sfp25_38_t;
typedef int64_t sfp24_39_t;
typedef int64_t sfp23_40_t;
typedef int64_t sfp22_41_t;
typedef int64_t sfp21_42_t;
typedef int64_t sfp20_43_t;
typedef int64_t sfp19_44_t;
typedef int64_t sfp18_45_t;
typedef int64_t sfp17_46_t;
typedef int64_t sfp16_47_t;
typedef int64_t sfp15_48_t;
typedef int64_t sfp14_49_t;
typedef int64_t sfp13_50_t;
typedef int64_t sfp12_51_t;
typedef int64_t sfp11_52_t;
typedef int64_t sfp10_53_t;
typedef int64_t sfp9_54_t;
typedef int64_t sfp8_55_t;
typedef int64_t sfp7_56_t;
typedef int64_t sfp6_57_t;
typedef int64_t sfp5_58_t;
typedef int64_t sfp4_59_t;
typedef int64_t sfp3_60_t;
typedef int64_t sfp2_61_t;
typedef int64_t sfp1_62_t;
typedef int64_t sfp0_63_t;

/* Unsigned 64 bits Fixed Point types */
typedef uint64_t ufp64_0_t;
typedef uint64_t ufp63_1_t;
typedef uint64_t ufp62_2_t;
typedef uint64_t ufp61_3_t;
typedef uint64_t ufp60_4_t;
typedef uint64_t ufp59_5_t;
typedef uint64_t ufp58_6_t;
typedef uint64_t ufp57_7_t;
typedef uint64_t ufp56_8_t;
typedef uint64_t ufp55_9_t;
typedef uint64_t ufp54_10_t;
typedef uint64_t ufp53_11_t;
typedef uint64_t ufp52_12_t;
typedef uint64_t ufp51_13_t;
typedef uint64_t ufp50_14_t;
typedef uint64_t ufp49_15_t;
typedef uint64_t ufp48_16_t;
typedef uint64_t ufp47_17_t;
typedef uint64_t ufp46_18_t;
typedef uint64_t ufp45_19_t;
typedef uint64_t ufp44_20_t;
typedef uint64_t ufp43_21_t;
typedef uint64_t ufp42_22_t;
typedef uint64_t ufp41_23_t;
typedef uint64_t ufp40_24_t;
typedef uint64_t ufp39_25_t;
typedef uint64_t ufp38_26_t;
typedef uint64_t ufp37_27_t;
typedef uint64_t ufp36_28_t;
typedef uint64_t ufp35_29_t;
typedef uint64_t ufp34_30_t;
typedef uint64_t ufp33_31_t;
typedef uint64_t ufp32_32_t;
typedef uint64_t ufp31_33_t;
typedef uint64_t ufp30_34_t;
typedef uint64_t ufp29_35_t;
typedef uint64_t ufp28_36_t;
typedef uint64_t ufp27_37_t;
typedef uint64_t ufp26_38_t;
typedef uint64_t ufp25_39_t;
typedef uint64_t ufp24_40_t;
typedef uint64_t ufp23_41_t;
typedef uint64_t ufp22_42_t;
typedef uint64_t ufp21_43_t;
typedef uint64_t ufp20_44_t;
typedef uint64_t ufp19_45_t;
typedef uint64_t ufp18_46_t;
typedef uint64_t ufp17_47_t;
typedef uint64_t ufp16_48_t;
typedef uint64_t ufp15_49_t;
typedef uint64_t ufp14_50_t;
typedef uint64_t ufp13_51_t;
typedef uint64_t ufp12_52_t;
typedef uint64_t ufp11_53_t;
typedef uint64_t ufp10_54_t;
typedef uint64_t ufp9_55_t;
typedef uint64_t ufp8_56_t;
typedef uint64_t ufp7_57_t;
typedef uint64_t ufp6_58_t;
typedef uint64_t ufp5_59_t;
typedef uint64_t ufp4_60_t;
typedef uint64_t ufp3_61_t;
typedef uint64_t ufp2_62_t;
typedef uint64_t ufp1_63_t;
typedef uint64_t ufp0_64_t;

/* Signed 32 bits Fixed Point types */
typedef int32_t sfp31_0_t;
typedef int32_t sfp30_1_t;
typedef int32_t sfp29_2_t;
typedef int32_t sfp28_3_t;
typedef int32_t sfp27_4_t;
typedef int32_t sfp26_5_t;
typedef int32_t sfp25_6_t;
typedef int32_t sfp24_7_t;
typedef int32_t sfp23_8_t;
typedef int32_t sfp22_9_t;
typedef int32_t sfp21_10_t;
typedef int32_t sfp20_11_t;
typedef int32_t sfp19_12_t;
typedef int32_t sfp18_13_t;
typedef int32_t sfp17_14_t;
typedef int32_t sfp16_15_t;
typedef int32_t sfp15_16_t;
typedef int32_t sfp14_17_t;
typedef int32_t sfp13_18_t;
typedef int32_t sfp12_19_t;
typedef int32_t sfp11_20_t;
typedef int32_t sfp10_21_t;
typedef int32_t sfp9_22_t;
typedef int32_t sfp8_23_t;
typedef int32_t sfp7_24_t;
typedef int32_t sfp6_25_t;
typedef int32_t sfp5_26_t;
typedef int32_t sfp4_27_t;
typedef int32_t sfp3_28_t;
typedef int32_t sfp2_29_t;
typedef int32_t sfp1_30_t;
typedef int32_t sfp0_31_t;

/* Unsigned 32 bits Fixed Point types */
typedef uint32_t ufp32_0_t;
typedef uint32_t ufp31_1_t;
typedef uint32_t ufp30_2_t;
typedef uint32_t ufp29_3_t;
typedef uint32_t ufp28_4_t;
typedef uint32_t ufp27_5_t;
typedef uint32_t ufp26_6_t;
typedef uint32_t ufp25_7_t;
typedef uint32_t ufp24_8_t;
typedef uint32_t ufp23_9_t;
typedef uint32_t ufp22_10_t;
typedef uint32_t ufp21_11_t;
typedef uint32_t ufp20_12_t;
typedef uint32_t ufp19_13_t;
typedef uint32_t ufp18_14_t;
typedef uint32_t ufp17_15_t;
typedef uint32_t ufp16_16_t;
typedef uint32_t ufp15_17_t;
typedef uint32_t ufp14_18_t;
typedef uint32_t ufp13_19_t;
typedef uint32_t ufp12_20_t;
typedef uint32_t ufp11_21_t;
typedef uint32_t ufp10_22_t;
typedef uint32_t ufp9_23_t;
typedef uint32_t ufp8_24_t;
typedef uint32_t ufp7_25_t;
typedef uint32_t ufp6_26_t;
typedef uint32_t ufp5_27_t;
typedef uint32_t ufp4_28_t;
typedef uint32_t ufp3_29_t;
typedef uint32_t ufp2_30_t;
typedef uint32_t ufp1_31_t;
typedef uint32_t ufp0_32_t;

/* Signed 16 bit fixed point types */
typedef int16_t sfp15_0_t;
typedef int16_t sfp14_1_t;
typedef int16_t sfp13_2_t;
typedef int16_t sfp12_3_t;
typedef int16_t sfp11_4_t;
typedef int16_t sfp10_5_t;
typedef int16_t sfp9_6_t;
typedef int16_t sfp8_7_t;
typedef int16_t sfp7_8_t;
typedef int16_t sfp6_9_t;
typedef int16_t sfp5_10_t;
typedef int16_t sfp4_11_t;
typedef int16_t sfp3_12_t;
typedef int16_t sfp2_13_t;
typedef int16_t sfp1_14_t;
typedef int16_t sfp0_15_t;

/* Unsigned 16 bit fixed point types */
typedef uint16_t ufp16_0_t;
typedef uint16_t ufp15_1_t;
typedef uint16_t ufp14_2_t;
typedef uint16_t ufp13_3_t;
typedef uint16_t ufp12_4_t;
typedef uint16_t ufp11_5_t;
typedef uint16_t ufp10_6_t;
typedef uint16_t ufp9_7_t;
typedef uint16_t ufp8_8_t;
typedef uint16_t ufp7_9_t;
typedef uint16_t ufp6_10_t;
typedef uint16_t ufp5_11_t;
typedef uint16_t ufp4_12_t;
typedef uint16_t ufp3_13_t;
typedef uint16_t ufp2_14_t;
typedef uint16_t ufp1_15_t;
typedef uint16_t ufp0_16_t;

/* Converts x into a fixed point representation at compile time. (x
 * could be a float/double constant, so use * (multiplication) instead
 * of << (shifting): this will properly calculate the fractional
 * part. */
#define SFP15_0(x)       ((sfp15_0_t) ((x) *     1))
#define SFP14_1(x)       ((sfp14_1_t) ((x) *     2))
#define SFP13_2(x)       ((sfp13_2_t) ((x) *     4))
#define SFP12_3(x)       ((sfp12_3_t) ((x) *     8))
#define SFP11_4(x)       ((sfp11_4_t) ((x) *    16))
#define SFP10_5(x)       ((sfp10_5_t) ((x) *    32))
#define SFP9_6(x)        ((sfp9_6_t)  ((x) *    64))
#define SFP8_7(x)        ((sfp8_7_t)  ((x) *   128))
#define SFP7_8(x)        ((sfp7_8_t)  ((x) *   256))
#define SFP6_9(x)        ((sfp6_9_t)  ((x) *   512))
#define SFP5_10(x)       ((sfp5_10_t) ((x) *  1024))
#define SFP4_11(x)       ((sfp4_11_t) ((x) *  2048))
#define SFP3_12(x)       ((sfp3_12_t) ((x) *  4096))
#define SFP2_13(x)       ((sfp2_13_t) ((x) *  8192))
#define SFP1_14(x)       ((sfp1_14_t) ((x) * 16384))
#define SFP0_15(x)       ((sfp0_15_t) ((x) * 32768))

#define UFP16_0(x)       ((ufp16_0_t) ((x) *     1))
#define UFP15_1(x)       ((ufp15_1_t) ((x) *     2))
#define UFP14_2(x)       ((ufp14_2_t) ((x) *     4))
#define UFP13_3(x)       ((ufp13_3_t) ((x) *     8))
#define UFP12_4(x)       ((ufp12_4_t) ((x) *    16))
#define UFP11_5(x)       ((ufp11_5_t) ((x) *    32))
#define UFP10_6(x)       ((ufp10_6_t) ((x) *    64))
#define UFP9_7(x)        ((ufp9_7_t)  ((x) *   128))
#define UFP8_8(x)        ((ufp8_8_t)  ((x) *   256))
#define UFP7_9(x)        ((ufp7_9_t)  ((x) *   512))
#define UFP6_10(x)       ((ufp6_10_t) ((x) *  1024))
#define UFP5_11(x)       ((ufp5_11_t) ((x) *  2048))
#define UFP4_12(x)       ((ufp4_12_t) ((x) *  4096))
#define UFP3_13(x)       ((ufp3_13_t) ((x) *  8192))
#define UFP2_14(x)       ((ufp2_14_t) ((x) * 16384))
#define UFP1_15(x)       ((ufp1_15_t) ((x) * 32768))
#define UFP0_16(x)       ((ufp0_16_t) ((x) * 65536))

/* Converts x into a fixed point representation at compile time. (x
 * could be a float/double constant, so use * (multiplication) instead
 * of << (shifting): this will properly calculate the fractional
 * part. The length of the fractionary part is specified as second arg */
#define fxp_UFP16(op, fractLength)    \
    ((uint16_t) ((op) * (1LL << (fractLength))))

#define fxp_SFP16(op, fractLength)    \
    ((int16_t) ((op) * (1LL << (fractLength))))

#define fxp_UFP32(op, fractLength)    \
    ((uint32_t) ((op) * (1LL << (fractLength))))

#define fxp_SFP32(op, fractLength)    \
    ((int32_t) ((op) * (1LL << (fractLength))))

#define fxp_SFP64(op, fractLength)    \
    ((int64_t) ((op) * (1LL << (fractLength))))

#define fxp_UFP64(op, fractLength)    \
    ((uint64_t) ((op) * (1LL << (fractLength))))

#define fxp_GET_INT_PART(op, fractLength)       \
    (((op) >> (fractLength)) << (fractLength))

#define fxp_GET_FRACT_PART(op, fractLength)             \
    ((op) - fxp_SFP_GET_INT_PART(op, fractLength))

#define fxp_UFP_GET_INT_PART_ROUNDED(op, fractLength)                   \
    (fxp_UROUNDED_NEXT_INTEG_RIGHT_SHIFT(op, fractLength) << (fractLength))

#define fxp_UFP_GET_FRACT_PART_ROUNDED(op, fractLength)         \
    ((op) - fxp_UFP_GET_INT_PART_ROUNDED(op, fractLength))

#define fxp_SFP_GET_INT_PART_ROUNDED(op, fractLength)                   \
    (fxp_SROUNDED_NEXT_INTEG_RIGHT_SHIFT(op, fractLength) << (fractLength))

#define fxp_SFP_GET_FRACT_PART_ROUNDED(op, fractLength)         \
    ((op) - fxp_SFP_GET_INT_PART_ROUNDED(op, fractLength))

/* ---- Rounded Shift Operations ------------------------------------------- */

#define fxp_CEIL_ROUND_R_SHIFT(inData, N)       \
    (((inData) + ((1LL << (N)) - 1)) >> (N))

#define fxp_FLOOR_ROUND_R_SHIFT(inData, N) \
    ((inData) >> (N))

/* Right shift with rounding to next integer*/
#define fxp_SFP_ROUND_NXT_INT_R_SHIFT(op, shift)                    \
    (((op) < 0) ? (fxp_CEIL_ROUND_R_SHIFT(((op) - (1LL << ((shift) - 1))), (shift))): \
     (fxp_FLOOR_ROUND_R_SHIFT(((op) + (1LL << ((shift) - 1))), (shift))))

/* Unsigned Right shift with rounding to next integer*/
#define fxp_UFP_ROUND_NXT_INT_R_SHIFT(op, shift)                    \
    (fxp_FLOOR_ROUND_R_SHIFT(((op) + (1LL << ((shift) - 1))), (shift)))

/* ---- Saturation Operations ---------------------------------------------- */

/* clampVal must be an absolute, positive value ! */
#define fxp_SFP_SATURATE_TO_ABS(input, absClampVal)                  \
    (((input) > (absClampVal)) ? (absClampVal) : \
     (((input) < - (absClampVal)) ? ( - (absClampVal)) : (input)))

/* ---- Fixed Point Multiplication, 32bit X 32bit into 32bit --------------- */

/* Use this macro ONLY if fractRes <= fractA + fractB */
#define fxp_SMUL_32X32_TO_32(fractA, fractB, fractRes, opA, opB)       \
    ((int32_t) ((((int64_t) (opA)) * ((int64_t) (opB))) >> ((fractA) + (fractB) - (fractRes))))

/* Use this macro ONLY if fractRes <= fractA + fractB */
#define fxp_UMUL_32X32_TO_32(fractA, fractB, fractRes, opA, opB)       \
    ((uint32_t) ((((uint64_t) (opA)) * ((uint64_t) (opB))) >> ((fractA) + (fractB) - (fractRes))))

/* Same as fxp_SMUL_32X32_TO_32, with rounding to next integer.
 * Use this function ONLY if fractRes < fractA + fractB (i.e. right shift is needed).
 * If fractRes = fractA + fractB (i.e. no right shift is needed)
 * use fxp_SMUL_32X32_TO_32 instead */
#define fxp_SMUL_32X32_TO_32_ROUND(fractA, fractB, fractRes, opA, opB)  \
    ((int32_t) fxp_SFP_ROUND_NXT_INT_R_SHIFT((((int64_t) (opA)) * ((int64_t) (opB))), \
                                             ((fractA) + (fractB) - (fractRes))))

/* Same as fxp_UMUL_32X32_TO_32, with rounding to next integer.
 * Use this function ONLY if fractRes < fractA + fractB (i.e. right shift is needed).
 * If fractRes = fractA + fractB (i.e. no right shift is needed)
 * use fxp_UMUL_32X32_TO_32 instead */
#define fxp_UMUL_32X32_TO_32_ROUND(fractA, fractB, fractRes, opA, opB)  \
    ((uint32_t) fxp_UFP_ROUND_NXT_INT_R_SHIFT((((uint64_t) (opA)) * ((uint64_t) (opB))), \
                                              ((fractA) + (fractB) - (fractRes))))

/* Same as fxp_SMUL_32X32_TO_32_ROUND, with saturation to the max 32bit result,
 * whichever the fixed point representation of the result is.
 * E.G.:  the max value of result of sfp3_28 x sfp3_28 into sfp1_30 will be (+/-)1.9999~,
 * therefore values between 1.999~ and 63.999~ would cause rollover in the result if
 * saturation is not performed.
 * Use this function ONLY if  fractRes < fractA + fractB (i.e. right shift is needed). */
#define fxp_SMUL_32X32_TO_32_ROUND_SAT(fractA, fractB, fractRes, opA, opB)  \
    ((int32_t) (fxp_SFP_SATURATE_TO_ABS(                              \
                   (fxp_SFP_ROUND_NXT_INT_R_SHIFT((((int64_t) (opA)) * ((int64_t) (opB))), \
                                                  ((fractA) + (fractB) - (fractRes)))), \
                   INT32_MAX)))

/* ---- Fixed Point Multiplication, 32bit X 32bit into 64bit --------------- */

#define fxp_SMUL_32X32_TO_64(opA, opB)          \
    (((int64_t) (opA)) * ((int64_t) (opB)))

/* Same as fxp_SMUL_32X32_TO_64, with rounding to next integer.
 * Use this function ONLY if fractRes < fractA + fractB (i.e. right shift is needed).
 * If fractRes = fractA + fractB (i.e. no right shift is needed)
 * use fxp_SMUL_32X32_TO_64 instead */
#define fxp_SMUL_32X32_TO_64_ROUND(fractA, fractB, fractRes, opA, opB)     \
    (fxp_SFP_ROUND_NXT_INT_R_SHIFT((((int64_t) (opA)) * ((int64_t) (opB))), \
                                        ((fractA) + (fractB) - (fractRes))))

/* ---- Fixed Point Division, 32bit X 32bit into 32bit --------------------- */

/* Signed division 32 by 32 into 32.
 * Use this macro ONLY if frDividend + 32 >= frDivisor + frQuotient */
#define fxp_SDIV_32_32_TO_32(frDividend, frDivisor, frQuotient, dividend, divisor) \
    (( int32_t) (((((int64_t) (dividend)) << 32) / ((int64_t) (divisor))) >> \
                 (frDividend + 32 - (frDivisor) - (frQuotient))))

/* Unsigned division 32 by 32 into 32.
 * Use this macro ONLY if frDividend + 32 >= frDivisor + frQuotient */
#define fxp_UDIV_32_32_TO_32(frDividend, frDivisor, frQuotient, dividend, divisor) \
    ((uint32_t) (((((uint64_t) (dividend)) << 32) / ((uint64_t) (divisor))) >> \
                 ((frDividend) + 32 - (frDivisor) - (frQuotient))))

/* Same as fxp_SDIV_32_32_TO_32, with rounding to next integer at the end.
 * Use this function ONLY if frDividend + 32 >= frDivisor + frQuotient (i.e. right shift is needed).
 * If frDividend + 32 = frDivisor + frQuotient (i.e. no right shift is needed)
 * use fxp_SDIV_32_32_TO_32 instead */
#define fxp_SDIV_32_32_TO_32_ROUND(frDividend, frDivisor, frQuotient, dividend, divisor) \
    ((int32_t) (fxp_SFP_ROUND_NXT_INT_R_SHIFT(((((int64_t) (dividend)) << 32) / ((int64_t) (divisor))),\
                                              (((frDividend)) + 32 - (frDivisor) - (frQuotient)))))

/* Same as fxp_UDIV_32_32_TO_32, with rounding to next integer at the end.
 * Use this function ONLY if frDividend + 32 >= frDivisor + frQuotient (i.e. right shift is needed).
 * If frDividend + 32 = frDivisor + frQuotient (i.e. no right shift is needed)
 * use fxp_UDIV_32_32_TO_32 instead */
#define fxp_UDIV_32_32_TO_32_ROUND(frDividend, frDivisor, frQuotient, dividend, divisor) \
    ((uint32_t) (fxp_UFP_ROUND_NXT_INT_R_SHIFT(((((uint64_t) (dividend)) << 32) / ((uint64_t) (divisor))),\
                                              ((frDividend) + 32 - (frDivisor) - (frQuotient)))))

#endif /* LFIXEDPOINT_H */
