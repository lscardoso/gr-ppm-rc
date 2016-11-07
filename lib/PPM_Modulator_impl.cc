#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <gnuradio/io_signature.h>
#include "PPM_Modulator_impl.h"


#include "PPM_Configuration.h"
#define BLUE "\033[00;34m"
#define WHITE "\033[00;37m"
#define RED "\033[00;35m"
#define NBR_CHANNEL 4


namespace gr {
	namespace PPM_Analog_RC {
		int getch(void){
			struct termios oldattr, newattr;
			int ch;
			tcgetattr( STDIN_FILENO, &oldattr );
			newattr = oldattr;
			newattr.c_lflag &= ~( ICANON | ECHO );
			tcsetattr( STDIN_FILENO, TCSANOW, &newattr );
			ch = getchar();
			tcsetattr( STDIN_FILENO, TCSANOW, &oldattr );
			return ch;
		}
		int kbhit(void){
			struct termios oldt, newt;
			int ch;
			int oldf;
			tcgetattr(STDIN_FILENO, &oldt);
			newt = oldt;
			newt.c_lflag &= ~(ICANON | ECHO);
			tcsetattr(STDIN_FILENO, TCSANOW, &newt);
			oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
			fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);
			ch = getchar();
			tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
			fcntl(STDIN_FILENO, F_SETFL, oldf);
			if(ch != EOF){
				ungetc(ch, stdin);
				return 1;
			}
			return 0;
		}
		PPM_Modulator::sptr
		PPM_Modulator::make(float samp_rate)
		{
			return gnuradio::get_initial_sptr
			(new PPM_Modulator_impl(samp_rate));
		}
		PPM_Modulator_impl::PPM_Modulator_impl(float samp_rate)
		: gr::block("PPM_Modulator",
			gr::io_signature::make(0, 0, sizeof(float)),
			gr::io_signature::make(1, 1, sizeof(float)))
		{

			// INIT
			d_nbr_samples = 0;
			d_nbr_channel = 0;
			d_nbr_samples_peak_duration = PEAK_DURATION * samp_rate;
			for(int i = 0; i < NBR_CHANNEL + 1; i++)
				d_nbr_samples_channel[i] = COMMAND_ZERO * samp_rate;
			d_nbr_samples_channel[NBR_CHANNEL + 1] = GUARD_TIME * samp_rate;
			d_command_step = COMMAND_STEP * samp_rate;

			// WELCOME
			printf("\n\n%sWelcome to Drone PPM Analog RC Transmitter!\n", RED);
			printf("%sRC>_ Commands :%s\n",BLUE, WHITE);
			printf("%sRC>_ 'z' -> CH1--\n%s",BLUE,WHITE);
			printf("%sRC>_ 's' -> CH1++\n%s",BLUE,WHITE);
			printf("%sRC>_ 'q' -> CH2--\n%s",BLUE,WHITE);
			printf("%sRC>_ 'd' -> CH2++\n%s",BLUE,WHITE);
			printf("%sRC>_ 'o' -> CH3--\n%s",BLUE,WHITE);
			printf("%sRC>_ 'l' -> CH3++\n%s",BLUE,WHITE);
			printf("%sRC>_ 'm' -> CH4--\n%s",BLUE,WHITE);
			printf("%sRC>_ 'k' -> CH4++\n%s",BLUE,WHITE);
		}

		PPM_Modulator_impl::~PPM_Modulator_impl(){}
		void
		PPM_Modulator_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
		{
			ninput_items_required[0] = noutput_items;
		}
		int
		PPM_Modulator_impl::general_work (int noutput_items,
			gr_vector_int &ninput_items,
			gr_vector_const_void_star &input_items,
			gr_vector_void_star &output_items)
		{
			const float *in = (const float *) input_items[0];
			float *out = (float *) output_items[0];

			for(int i = 0; i < noutput_items; i++){
				d_nbr_samples++;

	  			// PEAK GENERATION
				(d_nbr_samples < d_nbr_samples_peak_duration) ? out[i] = 1 : out[i] = 0;
				if(d_nbr_samples > d_nbr_samples_channel[d_nbr_channel]){
					d_nbr_samples = 0;
					d_nbr_channel = (d_nbr_channel + 1) % (NBR_CHANNEL + 2);
				}

	  			// CHECK COMMANDS
				if(kbhit()){
					switch(getch()){
						case 'z':
							d_nbr_samples_channel[0] -= d_command_step;
						break;
						case 's':
							d_nbr_samples_channel[0] += d_command_step;
						break;
						case 'q':
							d_nbr_samples_channel[1] -= d_command_step;
						break;
						case 'd':
							d_nbr_samples_channel[1] += d_command_step;
						break;
						case 'o':
							d_nbr_samples_channel[2] -= d_command_step;
						break;
						case 'l':
							d_nbr_samples_channel[2] += d_command_step;
						break;
						case 'm':
							d_nbr_samples_channel[3] -= d_command_step;
						break;
						case 'k':
							d_nbr_samples_channel[3] += d_command_step;
						break;
					}
				}			
			}      
			consume_each (noutput_items);
			return noutput_items;
	}
  } /* namespace PPM_Analog_RC */
} /* namespace gr */

