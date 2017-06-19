"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import os, struct, array
from fcntl import ioctl
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




    def connectTransmitter(self, obj):
        obj.lock()
        obj.connect((obj.PPM_Modulator, 0), (obj.variable_qtgui_range_00, 0))
        obj.connect((obj.low_pass_filter_transmitter, 0), (obj.multiply_const_transmitter, 0))
        obj.connect((obj.multiply_const_transmitter, 0), (obj.add_const_transmitter, 0))
        obj.connect((obj.root_raised_cosine_transmitter, 0), (obj.low_pass_filter_transmitter, 0))
        obj.connect((obj.variable_qtgui_range_00, 0), (obj.root_raised_cosine_transmitter, 0))
        obj.connect((obj.blocks_vco_c_0, 0), (obj.uhd_usrp_sink, 0))
        obj.connect((obj.add_const_transmitter, 0), (obj.blocks_vco_c_0, 0))
        obj.unlock()

    def disconnectTransmitter(self, obj):

        obj.lock()
        obj.disconnect((obj.PPM_Modulator, 0), (obj.variable_qtgui_range_00, 0))
        obj.disconnect((obj.low_pass_filter_transmitter, 0), (obj.multiply_const_transmitter, 0))
        obj.disconnect((obj.multiply_const_transmitter, 0), (obj.add_const_transmitter, 0))
        obj.disconnect((obj.root_raised_cosine_transmitter, 0), (obj.low_pass_filter_transmitter, 0))
        obj.disconnect((obj.variable_qtgui_range_00, 0), (obj.root_raised_cosine_transmitter, 0))
        obj.disconnect((obj.blocks_vco_c_0, 0), (obj.uhd_usrp_sink, 0))
        obj.disconnect((obj.add_const_transmitter, 0), (obj.blocks_vco_c_0, 0))
        obj.unlock()

    def nextChannel(self,obj):
        # Chan change
        newfreq = obj.frequency_carrier + self.channel_width   #Loop on available channels
        if (newfreq > self.high_freq_boundary):
            newfreq = self.low_freq_boundary
        obj.set_frequency_carrier(newfreq)
        obj.set_is_demod_on(0)
        # Ui reset
        self.window.detectedLabel.config(text=" Sweeping... ")
        self.window.freqLabel.config(text= "Frequency: " + str(newfreq/1000000.0) + "MHz")
        self.window.channelInfoLabel.config(text = '')
        self.window.channelInfoLabelEnergy.config(text = '')
        self.found_last[0] = 0
        self.found_last[1] = False
        self.decode = False




    def check_signal(self, obj):

        #Inititalize the ui and disconnect transmitter on first call
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
            joyInput = stick(self, obj)
            self._window_thread = threading.Thread(target=joyInput.updatePositionLoop)
            self._window_thread.daemon = True
            self._window_thread.start()
            self.disconnectTransmitter(obj)
            self.transmitting = False
            self.window.freqLabel.config(text= "Frequency: " + str(self.low_freq_boundary/1000000.0) + "MHz")
            return 0

        #Switch to next channel manually
        if self.input_key == 'escape':
            self.input_key = ''
            print 'Changing channel'
            self.nextChannel(obj)
            return 0


        #Switch transmission on/off
        if self.input_key == 'enter':
            self.input_key = ''
            print 'switching transmitter'
            if self.transmitting:
                self.disconnectTransmitter(obj)
                self.transmitting = False
            else:
                self.connectTransmitter(obj)
                self.transmitting = True


        #Actual check if signal is detected by the signal detector block
        if(obj.probing_block.level() >=1 or obj.probing_block_energy.level() >=1):
            if self.found_last[0] is True:      #To smooth burst of false results
                if self.found_last[1] is False: #To act only if we just arrived on this channel
                    self.window.detectedLabel.config(text='''Signal detected: press esc to continue sweep
Press enter to switch to transmittion mode''')
                    obj.set_is_demod_on(1)
                    self.found_last[1] = True
                    self.decode = True
                return 1
            else:
                self.found_last[0] = True
                return 0
        else :
            if self.found_last[0] is False:
                self.nextChannel(obj)
                print 'Changing channel nothing found'
                return 0
            else:
                self.found_last[0] = False
                return 1


    #Refresh the ui with channel values information
    def refreshUi(self, obj):
        if self.decode == True:
            if obj.probing_block.level() >=1 :
                channelValues = obj.PPM_Demodulator.get_channels()
                nbChannels = obj.PPM_Demodulator.get_nbr_channels()
                string = str(nbChannels) + " channels detected with FM demod: "
                if nbChannels > 0:
                    for i in xrange(1,nbChannels+1):
                        string = string + "CH" + str(i) + ": " + '{:03.2f}'.format(PPM_Analog_RC.floatArray_getitem(channelValues, index=(i-1))) + " | "
                self.window.channelInfoLabel.config(text = string)
            else:
                self.window.channelInfoLabel.config(text = '0 channels detected with FM demod.')

            if obj.probing_block_energy.level() >=1 :
                channelValues = obj.PPM_Demodulator_energy.get_channels()
                nbChannels = obj.PPM_Demodulator_energy.get_nbr_channels()
                string = str(nbChannels) + " channels detected with energy measurement: "
                if nbChannels > 0:
                    for i in xrange(1,nbChannels+1):
                        string = string + "CH" + str(i) + ": " + '{:03.2f}'.format(PPM_Analog_RC.floatArray_getitem(channelValues, index=(i-1))) + " | "
                self.window.channelInfoLabelEnergy.config(text = string)
            else:
                self.window.channelInfoLabelEnergy.config(text = '0 channels detected with FM demod.')


    #Not in use
    def work(self, input_items, output_items):
        """example: multiply with constant"""
        #output_items[0][:] = input_items[0] * self.example_param
        return len(output_items[0])








