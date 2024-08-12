/*****************************************************************************
 Copyright (C) 2015 LOGITECH
------------------------------------------------------------------------------

 rgb_algorithms.c
******************************************************************************/

/*
** --------------------------------------------------------
** Include section
** --------------------------------------------------------
*/
#include "rgb_algorithms.h"

/*
** --------------------------------------------------------
** Constants Definitions
** --------------------------------------------------------
*/
#define V_MAX 1.0
#define H_MAX 1.0
#define S_MAX 1.0

#define H_MAX_4_27 ((sfp4_27_t) fxp_SFP32(H_MAX, 27))
#define S_MAX_4_27 ((sfp4_27_t) fxp_SFP32(S_MAX, 27))
#define V_MAX_4_27 ((sfp4_27_t) fxp_SFP32(V_MAX, 27))

/*
** --------------------------------------------------------
** Type Definitions
** --------------------------------------------------------
*/

/*
** --------------------------------------------------------
** Exported Global Data
** --------------------------------------------------------
*/

/*
** --------------------------------------------------------
** Private Data
** --------------------------------------------------------
*/

static uint8_t GAMMA_8BIT_TABLE[256] =
{0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
 0,   0,   1,   1,   1,   1,   1,   1,   1,   1,   1,   1,   2,
 2,   2,   2,   2,   2,   2,   3,   3,   3,   3,   3,   4,   4,
 4,   4,   5,   5,   5,   5,   6,   6,   6,   6,   7,   7,   7,
 8,   8,   8,   9,   9,   9,  10,  10,  11,  11,  11,  12,  12,
 13,  13,  13,  14,  14,  15,  15,  16,  16,  17,  17,  18,  18,
 19,  19,  20,  20,  21,  22,  22,  23,  23,  24,  25,  25,  26,
 26,  27,  28,  28,  29,  30,  30,  31,  32,  33,  33,  34,  35,
 35,  36,  37,  38,  39,  39,  40,  41,  42,  43,  43,  44,  45,
 46,  47,  48,  49,  49,  50,  51,  52,  53,  54,  55,  56,  57,
 58,  59,  60,  61,  62,  63,  64,  65,  66,  67,  68,  69,  70,
 71,  73,  74,  75,  76,  77,  78,  79,  81,  82,  83,  84,  85,
 87,  88,  89,  90,  91,  93,  94,  95,  97,  98,  99, 100, 102,
 103, 105, 106, 107, 109, 110, 111, 113, 114, 116, 117, 119, 120,
 121, 123, 124, 126, 127, 129, 130, 132, 133, 135, 137, 138, 140,
 141, 143, 145, 146, 148, 149, 151, 153, 154, 156, 158, 159, 161,
 163, 165, 166, 168, 170, 172, 173, 175, 177, 179, 181, 182, 184,
 186, 188, 190, 192, 194, 196, 197, 199, 201, 203, 205, 207, 209,
 211, 213, 215, 217, 219, 221, 223, 225, 227, 229, 231, 234, 236,
 238, 240, 242, 244, 246, 248, 251, 253, 255};

/*
** --------------------------------------------------------
** Local Function Prototypes
** --------------------------------------------------------
*/

/*
** --------------------------------------------------------
** Inline Code Definition
** --------------------------------------------------------
*/
#if !defined(rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS)
error rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS must be defined
#endif /* !defined(rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS) */

/*
** --------------------------------------------------------
** Function definitions
** --------------------------------------------------------
*/

void rgb_initialise(void)
{
}

/*
** Apply Gamma 8bit -> 8bit table to linearize the sRGB input component
** C_linearRGB = C_sRGB ^ 2.2
**
*/
uint8_t rgb_gammaCrt8Table(volatile uint8_t geVal)
{
    return GAMMA_8BIT_TABLE[geVal];
}

