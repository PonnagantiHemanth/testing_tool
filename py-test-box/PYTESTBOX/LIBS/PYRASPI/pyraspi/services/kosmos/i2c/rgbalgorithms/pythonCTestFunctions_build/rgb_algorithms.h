/*****************************************************************************
 Copyright (C) 2015 LOGITECH
------------------------------------------------------------------------------

 rgb_algorithms.h
******************************************************************************/

#ifndef RGB_ALGORITHMS_H
#define RGB_ALGORITHMS_H

/*
** --------------------------------------------------------
** Include section
** --------------------------------------------------------
*/
#include "lfixedpoint.h"
#include "config/rgb_algorithms_cfg.h"
/*
** --------------------------------------------------------
** Constants Definitions
** --------------------------------------------------------
*/

/* Gamma constants */
#define rgb_GAMMA_SLOPE        (1.0 / 12.92)
#define rgb_GAMMA_SLOPE_SFP_31 ((sfp0_31_t) fxp_SFP32(rgb_GAMMA_SLOPE, 31))
#define rgb_GAMMA_SLOPE_SCALED_OUT_SFP_15 ((sfp16_15_t) fxp_SFP32((rgb_GAMMA_SLOPE * UINT16_MAX), 15))

#define rgb_GAMMA_LIN_POWER_TH     0.04045
#define rgb_GAMMA_LIN_POWER_TH_27 ((sfp4_27_t) fxp_SFP32(rgb_GAMMA_LIN_POWER_TH, 27))

#define rgb_GAMMA_A     0.055
#define rgb_GAMMA_A_27 ((sfp4_27_t) fxp_SFP32(rgb_GAMMA_A, 27))

#define rgb_GAMMA_1_DIVBY_1_PLUS_A (1.0 / (1.0 + rgb_GAMMA_A))
#define rgb_GAMMA_1_DIVBY_1_PLUS_A_31 ((sfp0_31_t) fxp_SFP32(rgb_GAMMA_1_DIVBY_1_PLUS_A, 31))

#define rgb_TAYLOR_B_02_1_29  ((sfp2_29_t) fxp_SFP32((0.2), 29))
#define rgb_TAYLOR_B_02_2_29  ((sfp2_29_t) fxp_SFP32((-0.08), 29))
#define rgb_TAYLOR_B_02_3_29  ((sfp2_29_t) fxp_SFP32((0.048), 29))
#define rgb_TAYLOR_B_02_4_29  ((sfp2_29_t) fxp_SFP32((-0.0336), 29))
#define rgb_TAYLOR_B_02_5_29  ((sfp2_29_t) fxp_SFP32((0.025536), 29))
#define rgb_TAYLOR_B_02_6_29  ((sfp2_29_t) fxp_SFP32((-0.0204288), 29))
#define rgb_TAYLOR_B_02_7_29  ((sfp2_29_t) fxp_SFP32((0.0169267), 29))
#define rgb_TAYLOR_B_02_8_29  ((sfp2_29_t) fxp_SFP32((-0.0143877), 29))
#define rgb_TAYLOR_B_02_9_29  ((sfp2_29_t) fxp_SFP32((0.0124694), 29))
#define rgb_TAYLOR_B_02_10_29 ((sfp2_29_t) fxp_SFP32((-0.010973), 29))


/*
** --------------------------------------------------------
** Type Definitions
** --------------------------------------------------------
*/
typedef struct
{
    sfp4_27_t h;
    sfp4_27_t s;
    sfp4_27_t v;
}rgb_hsvComponents_ts;

typedef struct
{
    uint16_t r;
    uint16_t g;
    uint16_t b;
}rgb_rgbComponents_ts;

typedef enum
{
    BOTTOM_SEG = 0,
    RAMP_UP    = 1,
    TOP_SEG    = 2,
    RAMP_DOWN  = 3,
    STARTUP    = 4,
    PASSTHROUGH= 5
}rgb_brState_te;

typedef struct
{
    uint16_t ccIndex;
    uint16_t brIndex;
    uint16_t brSegmIndex;
    rgb_rgbComponents_ts rgbCompOut;
    rgb_hsvComponents_ts hsvComp;
    rgb_hsvComponents_ts hsvCompOut;
    rgb_brState_te brState;
    int16_t ccDriftCnts;
    int16_t brDriftCnts;
}rgb_ledZoneParam_ts;

typedef struct
{
    uint16_t  ccPeriod;
    sfp4_27_t ccSlope;
    bool      ccEnabled;
    uint16_t  brPeriod;
    uint16_t  brRampPeriod;
    uint16_t  brBottomPeriod;
    uint16_t  brTopPeriod;
    sfp4_27_t brSlope;
    bool      brEnabled;
}rgb_ledZoneEffectParam_ts;

/*
** --------------------------------------------------------
** Exported Global Data
** --------------------------------------------------------
*/


/*
** --------------------------------------------------------
** Inline Code Definition
** --------------------------------------------------------
*/

/*
** --------------------------------------------------------
** Function Definitions
** --------------------------------------------------------
*/

void rgb_initialise(void);
uint16_t rgb_gammaCrt16Calc(volatile uint16_t geVal);
uint8_t rgb_gammaCrt8Table(volatile uint8_t geVal);
void rgb_gammaCrt16CalcRgb(volatile rgb_rgbComponents_ts *rgbIn,
                           volatile rgb_rgbComponents_ts *rgbOut);
void rgb_rgbToHsv(volatile rgb_rgbComponents_ts *rgb, volatile rgb_hsvComponents_ts *hsv);
void rgb_hsvToRgb(volatile rgb_hsvComponents_ts *hsv, volatile rgb_rgbComponents_ts *rgb);
void rgb_ccResetAndCalculateParam(volatile rgb_ledZoneEffectParam_ts *effectParam,
                                  volatile rgb_ledZoneParam_ts *ledParam,
                                  volatile uint16_t ccPeriod);
void rgb_ccCalculateParam(volatile rgb_ledZoneEffectParam_ts *effectParam,
                          volatile rgb_ledZoneParam_ts *ledParam,
                          volatile uint16_t ccPeriod);
void rgb_ccExecute(volatile rgb_ledZoneEffectParam_ts *effectParam,
                   volatile rgb_ledZoneParam_ts *ledParam);
#if rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS
sfp4_27_t rgb_calculateCubicFunction(volatile sfp4_27_t input);
#endif /* rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS */
ufp16_16_t rgb_applyCalibrationAndBoost(volatile rgb_rgbComponents_ts *rgb,
                                        volatile uint8_t *calibration,
                                        volatile rgb_rgbComponents_ts *rgbCalBoosted);
void rgb_brResetAndCalculateParam(volatile rgb_ledZoneEffectParam_ts *effectParam,
                                  volatile rgb_ledZoneParam_ts *ledParam,
                                  volatile uint16_t brPeriod);
void rgb_brSetPassThrough(volatile rgb_ledZoneEffectParam_ts *effectParam,
                          volatile rgb_ledZoneParam_ts *ledParam);
void rgb_brExecute(volatile rgb_ledZoneEffectParam_ts *effectParam,
                   volatile rgb_ledZoneParam_ts *ledParam);
void rgb_executeEffects(volatile rgb_ledZoneEffectParam_ts *effectParam,
                        volatile rgb_ledZoneParam_ts *ledParam);

#endif /* RGB_ALGORITHMS_H */
