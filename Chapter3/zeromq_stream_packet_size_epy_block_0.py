"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self):  # only default arguments here
        gr.sync_block.__init__(
            self,
            name='ZMQ size',   # will show up in GRC
            in_sig=[(np.complex64, 64)],
            out_sig=[]
        )
        self.n = 0

    def work(self, input_items, output_items):
        if self.n < 100:
            print(len(input_items[0]))
        self.n = self.n + 1
        return 0
