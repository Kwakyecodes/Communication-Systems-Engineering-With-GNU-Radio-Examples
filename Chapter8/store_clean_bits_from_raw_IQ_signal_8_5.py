#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Recover and store clean stream of bits (0s and 1s) from raw IQ signal
# Author: emmanuelkwakyenyantakyi
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import numpy
import sip
import threading



class store_clean_bits_from_raw_IQ_signal_8_5(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Recover and store clean stream of bits (0s and 1s) from raw IQ signal", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Recover and store clean stream of bits (0s and 1s) from raw IQ signal")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "store_clean_bits_from_raw_IQ_signal_8_5")

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
        self.symb_rate = symb_rate = 72e3
        self.samp_rate = samp_rate = 156.8e3
        self.sps = sps = samp_rate/symb_rate
        self.nfilts = nfilts = 8
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/sps, 0.35, int(11 * sps * nfilts))

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            'After carrier and timing synchronization', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_ZERO_CROSSING,
            sps,
            (2*numpy.pi/2000),
            0.707,
            2.5,
            1.5,
            1,
            digital.constellation_qpsk().base(),
            digital.IR_PFB_MF,
            nfilts,
            rrc_taps)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc((2*numpy.pi/500), 4, False)
        self.digital_constellation_soft_decoder_cf_0 = digital.constellation_soft_decoder_cf(digital.constellation_qpsk().base(), -1)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, (samp_rate*10), True, 0 if "auto" == "auto" else max( int(float(0.1) * (samp_rate*10)) if "auto" == "time" else int(0.1), 1) )
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 127)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/Users/emmanuelkwakyenyantakyi/Desktop/MeteorM2N_180501_17h52_after_resampler.sigmf-data', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/Users/emmanuelkwakyenyantakyi/Desktop/meteor_softbits.bin', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.analog_rail_ff_0 = analog.rail_ff((-1), (+1))
        self.analog_agc2_xx_0 = analog.agc2_cc((1e-1), (1e-2), 1.0, 1.0, 65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.analog_rail_ff_0, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_float_to_char_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.digital_constellation_soft_decoder_cf_0, 0), (self.analog_rail_ff_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_constellation_soft_decoder_cf_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_const_sink_x_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "store_clean_bits_from_raw_IQ_signal_8_5")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_symb_rate(self):
        return self.symb_rate

    def set_symb_rate(self, symb_rate):
        self.symb_rate = symb_rate
        self.set_sps(self.samp_rate/self.symb_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sps(self.samp_rate/self.symb_rate)
        self.blocks_throttle2_0.set_sample_rate((self.samp_rate*10))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/self.sps, 0.35, int(11 * self.sps * self.nfilts)))
        self.digital_symbol_sync_xx_0.set_sps(self.sps)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/self.sps, 0.35, int(11 * self.sps * self.nfilts)))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps




def main(top_block_cls=store_clean_bits_from_raw_IQ_signal_8_5, options=None):

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
