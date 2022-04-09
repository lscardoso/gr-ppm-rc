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


#ifndef INCLUDED_PPM_ANALOG_RC_PPM_PEAK_DETECTOR_H
#define INCLUDED_PPM_ANALOG_RC_PPM_PEAK_DETECTOR_H

#include <gnuradio/PPM_Analog_RC/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace PPM_Analog_RC {

    /*!
     * \brief <+description of block+>
     * \ingroup PPM_Analog_RC
     *
     */
    class PPM_ANALOG_RC_API PPM_Peak_Detector : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<PPM_Peak_Detector> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of PPM_Analog_RC::PPM_Peak_Detector.
       *
       * To avoid accidental use of raw pointers, PPM_Analog_RC::PPM_Peak_Detector's
       * constructor is in a private implementation
       * class. PPM_Analog_RC::PPM_Peak_Detector::make is the public interface for
       * creating new instances.
       */
      static sptr make(float peak_threshold);
    };

  } // namespace PPM_Analog_RC
} // namespace gr

#endif /* INCLUDED_PPM_ANALOG_RC_PPM_PEAK_DETECTOR_H */

