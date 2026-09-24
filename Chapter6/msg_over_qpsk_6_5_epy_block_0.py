import numpy as np
from gnuradio import gr
import pmt


class blk(gr.basic_block):
    """Packet Print ASCII"""

    def __init__(self):
        gr.basic_block.__init__(
            self,
            name="Packet Print ASCII",
            in_sig=None,
            out_sig=None
        )

        # Register message input port
        self.message_port_register_in(pmt.intern("in"))

        # Set message handler
        self.set_msg_handler(
            pmt.intern("in"),
            self.handle_message
        )

    def handle_message(self, msg):

        # Extract payload from PDU
        payload = pmt.cdr(msg)

        # Convert PMT vector to NumPy array
        data = pmt.u8vector_elements(payload)

        # Convert bytes to ASCII text
        text = bytes(data).decode("ascii", errors="replace")

        # Print received message
        print(text)