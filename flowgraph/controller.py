"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class controller(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""



    def __init__(self, low_freq_boundary=72010000, high_freq_boundary=72990000, channel_width=20000):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='PPM Demodulation controller',   # will show up in GRC
            in_sig=[],
            out_sig=[]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.low_freq_boundary = low_freq_boundary
        self.high_freq_boundary = high_freq_boundary
        self.channel_width = channel_width
        self.should_start = False

    def check_signal(self, obj):
    	if self.should_start == False :
    		self.should_start = True
    		return 0

    	if(obj.probing_block.level() >=1):
    		decode = 1
    		print 'Signal detected'
    		return 1
    	else :
            newfreq = obj.frequency_carrier + self.channel_width   #Loop on available channels
            if (newfreq > self.high_freq_boundary):
                newfreq = self.low_freq_boundary
            obj.set_frequency_carrier(newfreq)
            return 0


    def work(self, input_items, output_items):
        """example: multiply with constant"""
        #output_items[0][:] = input_items[0] * self.example_param
        return len(output_items[0])
