"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

	

    def __init__(self, example_param=1.0):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Embedded Python Block',   # will show up in GRC
            in_sig=[],
            out_sig=[]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.example_param = example_param
	self.should_start = False

    def check_signal(self, obj):
	if self.should_start == False :
		self.should_start = True
		return

	if(obj.probing_block.level() >=1):
		decode = 1
		print 'yay'
	else:
		newfreq = obj.frequency_carrier + 20000
		if newfreq > 72990000:				#Loop on available channels
			newfreq = 72010000
		obj.set_frequency_carrier(newfreq)
		#obj.frequency_carrierfreq = obj.frequency_carrier + 20000
		
		print 'truc'






def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0] * self.example_param
        return len(output_items[0])