/*
** Apply Gamma function to linearize the sRGB input component
** C_linearRGB = C_sRGB ^ 2.2
**
*/
uint16_t rgb_gammaCrt16Calc(volatile uint16_t geVal)
{
#if !defined(GAMMA_APPROX_ORDER)
error GAMMA approximation Order must be defined
#endif /* !defined(GAMMA_APPROX_ORDER) */
#if GAMMA_APPROX_ORDER > 5
error GAMMA approximation Order is max 5
#endif /* GAMMA_APPROX_ORDER > 5 */
#if GAMMA_APPROX_ORDER < 1
error GAMMA approximation Order is min 1
#endif /* GAMMA_APPROX_ORDER < 1 */

    sfp2_29_t geVal_29, geVal_2_29, geValminus1_29, container_29;

    sfp5_58_t container_58;
    sfp31_0_t container_0;
    uint16_t ClinearRGB;

    geVal_29 = fxp_SDIV_32_32_TO_32(0, 0, 29, (sfp31_0_t) geVal , (sfp31_0_t) UINT16_MAX);
    geValminus1_29 = geVal_29 - ((sfp2_29_t) fxp_SFP32(1.0, 29));

    geVal_2_29 = fxp_SMUL_32X32_TO_32(29, 29, 29, geVal_29, geVal_29);

#if GAMMA_APPROX_ORDER > 1
    sfp2_29_t  geValminus1_2_29;
    geValminus1_2_29 = fxp_SMUL_32X32_TO_32(29, 29, 29, geValminus1_29, geValminus1_29);
#endif /* GAMMA_APPROX_ORDER > 1 */

#if GAMMA_APPROX_ORDER > 2
    sfp2_29_t geValminus1_3_29;
    geValminus1_3_29 = fxp_SMUL_32X32_TO_32(29, 29, 29, geValminus1_2_29, geValminus1_29);
#endif /* GAMMA_APPROX_ORDER > 2 */

#if GAMMA_APPROX_ORDER > 3
    sfp2_29_t geValminus1_4_29;
    geValminus1_4_29 = fxp_SMUL_32X32_TO_32(29, 29, 29, geValminus1_3_29, geValminus1_29);
#endif /* GAMMA_APPROX_ORDER > 3 */

#if GAMMA_APPROX_ORDER > 4
    sfp2_29_t geValminus1_5_29;
    geValminus1_5_29 = fxp_SMUL_32X32_TO_32(29, 29, 29, geValminus1_4_29, geValminus1_29);
#endif /* GAMMA_APPROX_ORDER > 4 */

    /* We calculate the series for geVal^0.2*/
    container_58 = (sfp5_58_t) fxp_SFP64(1.0, 58);

    /* sfp2_29_t * sfp2_29_t -> sfp4_58_t */
    container_58 += fxp_SMUL_32X32_TO_64(rgb_TAYLOR_B_02_1_29, geValminus1_29);

#if GAMMA_APPROX_ORDER > 1
    container_58 += fxp_SMUL_32X32_TO_64(rgb_TAYLOR_B_02_2_29, geValminus1_2_29);
#endif /* GAMMA_APPROX_ORDER > 1 */
#if GAMMA_APPROX_ORDER > 2
    container_58 += fxp_SMUL_32X32_TO_64(rgb_TAYLOR_B_02_3_29, geValminus1_3_29);
#endif /* GAMMA_APPROX_ORDER > 2 */
#if GAMMA_APPROX_ORDER > 3
    container_58 += fxp_SMUL_32X32_TO_64(rgb_TAYLOR_B_02_4_29, geValminus1_4_29);
#endif /* GAMMA_APPROX_ORDER > 3 */
#if GAMMA_APPROX_ORDER > 4
    container_58 += fxp_SMUL_32X32_TO_64(rgb_TAYLOR_B_02_5_29, geValminus1_5_29);
#endif /* GAMMA_APPROX_ORDER > 4 */
    container_29 = (sfp2_29_t) fxp_SFP_ROUND_NXT_INT_R_SHIFT(container_58,29);

    /* geVal^2 * geVal^0.2 */
    container_29 = fxp_SMUL_32X32_TO_32(29, 29, 29, geVal_2_29, container_29);

    if (container_29 > ((sfp2_29_t) fxp_SFP32(1.0, 29)))
    {
        container_29 = (sfp2_29_t) fxp_SFP32(1.0, 29);
    }
    else if (container_29 < 0x00000000)
    {
        container_29 = 0x00000000;
    }

    container_0 = fxp_SMUL_32X32_TO_32(29, 0, 0, container_29, ((sfp31_0_t) UINT16_MAX));

    ClinearRGB = (uint16_t) container_0;

    return ClinearRGB;
}

