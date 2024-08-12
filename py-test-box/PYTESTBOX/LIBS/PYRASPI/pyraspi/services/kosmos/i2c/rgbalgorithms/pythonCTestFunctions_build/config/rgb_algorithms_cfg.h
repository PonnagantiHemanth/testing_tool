/**********************************************************************************
Copyright (C) 2015
LOGITECH SA, CH-1015 Lausanne
-------------------------------------------------------------------------------
\author    David Tarongi
\file      rgb_algorithms_cfg.h
Date       13-May-2015
Revision   13-May-2015/DT
 
\brief    Provides the config info functionality for:
         -RGB Algorithms engine
              
**********************************************************************************/
#ifndef __RGB_ALGORITHMS_CFG_H__
#define __RGB_ALGORITHMS_CFG_H__


/* For the following ratios:
   2 * PERIOD_TO_RAMP_PERIOD + PERIOD_TO_TOP_PERIOD + PERIOD_TO_BOTTOM_PERIOD = 1.0
 */
#define BR_TOP_SEGMENT_PRESENT      0
#define BR_BOTTOM_SEGMENT_PRESENT   0

#define rgb_BR_PERIOD_TO_TOP_PERIOD_RATIO    ((sfp0_31_t)fxp_SFP32((0.0), 31))
#define rgb_BR_PERIOD_TO_BOTTOM_PERIOD_RATIO ((sfp0_31_t)fxp_SFP32((0.0), 31))

#define GAMMA_APPROX_ORDER           2

/* Fixme: this definitions should be automated in case bottom and top segments missing*/
#define rgb_BR_PERIOD_TO_RAMP_PERIOD_RATIO   ((sfp0_31_t)fxp_SFP32((0.5), 31))
/*In any case, rgb_BR_PERIOD_TO_TOP_PERIOD_RATIO + rgb_BR_PERIOD_TO_BOTTOM_PERIOD_RATIO + 2*rgb_BR_PERIOD_TO_RAMP_PERIOD_RATIO = 1*/

#define rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS   0

/* The following constant is only used by the new RGB boost algorithm in LFA, which is not called by Heat code */
/* The constant must be defined here to allow compilation of the new version of rgb_algorithms module on LFA  */
#define rgb_MAX_DIE_OVER_MAX_LAMP_CURRENT           (1.0)      /* Max Current Lamp = Max Current Die: Standard Color Boost Algorithm */
#define rgb_MAX_DIE_OVER_MAX_LAMP_CURRENT_UFP1_31 ((ufp1_31_t)fxp_UFP32((rgb_MAX_DIE_OVER_MAX_LAMP_CURRENT), 31))

#endif /*  __RGB_ALGORITHMS_CFG_H__ */
