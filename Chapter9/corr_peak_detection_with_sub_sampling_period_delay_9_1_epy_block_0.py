import numpy as np
from gnuradio import gr


class blk(gr.basic_block):
    """Parabolic correlation peak fitting."""

    def __init__(self, N=1, cancel=True, cancelP=1, printres=True):
        gr.basic_block.__init__(
            self,
            name='peak fit',
            in_sig=[np.complex64],
            out_sig=[np.float32]
        )

        self.N = N
        self.cancel = cancel
        self.bigarray = np.ones(5 * self.N, dtype=np.complex64)
        self.posarray = 0
        self.printres = printres
        self.cancelP = cancelP

    def general_work(self, input_items, output_items):

        # Tell GNU Radio that we consume all supplied input samples
        self.consume(0, len(input_items[0]))

        # Add incoming samples to our internal buffer
        self.bigarray[
            self.posarray:self.posarray + len(input_items[0])
        ] = input_items[0]

        self.posarray += len(input_items[0])

        nbsol = 0

        # Process one complete correlation vector whenever N samples
        # have accumulated
        while self.posarray >= self.N:

            # Optionally suppress correlation around zero delay
            if self.cancel:
                self.bigarray[
                    self.N // 2 - self.cancelP:
                    self.N // 2 + self.cancelP
                ] = 0

            # Find the coarse (integer-sample) correlation peak
            coarse = np.argmax(
                np.absolute(self.bigarray[0:self.N])
            )

            # Magnitudes of peak and its two neighbours
            s1 = np.absolute(self.bigarray[coarse - 1])
            s2 = np.absolute(self.bigarray[coarse])
            s3 = np.absolute(self.bigarray[coarse + 1])

            # Parabolic interpolation
            denominator = s1 + s3 - 2 * s2

            if denominator == 0:
                print("ERROR")
                correction = 0
            else:
                correction = (s1 - s3) / denominator / 2

            solution = coarse + correction

            # Remove the N samples we've just processed
            self.bigarray[
                0:self.posarray - self.N
            ] = self.bigarray[
                self.N:self.posarray
            ]

            self.posarray -= self.N

            # Express delay relative to zero-delay at N/2
            output_items[0][nbsol] = solution - self.N / 2

            if self.printres:
                print(
                    f"{nbsol} "
                    f"{output_items[0][nbsol]:.6f}"
                )

            nbsol += 1

        return nbsol