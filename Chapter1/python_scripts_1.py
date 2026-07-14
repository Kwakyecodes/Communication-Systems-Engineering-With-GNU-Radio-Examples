import numpy as np
from matplotlib import pyplot as plt
fs = 400
t = np.linspace(0, 1, fs)
s = np.cos(2*np.pi*100*t) + 0.1
freq = np.linspace(-fs/2, fs/2 - fs/len(s), len(s))
# plt.plot(freq, np.fft.fftshift(np.fft.fft(s)))
plt.plot(freq, np.fft.fft(s))
plt.show()