/*
** Function to linearize a set of sRGB input components
** C_linearRGB = C_sRGB ^ 2.2
**
*/
void rgb_gammaCrt16CalcRgb(volatile rgb_rgbComponents_ts *rgbIn, volatile rgb_rgbComponents_ts *rgbOut)
{
    rgbOut->r = rgb_gammaCrt16Calc(rgbIn->r);
    rgbOut->g = rgb_gammaCrt16Calc(rgbIn->g);
    rgbOut->b = rgb_gammaCrt16Calc(rgbIn->b);
}

/*
** HSV: Hue, Saturation, Value
** H: position in the spectrum
** S: color saturation ("purity")
** V: color brightness

    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc-minc) / maxc
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)

    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, s, v

*/
void rgb_rgbToHsv(volatile rgb_rgbComponents_ts *rgb, volatile rgb_hsvComponents_ts *hsv)
{
    sfp4_27_t invMaxComp_minComp, rc, gc, bc, tmpH;
    sfp31_0_t  Rin, Gin, Bin, maxComp, minComp, maxComp_minComp;

    Rin = (sfp31_0_t) rgb->r;
    Gin = (sfp31_0_t) rgb->g;
    Bin = (sfp31_0_t) rgb->b;

    maxComp = MAX(Rin, Gin);
    maxComp = MAX(Bin, maxComp);

    minComp = MIN(Rin, Gin);
    minComp = MIN(Bin, minComp);

    hsv->v = fxp_SDIV_32_32_TO_32_ROUND(0, 0, 27, maxComp , ((sfp31_0_t) UINT16_MAX));

    if (minComp == maxComp)
    {
        hsv->h = 0x00000000;
        hsv->s = 0x00000000;
        return;
    }

    maxComp_minComp = maxComp - minComp;
    invMaxComp_minComp = fxp_SDIV_32_32_TO_32_ROUND(27, 0, 27, ((sfp4_27_t) fxp_SFP32(1.0, 27)), maxComp_minComp);

    hsv->s = fxp_SDIV_32_32_TO_32_ROUND(0, 0, 27, maxComp_minComp, maxComp);

    /*fractA + fractB = fractRes -> no rounding needed in mult */
    rc = fxp_SMUL_32X32_TO_32(0,27,27, (maxComp - Rin), invMaxComp_minComp);
    gc = fxp_SMUL_32X32_TO_32(0,27,27, (maxComp - Gin), invMaxComp_minComp);
    bc = fxp_SMUL_32X32_TO_32(0,27,27, (maxComp - Bin), invMaxComp_minComp);

    if (Rin == maxComp)
    {
        tmpH = bc - gc;
    }
    else if (Gin == maxComp)
    {
        tmpH = ((sfp4_27_t) fxp_SFP32(2.0, 27)) + rc - bc;
    }
    else
    {
        tmpH = ((sfp4_27_t) fxp_SFP32(4.0, 27)) + gc - rc;
    }

    tmpH = fxp_SDIV_32_32_TO_32_ROUND(27, 27, 27, tmpH, ((sfp4_27_t) fxp_SFP32(6.0, 27)));

    /* tmpH = tmpH % 1 */
    /* Modulus has to be calculated using signed integers, in the way: a%b = a-b*floor(a/b)
       in our case: a%1 = a - floor(a). Since tmpH/6 will always be bigger than -1 and smaller than 1
       a%1 = (a<0)?(1+a):(a) */
    if (tmpH < 0)
    {
        tmpH = ((sfp4_27_t) fxp_SFP32(1.0, 27)) + tmpH;
    }
    hsv->h = tmpH;
}

