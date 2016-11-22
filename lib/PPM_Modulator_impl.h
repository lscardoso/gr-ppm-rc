#ifndef INCLUDED_PPM_ANALOG_RC_PPM_MODULATOR_IMPL_H
#define INCLUDED_PPM_ANALOG_RC_PPM_MODULATOR_IMPL_H
#include <PPM_Analog_RC/PPM_Modulator.h>
namespace gr {
  namespace PPM_Analog_RC {
    class PPM_Modulator_impl : public PPM_Modulator
    {
     private:
      int d_nbr_samples;
      int d_nbr_channel;
      float d_nbr_samples_peak_duration;
      float d_nbr_samples_channel[4 + 2];
      float d_command_step;
      float d_nbr_samples_command_spread;
      float d_nbr_samples_command_zero;

     public:
      PPM_Modulator_impl(float samp_rate);
      ~PPM_Modulator_impl();
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      void set_axis(int axis_nbr, float value){
        d_nbr_samples_channel[axis_nbr] = (value * d_nbr_samples_command_spread) + d_nbr_samples_command_zero;
      }




      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };
  } // namespace PPM_Analog_RC
} // namespace gr
#endif /* INCLUDED_PPM_ANALOG_RC_PPM_MODULATOR_IMPL_H */
