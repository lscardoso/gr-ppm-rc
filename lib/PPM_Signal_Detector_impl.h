/* -*- c++ -*- */
/* 
 * Copyright 2016 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_PPM_ANALOG_RC_PPM_SIGNAL_DETECTOR_IMPL_H
#define INCLUDED_PPM_ANALOG_RC_PPM_SIGNAL_DETECTOR_IMPL_H

#include <gnuradio/PPM_Analog_RC/PPM_Signal_Detector.h>

namespace gr {
  namespace PPM_Analog_RC {

    class PPM_Signal_Detector_impl : public PPM_Signal_Detector
    {
    private:
      int d_nbr_samples;
      int d_nbr_samples_to_process;
      int d_samp_rate;
      int d_bool_signal_energy;
      float d_time_constant;
      float d_max_time_constant;
      int d_bool_guard_time;
      float d_energy_threshold;

    public:
      PPM_Signal_Detector_impl(float samp_rate, float energy_threshold);
      ~PPM_Signal_Detector_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
       gr_vector_int &ninput_items,
       gr_vector_const_void_star &input_items,
       gr_vector_void_star &output_items);
    };

  } // namespace PPM_Analog_RC
} // namespace gr

#endif /* INCLUDED_PPM_ANALOG_RC_PPM_SIGNAL_DETECTOR_IMPL_H */