/*
** HSV: Hue, Saturation, Value
** H: position in the spectrum, must be >= 0.0 and <= 1.0
** S: color saturation ("purity"), must be >= 0.0 and <= 1.0
** V: color brightness, must be >= 0.0 and <= 1.0

    if s == 0.0:
        return v, v, v
    i = int(h*6.0) # XXX assume int() truncates!
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q
*/
void rgb_hsvToRgb(volatile rgb_hsvComponents_ts *hsv, volatile rgb_rgbComponents_ts *rgb)
{
    int8_t modInt6H;
    sfp4_27_t tmpI, int6H, fract6H, p, q, t, tmpQ, tmpP, tmpT;
    uint16_t p_16, q_16, t_16, v_16;
    sfp31_0_t p_31_0, q_31_0, t_31_0, v_31_0;

    v_31_0 = fxp_SMUL_32X32_TO_32_ROUND(27, 0, 0, hsv->v, ((sfp31_0_t) UINT16_MAX));
    if (v_31_0 > UINT16_MAX)
    {
        v_31_0 = UINT16_MAX;
    }
    v_16 = (uint16_t) v_31_0;

    if (hsv->s == 0x00000000)
    {
        rgb->r = v_16;
        rgb->g = v_16;
        rgb->b = v_16;
    }

    tmpI = fxp_SMUL_32X32_TO_32_ROUND(27, 27, 27, ((sfp4_27_t) fxp_SFP32(6.0, 27)), hsv->h);
    int6H = fxp_GET_INT_PART(tmpI, 27);

    fract6H = tmpI - int6H;

    tmpP = ((sfp4_27_t) fxp_SFP32(1.0, 27)) - hsv->s;
    p =  fxp_SMUL_32X32_TO_32_ROUND(27, 27, 27, hsv->v, tmpP);

    tmpQ = fxp_SMUL_32X32_TO_32_ROUND(27, 27, 27, hsv->s, fract6H);
    tmpQ =((sfp4_27_t) fxp_SFP32(1.0, 27)) - tmpQ;
    q = fxp_SMUL_32X32_TO_32_ROUND(27, 27, 27, hsv->v, tmpQ);

    tmpT = ((sfp4_27_t) fxp_SFP32(1.0, 27)) - fract6H;
    tmpT = fxp_SMUL_32X32_TO_32_ROUND(27, 27, 27, hsv->s, tmpT);
    tmpT = ((sfp4_27_t) fxp_SFP32(1.0, 27)) - tmpT;
    t = fxp_SMUL_32X32_TO_32_ROUND(27, 27, 27, hsv->v, tmpT);

    p_31_0 = fxp_SMUL_32X32_TO_32_ROUND(27, 0, 0, p, ((sfp31_0_t) UINT16_MAX));
    if (p_31_0 > UINT16_MAX)
    {
        p_31_0 = UINT16_MAX;
    }
    q_31_0 = fxp_SMUL_32X32_TO_32_ROUND(27, 0, 0, q, ((sfp31_0_t) UINT16_MAX));
    if (q_31_0 > UINT16_MAX)
    {
        q_31_0 = UINT16_MAX;
    }
    t_31_0 = fxp_SMUL_32X32_TO_32_ROUND(27, 0, 0, t, ((sfp31_0_t) UINT16_MAX));
    if (t_31_0 > UINT16_MAX)
    {
        t_31_0 = UINT16_MAX;
    }

    p_16 = (uint16_t) p_31_0;
    q_16 = (uint16_t) q_31_0;
    t_16 = (uint16_t) t_31_0;

    modInt6H = (int8_t) (int6H >> 27); /* No need to round here, fractionary part is zero */
    modInt6H = modInt6H % 6;

    switch(modInt6H)
    {
    case 0:
        rgb->r = v_16;
        rgb->g = t_16;
        rgb->b = p_16;
        break;
    case 1:
        rgb->r = q_16;
        rgb->g = v_16;
        rgb->b = p_16;
        break;
    case 2:
        rgb->r = p_16;
        rgb->g = v_16;
        rgb->b = t_16;
        break;
    case 3:
        rgb->r = p_16;
        rgb->g = q_16;
        rgb->b = v_16;
        break;
    case 4:
        rgb->r = t_16;
        rgb->g = p_16;
        rgb->b = v_16;
        break;
    case 5:
        rgb->r = v_16;
        rgb->g = p_16;
        rgb->b = q_16;
        break;
    }
}

