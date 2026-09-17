import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, Fft_Len=512, Samp_Rate=300000, Previous_Freq=0.0):
        gr.sync_block.__init__(
            self,
            name='Carrier Offset Calculation',
            in_sig=[np.float32],  # Receives the float index from 'Short to Float'
            out_sig=[np.int32]  # Outputs the calculated frequency offset in Hz
        )
        self.Fft_Len = Fft_Len
        self.Samp_Rate = Samp_Rate
        self.Previous_Freq = Previous_Freq

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        for i in range(len(in0)):
            bin_index = in0[i]
            
            # Shift the FFT bins so index 0 centers around 0 Hz (handling negative frequencies)
            if bin_index >= self.Fft_Len / 2:
                bin_index -= self.Fft_Len
            
            # 1. Convert bin index to the multiplied frequency domain
            freq_in_multiplied_domain = (bin_index * self.Samp_Rate) / self.Fft_Len
            
            # 2. Divide by 4 because the prior x4 Multiply blocks magnified the error 4x
            true_hardware_offset = freq_in_multiplied_domain / 4.0
            
            out[i] = ınt(true_hardware_offset)
            
        return len(out)
