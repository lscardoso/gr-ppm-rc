#ifndef INCLUDED_PPM_ANALOG_RC_PPM_PEAK_DETECTOR_IMPL_H
#define INCLUDED_PPM_ANALOG_RC_PPM_PEAK_DETECTOR_IMPL_H
#include <PPM_Analog_RC/PPM_Peak_Detector.h>
#include "PPM_Configuration.h"

namespace gr {
  namespace PPM_Analog_RC {
    class PPM_Peak_Detector_impl : public PPM_Peak_Detector
    {
     private:
      float d_peak_threshold;
      int d_symbol_length;
      float d_correlation_history[2];

     public:
      PPM_Peak_Detector_impl(float peak_threshold, int samp_rate);
      ~PPM_Peak_Detector_impl();
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };
  } // namespace PPM_Analog_RC
} // namespace gr
#endif /* INCLUDED_PPM_ANALOG_RC_PPM_PEAK_DETECTOR_IMPL_H */
