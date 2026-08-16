#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Demonstration of linearity of correlation...
# Author: emmanuelkwakyenyantakyi
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip
import threading
import time



class cross_corr_delay_using_function_probe_4_2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Demonstration of linearity of correlation...", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Demonstration of linearity of correlation...")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "cross_corr_delay_using_function_probe_4_2")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 320000
        self.N = N = 1024
        self.D2 = D2 = 0
        self.D1 = D1 = 0
        self.D0 = D0 = 0

        ##################################################
        # Blocks
        ##################################################

        self.probe2 = blocks.probe_signal_i()
        self.probe1 = blocks.probe_signal_i()
        self.probe0 = blocks.probe_signal_i()
        def _D2_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.probe2.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_D2,val))
              except AttributeError:
                self.set_D2(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _D2_thread = threading.Thread(target=_D2_probe)
        _D2_thread.daemon = True
        _D2_thread.start()
        def _D1_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.probe1.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_D1,val))
              except AttributeError:
                self.set_D1(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _D1_thread = threading.Thread(target=_D1_probe)
        _D1_thread.daemon = True
        _D1_thread.start()
        def _D0_probe():
          self.flowgraph_started.wait()
          while True:

            val = self.probe0.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_D0,val))
              except AttributeError:
                self.set_D0(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (10))
        _D0_thread = threading.Thread(target=_D0_probe)
        _D0_thread.daemon = True
        _D0_thread.start()
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(0, 80)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.fft_vxx_1_0 = fft.fft_vcc(1024, False, window.blackmanharris(1024), True, 1)
        self.fft_vxx_1 = fft.fft_vcc(1024, False, window.blackmanharris(1024), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(1024, True, window.blackmanharris(1024), True, 1)
        self.blocks_vector_to_stream_1 = blocks.vector_to_stream(gr.sizeof_float*1, N)
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, N)
        self.blocks_throttle2_3 = blocks.throttle( gr.sizeof_int*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_2 = blocks.throttle( gr.sizeof_int*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_1 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_int*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_to_vector_0_2 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, N)
        self.blocks_stream_to_vector_0_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, N)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, N)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, N)
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(N)
        self.blocks_delay_0_1 = blocks.delay(gr.sizeof_gr_complex*1, D2)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_gr_complex*1, D1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, D0)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(N)
        self.blocks_add_xx_0 = blocks.add_vcc(N)
        self.analog_sig_source_x_2 = analog.sig_source_i(samp_rate, analog.GR_SQR_WAVE, 0.1, 128, 64, 0)
        self.analog_sig_source_x_1 = analog.sig_source_i(samp_rate, analog.GR_COS_WAVE, 0.1, 128, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_i(samp_rate, analog.GR_TRI_WAVE, 0.1, 128, 0, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_throttle2_1, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_throttle2_3, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.analog_sig_source_x_2, 0), (self.blocks_throttle2_2, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.fft_vxx_1_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.blocks_vector_to_stream_1, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_stream_to_vector_0_2, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_stream_to_vector_0_1, 0))
        self.connect((self.blocks_delay_0_1, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_1, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_stream_to_vector_0_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_stream_to_vector_0_2, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.probe2, 0))
        self.connect((self.blocks_throttle2_1, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_throttle2_1, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_throttle2_1, 0), (self.blocks_delay_0_1, 0))
        self.connect((self.blocks_throttle2_1, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_throttle2_2, 0), (self.probe1, 0))
        self.connect((self.blocks_throttle2_3, 0), (self.probe0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_vector_to_stream_1, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.fft_vxx_1, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.fft_vxx_1_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "cross_corr_delay_using_function_probe_4_2")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_2.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_2.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_3.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N

    def get_D2(self):
        return self.D2

    def set_D2(self, D2):
        self.D2 = D2
        self.blocks_delay_0_1.set_dly(int(self.D2))

    def get_D1(self):
        return self.D1

    def set_D1(self, D1):
        self.D1 = D1
        self.blocks_delay_0_0.set_dly(int(self.D1))

    def get_D0(self):
        return self.D0

    def set_D0(self, D0):
        self.D0 = D0
        self.blocks_delay_0.set_dly(int(self.D0))




def main(top_block_cls=cross_corr_delay_using_function_probe_4_2, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
