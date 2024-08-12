/*****************************************************************************
 Copyright (C) 2015 LOGITECH
------------------------------------------------------------------------------

 Provides the functionality to manage TDD on RGB Algorithms engine, by
 exporting the function calls to python
******************************************************************************/

/*
** --------------------------------------------------------
** Include section
** --------------------------------------------------------
*/
#include <python3.11/Python.h>
#include "test_rgb_algorithms.h"

/*
** --------------------------------------------------------
** Constants Definitions
** --------------------------------------------------------
*/

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
volatile rgb_ledZoneEffectParam_ts  zone1EffectParam, zone2EffectParam;
volatile rgb_ledZoneParam_ts        zone1ledParam, zone2ledParam;

/*
** --------------------------------------------------------
** Private Data
** --------------------------------------------------------
*/

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

/*
** --------------------------------------------------------
** Function definitions
** --------------------------------------------------------
*/

/* As per web: http://aplawrence.com/Girish/c-functions-from-python.html */

/*  Functions to be called from Python */

static PyObject* py_rgb_Init(PyObject* self, PyObject* args)
{
    PyArg_ParseTuple(args,"");
    rgb_initialise();
    return Py_BuildValue("");
}

static PyObject* py_rgb_gammaCrt16Calc(PyObject* self, PyObject* args)
{
    sfp31_0_t CsRGB, ClinRGB;
    volatile uint16_t CsRGB_16, ClinRGB_16;

    PyArg_ParseTuple(args,"i", &CsRGB);

    CsRGB_16 = (uint16_t) CsRGB;

    ClinRGB_16 = rgb_gammaCrt16Calc(CsRGB_16);

    ClinRGB = (sfp31_0_t) ClinRGB_16;

    return Py_BuildValue("i",ClinRGB);
}

static PyObject* py_rgb_gammaCrt8Table(PyObject* self, PyObject* args)
{
    sfp31_0_t CsRGB, ClinRGB;
    volatile uint8_t CsRGB_8, ClinRGB_8;

    PyArg_ParseTuple(args,"i", &CsRGB);

    CsRGB_8 = (uint8_t) CsRGB;

    ClinRGB_8 = rgb_gammaCrt8Table(CsRGB_8);

    ClinRGB = (sfp31_0_t) ClinRGB_8;

    return Py_BuildValue("i",ClinRGB);
}

static PyObject* py_rgb_rgbToHsv(PyObject* self, PyObject* args)
{
    rgb_rgbComponents_ts RGBinput;
    sfp31_0_t R,G,B;
    rgb_hsvComponents_ts HSVoutput;
    PyArg_ParseTuple(args,"iii", &R,&G,&B);

    RGBinput.r=(uint16_t) R;
    RGBinput.g=(uint16_t) G;
    RGBinput.b=(uint16_t) B;

    rgb_rgbToHsv(&RGBinput,&HSVoutput);
    return Py_BuildValue("iii",HSVoutput.h,HSVoutput.s,HSVoutput.v);
}

static PyObject* py_rgb_hsvToRgb(PyObject* self, PyObject* args)
{
    rgb_hsvComponents_ts HSVinput;
    rgb_rgbComponents_ts RGBoutput;
    sfp31_0_t R,G,B;

    PyArg_ParseTuple(args,"iii", &HSVinput.h,&HSVinput.s,&HSVinput.v);

    rgb_hsvToRgb(&HSVinput,&RGBoutput);

    R = (sfp31_0_t) RGBoutput.r;
    G = (sfp31_0_t) RGBoutput.g;
    B = (sfp31_0_t) RGBoutput.b;

    return Py_BuildValue("iii",R,G,B);
}


static PyObject* py_rgb_getLedEffectParam(PyObject* self, PyObject* args)
{
    volatile rgb_ledZoneEffectParam_ts *effectParam;
    uint32_t zoneNb;

    PyArg_ParseTuple(args,"I", &zoneNb);


    if(zoneNb == 1)
    {
        effectParam = &zone1EffectParam;

    }
    else if (zoneNb == 2)
    {
        effectParam = &zone2EffectParam;
    }

    return Py_BuildValue("IIiIIIIIiI",
                         zoneNb,
                         (uint32_t) (effectParam->ccPeriod),
                         effectParam->ccSlope,
                         (uint32_t) effectParam->ccEnabled,
                         (uint32_t) effectParam->brPeriod,
                         (uint32_t) effectParam->brRampPeriod,
                         (uint32_t) effectParam->brBottomPeriod,
                         (uint32_t) effectParam->brTopPeriod,
                         effectParam->brSlope,
                         (uint32_t) effectParam->brEnabled);
}