/*
** Function to:
**   -apply the RGB calibration coefficients
**   -calculate and apply the boost factor, to allow rising the LED intensity
**    up to the limit given by (the most restrictive of the following):
**        -The max current allowed per die
**        -The max current allowed in total per RGB LED lamp
** keeping the R,G,B component ratios, thus chroma.
** The constant rgb_MAX_DIE_OVER_MAX_LAMP_CURRENT_UFP1_31 defines the ratio between
** die and total lamp current and must be defined in the project (rgb_algorithms_cfg.h)
** Input:
**        volatile rgb_rgbComponents_ts *rgb
**        volatile uint8_t *calibration
** Output:
**        volatile rgb_rgbComponents_ts *rgbCalBoosted
**        ufp16_16_t boostResult
*/
ufp16_16_t rgb_applyCalibrationAndBoost(volatile rgb_rgbComponents_ts *rgb,
                                        volatile uint8_t *calibration,
                                        volatile rgb_rgbComponents_ts *rgbCalBoosted)
{
/* Calculating 1/k instead of k allows the best code optimisation by far */
/*              I_maxDie                                                 */
/*  1/K_lamp = ----------- x (rIn x rCal + gIn x gCal + bIn x bCal)      */
/*              I_maxLamp                                                */
/*                                                                       */
/*  1/K_r  =  rIn x rCal                                                 */
/*  1/K_g  =  gIn x gCal                                                 */
/*  1/K_b  =  bIn x bCal                                                 */
/*                                 1                                     */
/*  K = max(R,G,B) x -----------------------------------                 */
/*                    max(1/K_lamp, 1/K_r, 1/K_g, 1/K_b)                 */
/*                                                                       */
/*  Rcalboosted = rIn * rCal * K                                         */
/*  Gcalboosted = gIn * gCal * K                                         */
/*  Bcalboosted = bIn * bCal * K                                         */

    ufp16_16_t boostResult;
    ufp26_6_t oneOverK_lamp, oneOverK_r, oneOverK_g, oneOverK_b, maxOneOverK;
    ufp32_0_t rIn, gIn, bIn, rCal, gCal, bCal, maxRgb, rCalibrated, gCalibrated, bCalibrated,
        rCalBoosted32, gCalBoosted32, bCalBoosted32;

    rIn = (ufp32_0_t) rgb->r;
    gIn = (ufp32_0_t) rgb->g;
    bIn = (ufp32_0_t) rgb->b;

    /* calibration array contains the calibration values in the order rInR, gIn, bIn */
    rCal = (ufp32_0_t) calibration[0];
    gCal = (ufp32_0_t) calibration[1];
    bCal = (ufp32_0_t) calibration[2];

    rCalibrated =  rIn * rCal;
    gCalibrated =  gIn * gCal;
    bCalibrated =  bIn * bCal;

    oneOverK_r =(ufp26_6_t) fxp_UFP32(rCalibrated, 6); /* used range: ufp24_6 */
    oneOverK_g =(ufp26_6_t) fxp_UFP32(gCalibrated, 6); /* used range: ufp24_6 */
    oneOverK_b =(ufp26_6_t) fxp_UFP32(bCalibrated, 6); /* used range: ufp24_6 */

    oneOverK_lamp = oneOverK_r + oneOverK_g + oneOverK_b; /* ufp24_6 + ufp24_6 + ufp24_6 --> ufp26_6 */
    oneOverK_lamp = (ufp26_6_t) fxp_UMUL_32X32_TO_32_ROUND(31, 6, 6,
                                                          rgb_MAX_DIE_OVER_MAX_LAMP_CURRENT_UFP1_31,
                                                          oneOverK_lamp);

    maxRgb = MAX(rIn, gIn);
    maxRgb = MAX(maxRgb, bIn);

    maxOneOverK = MAX(oneOverK_r, oneOverK_g);
    maxOneOverK = MAX(maxOneOverK, oneOverK_b);
    maxOneOverK = MAX(maxOneOverK, oneOverK_lamp);

    if (maxOneOverK != 0x00000000)
    {
        boostResult = (ufp16_16_t) fxp_UDIV_32_32_TO_32_ROUND(0, 6, 16, maxRgb, maxOneOverK);
    }
    else
    {
        boostResult = 0x00000000;
    }

    rCalBoosted32 = fxp_UMUL_32X32_TO_32_ROUND(16, 0, 0, boostResult, rCalibrated);
    gCalBoosted32 = fxp_UMUL_32X32_TO_32_ROUND(16, 0, 0, boostResult, gCalibrated);
    bCalBoosted32 = fxp_UMUL_32X32_TO_32_ROUND(16, 0, 0, boostResult, bCalibrated);

    if (rCalBoosted32 > UINT16_MAX)
    {
        rCalBoosted32 = UINT16_MAX;
    }
    if (gCalBoosted32 > UINT16_MAX)
    {
        gCalBoosted32 = UINT16_MAX;
    }
    if (bCalBoosted32 > UINT16_MAX)
    {
        bCalBoosted32 = UINT16_MAX;
    }

    rgbCalBoosted->r = (uint16_t) rCalBoosted32;
    rgbCalBoosted->g = (uint16_t) gCalBoosted32;
    rgbCalBoosted->b = (uint16_t) bCalBoosted32;

    return boostResult;
}

