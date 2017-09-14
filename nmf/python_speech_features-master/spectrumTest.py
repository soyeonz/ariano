import numpy as np
from scipy.io.wavfile import read
from pylab import plot
from pylab import plot, psd, magnitude_spectrum
import matplotlib.pyplot as plt

#Hello Signal!!!
(fs, x) = read('butterfly.wav')

#Remove silence out of beginning of signal with threshold of 1000

def indices(a, func):
    #This allows to use the lambda function for equivalent of find() in matlab
    return [i for (i, val) in enumerate(a) if func(val)]

#Make the signal smaller so it uses less resources
x_tiny = x[0:100000]
#threshold is 1000, 0 is calling the first index greater than 1000
thresh = indices(x_tiny, lambda y: y > 1000)[1]
# backs signal up 20 bins, so to not ignore the initial pluck sound...
thresh_start = thresh-20
#starts at threshstart ends at end of signal (-1 is just a referencing thing)
analysis_signal = x[thresh_start-1:]

#Split signal so it is 1 second long
one_sec = 1*fs
onesec = x[thresh_start-1:one_sec]

#***unsure is just a placeholder because it spits out a weird error if I don't use
#a third variable
(xsig, ysig, unsure) = magnitude_spectrum(onesec, Fs=fs)