static PyObject* py_rgb_setLedEffectParam(PyObject* self, PyObject* args)
{
    volatile rgb_ledZoneEffectParam_ts *effectParam;
    uint32_t zoneNb, CCNMax, CCEnabled, BRNMax, BRRampNMax, BRBottomNMax, BRTopNMax,BREnabled;
    int32_t CCSlope, BRSlope;

    PyArg_ParseTuple(args,"IIiIIIIIiI",
                     &zoneNb,
                     &CCNMax,
                     &CCSlope,
                     &CCEnabled,
                     &BRNMax,
                     &BRRampNMax,
                     &BRBottomNMax,
                     &BRTopNMax,
                     &BRSlope,
                     &BREnabled);

    if(zoneNb == 1)
    {
        effectParam = &zone1EffectParam;
    }
    else if (zoneNb == 2)
    {
        effectParam = &zone2EffectParam;
    }

    effectParam->ccPeriod = CCNMax;
    effectParam->ccSlope = CCSlope;
    effectParam->ccEnabled = (CCEnabled == 0) ? FALSE : TRUE;
    effectParam->brPeriod =BRNMax ;
    effectParam->brRampPeriod = BRRampNMax;
    effectParam->brBottomPeriod = BRBottomNMax;
    effectParam->brTopPeriod = BRTopNMax;
    effectParam->brSlope = BRSlope;
    effectParam->brEnabled = (BREnabled == 0) ? FALSE : TRUE;

    return Py_BuildValue("");
}

static PyObject* py_rgb_getLedParam(PyObject* self, PyObject* args)
{
    volatile rgb_ledZoneParam_ts *ledParam;
    uint32_t zoneNb;

    PyArg_ParseTuple(args,"I", &zoneNb);


    if(zoneNb == 1)
    {
        ledParam    = &zone1ledParam;
    }
    else if (zoneNb == 2)
    {
        ledParam    = &zone2ledParam;
    }

    return Py_BuildValue("IIIIIIIiiiiiiIii",
                         zoneNb,
                         (uint32_t) ledParam->ccIndex,
                         (uint32_t) ledParam->brIndex,
                         (uint32_t) ledParam->brSegmIndex,
                         (uint32_t) ledParam->rgbCompOut.r,
                         (uint32_t) ledParam->rgbCompOut.g,
                         (uint32_t) ledParam->rgbCompOut.b,
                         ledParam->hsvComp.h,
                         ledParam->hsvComp.s,
                         ledParam->hsvComp.v,
                         ledParam->hsvCompOut.h,
                         ledParam->hsvCompOut.s,
                         ledParam->hsvCompOut.v,
                         (uint32_t) ledParam->brState,
                         (int32_t) ledParam->ccDriftCnts,
                         (int32_t) ledParam->brDriftCnts);
}

static PyObject* py_rgb_setLedParam(PyObject* self, PyObject* args)
{
    volatile rgb_ledZoneParam_ts *ledParam;
    uint32_t zoneNb, CCIndex, BRIndex, BRSegmIndex, RGBOutR, RGBOutG,
        RGBOutB, BR_State;
    int32_t HSVH, HSVS, HSVV, HSVOutH, HSVOutS, HSVOutV, CC_DriftCnts, BR_DriftCnts;

    PyArg_ParseTuple(args,"IIIIIIIiiiiiiIii",
                     &zoneNb,
                     &CCIndex,
                     &BRIndex,
                     &BRSegmIndex,
                     &RGBOutR,
                     &RGBOutG,
                     &RGBOutB,
                     &HSVH,
                     &HSVS,
                     &HSVV,
                     &HSVOutH,
                     &HSVOutS,
                     &HSVOutV,
                     &BR_State,
                     &CC_DriftCnts,
                     &BR_DriftCnts);

    if(zoneNb == 1)
    {
        ledParam    = &zone1ledParam;
    }
    else if (zoneNb == 2)
    {
        ledParam    = &zone2ledParam;
    }

    ledParam->ccIndex = CCIndex;
    ledParam->brIndex = BRIndex;
    ledParam->brSegmIndex = BRSegmIndex;
    ledParam->rgbCompOut.r = RGBOutR;
    ledParam->rgbCompOut.g = RGBOutG;
    ledParam->rgbCompOut.b = RGBOutB;
    ledParam->hsvComp.h = HSVH;
    ledParam->hsvComp.s = HSVS;
    ledParam->hsvComp.v = HSVV;
    ledParam->hsvCompOut.h = HSVOutH ;
    ledParam->hsvCompOut.s = HSVOutS;
    ledParam->hsvCompOut.v = HSVOutV;
    ledParam->brState = BR_State;
    ledParam->ccDriftCnts = CC_DriftCnts;
    ledParam->brDriftCnts = BR_DriftCnts;

    return Py_BuildValue("");
}

