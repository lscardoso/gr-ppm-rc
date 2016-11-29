#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Tue Nov 29 17:56:22 2016
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
from optparse import OptionParser
import PPM_Analog_RC
import controller
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
        self.Config_values = Config_values = struct({'LowFreqBoundary': 41.200e6 , 'HighFreqBoundary': 41.200e6, 'ChannelWidth': 10e3, 'SampRate': 400e3, 'TransmissionSampRate': 500e3, 'Multiplied': -1, 'Added': 0.02, })
        self.refresh_ui = refresh_ui = 1
        self.is_demod_on = is_demod_on = 0
        self.frequency_carrier = frequency_carrier = Config_values.LowFreqBoundary
        self.controller_callback = controller_callback = 1

        ##################################################
        # Blocks
        ##################################################
        self.controller = controller.controller(low_freq_boundary=Config_values.LowFreqBoundary, high_freq_boundary=Config_values.HighFreqBoundary, channel_width=Config_values.ChannelWidth)
        self.variable_qtgui_range_00 = blocks.multiply_const_vff((0.5, ))
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(1e6)
        self.uhd_usrp_source_0.set_center_freq(frequency_carrier, 0)
        self.uhd_usrp_source_0.set_gain(1, 0)
        self.uhd_usrp_source_0.set_antenna('RX2', 0)
        self.uhd_usrp_sink = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink.set_samp_rate(Config_values.TransmissionSampRate)
        self.uhd_usrp_sink.set_center_freq(frequency_carrier, 0)
        self.uhd_usrp_sink.set_gain(200, 0)
        self.uhd_usrp_sink.set_antenna('TX/RX', 0)
        self.root_raised_cosine_transmitter = filter.fir_filter_fff(1, firdes.root_raised_cosine(
        	1, Config_values.TransmissionSampRate, 1, 0.35, 20))
        
        def _refresh_ui_probe():
            while True:
                val = self.controller.refreshUi(self)
                try:
                    self.set_refresh_ui(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (5))
        _refresh_ui_thread = threading.Thread(target=_refresh_ui_probe)
        _refresh_ui_thread.daemon = True
        _refresh_ui_thread.start()
            
        self.qtgui_time_sink_x_2_0 = qtgui.time_sink_c(
        	10240, #size
        	Config_values.SampRate, #samp_rate
        	"Post AGC", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_2_0.set_update_time(0.10)
        self.qtgui_time_sink_x_2_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_2_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_2_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_2_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_0.enable_autoscale(False)
        self.qtgui_time_sink_x_2_0.enable_grid(False)
        self.qtgui_time_sink_x_2_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_0.enable_control_panel(False)
        
        if not True:
          self.qtgui_time_sink_x_2_0.disable_legend()
        
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
                    self.qtgui_time_sink_x_2_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_2_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_2_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_2_0_win = sip.wrapinstance(self.qtgui_time_sink_x_2_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_2_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	40240, #size
        	Config_values.SampRate, #samp_rate
        	"Peaks", #name
        	3 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)
        
        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
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
        
        for i in xrange(3):
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
        self.multiply_const_transmitter = blocks.multiply_const_vff((Config_values.Multiplied, ))
        self.moving_average = blocks.moving_average_ff(int(Config_values.SampRate*0.04), 1.0/(int(Config_values.SampRate*0.04)), 4000)
        self.low_pass_filter_transmitter = filter.fir_filter_fff(1, firdes.low_pass(
        	1, Config_values.TransmissionSampRate, 1e3, 8e3, firdes.WIN_HANN, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, Config_values.SampRate, Config_values.ChannelWidth-(Config_values.ChannelWidth/7), Config_values.ChannelWidth/20, firdes.WIN_HAMMING, 6.76))
        self.fractional_resampler_xx_0 = filter.fractional_resampler_cc(0, 1000000/Config_values.SampRate)
        
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
            
        self.blocks_vco_c_0 = blocks.vco_c(Config_values.TransmissionSampRate, 100000, 1)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((-1, ))
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.analog_agc2_xx_0_0 = analog.agc2_ff(1, 10, 1.2, 1.0)
        self.analog_agc2_xx_0_0.set_max_gain(0)
        self.analog_agc2_xx_0 = analog.agc2_cc(1e-1, 1e-0, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)
        self.add_const_transmitter = blocks.add_const_vff((Config_values.Added, ))
        self.PPM_Modulator = PPM_Analog_RC.PPM_Modulator(Config_values.TransmissionSampRate)
        self.PPM_Demodulator = PPM_Analog_RC.PPM_Demodulator(Config_values.SampRate, is_demod_on)
        self.PPM_Analog_RC_PPM_Signal_Detector_0 = PPM_Analog_RC.PPM_Signal_Detector(Config_values.SampRate, 1e-14)
        self.PPM_Analog_RC_PPM_Peak_Detector_0 = PPM_Analog_RC.PPM_Peak_Detector(0.9)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.PPM_Analog_RC_PPM_Peak_Detector_0, 0), (self.PPM_Analog_RC_PPM_Signal_Detector_0, 0))    
        self.connect((self.PPM_Analog_RC_PPM_Peak_Detector_0, 0), (self.PPM_Demodulator, 0))    
        self.connect((self.PPM_Analog_RC_PPM_Peak_Detector_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.PPM_Analog_RC_PPM_Signal_Detector_0, 0), (self.probing_block, 0))    
        self.connect((self.PPM_Modulator, 0), (self.variable_qtgui_range_00, 0))    
        self.connect((self.add_const_transmitter, 0), (self.blocks_vco_c_0, 0))    
        self.connect((self.analog_agc2_xx_0, 0), (self.qtgui_time_sink_x_2_0, 0))    
        self.connect((self.analog_agc2_xx_0_0, 0), (self.blocks_sub_xx_0, 0))    
        self.connect((self.analog_agc2_xx_0_0, 0), (self.moving_average, 0))    
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.PPM_Analog_RC_PPM_Signal_Detector_0, 1))    
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.analog_agc2_xx_0_0, 0))    
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.qtgui_time_sink_x_0, 2))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.PPM_Analog_RC_PPM_Peak_Detector_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 1))    
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_vco_c_0, 0), (self.uhd_usrp_sink, 0))    
        self.connect((self.fractional_resampler_xx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_agc2_xx_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.low_pass_filter_transmitter, 0), (self.multiply_const_transmitter, 0))    
        self.connect((self.moving_average, 0), (self.blocks_sub_xx_0, 1))    
        self.connect((self.multiply_const_transmitter, 0), (self.add_const_transmitter, 0))    
        self.connect((self.root_raised_cosine_transmitter, 0), (self.low_pass_filter_transmitter, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.fractional_resampler_xx_0, 0))    
        self.connect((self.variable_qtgui_range_00, 0), (self.root_raised_cosine_transmitter, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_Config_values(self):
        return self.Config_values

    def set_Config_values(self, Config_values):
        self.Config_values = Config_values

    def get_refresh_ui(self):
        return self.refresh_ui

    def set_refresh_ui(self, refresh_ui):
        self.refresh_ui = refresh_ui

    def get_is_demod_on(self):
        return self.is_demod_on

    def set_is_demod_on(self, is_demod_on):
        self.is_demod_on = is_demod_on
        self.PPM_Demodulator.set_demod_on(self.is_demod_on)

    def get_frequency_carrier(self):
        return self.frequency_carrier

    def set_frequency_carrier(self, frequency_carrier):
        self.frequency_carrier = frequency_carrier
        self.uhd_usrp_source_0.set_center_freq(self.frequency_carrier, 0)
        self.uhd_usrp_sink.set_center_freq(self.frequency_carrier, 0)

    def get_controller_callback(self):
        return self.controller_callback

    def set_controller_callback(self, controller_callback):
        self.controller_callback = controller_callback


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
