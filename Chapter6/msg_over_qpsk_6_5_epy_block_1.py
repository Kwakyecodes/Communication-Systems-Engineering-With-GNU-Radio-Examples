import numpy as np
from gnuradio import gr
import pmt


class blk(gr.basic_block):
    """Insert idle bits after each tagged packet."""

    def __init__(self, idle_bytes=24000, length_tag_key="tr_len_key"):
        gr.basic_block.__init__(
            self,
            name="Packet + Idle Bits",
            in_sig=[np.uint8],
            out_sig=[np.uint8],
        )

        self.idle_bytes = int(idle_bytes)
        self.length_tag_key = pmt.intern(length_tag_key)

        self.packet = []
        self.packet_remaining = 0
        self.idle_remaining = 0

    def general_work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]

        n_in = len(inp)
        n_out = len(out)

        consumed = 0
        produced = 0

        while produced < n_out:

            # Output idle bits between packets.
            if self.idle_remaining > 0:
                count = min(self.idle_remaining, n_out - produced)
                out[produced:produced + count] = np.random.randint(
                    0, 2, count, dtype=np.uint8
                )
                produced += count
                self.idle_remaining -= count
                continue

            # Wait for a packet-length tag.
            if self.packet_remaining == 0:
                tags = self.get_tags_in_range(
                    0,
                    self.nitems_read(0) + consumed,
                    self.nitems_read(0) + consumed + 1,
                    self.length_tag_key,
                )

                if not tags:
                    break

                self.packet_remaining = int(
                    pmt.to_long(tags[0].value)
                )

            # Copy the complete packet.
            count = min(
                self.packet_remaining,
                n_in - consumed,
                n_out - produced,
            )

            if count == 0:
                break

            out[produced:produced + count] = inp[
                consumed:consumed + count
            ]

            consumed += count
            produced += count
            self.packet_remaining -= count

            if self.packet_remaining == 0:
                self.idle_remaining = self.idle_bytes

        self.consume(0, consumed)
        return produced