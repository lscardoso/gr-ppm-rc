#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#include <stdio.h>
#include <gnuradio/io_signature.h>
#include "PPM_Demodulator_impl.h"


#include "PPM_Configuration.h"
#define DETECTION 0
#define CHANNEL_READING 1
#define BLUE "\033[00;34m"
#define WHITE "\033[00;37m"
#define RED "\033[00;35m"


namespace gr {
  namespace PPM_Analog_RC {
    PPM_Demodulator::sptr
    PPM_Demodulator::make(float samp_rate, int demod_on)
    {
      return gnuradio::get_initial_sptr
        (new PPM_Demodulator_impl(samp_rate, demod_on));
    }
    PPM_Demodulator_impl::PPM_Demodulator_impl(float samp_rate, int demod_on)
      : gr::block("PPM_Demodulator",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(0, 0, sizeof(float))),
        d_demod_on(demod_on)
    {
      //INIT
      d_nbr_of_channels = 0;
      d_nbr_peak_detected= 0;
      d_nbr_samples_since_displayed = 0;
      d_nbr_samples_since_last_peak = 0;
      d_nbr_samples_guard_time = samp_rate * GUARD_TIME_RECEPTION;
      d_nbr_samples_refreshing_display = samp_rate * 1.0 / 12.0 ;
      d_nbr_samples_command_spread = COMMAND_SPREAD * samp_rate;
      d_nbr_samples_command_zero = COMMAND_ZERO * samp_rate;
	  d_nbr_samples_min_symbol_time = COMMAND_MIN * samp_rate;

      // Welcome
      d_state = DETECTION;
      printf("\n\n%sWelcome to Drone Analog RC decoding!\n", RED);
    }

    PPM_Demodulator_impl::~PPM_Demodulator_impl(){}
    void
    PPM_Demodulator_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items;
    }
    int
    PPM_Demodulator_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];



      for(int i = 0; i < noutput_items; i++){
          if(d_demod_on==1){

          switch(d_state){



            case DETECTION:
              // PEAK DETECTED
              if(in[i] > 0){

                d_state = CHANNEL_READING;
                d_nbr_samples_since_last_peak = 0;
                d_nbr_peak_detected= 1;
                //printf("%s\n", "Signal ");
              }
            break;



            case CHANNEL_READING:
              // SECURITY OUT OF FRAME
              d_nbr_samples_since_last_peak++;

              if(d_nbr_samples_since_last_peak > d_nbr_samples_guard_time){
                d_state = DETECTION;
                d_nbr_of_channels = d_nbr_peak_detected - 1;
                break;
              }
              if(d_nbr_peak_detected>18){
                d_state = DETECTION;
                d_nbr_of_channels = 0;
                printf("%s\n", "Too many peaks detected in a row ");
                break;
              }

              // PEAK DETECTED
              if(in[i] > 0 && d_nbr_samples_since_last_peak > d_nbr_samples_min_symbol_time){
                d_command_values[d_nbr_peak_detected- 1] =/* 5 + */(d_nbr_samples_since_last_peak - d_nbr_samples_command_zero) / d_nbr_samples_command_spread;
                d_state = CHANNEL_READING;
                d_nbr_peak_detected++;
                d_nbr_samples_since_last_peak = 0;
                //printf("%s\n", "Peak!! ");
              }
            break;
          }


/*
          // DISPLAY COMMANDS
          d_nbr_samples_since_displayed++;
          if(d_nbr_samples_since_displayed > d_nbr_samples_refreshing_display){
            d_nbr_samples_since_displayed = 0;
            printf("\rRC>_ ");
            for(int j = 0; j < d_nbr_of_channels; j++)
              printf("%sCH%d = %1.2f \t %s", BLUE, (j+1), d_command_values[j], WHITE);
          }*/
        }
      }


      consume_each (noutput_items);
      return noutput_items;
    }
  } /* namespace PPM_Analog_RC */
} /* namespace gr */
