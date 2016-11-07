#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#include <gnuradio/io_signature.h>
#include "PPM_Peak_Detector_impl.h"
namespace gr {
  namespace PPM_Analog_RC {
    PPM_Peak_Detector::sptr
    PPM_Peak_Detector::make(float peak_threshold)
    {
      return gnuradio::get_initial_sptr
        (new PPM_Peak_Detector_impl(peak_threshold));
    }

    PPM_Peak_Detector_impl::PPM_Peak_Detector_impl(float peak_threshold)
      : gr::sync_block("PPM_Peak_Detector",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(float)))
    {
      d_peak_threshold = peak_threshold;
      set_history(1);
    }
    PPM_Peak_Detector_impl::~PPM_Peak_Detector_impl(){}
    int
    PPM_Peak_Detector_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];


      for(int i = 0; i < noutput_items; i++){
        // RISING EDGE ABOVE THRESHOLD
        (in[i] > d_peak_threshold && in[i - 1] < d_peak_threshold) ? out[i] = 1 : out[i] = 0;      
      }


      return noutput_items;
    }
  } /* namespace PPM_Analog_RC */
} /* namespace gr */

