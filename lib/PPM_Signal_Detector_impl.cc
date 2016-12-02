#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#include <gnuradio/io_signature.h>
#include "PPM_Signal_Detector_impl.h"


#include "PPM_Configuration.h"


namespace gr {
	namespace PPM_Analog_RC {
		PPM_Signal_Detector::sptr
		PPM_Signal_Detector::make(float samp_rate, float energy_threshold)
		{
			return gnuradio::get_initial_sptr
			(new PPM_Signal_Detector_impl(samp_rate, energy_threshold));
		}
		PPM_Signal_Detector_impl::PPM_Signal_Detector_impl(float samp_rate, float energy_threshold)
		: gr::block("PPM_Signal_Detector",
			gr::io_signature::make(2, 2, sizeof(float)),
			gr::io_signature::make(1, 1, sizeof(float)))
		{
			d_nbr_samples = 0;
			d_samp_rate = samp_rate;
			d_nbr_samples_to_process = 0.001 * samp_rate;
			d_bool_signal_energy = 0;
			d_bool_guard_time = 0;
			d_time_constant = 0;
			d_max_time_constant = 0;
			d_energy_threshold = energy_threshold;
			set_history(d_nbr_samples_to_process);
		}
		PPM_Signal_Detector_impl::~PPM_Signal_Detector_impl(){}

		void
		PPM_Signal_Detector_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
		{
	  		ninput_items_required[0] = noutput_items;
		}
		int
		PPM_Signal_Detector_impl::general_work (int noutput_items,
			gr_vector_int &ninput_items,
			gr_vector_const_void_star &input_items,
			gr_vector_void_star &output_items)
		{
			const float *in = (const float *) input_items[0];
			const float *in1 = (const float *) input_items[1];
			float *out = (float *) output_items[0];
			in += d_nbr_samples_to_process - 1;
			in1 += d_nbr_samples_to_process - 1;


			for(int i = 0; i < noutput_items; i++){
				out[i] = out[i - 1];
				d_nbr_samples++;


				// TEST ENERGY EVERY 1MS
				if(d_nbr_samples % d_nbr_samples_to_process == 0){
					d_nbr_samples = 0;
					float signal_energy = 0;
					for(int j = 0; j < d_nbr_samples_to_process; j++)
						signal_energy += pow(in1[i-j], 1);
					(signal_energy > d_energy_threshold) ? d_bool_signal_energy = 1 : d_bool_signal_energy = 0;
				}


				// TEST GUARD TIME
				(in[i] > 0.025) ? d_time_constant = 0 : d_time_constant++;
				(d_time_constant > d_max_time_constant) ? d_max_time_constant = d_time_constant : 1;
				(d_max_time_constant / d_samp_rate > GUARD_TIME_MIN && d_max_time_constant / d_samp_rate < GUARD_TIME_MAX) ? d_bool_guard_time = 1 : d_bool_guard_time = 0;


				// OUTPUT
				if(d_bool_signal_energy && d_bool_guard_time){
					out[i] = 1;
				}else{
					out[i] = 0;
					d_max_time_constant = 0;
				}


			}
			consume_each (noutput_items);
			return noutput_items;
		}
  } /* namespace PPM_Analog_RC */
} /* namespace gr */