void rgb_ccResetAndCalculateParam(volatile rgb_ledZoneEffectParam_ts *effectParam,
                                   volatile rgb_ledZoneParam_ts *ledParam,
                                   volatile uint16_t ccPeriod)
{
    effectParam->ccPeriod = ccPeriod;
    effectParam->ccSlope = fxp_SDIV_32_32_TO_32_ROUND(27, 0, 27, H_MAX_4_27,(sfp31_0_t) effectParam->ccPeriod);
    effectParam->ccEnabled = TRUE;
    ledParam->ccIndex = effectParam->ccPeriod; /* The first CC execution will force the index to be 0 */
}

void rgb_ccCalculateParam(volatile rgb_ledZoneEffectParam_ts *effectParam,
                           volatile rgb_ledZoneParam_ts *ledParam,
                           volatile uint16_t ccPeriod)
{
    effectParam->ccPeriod = ccPeriod;
    effectParam->ccSlope = fxp_SDIV_32_32_TO_32_ROUND(27, 0, 27, H_MAX_4_27,(sfp31_0_t) effectParam->ccPeriod);
    effectParam->ccEnabled = TRUE;
    ledParam->ccIndex = (uint16_t) fxp_SDIV_32_32_TO_32_ROUND(27, 27, 0, ledParam->hsvComp.h, effectParam->ccSlope);
}

void rgb_ccExecute(volatile rgb_ledZoneEffectParam_ts *effectParam,
                    volatile rgb_ledZoneParam_ts *ledParam)
{
    if (effectParam->ccEnabled)
    {
        if (ledParam->ccIndex < effectParam->ccPeriod)
        {
            ledParam->ccIndex++;
            /*fractA + fractB = fractRes -> no rounding needed in mult */
            ledParam->hsvCompOut.h = fxp_SMUL_32X32_TO_32(0, 27, 27, ((sfp31_0_t) ledParam->ccIndex), effectParam->ccSlope);
        }
        if (ledParam->ccIndex >= effectParam->ccPeriod)
        {
            ledParam->ccIndex = 0x0000;
            ledParam->hsvCompOut.h = 0x00000000;
        }
    }
    else
    {
        ledParam->hsvCompOut.h = ledParam->hsvComp.h;
    }
}