class ui(tk.Frame):
    def __init__(self, calling, master=None):
        tk.Frame.__init__(self, master)
        self.config(height = 50, width = 500)
        self.grid()
        self.createWidgets()
        self.calling = calling

    def createWidgets(self):
        #self.frameOptions = tk.Frame()
        #self.frameSate = tk.Frame()

        self.freqLabel = tk.Label()
        self.freqLabel.grid()
        self.detectedLabel = tk.Label(text=" Sweeping... ")
        self.detectedLabel.grid()
        self.channelInfoLabel = tk.Label(text="  No channels  ")
        self.channelInfoLabel.grid()
        self.channelInfoLabelEnergy = tk.Label(text="  No channels  ")
        self.channelInfoLabelEnergy.grid()
        self.freqLabel.bind_all('<KeyPress-Return>', self._enterHandler)
        self.freqLabel.bind_all('<KeyPress-Escape>', self._escapeHandler)


    def _enterHandler(self,event):
        self.calling.input_key = 'enter'
    def _escapeHandler(self,event):
        self.calling.input_key = 'escape'


#Handle joystick inputs
class stick():
    def __init__(self, calling, top_block):
        self.calling = calling
        self.top_block = top_block

        # Iterate over the joystick devices.
        print('Available devices:')

        for fn in os.listdir('/dev/input'):
            if fn.startswith('js'):
                print('  /dev/input/%s' % (fn))

        # We'll store the states here.
        self.axis_states = {}
        self.button_states = {}

        # These constants were borrowed from linux/input.h
        self.axis_names = {
            0x00 : 'x',
            0x01 : 'y',
            0x02 : 'z',
            0x03 : 'rx',
            0x04 : 'ry',
            0x05 : 'rz',
            0x06 : 'trottle',
            0x07 : 'rudder',
            0x08 : 'wheel',
            0x09 : 'gas',
            0x0a : 'brake',
            0x10 : 'hat0x',
            0x11 : 'hat0y',
            0x12 : 'hat1x',
            0x13 : 'hat1y',
            0x14 : 'hat2x',
            0x15 : 'hat2y',
            0x16 : 'hat3x',
            0x17 : 'hat3y',
            0x18 : 'pressure',
            0x19 : 'distance',
            0x1a : 'tilt_x',
            0x1b : 'tilt_y',
            0x1c : 'tool_width',
            0x20 : 'volume',
            0x28 : 'misc',
        }

        self.button_names = {
            0x120 : 'trigger',
            0x121 : 'thumb',
            0x122 : 'thumb2',
            0x123 : 'top',
            0x124 : 'top2',
            0x125 : 'pinkie',
            0x126 : 'base',
            0x127 : 'base2',
            0x128 : 'base3',
            0x129 : 'base4',
            0x12a : 'base5',
            0x12b : 'base6',
            0x12f : 'dead',
            0x130 : 'a',
            0x131 : 'b',
            0x132 : 'c',
            0x133 : 'x',
            0x134 : 'y',
            0x135 : 'z',
            0x136 : 'tl',
            0x137 : 'tr',
            0x138 : 'tl2',
            0x139 : 'tr2',
            0x13a : 'select',
            0x13b : 'start',
            0x13c : 'mode',
            0x13d : 'thumbl',
            0x13e : 'thumbr',

            0x220 : 'dpad_up',
            0x221 : 'dpad_down',
            0x222 : 'dpad_left',
            0x223 : 'dpad_right',

            # XBox 360 controller uses these codes.
            0x2c0 : 'dpad_left',
            0x2c1 : 'dpad_right',
            0x2c2 : 'dpad_up',
            0x2c3 : 'dpad_down',
        }

        self.axis_map = []
        self.button_map = []

        # Open the joystick device.
        fn = '/dev/input/js0'
        print('Opening %s...' % fn)
        try:
            self.jsdev = open(fn, 'rb')
        except:
            print 'No device found'
            self.controller = False
            return
        self.controller = True

        # Get the device name.
        #buf = bytearray(63)
        buf = array.array('c', ['\0'] * 64)
        ioctl(self.jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
        js_name = buf.tostring()
        print('Device name: %s' % js_name)

        # Get number of axes and buttons.
        buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016a11, buf) # JSIOCGAXES
        num_axes = buf[0]

        buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
        num_buttons = buf[0]

        # Get the axis map.
        buf = array.array('B', [0] * 0x40)
        ioctl(self.jsdev, 0x80406a32, buf) # JSIOCGAXMAP

        for axis in buf[:num_axes]:
            axis_name = self.axis_names.get(axis, 'unknown(0x%02x)' % axis)
            self.axis_map.append(axis_name)
            self.axis_states[axis_name] = 0.0

        # Get the button map.
        buf = array.array('H', [0] * 200)
        ioctl(self.jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

        for btn in buf[:num_buttons]:
            btn_name = self.button_names.get(btn, 'unknown(0x%03x)' % btn)
            self.button_map.append(btn_name)
            self.button_states[btn_name] = 0

        print '%d axes found: %s' % (num_axes, ', '.join(self.axis_map))
        print '%d buttons found: %s' % (num_buttons, ', '.join(self.button_map))

    def updatePositionLoop(self):
        if not self.controller:
            return

        # Main event loop
        while True:
            evbuf = self.jsdev.read(8)
            if evbuf:
                time, value, type, number = struct.unpack('IhBB', evbuf)

                if type & 0x80:
                     print "(initial)",

                if type & 0x01:
                    button = self.button_map[number]
                    if button:
                        self.button_states[button] = value
                        if value:
                            #print "%s pressed" % (button)
                            if button == 'trigger':
                                self.calling.input_key = 'enter'
                            elif button == 'thumb':
                                self.calling.input_key = 'escape'
                        else:
                            pass
                            #print "%s released" % (button)


                if type & 0x02:
                    axis = self.axis_map[number]
                    if axis:
                        fvalue = value / 32767.0
                        self.axis_states[axis] = fvalue
                        if axis == 'trottle':
                            self.top_block.PPM_Modulator.set_axis(2, fvalue)
                        elif axis == 'y':
                            self.top_block.PPM_Modulator.set_axis(1, fvalue)
                        elif axis == 'x':
                            self.top_block.PPM_Modulator.set_axis(0, fvalue)
                        elif axis == 'rz':
                            self.top_block.PPM_Modulator.set_axis(3, fvalue)
