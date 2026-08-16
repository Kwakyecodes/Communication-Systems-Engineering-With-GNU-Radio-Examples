import numpy as np

def generate_gps_ca_code(prn):
    assignments = {
        31: (3, 8),
        32: (4, 9)
    }

    if prn not in assignments:
        raise ValueError(f"Unsupported PRN: {prn}")

    g2_tap1, g2_tap2 = assignments[prn]

    g1 = np.ones(10, dtype=np.int8)
    g2 = np.ones(10, dtype=np.int8)

    code = np.empty(1023, dtype=np.float32)

    for i in range(1023):
        g1_out = g1[9]
        g2_out = g2[g2_tap1 - 1] ^ g2[g2_tap2 - 1]

        ca_bit = g1_out ^ g2_out

        # GPS C/A BPSK representation
        code[i] = 1.0 if ca_bit == 0 else -1.0

        # G1
        feedback1 = g1[2] ^ g1[9]
        g1[1:] = g1[:-1]
        g1[0] = feedback1

        # G2
        feedback2 = (
            g2[1] ^ g2[2] ^ g2[5] ^
            g2[7] ^ g2[8] ^ g2[9]
        )

        g2[1:] = g2[:-1]
        g2[0] = feedback2

    return code


def upsample_code(code, target_samples=4000):
    indices = np.floor(
        np.arange(target_samples) * len(code) / target_samples
    ).astype(int)

    return code[indices].astype(np.complex64)


for prn in [31, 32]:
    code = generate_gps_ca_code(prn)
    samples = upsample_code(code)

    filename = f"gps_L1_PRN{prn:02d}_4Msps.dat"
    samples.tofile(filename)

    print(f"Generated {filename}")