#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Nov 18 17:00:27 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

def struct(data): return type('Struct', (object,), data)()
from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import PPM_Analog_RC
import controller
import osmosdr
import sip
import sys
import threading
import time


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.Config_values = Config_values = struct({'LowFreqBoundary': 72.010e6, 'HighFreqBoundary': 72.900e6, 'ChannelWidth': 20e3, 'TransmissionSampRate': 250e3, })
        self.symbol_rate = symbol_rate = 0.35
        self.samp_rate = samp_rate = 1000000
        self.multiplied = multiplied = -2
        self.is_demod_on = is_demod_on = 0
        self.frequency_carrier = frequency_carrier = Config_values.LowFreqBoundary
        self.controller_callback_0 = controller_callback_0 = 1
        self.controller_callback = controller_callback = 1
        self.added = added = 0.02

        ##################################################
        # Blocks
        ##################################################
        self._multiplied_range = Range(-100, 0, 1, -2, 200)
        self._multiplied_win = RangeWidget(self._multiplied_range, self.set_multiplied, "multiplied", "counter_slider", float)
        self.top_layout.addWidget(self._multiplied_win)
        self.controller = controller.controller(low_freq_boundary=Config_values.LowFreqBoundary, high_freq_boundary=Config_values.HighFreqBoundary, channel_width=Config_values.ChannelWidth)
        self._added_range = Range(-1, 1, 0.001, 0.02, 200)
        self._added_win = RangeWidget(self._added_range, self.set_added, "added", "counter_slider", float)
        self.top_layout.addWidget(self._added_win)
        self.uhd_usrp_sink = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink.set_samp_rate(Config_values.TransmissionSampRate)
        self.uhd_usrp_sink.set_center_freq(frequency_carrier, 0)
        self.uhd_usrp_sink.set_gain(100, 0)
        self.uhd_usrp_sink.set_antenna('TX/RX', 0)
        self._symbol_rate_range = Range(0, 2, 0.01, 0.35, 200)
        self._symbol_rate_win = RangeWidget(self._symbol_rate_range, self.set_symbol_rate, 'Alpha', "counter_slider", float)
        self.top_layout.addWidget(self._symbol_rate_win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(frequency_carrier, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(20.7, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.root_raised_cosine_transmitter = filter.fir_filter_fff(1, firdes.root_raised_cosine(
        	1, Config_values.TransmissionSampRate, 1, 0.35, 50))
        self.qtgui_time_sink_x_3 = qtgui.time_sink_c(
        	40240, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_3.set_update_time(0.10)
        self.qtgui_time_sink_x_3.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_3.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_3.enable_tags(-1, True)
        self.qtgui_time_sink_x_3.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_3.enable_autoscale(False)
        self.qtgui_time_sink_x_3.enable_grid(False)
        self.qtgui_time_sink_x_3.enable_axis_labels(True)
        self.qtgui_time_sink_x_3.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_3.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2*1):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_3.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_3.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_3.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_3.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_3.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_3.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_3.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_3.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_3_win = sip.wrapinstance(self.qtgui_time_sink_x_3.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_3_win)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
        	10060, #size
        	Config_values.TransmissionSampRate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_2.enable_tags(-1, True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_2.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
        	40240, #size
        	samp_rate, #samp_rate
        	"Filtered", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_1.enable_tags(-1, True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_1.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
        	20240, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(Config_values.LowFreqBoundary, Config_values.HighFreqBoundary)
        
        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 100, 0.01, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	40240, #size
        	samp_rate, #samp_rate
        	"Peaks", #name
        	2 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.5, 0.01, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.probing_block = blocks.probe_signal_f()
        self.multiply_const_transmitter = blocks.multiply_const_vff((multiplied, ))
        self.moving_average = blocks.moving_average_ff(int(samp_rate*0.04), 1.0/(int(samp_rate*0.04)), 4000)
        self.low_pass_filter_transmitter = filter.fir_filter_fff(1, firdes.low_pass(
        	1, Config_values.TransmissionSampRate, 10e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_1 = filter.fir_filter_fff(1, firdes.low_pass(
        	100, samp_rate, 5e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	3, samp_rate, Config_values.ChannelWidth, Config_values.ChannelWidth/2, firdes.WIN_HAMMING, 6.76))
        
        def _controller_callback_0_probe():
            while True:
                val = self.controller.refreshUi(self)
                try:
                    self.set_controller_callback_0(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (5))
        _controller_callback_0_thread = threading.Thread(target=_controller_callback_0_probe)
        _controller_callback_0_thread.daemon = True
        _controller_callback_0_thread.start()
            
        
        def _controller_callback_probe():
            while True:
                val = self.controller.check_signal(self)
                try:
                    self.set_controller_callback(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (5))
        _controller_callback_thread = threading.Thread(target=_controller_callback_probe)
        _controller_callback_thread.daemon = True
        _controller_callback_thread.start()
            
        self.blocks_threshold_ff_0 = blocks.threshold_ff(0.1, 0.1, 0)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_rms_xx_0 = blocks.rms_cf(0.0001)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vff((1, ))
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((frequency_carrier, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((-1, ))
        self.analog_wfm_tx = analog.wfm_tx(
        	audio_rate=250000,
        	quad_rate=250000,
        	tau=75e-6,
        	max_dev=5e3,
        	fh=0,
        )
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=Config_values.ChannelWidth,
        	audio_decimation=1,
        )
        self.analog_const_source_x_0_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 1)
        self.add_const_transmitter = blocks.add_const_vff((added, ))
        self.PPM_Modulator = PPM_Analog_RC.PPM_Modulator(Config_values.TransmissionSampRate)
        self.PPM_Demodulator = PPM_Analog_RC.PPM_Demodulator(samp_rate, is_demod_on)
        self.PPM_Analog_RC_PPM_Signal_Detector_0 = PPM_Analog_RC.PPM_Signal_Detector(samp_rate, 10)
        self.PPM_Analog_RC_PPM_Peak_Detector_0 = PPM_Analog_RC.PPM_Peak_Detector(0.005)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.PPM_Analog_RC_PPM_Peak_Detector_0, 0), (self.PPM_Analog_RC_PPM_Signal_Detector_0, 0))    
        self.connect((self.PPM_Analog_RC_PPM_Peak_Detector_0, 0), (self.PPM_Demodulator, 0))    
        self.connect((self.PPM_Analog_RC_PPM_Peak_Detector_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.PPM_Analog_RC_PPM_Signal_Detector_0, 0), (self.probing_block, 0))    
        self.connect((self.PPM_Analog_RC_PPM_Signal_Detector_0, 0), (self.qtgui_time_sink_x_0, 1))    
        self.connect((self.PPM_Modulator, 0), (self.blocks_multiply_const_vxx_1_0, 0))    
        self.connect((self.add_const_transmitter, 0), (self.analog_wfm_tx, 0))    
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_multiply_const_vxx_1, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.analog_wfm_tx, 0), (self.uhd_usrp_sink, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.PPM_Analog_RC_PPM_Peak_Detector_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_time_sink_x_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.root_raised_cosine_transmitter, 0))    
        self.connect((self.blocks_rms_xx_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.PPM_Analog_RC_PPM_Signal_Detector_0, 1))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_rms_xx_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_time_sink_x_3, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.blocks_sub_xx_0, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.moving_average, 0))    
        self.connect((self.low_pass_filter_transmitter, 0), (self.multiply_const_transmitter, 0))    
        self.connect((self.moving_average, 0), (self.blocks_sub_xx_0, 1))    
        self.connect((self.moving_average, 0), (self.qtgui_time_sink_x_1, 1))    
        self.connect((self.multiply_const_transmitter, 0), (self.add_const_transmitter, 0))    
        self.connect((self.root_raised_cosine_transmitter, 0), (self.low_pass_filter_transmitter, 0))    
        self.connect((self.root_raised_cosine_transmitter, 0), (self.qtgui_time_sink_x_2, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_Config_values(self):
        return self.Config_values

    def set_Config_values(self, Config_values):
        self.Config_values = Config_values

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_3.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.moving_average.set_length_and_scale(int(self.samp_rate*0.04), 1.0/(int(self.samp_rate*0.04)))
        self.low_pass_filter_1.set_taps(firdes.low_pass(100, self.samp_rate, 5e3, 1e3, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(3, self.samp_rate, Config_values.ChannelWidth, Config_values.ChannelWidth/2, firdes.WIN_HAMMING, 6.76))

    def get_multiplied(self):
        return self.multiplied

    def set_multiplied(self, multiplied):
        self.multiplied = multiplied
        self.multiply_const_transmitter.set_k((self.multiplied, ))

    def get_is_demod_on(self):
        return self.is_demod_on

    def set_is_demod_on(self, is_demod_on):
        self.is_demod_on = is_demod_on
        self.PPM_Demodulator.set_demod_on(self.is_demod_on)

    def get_frequency_carrier(self):
        return self.frequency_carrier

    def set_frequency_carrier(self, frequency_carrier):
        self.frequency_carrier = frequency_carrier
        self.uhd_usrp_sink.set_center_freq(self.frequency_carrier, 0)
        self.rtlsdr_source_0.set_center_freq(self.frequency_carrier, 0)
        self.blocks_multiply_const_vxx_1.set_k((self.frequency_carrier, ))

    def get_controller_callback_0(self):
        return self.controller_callback_0

    def set_controller_callback_0(self, controller_callback_0):
        self.controller_callback_0 = controller_callback_0

    def get_controller_callback(self):
        return self.controller_callback

    def set_controller_callback(self, controller_callback):
        self.controller_callback = controller_callback

    def get_added(self):
        return self.added

    def set_added(self, added):
        self.added = added
        self.add_const_transmitter.set_k((self.added, ))


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
