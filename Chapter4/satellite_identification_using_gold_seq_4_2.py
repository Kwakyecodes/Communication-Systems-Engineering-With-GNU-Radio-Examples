#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Identify which satellite is broadasting gps signal using correlation with gold sequence...
# Author: emmanuelkwakyenyantakyi
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
import pmt
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip
import threading



class satellite_identification_using_gold_seq_4_2(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Identify which satellite is broadasting gps signal using correlation with gold sequence...", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Identify which satellite is broadasting gps signal using correlation with gold sequence...")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "satellite_identification_using_gold_seq_4_2")

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
        self.samp_rate = samp_rate = 4e6
        self.df = df = 5200
        self.N = N = samp_rate/1000

        ##################################################
        # Blocks
        ##################################################

        self._df_range = qtgui.Range(-7e3, 7e3, 250, 5200, 200)
        self._df_win = qtgui.RangeWidget(self._df_range, self.set_df, "'df'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._df_win)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            int(N), #size
            samp_rate, #samp_rate
            "xcorr prn32", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


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
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            int(N), #size
            samp_rate, #samp_rate
            "xcorr prn31", #name
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
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccf(1, [1], df, samp_rate)
        self.fft_vxx_0_2_0 = fft.fft_vcc(int(N), True, [], True, 1)
        self.fft_vxx_0_2 = fft.fft_vcc(int(N), True, [], True, 1)
        self.fft_vxx_0_1_0 = fft.fft_vcc(int(N), False, [], True, 1)
        self.fft_vxx_0_1 = fft.fft_vcc(int(N), False, [], True, 1)
        self.fft_vxx_0 = fft.fft_vcc(int(N), False, [], True, 1)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, int(N))
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, int(N))
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_to_vector_1_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, int(N))
        self.blocks_stream_to_vector_1 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, int(N))
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, int(N))
        self.blocks_multiply_conjugate_cc_0_0 = blocks.multiply_conjugate_cc(int(N))
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(int(N))
        self.blocks_interleaved_short_to_complex_0 = blocks.interleaved_short_to_complex(False, False,32768)
        self.blocks_file_source_0_1 = blocks.file_source(gr.sizeof_gr_complex*1, '/Users/emmanuelkwakyenyantakyi/Desktop/Documents/College/SDR_2026_27/GNU_SDR_Intro/Chapter4/gps_L1_PRN32_4Msps.dat', True, 0, 0)
        self.blocks_file_source_0_1.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/Users/emmanuelkwakyenyantakyi/Desktop/Documents/College/SDR_2026_27/GNU_SDR_Intro/Chapter4/gps_L1_PRN31_4Msps.dat', True, 0, 0)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, '/Users/emmanuelkwakyenyantakyi/Desktop/Documents/College/SDR_2026_27/GNU_SDR_Intro/Chapter4/GPS-L1-2022-03-27.sigmf-data', True, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_complex_to_mag_2_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_2 = blocks.complex_to_mag(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_2, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_complex_to_mag_2_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_interleaved_short_to_complex_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.blocks_stream_to_vector_1_0, 0))
        self.connect((self.blocks_file_source_0_1, 0), (self.blocks_stream_to_vector_1, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.fft_vxx_0_2, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0_0, 0), (self.fft_vxx_0_2_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_1, 0), (self.fft_vxx_0_1, 0))
        self.connect((self.blocks_stream_to_vector_1_0, 0), (self.fft_vxx_0_1_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_complex_to_mag_2, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_complex_to_mag_2_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_multiply_conjugate_cc_0_0, 0))
        self.connect((self.fft_vxx_0_1, 0), (self.blocks_multiply_conjugate_cc_0_0, 1))
        self.connect((self.fft_vxx_0_1_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.fft_vxx_0_2, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.fft_vxx_0_2_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.blocks_stream_to_vector_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "satellite_identification_using_gold_seq_4_2")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_N(self.samp_rate/1000)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)

    def get_df(self):
        return self.df

    def set_df(self, df):
        self.df = df
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.df)

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N




def main(top_block_cls=satellite_identification_using_gold_seq_4_2, options=None):

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
