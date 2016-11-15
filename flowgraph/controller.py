"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import sys, tty, termios
import threading
import numpy as np
import Tkinter as tk
from gnuradio import gr
import time
import PPM_Analog_RC


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
        self.found_last = [False,False]
        self.input_key = ''
        self.decode = False


    def check_signal(self, obj):
        if self.should_start == False :
            self.should_start = True
            def launchWindow():
                self.window = ui(self)
                self.window.master.title('PPM RC Hack')
                self.window.mainloop()
            self._window_thread = threading.Thread(target=launchWindow)
            self._window_thread.daemon = True
            self._window_thread.start()
            time.sleep(0.1)
            self.window.freqLabel.config(text= "Frequency: " + str(self.low_freq_boundary/1000000.0) + "MHz")
            return 0

        if self.input_key == 'escape':
            self.input_key = ''
            newfreq = obj.frequency_carrier + self.channel_width   #Loop on available channels
            if (newfreq > self.high_freq_boundary):
                newfreq = self.low_freq_boundary
            obj.set_frequency_carrier(newfreq)
            obj.set_is_demod_on(0)
            print 'Changing channel'
            self.window.freqLabel.config(text= "Frequency: " + str(newfreq/1000000.0) + "MHz")
            self.window.channelInfoLabel.config(text = '')
            self.found_last[0] = 0
            self.found_last[1] = False
            self.decode = False
            return 0

        if self.input_key == 'enter':       #Placeholder to switch to transmission
            self.input_key = ''

        if(obj.probing_block.level() >=1):      #Actual check if signal is detected by the signal detector block
            if self.found_last[0] is True:      #To smooth burst of false results
                if self.found_last[1] is False: #To act only if we just arrived on this channel
                    self.window.detectedLabel.config(text='''Signal detected: press esc to continue sweep
press enter to switch to transmittion mode (not implemented yet)''')
                    obj.set_is_demod_on(1)
                    self.found_last[1] = True
                    self.decode = True
                return 1
            else:
                self.found_last[0] = True
                return 0
        else :
            if self.found_last[0] is False:
                newfreq = obj.frequency_carrier + self.channel_width   #Loop on available channels
                if (newfreq > self.high_freq_boundary):
                    newfreq = self.low_freq_boundary
                obj.set_frequency_carrier(newfreq)
                obj.set_is_demod_on(0)

                self.window.detectedLabel.config(text=" Sweeping... ")
                self.window.freqLabel.config(text= "Frequency: " + str(newfreq/1000000.0) + "MHz")
                self.window.channelInfoLabel.config(text = '')
                self.found_last[0] = 0
                self.found_last[1] = False
                self.decode = False
                print 'Changing channel nothing found' + "  Frequency: " +str(newfreq/1000000.0) + "MHz"
                return 0
            else:
                self.found_last[0] = False
                return 1

    def refreshUi(self, obj):
        if self.decode == True:
            channelValues = obj.PPM_Demodulator.get_channels()
            nbChannels = obj.PPM_Demodulator.get_nbr_channels()
            string = str(nbChannels) + " channels detected: "
            if nbChannels > 0:
                for i in xrange(1,nbChannels+1):
                    string = string + "CH" + str(i) + ": " + '{:03.2f}'.format(PPM_Analog_RC.floatArray_getitem(channelValues, index=(i-1))) + " | "
            self.window.channelInfoLabel.config(text = string)



    def work(self, input_items, output_items):
        """example: multiply with constant"""
        #output_items[0][:] = input_items[0] * self.example_param
        return len(output_items[0])








class ui(tk.Frame):
    def __init__(self, calling, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        self.calling = calling

    def createWidgets(self):
        self.freqLabel = tk.Label()
        self.freqLabel.grid()
        self.detectedLabel = tk.Label(text=" Sweeping... ")
        self.detectedLabel.grid()
        self.channelInfoLabel = tk.Label(text="  No channels  ")
        self.channelInfoLabel.grid()
        self.freqLabel.bind_all('<KeyPress-Return>', self._enterHandler)
        self.freqLabel.bind_all('<KeyPress-Escape>', self._escapeHandler)


    def _enterHandler(self,event):
        self.calling.input_key = 'enter'
    def _escapeHandler(self,event):
        self.calling.input_key = 'escape'
