import numpy as np 
from matplotlib import pyplot as plt
import pylab
from scipy import signal
from scipy.io.wavfile import write
import hparams
import sys
from math import pi
from scipy.io.wavfile import write

# Create a signal of frequency F0Hz. 
# Signal time length = t0 seconds
# Signal sampling frequency is Fs

F1 = np.array(hparams.formant_freq)
B1 = np.array(hparams.formant_bw)
Fs = hparams.samp_freq
T = 1.0/Fs
t0 = hparams.time_length
num_samples = Fs*t0
F0 = hparams.sig_freq
t = np.linspace(0, t0, num_samples)
fig = plt.figure()

sig = signal.square(2 * np.pi * F0 * t, duty=0.01)
#sig = signal.sawtooth(2 * np.pi * F0 * t)

ax1 = fig.add_subplot(211)
plt.ylabel('Input Signal')
plt.plot(t[0:1000], sig[0:1000])

# Calculate pole angles and radii
R = np.exp(-pi*B1/Fs)
theta = 2*pi*F1/Fs

# Get poles and an equal number of zeros
poles = np.array([R * np.exp(1j*theta), R * np.exp(-1j*theta)])
zeros = np.zeros(poles.shape, poles.dtype)

b, a = signal.zpk2tf(zeros, poles, 1)

y = np.zeros(sig.shape, sig.dtype)

for i in range(len(sig)):
    y[i] = y[i] + a[0]*sig[i]
    for j in range(1, len(a)):
        if i-j >= 0:
            y[i] = y[i] - a[j]*y[i-j]

# plt.title('Filter Output')
ax2 = fig.add_subplot(212)

plt.plot(t[0:1000], y[0:1000], 'b')
plt.ylabel('Filter output', color='b')
plt.xlabel('Time [seconds]')
pylab.savefig('./results/' + 'q2' + '_' + 'trial0' + '.png')
write('trial0.wav', Fs, y)
plt.show()

