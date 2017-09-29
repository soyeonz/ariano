
import scipy.io.wavfile as wavfile
import numpy as np
import pylab as pl

rate, data = wavfile.read("Butterfly.wav")
t = np.arange(len(data[:,0]))*1.0/rate

#Original Signal graph
fig = pl.figure()
g1 = fig.add_subplot(221)
g1.set_title("Original signal")
g1.plot(data)


for i in range(0,180778):
  if(data[i,1]>0):
      start = i
      break
print(start)
temp = np.abs(np.fft.rfft(data[start:180778,1]))

p = [20*np.log10(x) if x>=1 else 1 for x in temp]


f = np.linspace(0, rate/2.0, len(p))

g2 = fig.add_subplot(222)
g2.set_title("FFT")

g2.plot(f, p)
# g2.xlabel("Frequency(Hz)")
# g2.ylabel("Power(dB)")

pl.show()