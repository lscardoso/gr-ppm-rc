#ifndef INCLUDED_PPM_ANALOG_RC_PPM_DEMODULATOR_IMPL_H
#define INCLUDED_PPM_ANALOG_RC_PPM_DEMODULATOR_IMPL_H
#include <PPM_Analog_RC/PPM_Demodulator.h>

#include "PPM_Configuration.h"

namespace gr {
  namespace PPM_Analog_RC {
    class PPM_Demodulator_impl : public PPM_Demodulator
    {
     private:
      int d_state;
      int d_demod_on;
      int d_nbr_of_channels;
      int d_nbr_peak_detected;
      float d_nbr_samples_since_last_peak;
      float d_nbr_samples_guard_time;
      float d_nbr_samples_since_displayed;
      float d_nbr_samples_refreshing_display;
      float d_nbr_samples_command_spread;
      float d_nbr_samples_command_zero;
      float d_command_values[MAX_NBR_CHANNELS + 1];

     public:
      PPM_Demodulator_impl(float samp_rate, int demod_on);
      ~PPM_Demodulator_impl();
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      void set_demod_on(int new_state) {d_demod_on = new_state;}

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };
  } // namespace PPM_Analog_RC
} // namespace gr
#endif /* INCLUDED_PPM_ANALOG_RC_PPM_DEMODULATOR_IMPL_H */