static PyObject* py_rgb_applyCalibrationAndBoost(PyObject* self, PyObject* args)
{
    volatile rgb_rgbComponents_ts rgb, rgbCalBoosted;
    volatile uint8_t calibration[3];
    uint32_t R, G, B, Rcal, Gcal, Bcal, RcalBoosted, GcalBoosted, BcalBoosted;
    ufp16_16_t boostResult;

    PyArg_ParseTuple(args, "IIIIII", &R, &G, &B, &Rcal, &Gcal, &Bcal);

    rgb.r = (uint16_t)R;
    rgb.g = (uint16_t)G;
    rgb.b = (uint16_t)B;

    calibration[0] = (uint8_t)Rcal;
    calibration[1] = (uint8_t)Gcal;
    calibration[2] = (uint8_t)Bcal;

    boostResult = rgb_applyCalibrationAndBoost(&rgb, calibration, &rgbCalBoosted);

    RcalBoosted = rgbCalBoosted.r;
    GcalBoosted = rgbCalBoosted.g;
    BcalBoosted = rgbCalBoosted.b;

    return Py_BuildValue("IIII", boostResult, RcalBoosted, GcalBoosted, BcalBoosted);
}

static PyObject* py_rgb_ccResetAndCalculateParam(PyObject* self, PyObject* args)
{
    volatile rgb_ledZoneEffectParam_ts *effectParam;
    volatile rgb_ledZoneParam_ts *ledParam;
    uint32_t zoneNb, Nmax;

    PyArg_ParseTuple(args,"II", &zoneNb, &Nmax);


    if(zoneNb == 1)
    {
        effectParam = &zone1EffectParam;
        ledParam    = &zone1ledParam;
    }
    else if (zoneNb == 2)
    {
        effectParam = &zone2EffectParam;
        ledParam    = &zone2ledParam;
    }

    rgb_ccResetAndCalculateParam(effectParam, ledParam, Nmax);

    return Py_BuildValue("");

}

static PyObject* py_rgb_ccCalculateParam(PyObject* self, PyObject* args)
{
    volatile rgb_ledZoneEffectParam_ts *effectParam;
    volatile rgb_ledZoneParam_ts *ledParam;

    uint32_t zoneNb, Nmax;

    PyArg_ParseTuple(args,"II", &zoneNb, &Nmax);

    if(zoneNb == 1)
    {
        effectParam = &zone1EffectParam;
        ledParam    = &zone1ledParam;
    }
    else if (zoneNb == 2)
    {
        effectParam = &zone2EffectParam;
        ledParam    = &zone2ledParam;
    }

    rgb_ccCalculateParam(effectParam, ledParam, Nmax);

    return Py_BuildValue("");
}

static PyObject* py_rgb_calculateCubicFunction(PyObject* self, PyObject* args)
{
    sfp4_27_t input, result;

    PyArg_ParseTuple(args,"i", &input);
    result = 0;
    #if rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS
    result = rgb_calculateCubicFunction(input);
    #endif /* rgb_USE_CUBIC_FUNCTION_IN_BREATHING_RAMPS */

    return Py_BuildValue("i",result);
}



static PyObject* py_rgb_brResetAndCalculateParam(PyObject* self, PyObject* args)
{
    volatile rgb_ledZoneEffectParam_ts *effectParam;
    volatile rgb_ledZoneParam_ts *ledParam;

    uint32_t zoneNb, Nmax;

    PyArg_ParseTuple(args,"II", &zoneNb, &Nmax);

    if(zoneNb == 1)
    {
        effectParam = &zone1EffectParam;
        ledParam    = &zone1ledParam;
    }
    else if (zoneNb == 2)
    {
        effectParam = &zone2EffectParam;
        ledParam    = &zone2ledParam;
    }

    rgb_brResetAndCalculateParam(effectParam, ledParam, Nmax);

    return Py_BuildValue("");
}

