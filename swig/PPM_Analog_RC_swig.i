/* -*- c++ -*- */

#define PPM_ANALOG_RC_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "PPM_Analog_RC_swig_doc.i"

%{
#include "PPM_Analog_RC/PPM_Peak_Detector.h"
#include "PPM_Analog_RC/PPM_Demodulator.h"
#include "PPM_Analog_RC/PPM_Signal_Detector.h"
#include "PPM_Analog_RC/PPM_Modulator.h"
%}


%include "PPM_Analog_RC/PPM_Peak_Detector.h"
GR_SWIG_BLOCK_MAGIC2(PPM_Analog_RC, PPM_Peak_Detector);

%include "PPM_Analog_RC/PPM_Demodulator.h"
GR_SWIG_BLOCK_MAGIC2(PPM_Analog_RC, PPM_Demodulator);
%include "PPM_Analog_RC/PPM_Signal_Detector.h"
GR_SWIG_BLOCK_MAGIC2(PPM_Analog_RC, PPM_Signal_Detector);

%include "PPM_Analog_RC/PPM_Modulator.h"
GR_SWIG_BLOCK_MAGIC2(PPM_Analog_RC, PPM_Modulator);