#if rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS
/*
*
* By defining the appropriate ranges in this function (s4_27 to s4_27), and since max value = 1.0
* mapped to 1.0 at the output, the scale factor is 1
*/
sfp4_27_t rgb_calculateCubicFunction(volatile sfp4_27_t input)
{
    sfp4_27_t result, tmpVal_4_27;

    tmpVal_4_27 = fxp_SMUL_32X32_TO_32_ROUND(27, 27, 27, input, input);
    result = fxp_SMUL_32X32_TO_32_ROUND(27, 27, 27, tmpVal_4_27, input);

    return result;
}
#endif /* rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS */

void rgb_brResetAndCalculateParam(volatile rgb_ledZoneEffectParam_ts *effectParam,
                                   volatile rgb_ledZoneParam_ts *ledParam,
                                   volatile uint16_t brPeriod)
{
    effectParam->brRampPeriod = fxp_SMUL_32X32_TO_32_ROUND( 0, 31, 0, brPeriod, rgb_BR_PERIOD_TO_RAMP_PERIOD_RATIO);

#if BR_TOP_SEGMENT_PRESENT
    effectParam->brTopPeriod = fxp_SMUL_32X32_TO_32_ROUND(0, 31, 0, brPeriod, rgb_BR_PERIOD_TO_TOP_PERIOD_RATIO);
#else
    effectParam->brTopPeriod = 0x0000;
#endif

#if BR_BOTTOM_SEGMENT_PRESENT
    effectParam->brBottomPeriod = fxp_SMUL_32X32_TO_32_ROUND(0, 31, 0, brPeriod, rgb_BR_PERIOD_TO_BOTTOM_PERIOD_RATIO);
#else
    effectParam->brBottomPeriod = 0x0000;
#endif

    effectParam->brSlope = fxp_SDIV_32_32_TO_32_ROUND(27, 0, 27, V_MAX_4_27, (sfp31_0_t) effectParam->brRampPeriod);
    ledParam->hsvCompOut.v = 0x00000000;
    ledParam->brState = STARTUP;
    effectParam->brEnabled = TRUE;
}

void rgb_brSetPassThrough(volatile rgb_ledZoneEffectParam_ts *effectParam,
                            volatile rgb_ledZoneParam_ts *ledParam)
{
 ledParam->brState = PASSTHROUGH;
 effectParam->brEnabled = FALSE;
}