static PyObject* py_rgb_brExecute(PyObject* self, PyObject* args)
{
    volatile rgb_ledZoneEffectParam_ts *effectParam;
    volatile rgb_ledZoneParam_ts *ledParam;

    uint32_t zoneNb;

    PyArg_ParseTuple(args,"I", &zoneNb);

    if(zoneNb == 1)
    {
        effectParam = &zone1EffectParam;
        ledParam    = &zone1ledParam;
    }
    else if (zoneNb == 2)
    {
        effectParam = &zone2EffectParam;
        ledParam    = &zone2ledParam;
    }

    rgb_brExecute(effectParam, ledParam);

    return Py_BuildValue("");
}

static PyObject* py_rgb_ccExecute(PyObject* self, PyObject* args)
{

    volatile rgb_ledZoneEffectParam_ts *effectParam;
    volatile rgb_ledZoneParam_ts *ledParam;

    uint32_t zoneNb;

    PyArg_ParseTuple(args,"I", &zoneNb);

    if(zoneNb == 1)
    {
        effectParam = &zone1EffectParam;
        ledParam    = &zone1ledParam;
    }
    else if (zoneNb == 2)
    {
        effectParam = &zone2EffectParam;
        ledParam    = &zone2ledParam;
    }

    rgb_ccExecute(effectParam, ledParam);

    return Py_BuildValue("");
}

/*  wrapped rgb_executeEffects function */
static PyObject* py_rgb_executeEffects(PyObject* self, PyObject* args)
{
    volatile rgb_ledZoneEffectParam_ts *effectParam;
    volatile rgb_ledZoneParam_ts *ledParam;

    uint32_t zoneNb;

    PyArg_ParseTuple(args,"I", &zoneNb);

    if(zoneNb == 1)
    {
        effectParam = &zone1EffectParam;
        ledParam    = &zone1ledParam;
    }
    else if (zoneNb == 2)
    {
        effectParam = &zone2EffectParam;
        ledParam    = &zone2ledParam;
    }

    rgb_executeEffects(effectParam, ledParam);

    return Py_BuildValue("");
}

/*  define functions in module */
static PyMethodDef myModule_methods[] =
{{"rgb_Init",py_rgb_Init, METH_VARARGS},
 {"rgb_gammaCrt16Calc",py_rgb_gammaCrt16Calc, METH_VARARGS},
 {"rgb_gammaCrt8Table",py_rgb_gammaCrt8Table, METH_VARARGS},
 {"rgb_rgbToHsv",py_rgb_rgbToHsv, METH_VARARGS},
 {"rgb_hsvToRgb",py_rgb_hsvToRgb, METH_VARARGS},
 {"rgb_applyCalibrationAndBoost",py_rgb_applyCalibrationAndBoost, METH_VARARGS},
 {"rgb_ccResetAndCalculateParam",py_rgb_ccResetAndCalculateParam, METH_VARARGS},
 {"rgb_ccCalculateParam",py_rgb_ccCalculateParam, METH_VARARGS},
 {"rgb_calculateCubicFunction",py_rgb_calculateCubicFunction, METH_VARARGS},
 {"rgb_brResetAndCalculateParam",py_rgb_brResetAndCalculateParam, METH_VARARGS},
 {"rgb_brExecute",py_rgb_brExecute, METH_VARARGS},
 {"rgb_ccExecute",py_rgb_ccExecute, METH_VARARGS},
 {"rgb_executeEffects",py_rgb_executeEffects, METH_VARARGS},
 {"rgb_getLedEffectParam",py_rgb_getLedEffectParam, METH_VARARGS},
 {"rgb_getLedParam",py_rgb_getLedParam, METH_VARARGS},
 {"rgb_setLedEffectParam",py_rgb_setLedEffectParam, METH_VARARGS},
 {"rgb_setLedParam",py_rgb_setLedParam, METH_VARARGS},
 {NULL, NULL}};

/* module initialization */
/* Python version 3*/
static struct PyModuleDef cModPyDem =
{
    PyModuleDef_HEAD_INIT,
    "pythonCTestFunctions", /* name of module */
    "",          /* module documentation, may be NULL */
    -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
    myModule_methods
};

PyMODINIT_FUNC PyInit_pythonCTestFunctions(void)
{
    return PyModule_Create(&cModPyDem);
}