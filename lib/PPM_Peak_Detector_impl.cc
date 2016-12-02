#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#include <gnuradio/io_signature.h>
#include "PPM_Peak_Detector_impl.h"
namespace gr {
  namespace PPM_Analog_RC {
    PPM_Peak_Detector::sptr
    PPM_Peak_Detector::make(float peak_threshold, int samp_rate)
    {
      return gnuradio::get_initial_sptr
        (new PPM_Peak_Detector_impl(peak_threshold, samp_rate));
    }

    PPM_Peak_Detector_impl::PPM_Peak_Detector_impl(float peak_threshold, int samp_rate)
      : gr::sync_block("PPM_Peak_Detector",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(float)))
    {
      d_peak_threshold = peak_threshold;
      d_symbol_length = samp_rate * PEAK_DURATION;
      set_history(d_symbol_length);
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
        //(in[i] > d_peak_threshold && in[i - 1] < d_peak_threshold) ? out[i] = 1 : out[i] = 0;
        float corr = 0;
        for(int j = 0; j<d_symbol_length; j++){
          corr += in[i+j];
        }
        corr = (corr < 0)?0:corr;
        if(corr > d_peak_threshold && (corr < d_correlation_history[0] && d_correlation_history[1] < d_correlation_history[0])){
          out[i] = 1;
        }else{
          out[i] = 0;
        }
        d_correlation_history[1] = d_correlation_history[0];
        d_correlation_history[0] = corr;
      }


      return noutput_items;
    }
  } /* namespace PPM_Analog_RC */
} /* namespace gr */