void rgb_brExecute(volatile rgb_ledZoneEffectParam_ts *effectParam,
                    volatile rgb_ledZoneParam_ts *ledParam)
{
    switch(ledParam->brState)
    {
    case RAMP_UP:
        if (ledParam->brSegmIndex < effectParam->brRampPeriod)
        {
            sfp4_27_t tmpBreathVout;

            ledParam->brSegmIndex++;

            /*fractA + fractB = fractRes -> no rounding needed in mult */
            tmpBreathVout = fxp_SMUL_32X32_TO_32(0, 27, 27, ((sfp31_0_t) ledParam->brSegmIndex), effectParam->brSlope);
#if rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS
            tmpBreathVout = rgb_calculateCubicFunction(tmpBreathVout);
#endif /* rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS */
            ledParam->hsvCompOut.v = fxp_SMUL_32X32_TO_32_ROUND(27, 27, 27, ledParam->hsvComp.v, tmpBreathVout);

            if (ledParam->brSegmIndex >= effectParam->brRampPeriod)
            {
                if (effectParam->brTopPeriod > 0x0000)
                {
                    ledParam->brState = TOP_SEG;
                    ledParam->brSegmIndex = 0x0000;
                }
                else
                {
                    ledParam->brState = RAMP_DOWN;
                    ledParam->brSegmIndex = effectParam->brRampPeriod;
                }
            }
        }
        ledParam->brIndex++;
        break;

    case TOP_SEG:
        if (effectParam->brEnabled)
        { /* If Breathing disabled during ramp up, we stay here forever */
            if (ledParam->brSegmIndex < effectParam->brTopPeriod)
            {/* Output level maintained to Max during this sample */
                ledParam->brSegmIndex++;
            }
            if (ledParam->brSegmIndex >= effectParam->brTopPeriod)
            {/* Output level maintained to Max during this sample */
                ledParam->brState = RAMP_DOWN;
                ledParam->brSegmIndex = effectParam->brRampPeriod;
            }
        }
        ledParam->brIndex++;
        break;

    case RAMP_DOWN:
        if (ledParam->brSegmIndex > 0x0000)
        {
            sfp4_27_t tmpBreathVout;

            ledParam->brSegmIndex--;

            /*fractA + fractB = fractRes -> no rounding needed in mult */
            tmpBreathVout = fxp_SMUL_32X32_TO_32(0, 27, 27, ((sfp31_0_t) ledParam->brSegmIndex), effectParam->brSlope);
#if rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS
            tmpBreathVout = rgb_calculateCubicFunction(tmpBreathVout);
#endif /* rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS */
            ledParam->hsvCompOut.v = fxp_SMUL_32X32_TO_32_ROUND(27, 27, 27, ledParam->hsvComp.v, tmpBreathVout);

            ledParam->brIndex++;

            if (ledParam->brSegmIndex == 0x0000)
            {
                if (effectParam->brBottomPeriod > 0x0000)
                {
                    ledParam->brState = BOTTOM_SEG;
                    ledParam->brSegmIndex = 0x0000;
                }
                else
                {
                    ledParam->brState = RAMP_UP;
                    ledParam->brSegmIndex = 0x0000;
                    ledParam->brIndex = 0x0000;
                }
            }
        }
        break;

    case BOTTOM_SEG:
        if (effectParam->brEnabled)
        { /* If Breathing disabled during ramp down, we stay here forever */
            if (ledParam->brSegmIndex < effectParam->brBottomPeriod)
            {/* Output level maintained to Max during this sample */
                ledParam->brSegmIndex++;
                ledParam->brIndex++;
            }
            if (ledParam->brSegmIndex >= effectParam->brBottomPeriod)
            {/* Output level maintained to Max during this sample */
                ledParam->brState = RAMP_UP;
                ledParam->brSegmIndex = 0x0000;
                ledParam->brIndex = 0x0000;
            }
        }
        break;

    case STARTUP:
        ledParam->brState = RAMP_UP;
        ledParam->brSegmIndex = 0x0000;
        ledParam->brIndex = 0x0000;
        break;

    case PASSTHROUGH:
        ledParam->hsvCompOut.v = ledParam->hsvComp.v;
        break;
    }
}

void rgb_executeEffects(volatile rgb_ledZoneEffectParam_ts *effectParam,
                        volatile rgb_ledZoneParam_ts *ledParam)
{
    if (ledParam->ccDriftCnts == 0)
    { /* No drift to correct */
        rgb_ccExecute(effectParam, ledParam);
    }
    else  if (ledParam->ccDriftCnts > 0)
    { /* Positive drift to correct, hurry up! */
        rgb_ccExecute(effectParam, ledParam);
        rgb_ccExecute(effectParam, ledParam);
        ledParam->ccDriftCnts--;
    }
    else  if (ledParam->ccDriftCnts < 0)
    { /* Negative drift to correct, slow down! */
        ledParam->ccDriftCnts++;
    }

    if (effectParam->ccEnabled)
    {
        ledParam->hsvCompOut.s = S_MAX_4_27;
    }
    else
    {
        ledParam->hsvCompOut.s = ledParam->hsvComp.s;
    }

    if (ledParam->brDriftCnts == 0)
    { /* No drift to correct */
        rgb_brExecute(effectParam, ledParam);
    }
    else  if (ledParam->brDriftCnts > 0)
    { /* Positive drift to correct, hurry up! */
        rgb_brExecute(effectParam, ledParam);
        rgb_brExecute(effectParam, ledParam);
        ledParam->brDriftCnts--;
    }
    else  if (ledParam->brDriftCnts < 0)
    { /* Negative drift to correct, slow down! */
        ledParam->brDriftCnts++;
    }

    rgb_hsvToRgb(&ledParam->hsvCompOut, &ledParam->rgbCompOut);
}
